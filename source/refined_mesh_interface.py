import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap


class RefinementInterfaceApp:
    """
    Interface gráfica para refinamento de malhas 3D.

    Esta classe implementa uma interface de usuário para a definição de regiões
    de refinamento em malhas tridimensionais.

    Parameters
    ----------
    root : tk.Tk
        Janela raiz para a interface
    mesh : numpy.ndarray
        Malha 3D a ser refinada
    refine_function : callable
        Função que refina a malha 3D com a assinatura:
        refine_function(mesh, refinement_regions) -> numpy.ndarray
    on_refinement_complete : callable, optional
        Callback que será chamado quando uma malha for refinada, recebe a malha refinada como parâmetro

    Attributes
    ----------
    root : tk.Tk
        Janela raiz da aplicação
    mesh : numpy.ndarray
        Malha 3D a ser refinada
    refine_mesh : callable
        Referência à função fornecida para refinamento da malha
    on_refinement_complete : callable
        Callback para notificar quando uma malha é refinada
    refinement_regions : dict
        Dicionário hierárquico de regiões de refinamento no formato {z: {x: [(y_start, y_end, factor_i, factor_j, factor_k), ...]}}
    refined_mesh : numpy.ndarray, optional
        Última malha refinada, apenas disponível após chamar generate_refined_mesh()
    """
    def __init__(self, root, mesh, refine_function, on_refinement_complete=None):
        """
        Inicializa a interface para refinamento de malha 3D

        Parameters
        ----------
        root : tk.Tk
            Janela raiz para a interface
        mesh : numpy.ndarray
            Malha 3D a ser refinada
        refine_function : callable
            Função que refina a malha 3D
        on_refinement_complete : callable, optional
            Callback que será chamado quando uma malha for refinada, recebe a malha refinada como parâmetro
        """
        self.root = root
#        self.root.title("Interface para Refinamento de Malha")
        if isinstance(self.root, tk.Tk): # Check if self.root is a tk.Tk instance
            self.root.geometry("900x700")
        # Armazenar a malha e a função de refinamento
        self.mesh = mesh
        self.refine_mesh = refine_function

        # Callback para quando a malha for refinada
        self.on_refinement_complete = on_refinement_complete

        # Obter dimensões da malha
        self.nx, self.ny, self.nz = mesh.shape
        # Labels para informações da malha, inicializados aqui para serem acessíveis globalmente dentro da classe
        self.dimensions_label = None
        self.active_cells_label = None

        # Variáveis para entrada de regiões de refinamento
        self.z_layer_var = tk.IntVar(value=0)
        self.x_line_var = tk.IntVar(value=0)
        self.y_start_var = tk.IntVar(value=0)
        self.y_end_var = tk.IntVar(value=0)
        self.factor_i_var = tk.IntVar(value=1)
        self.factor_j_var = tk.IntVar(value=1)
        self.factor_k_var = tk.IntVar(value=1)

        # Dicionário para armazenar as regiões de refinamento
        self.refinement_regions = {}

        # Criar e configurar os widgets
        self.create_widgets()

        # Carregar valores padrão de exemplo
        self.load_default_regions()

        # Configurar visualização da malha
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.visualization_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Atualizar a visualização inicialmente
        self.update_visualization()

        # Para controlar eventos de redimensionamento
        self.resize_id = None

        # Configurar ação de fechamento da janela
         # Configurar ação de fechamento da janela
        if isinstance(self.root, tk.Tk): # Check if self.root is a tk.Tk instance
            self.root.protocol("WM_DELETE_WINDOW", self.close_application)

    
    def create_widgets(self):
        """
        Cria todos os widgets da interface com layout estável e organização vertical
        """
        # ==================================================================
        # Usar pack para o layout principal da janela
        # ==================================================================
       # Container principal (contém tudo exceto os botões) - PACK AFTER BUTTONS
        main_container = ttk.Frame(self.root)

        # Painel para botões - sempre fixo na parte inferior (PACK FIRST WITH SIDE=BOTTOM)
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.BOTTOM, expand=False) # Pack button_frame at the BOTTOM FIRST

        main_container.pack(fill=tk.BOTH, expand=True, side=tk.TOP)  # Main container expands to fill remaining space at TOP


        # ==================================================================
        # PanedWindow principal (divisão horizontal)
        # ==================================================================
        main_paned = tk.PanedWindow(
            main_container,
            orient=tk.HORIZONTAL,
            sashrelief=tk.RAISED,
            sashwidth=5
        )

        main_paned.pack(fill=tk.BOTH, expand=True)


        # ==================================================================
        # Painel Esquerdo (Controles)
        # ==================================================================
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, width=300, minsize=250)

        # ------ Seção 1: Informações da Malha ------
        info_frame = ttk.LabelFrame(
            left_frame,
            text="Informações da Malha",
            padding=10
        )
        info_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(info_frame, text="Dimensões:").pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)
        self.dimensions_label = ttk.Label(info_frame, text=f"{self.nx} × {self.ny} × {self.nz}") # Store label as attribute
        self.dimensions_label.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)

        ttk.Label(info_frame, text="Células ativas:").pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)
        active_cells = np.sum(self.mesh > 0)
        self.active_cells_label = ttk.Label(info_frame, text=f"{active_cells}") # Store label as attribute
        self.active_cells_label.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)

        # ------ Seção 2: Adicionar Regiões de Refinamento ------
        region_input_frame = ttk.LabelFrame(
            left_frame,
            text="Adicionar Região de Refinamento",
            padding=10
        )
        region_input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Posição
        ttk.Label(region_input_frame, text="Camada Z:").pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)
        self.z_spinbox = ttk.Spinbox(region_input_frame, from_=0, to=self.nz-1, textvariable=self.z_layer_var, width=8)
        self.z_spinbox.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)

        ttk.Label(region_input_frame, text="Linha X:").pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)
        self.x_spinbox = ttk.Spinbox(region_input_frame, from_=0, to=self.nx-1, textvariable=self.x_line_var, width=8)
        self.x_spinbox.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)

        ttk.Label(region_input_frame, text="De Y:").pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)
        self.y_start_spinbox = ttk.Spinbox(region_input_frame, from_=0, to=self.ny-1, textvariable=self.y_start_var, width=8)
        self.y_start_spinbox.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)

        ttk.Label(region_input_frame, text="Até Y:").pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)
        self.y_end_spinbox = ttk.Spinbox(region_input_frame, from_=0, to=self.ny-1, textvariable=self.y_end_var, width=8)
        self.y_end_spinbox.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)

        # Separador
        ttk.Separator(region_input_frame, orient="horizontal").pack(fill=tk.X, pady=5)

        # Fatores de refinamento
        ttk.Label(region_input_frame, text="Fator X:").pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)
        ttk.Spinbox(region_input_frame, from_=1, to=10, textvariable=self.factor_i_var, width=8).pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)

        ttk.Label(region_input_frame, text="Fator Y:").pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)
        ttk.Spinbox(region_input_frame, from_=1, to=10, textvariable=self.factor_j_var, width=8).pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)

        ttk.Label(region_input_frame, text="Fator Z:").pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)
        ttk.Spinbox(region_input_frame, from_=1, to=10, textvariable=self.factor_k_var, width=8).pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)

        # Botão de adicionar
        ttk.Button(
            region_input_frame,
            text="Adicionar Região",
            command=self.add_refinement_region
        ).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # ------ Seção 3: Regiões de Refinamento (Treeview) ------
        region_display_frame = ttk.LabelFrame(
            left_frame,
            text="Regiões de Refinamento",
            padding=10
        )
        region_display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Criando a Treeview
        self.tree = ttk.Treeview(region_display_frame, columns=("fatores",), show="tree headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tree_scroll = ttk.Scrollbar(
            region_display_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        # ==================================================================
        # Painel Direito (Visualização da Malha)
        # ==================================================================
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, minsize=500)

        self.visualization_frame = ttk.LabelFrame(
            right_frame,
            text="Visualização da Malha",
            padding=10
        )
        self.visualization_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ==================================================================
        # Botões na parte inferior
        # ==================================================================

        ttk.Button(
            button_frame,
            text="Remover Selecionado",
            command=self.remove_selected_region
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            button_frame,
            text="Limpar Todos",
            command=self.clear_regions
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            button_frame,
            text="Gerar Malha Refinada",
            command=self.generate_refined_mesh
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            button_frame,
            text="Restaurar Padrões",
            command=self.restore_defaults
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            button_frame,
            text="Fechar",
            command=self.close_application
        ).pack(side=tk.RIGHT, padx=2)

        # Definir proporção inicial do PanedWindow
        self.root.update_idletasks()
        main_paned.sash_place(0, 300, 0)

    def update_mesh_info_display(self):
        """
        Atualiza as informações da malha na interface.
        """
        if self.dimensions_label:
            self.dimensions_label.config(text=f"{self.nx} × {self.ny} × {self.nz}")  
        if self.active_cells_label:
            active_cells = np.sum(self.mesh > 0)
            self.active_cells_label.config(text=f"{active_cells}")  
        self.root.update_idletasks() # Force UI update

    
    def get_default_regions(self):
        """
        Retorna as regiões de refinamento padrão para inicialização

        Returns
        -------
        dict
            Dicionário de regiões de refinamento no formato {z: {x: [(y_start, y_end, factor_i, factor_j, factor_k), ...]}}
        """
        return {
            1: {
                3: [(3, 4, 2, 2, 1)],
                4: [(3, 4, 2, 2, 1)]
            },
            2: {
                3: [(3, 4, 2, 2, 1)],
                4: [(3, 4, 2, 2, 1)]
            }
        }

    def load_default_regions(self):
        """
        Carrega as regiões de refinamento padrão e atualiza a interface
        """
        self.refinement_regions = self.get_default_regions()
        self.update_regions_display()

    def add_refinement_region(self):
        """
        Adiciona uma nova região de refinamento baseada nos valores atuais dos spinboxes

        Esta função valida os valores de entrada e adiciona uma nova região de refinamento
        para a posição X,Z especificada na estrutura de regiões de refinamento.
        """
        try:
            z = self.z_layer_var.get()
            x = self.x_line_var.get()
            y_start = self.y_start_var.get()
            y_end = self.y_end_var.get()
            factor_i = self.factor_i_var.get()
            factor_j = self.factor_j_var.get()
            factor_k = self.factor_k_var.get()

            # Validar intervalo Y
            if y_start > y_end:
                messagebox.showerror("Erro", "O valor inicial do intervalo Y deve ser menor ou igual ao valor final.")
                return

            # Validar fatores de refinamento
            if factor_i < 1 or factor_j < 1 or factor_k < 1:
                messagebox.showerror("Erro", "Os fatores de refinamento devem ser maiores ou iguais a 1.")
                return

            # Garantir que os dicionários existam
            if z not in self.refinement_regions:
                self.refinement_regions[z] = {}
            if x not in self.refinement_regions[z]:
                self.refinement_regions[z][x] = []

            # Criar a tupla da região de refinamento
            new_region = (y_start, y_end, factor_i, factor_j, factor_k)

            # Verificar se a região já existe
            if new_region in self.refinement_regions[z][x]:
                messagebox.showinfo("Informação", "Esta região de refinamento já existe.")
                return

            # Adicionar a nova região
            self.refinement_regions[z][x].append(new_region)

            # Atualizar a visualização
            self.update_regions_display()

            # Limpar campos do intervalo Y para facilitar a inserção de novos
            self.y_start_var.set(0)
            self.y_end_var.set(0)
            # Manter fatores de refinamento para facilitar a inserção de regiões com os mesmos fatores

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar região de refinamento: {str(e)}")

    def update_regions_display(self):
        """
        Atualiza a exibição das regiões de refinamento na árvore

        Esta função atualiza a visualização das regiões de refinamento na interface,
        mostrando a hierarquia de camadas Z, linhas X e intervalos Y com seus fatores.
        """
        # Atualizar treeview
        self.tree.delete(*self.tree.get_children())

        for z in sorted(self.refinement_regions.keys()):
            z_node = self.tree.insert("", "end", text=f"Camada Z={z}", open=True)

            for x in sorted(self.refinement_regions[z].keys()):
                x_node = self.tree.insert(z_node, "end", text=f"Linha X={x}", open=True)

                for region in self.refinement_regions[z][x]:
                    y_start, y_end, factor_i, factor_j, factor_k = region
                    region_text = f"Y: [{y_start}, {y_end}]"
                    factors_text = f"Fatores: X={factor_i}, Y={factor_j}, Z={factor_k}"
                    self.tree.insert(x_node, "end", text=region_text, values=(factors_text,))

    def remove_selected_region(self):
        """
        Remove as regiões de refinamento selecionadas na árvore

        Esta função remove todos os itens selecionados na treeview,
        sejam eles camadas Z completas, linhas X específicas ou regiões individuais.
        """
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Informação", "Selecione um item para remover.")
            return

        # Processa cada item selecionado
        items_removed = False
        for item_id in selected_items:
            parent_id = self.tree.parent(item_id)
            grand_parent_id = self.tree.parent(parent_id) if parent_id else ""

            # Se for um nó de camada Z (sem pai)
            if not parent_id:
                z = int(self.tree.item(item_id)["text"].split("=")[1])
                if z in self.refinement_regions:
                    del self.refinement_regions[z]
                    items_removed = True

            # Se for um nó de linha X (pai é camada Z)
            elif not grand_parent_id:
                z = int(self.tree.item(parent_id)["text"].split("=")[1])
                x = int(self.tree.item(item_id)["text"].split("=")[1])
                if z in self.refinement_regions and x in self.refinement_regions[z]:
                    del self.refinement_regions[z][x]
                    items_removed = True
                    # Se a camada Z ficou vazia, remover também
                    if not self.refinement_regions[z]:
                        del self.refinement_regions[z]

            # Se for uma região individual (avô é camada Z, pai é linha X)
            else:
                z = int(self.tree.item(grand_parent_id)["text"].split("=")[1])
                x = int(self.tree.item(parent_id)["text"].split("=")[1])
                if z in self.refinement_regions and x in self.refinement_regions[z]:
                    region_text = self.tree.item(item_id)["text"]
                    # Extrair y_start e y_end do texto da região
                    import re
                    match = re.match(r"Y: \[(\d+), (\d+)\]", region_text)
                    if match:
                        y_start, y_end = int(match.group(1)), int(match.group(2))

                        # Extrair os fatores do texto da região
                        factors_text = self.tree.item(item_id)["values"][0]
                        match = re.match(r"Fatores: X=(\d+), Y=(\d+), Z=(\d+)", factors_text)
                        if match:
                            factor_i, factor_j, factor_k = int(match.group(1)), int(match.group(2)), int(match.group(3))

                            # Procurar e remover a região
                            region = (y_start, y_end, factor_i, factor_j, factor_k)
                            if region in self.refinement_regions[z][x]:
                                self.refinement_regions[z][x].remove(region)
                                items_removed = True
                                # Se a linha X ficou vazia, remover também
                                if not self.refinement_regions[z][x]:
                                    del self.refinement_regions[z][x]
                                    # Se a camada Z ficou vazia, remover também
                                    if not self.refinement_regions[z]:
                                        del self.refinement_regions[z]

        if items_removed:
            # Atualizar a visualização
            self.update_regions_display()
        else:
            messagebox.showinfo("Informação", "Nenhum item válido foi removido.")

    def clear_regions(self):
        """
        Limpa todas as regiões de refinamento

        Esta função remove todas as regiões de refinamento após confirmação do usuário.
        """
        if messagebox.askyesno("Confirmação", "Remover todas as regiões de refinamento?"):
            self.refinement_regions = {}
            self.update_regions_display()

    def restore_defaults(self):
        """
        Restaura as regiões de refinamento padrão

        Esta função restaura as regiões de refinamento para seus valores padrão
        após confirmação do usuário.
        """
        if messagebox.askyesno("Confirmação", "Restaurar todas as regiões para o padrão?"):
            self.load_default_regions()

    def generate_refined_mesh(self):
        """
        Gera a malha refinada com os parâmetros atuais e chama o callback

        Esta função chama a função refine_mesh com a malha original e as regiões de refinamento atuais
        e armazena a malha resultante, além de chamar o callback se definido.

        Returns
        -------
        numpy.ndarray
            A malha refinada
        """
        try:
            if self.refinement_regions:
                # Gerar a malha refinada usando a função fornecida
                self.refined_mesh = self.refine_mesh(self.mesh, self.refinement_regions)
                # Atualizar visualização com a malha refinada
                self.update_visualization(use_refined=True)

                # Chamar o callback com a malha refinada
                if self.on_refinement_complete:
                    self.on_refinement_complete(self.refined_mesh)

                messagebox.showinfo("Sucesso", "Malha refinada gerada com sucesso!")

                # Retornar a malha refinada
                return self.refined_mesh
            else:
                messagebox.showwarning("Aviso", "Não há regiões de refinamento definidas. A malha não será alterada.")

                # Retornar a malha original sem alterações
                self.refined_mesh = np.copy(self.mesh)
                return self.refined_mesh
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar malha refinada: {str(e)}")

            # Retornar a malha original em caso de erro
            return self.mesh


    def update_visualization(self, use_refined=False):
        """
        Atualiza a visualização da malha com suporte a múltiplos níveis de refinamento
        """
        try:
            mesh_to_visualize = self.refined_mesh if hasattr(self, 'refined_mesh') and use_refined else self.mesh

            # Configuração inicial da figura
            self.fig.clf()
            nx, ny, nz = mesh_to_visualize.shape

            # Configurar layout dos subplots
            rows = 1 if nz <= 3 else int(np.ceil(np.sqrt(nz)))
            cols = nz if nz <= 3 else int(np.ceil(nz / rows))

            # Criar subplots para cada camada Z
            axes = []
            for k in range(nz):
                ax = self.fig.add_subplot(rows, cols, k+1)
                axes.append(ax)

                # Determinar valores máximo e mínimo para a escala de cores
                max_val = np.max(mesh_to_visualize)
                min_val = np.min(mesh_to_visualize)

                # Usar mapa de cores apropriado
                if max_val > 1 or use_refined:
                    cmap = 'viridis'
                    vmin = min_val
                    vmax = max_val if max_val > 0 else 1
                else:
                    cmap = ListedColormap(['white', '#1f77b4'])
                    vmin = 0
                    vmax = 1

                # Plotar a camada Z
                im = ax.imshow(mesh_to_visualize[:, :, k].T,
                             cmap=cmap,
                             origin='lower',
                             vmin=vmin,
                             vmax=vmax)

                # Configurar labels e ticks
                ax.set_title(f'Z = {k}', fontsize=9)
                ax.set_xlabel('X', fontsize=8)
                ax.set_ylabel('Y', fontsize=8)
                ax.set_xticks(np.arange(0, nx, max(1, nx//5)))
                ax.set_yticks(np.arange(0, ny, max(1, ny//5)))
                ax.tick_params(labelsize=7)

            # Adicionar barra de cores única
            cax = self.fig.add_axes([0.92, 0.15, 0.02, 0.7])
            self.fig.colorbar(im, cax=cax).set_label('Nível de Refinamento', fontsize=8)

            # Ajustar layout e redesenhar
            self.fig.tight_layout(rect=[0, 0, 0.9, 1])
            self.fig.suptitle('Malha Original' if not use_refined else 'Malha Refinada', y=0.98)
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Erro de Visualização", f"Erro ao atualizar a visualização: {str(e)}")

    def on_frame_resize(self, event=None):
        """
        Atualiza dinamicamente o tamanho da visualização
        """
        if hasattr(self, 'fig'):
            self.fig.set_size_inches(
                self.visualization_frame.winfo_width()/100,
                self.visualization_frame.winfo_height()/100
            )
            self.canvas.draw()

    def close_application(self):
        """
        Fecha a aplicação garantindo a execução do callback final
        """
        if hasattr(self, 'refined_mesh') and self.on_refinement_complete:
            self.on_refinement_complete(self.refined_mesh)
        self.root.destroy()


# def open_refinement_interface(mesh, refine_function):
    # """
    # Abre a interface de refinamento e retorna a malha refinada

    # Parameters:
    # mesh (np.ndarray): Malha 3D original
    # refine_function (callable): Função de refinamento
    # Returns:
    # np.ndarray: Malha refinada ou original se cancelado
    # """
    # result = [mesh]  # Armazenamento para o resultado

    # def callback(refined_mesh):
    #     result[0] = refined_mesh

    # root = tk.Tk()
    # app = RefinementInterfaceApp(root, mesh, refine_function, callback)
    # root.mainloop()

    # return result[0]