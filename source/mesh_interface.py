import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import json
import ast
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap
from mesh3d import create_3d_mesh


class MeshInterfaceApp:
    """
    Interface gráfica para criação e visualização de malhas 3D.

    Esta classe implementa uma interface de usuário completa para a geração
    de malhas tridimensionais baseadas em intervalos ativos especificados pelo usuário.

    Parameters
    ----------
    root : tk.Tk
        Janela raiz para a interface
    mesh_function : callable
        Função que cria a malha 3D com a assinatura:
        mesh_function(nx, ny, nz, active_intervals) -> numpy.ndarray
    on_mesh_created : callable, optional
        Callback que será chamado quando uma malha for gerada, recebe a malha como parâmetro

    Attributes
    ----------
    root : tk.Tk
        Janela raiz da aplicação
    create_3d_mesh : callable
        Referência à função fornecida para criação da malha
    on_mesh_created : callable
        Callback para notificar quando uma malha é gerada
    active_intervals : dict
        Dicionário hierárquico de intervalos ativos no formato {z: {x: [(y_start, y_end), ...]}}
    mesh : numpy.ndarray, optional
        Última malha gerada, apenas disponível após chamar generate_mesh()
    """
    def __init__(self, root, mesh_function, on_mesh_created=None):
        """
        Inicializa a interface para a função create_3d_mesh

        Parameters
        ----------
        root : tk.Tk
            Janela raiz para a interface
        mesh_function : callable
            Função que cria a malha 3D (sua função create_3d_mesh existente)
        on_mesh_created : callable, optional
            Callback que será chamado quando uma malha for gerada, recebe a malha como parâmetro
        """
        self.root = root  # Store the Tk root window
        # self.root.title("Interface para create_3d_mesh") # Remove this line
        #self.root.geometry("900x700")  # Remove this line

        # Armazena a função create_3d_mesh existente
        self.create_3d_mesh = mesh_function

        # Callback para quando a malha for criada
        self.on_mesh_created = on_mesh_created

        # Variáveis para armazenar os valores dos parâmetros
        self.nx_var = tk.IntVar(value=8)
        self.ny_var = tk.IntVar(value=8)
        self.nz_var = tk.IntVar(value=3)

        # Variáveis para entrada de intervalos
        self.z_layer_var = tk.IntVar(value=0)
        self.x_line_var = tk.IntVar(value=0)
        self.y_start_var = tk.IntVar(value=0)
        self.y_end_var = tk.IntVar(value=0)

        # Dicionário para armazenar os intervalos ativos
        self.active_intervals = {}

        # Criar e configurar os widgets - IMPORTANTE: isso deve vir antes de carregar intervalos
        self.create_widgets()

        # IMPORTANTE: Mover o carregamento de valores padrão para depois da criação dos widgets
        self.load_default_intervals()

        # Configurar visualização da malha
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.visualization_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Atualizar a visualização inicialmente
        self.update_visualization()

        # Para controlar eventos de redimensionamento
        self.resize_id = None

        # Configurar ação de fechamento da janela
        if isinstance(self.root, tk.Tk):  # Check if self.root is a tk.Tk instance
            self.root.protocol("WM_DELETE_WINDOW", self.close_application)

    def create_widgets(self):
        """
        Cria todos os widgets da interface com layout estável e organização vertical
        """
    # Usar pack para o layout principal da janela
        # ==================================================================

       # Container principal (contém tudo exceto os botões) - PACK AFTER BUTTONS
        main_container = ttk.Frame(self.root)
        # Painel para botões - sempre fixo na parte inferior (PACK FIRST WITH SIDE=BOTTOM)
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.BOTTOM, expand=False) # Pack button_frame at the BOTTOM FIRST

        main_container.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        # Main container expands to fill remaining space at TOP
       # Force layout update to show buttons initially
#        self.root.update_idletasks()


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

        # ------ Seção 1: Parâmetros da Malha ------
        params_frame = ttk.LabelFrame(
            left_frame,
            text="Parâmetros da Malha",
            padding=10
        )
        params_frame.pack(fill=tk.X, padx=5, pady=5)  # Use pack here

        # Layout vertical para os parâmetros
        # Remove as configurações de grid
        # params_frame.columnconfigure(0, weight=1)
        # params_frame.columnconfigure(1, weight=1)

        ttk.Label(params_frame, text="nx:").pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)  # Use pack here
        ttk.Spinbox(params_frame, from_=1, to=40, textvariable=self.nx_var, width=8).pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)  # Use pack here

        ttk.Label(params_frame, text="ny:").pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)  # Use pack here
        ttk.Spinbox(params_frame, from_=1, to=40, textvariable=self.ny_var, width=8).pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)  # Use pack here

        ttk.Label(params_frame, text="nz:").pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)  # Use pack here
        ttk.Spinbox(params_frame, from_=1, to=40, textvariable=self.nz_var, width=8).pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)  # Use pack here

        # ------ Seção 2: Adicionar Intervalos ------
        interval_input_frame = ttk.LabelFrame(
            left_frame,
            text="Adicionar Intervalos Ativos",
            padding=10
        )
        interval_input_frame.pack(fill=tk.X, padx=5, pady=5)  # Use pack here

        # Layout vertical para os intervalos
        # Remove as configurações de grid
        # interval_input_frame.columnconfigure(0, weight=1)
        # interval_input_frame.columnconfigure(1, weight=1)

        entries = [
            ("Camada Z:", self.z_layer_var),
            ("Linha X:", self.x_line_var),
            ("De Y:", self.y_start_var),
            ("Até Y:", self.y_end_var)
        ]

        for label, var in entries:
            ttk.Label(interval_input_frame, text=label).pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)  # Use pack here
            spin = ttk.Spinbox(interval_input_frame, textvariable=var, width=8)
            spin.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=2)  # Use pack here

            if label == "Camada Z:":
                self.z_spinbox = spin
            elif label == "Linha X:":
                self.x_spinbox = spin
            elif label == "De Y:":
                self.y_start_spinbox = spin
            elif label == "Até Y:":
                self.y_end_spinbox = spin

        # Botão de adicionar na parte inferior do frame de intervalos
        ttk.Button(
            interval_input_frame,
            text="Adicionar Intervalo",
            command=self.add_interval
        ).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)  # Use pack here

        # ------ Seção 3: Intervalos Ativos (Treeview) ------
        interval_display_frame = ttk.LabelFrame(
            left_frame,
            text="Intervalos Ativos",
            padding=10
        )
        interval_display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Use pack here

        # Remove as configurações de grid
        # interval_display_frame.rowconfigure(0, weight=1)
        # interval_display_frame.columnconfigure(0, weight=1)

        # IMPORTANTE: Definindo self.tree aqui
        self.tree = ttk.Treeview(interval_display_frame, columns=("intervalos",), show="tree headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Use pack here

        tree_scroll = ttk.Scrollbar(
            interval_display_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)  # Use pack here
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
            command=self.remove_selected_interval
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            button_frame,
            text="Limpar Todos",
            command=self.clear_intervals
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            button_frame,
            text="Gerar Malha",
            command=self.generate_mesh
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

        # Configurar eventos para atualizar os limites dos spinboxes
        self.nx_var.trace_add('write', self.update_spinbox_limits)
        self.ny_var.trace_add('write', self.update_spinbox_limits)
        self.nz_var.trace_add('write', self.update_spinbox_limits)

        # Definir proporção inicial do PanedWindow
        # Ajustando para que o painel de controles tenha tamanho fixo adequado
        self.root.update_idletasks()
        main_paned.sash_place(0, 300, 0)  # Posição do divisor em 300 pixels da esquerda

    def update_spinbox_limits(self, *args):
        """
        Atualiza os limites dos spinboxes com base nos valores de nx, ny e nz

        Parameters
        ----------
        *args
            Argumentos adicionais requeridos pelo sistema de callbacks do Tkinter
        """
        try:
            # Obtém os valores atuais
            nx = self.nx_var.get()
            ny = self.ny_var.get()
            nz = self.nz_var.get()

            # Atualiza os limites dos spinboxes
            self.z_spinbox.config(from_=0, to=max(0, self.nz - 1))
            self.x_spinbox.config(from_=0, to=max(0, self.nx - 1))
            self.y_start_spinbox.config(from_=0, to=max(0, self.ny - 1))
            self.y_end_spinbox.config(from_=0, to=max(0, self.ny - 1))

            # Ajusta os valores atuais para estarem dentro dos novos limites
            if self.z_layer_var.get() >= self.nz:
                self.z_layer_var.set(max(0, self.nz-1))
            if self.x_line_var.get() >= self.nx:
                self.x_line_var.set(max(0, self.nx-1))
            if self.y_start_var.get() >= self.ny:
                self.y_start_var.set(max(0, self.ny-1))
            if self.y_end_var.get() >= self.ny:
                self.y_end_var.set(max(0, self.ny-1))       
        except Exception as e:
            print(f"Erro ao atualizar limites: {str(e)}")

    def get_default_intervals(self):
        """
        Retorna os intervalos padrão para inicialização

        Returns
        -------
        dict
            Dicionário de intervalos ativos no formato {z: {x: [(y_start, y_end), ...]}}
        """
        return {
            0: {2: [(3, 4)], 3: [(2, 5)], 4: [(2, 5)], 5: [(3, 4)]},
            1: {1: [(2, 5)], 2: [(1, 6)], 3: [(1, 6)], 4: [(1, 6)], 5: [(1, 6)], 6: [(2, 5)]},
            2: {0: [(2, 5)], 1: [(1, 6)], 2: [(0, 7)], 3: [(0, 7)], 4: [(0, 7)], 5: [(0, 7)], 6: [(1, 6)], 7: [(2, 5)]}
        }

    def load_default_intervals(self):
        """
        Carrega os intervalos padrão e atualiza a interface
        """
        self.active_intervals = self.get_default_intervals()
        self.update_intervals_display()

    def add_interval(self):
        """
        Adiciona um novo intervalo baseado nos valores atuais dos spinboxes

        Esta função valida os valores de entrada e adiciona um novo intervalo Y
        para a posição X,Z especificada na estrutura de intervalos ativos.
        """
        try:
            z = self.z_layer_var.get()
            x = self.x_line_var.get()
            y_start = self.y_start_var.get()
            y_end = self.y_end_var.get()

            # Validar intervalo Y
            if y_start > y_end:
                messagebox.showerror("Erro", "O valor inicial do intervalo Y deve ser menor ou igual ao valor final.")
                return

            # Garantir que os dicionários existam
            if z not in self.active_intervals:
                self.active_intervals[z] = {}
            if x not in self.active_intervals[z]:
                self.active_intervals[z][x] = []

            # Verificar se o intervalo já existe
            new_interval = (y_start, y_end)
            if new_interval in self.active_intervals[z][x]:
                messagebox.showinfo("Informação", "Este intervalo já existe.")
                return

            # Adicionar o novo intervalo
            self.active_intervals[z][x].append(new_interval)

            # Atualizar a visualização
            self.update_intervals_display()

            # Atualizar visualização da malha
            self.update_visualization()

            # Limpar campos do intervalo Y para facilitar a inserção de novos
            self.y_start_var.set(0)
            self.y_end_var.set(0)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar intervalo: {str(e)}")

    def update_intervals_display(self):
        """
        Atualiza a exibição dos intervalos na árvore e no campo de texto

        Esta função atualiza a visualização dos intervalos ativos na interface,
        tanto na visualização em árvore quanto na representação textual.
        """
        # Atualizar treeview
        self.tree.delete(*self.tree.get_children())

        for z in sorted(self.active_intervals.keys()):
            z_node = self.tree.insert("", "end", text=f"Camada Z={z}", open=True)

            for x in sorted(self.active_intervals[z].keys()):
                intervals = self.active_intervals[z][x]
                intervals_str = ", ".join([f"({y1}, {y2})" for y1, y2 in intervals])
                x_node = self.tree.insert(z_node, "end", text=f"Linha X={x}", values=(intervals_str,))

        # Atualizar campo de texto

    def remove_selected_interval(self):
        """
        Remove todos os intervalos selecionados na árvore

        Esta função remove todos os itens selecionados na treeview,
        sejam eles camadas Z completas ou linhas X específicas.
        """
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Informação", "Selecione um item para remover.")
            return

        # Processa cada item selecionado
        items_removed = False
        for item_id in selected_items:
            parent_id = self.tree.parent(item_id)

            # Se for um nó de camada Z
            if not parent_id:
                z = int(self.tree.item(item_id)["text"].split("=")[1])
                if z in self.active_intervals:
                    del self.active_intervals[z]
                    items_removed = True
            # Se for um nó de linha X
            else:
                z = int(self.tree.item(parent_id)["text"].split("=")[1])
                x = int(self.tree.item(item_id)["text"].split("=")[1])
                if z in self.active_intervals and x in self.active_intervals[z]:
                    del self.active_intervals[z][x]
                    items_removed = True
                    # Se a camada Z ficou vazia, remover também
                    if not self.active_intervals[z]:
                        del self.active_intervals[z]

        if items_removed:
            # Atualizar a visualização
            self.update_intervals_display()
            self.update_visualization()
        else:
            messagebox.showinfo("Informação", "Nenhum item válido foi removido.")
    def clear_intervals(self):
        """
        Limpa todos os intervalos ativos

        Esta função remove todos os intervalos ativos após confirmação do usuário.
        """
        if messagebox.askyesno("Confirmação", "Remover todos os intervalos?"):
            self.active_intervals = {}
            self.update_intervals_display()
            self.update_visualization()

    def restore_defaults(self):
        """
        Restaura os valores padrão de todos os parâmetros

        Esta função restaura as dimensões da malha e os intervalos ativos
        para seus valores padrão após confirmação do usuário.
        """
        if messagebox.askyesno("Confirmação", "Restaurar todos os valores para o padrão?"):
            self.nx_var.set(8)
            self.ny_var.set(8)
            self.nz_var.set(3)
            self.load_default_intervals()
            self.update_visualization()

    def generate_mesh(self):
        """
        Gera a malha com os parâmetros atuais e chama o callback

        Esta função chama a função create_3d_mesh com os parâmetros atuais
        e armazena a malha resultante, além de chamar o callback se definido.

        Returns
        -------
        numpy.ndarray
            A malha 3D gerada
        """
        try:
            nx = self.nx_var.get()
            ny = self.ny_var.get()
            nz = self.nz_var.get()

            if self.active_intervals:
                # Gerar a malha usando a função fornecida
                self.mesh = self.create_3d_mesh(nx=nx, ny=ny, nz=nz, active_intervals=self.active_intervals)
                self.update_visualization()

                # Chamar o callback com a malha gerada
                if self.on_mesh_created:
                    self.on_mesh_created(self.mesh)

                messagebox.showinfo("Sucesso", f"Malha gerada com dimensões: {nx}x{ny}x{nz}")
            else:
                messagebox.showwarning("Aviso", "Não há intervalos ativos definidos. A malha será vazia.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar malha: {str(e)}")

    def update_visualization(self):
        """
        Atualiza a visualização da malha

        Esta função recria completamente o canvas e os gráficos para visualização
        da malha atual, ajustando ao tamanho disponível na janela.
        """
        try:
            # Gerar malha com parâmetros atuais
            nx = self.nx_var.get()
            ny = self.ny_var.get()
            nz = self.nz_var.get()

            # Destruir completamente o canvas atual
            if hasattr(self, 'canvas'):
                self.canvas.get_tk_widget().destroy()

            # Limpar todos os widgets filhos do frame de visualização
            for widget in self.visualization_frame.winfo_children():
                widget.destroy()

            # Obter as dimensões atuais do frame de visualização
            self.visualization_frame.update()
            frame_width = self.visualization_frame.winfo_width()
            frame_height = self.visualization_frame.winfo_height()

            # Criar nova figura com tamanho baseado no frame atual
            # Converter pixels para polegadas (assumindo 100 dpi)
            fig_width = max(5, frame_width / 100)
            fig_height = max(4, frame_height / 100)
            self.fig = Figure(figsize=(fig_width, fig_height), dpi=100)

            # Determinar o layout para os subplots
            if nz <= 3:
                rows, cols = 1, nz
            else:
                # Calcular layout aproximadamente quadrado
                cols = int(np.ceil(np.sqrt(nz)))
                rows = int(np.ceil(nz / cols))

            # Ajustar margens da figura
            self.fig.subplots_adjust(left=0.08, right=0.92, bottom=0.10, top=0.90, wspace=0.3, hspace=0.4)

            # Título principal
            self.fig.suptitle(f'Malha 3D ({nx}x{ny}x{nz})', fontsize=10)

            # Gerar a malha apenas se houver intervalos ativos
            if self.active_intervals:
                mesh = self.create_3d_mesh(nx=nx, ny=ny, nz=nz, active_intervals=self.active_intervals)
            else:
                # Criar uma malha vazia (tudo inativo) se não houver intervalos
                mesh = np.zeros((nx, ny, nz))

            # Criando subplots para cada camada Z
            for k in range(nz):
                ax = self.fig.add_subplot(rows, cols, k+1)

                # Usar uma paleta de cores personalizada para garantir que 0 seja branco
                # e 1 seja azul, sem valores intermediários
                custom_cmap = ListedColormap(['white', '#1f77b4'])  # branco para 0, azul para 1

                # Configurar os limites da escala de cores para garantir que apenas 0 e 1 sejam mostrados
                im = ax.imshow(mesh[:, :, k].T, cmap=custom_cmap, origin='lower', vmin=0, vmax=1)

                # Configurações do subplot
                ax.set_title(f'Z={k}', fontsize=9)
                ax.set_xlabel('X', fontsize=8)
                ax.set_ylabel('Y', fontsize=8)

                # Ajustar as marcações dos eixos
                ax.set_xticks(range(0, nx, max(1, nx//5)))
                ax.set_yticks(range(0, ny, max(1, ny//5)))
                ax.tick_params(axis='both', which='major', labelsize=7)

            # Adicionar barra de cores
            cax = self.fig.add_axes([0.93, 0.15, 0.02, 0.7])
            cbar = self.fig.colorbar(im, cax=cax, ticks=[0, 1])
            cbar.set_label('Estado', fontsize=8)
            cbar.set_ticklabels(['Inativa', 'Ativa'])

            # Criar novo canvas e empacotá-lo para preencher o frame
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.visualization_frame)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Desenhar o canvas
            self.canvas.draw()

            # Adicionar evento de redimensionamento
            self.visualization_frame.bind("<Configure>", self.on_frame_resize)

        except Exception as e:
            print(f"Erro na visualização: {str(e)}")
            import traceback
            traceback.print_exc()

    def on_frame_resize(self, event=None):
        """
        Responde ao redimensionamento do frame ajustando o tamanho da figura

        Parameters
        ----------
        event : tk.Event, optional
            Evento de redimensionamento
        """
        if hasattr(self, 'fig') and event is not None:
            # Cancela o agendamento anterior se existir
            if hasattr(self, 'resize_id') and self.resize_id is not None:
                try:
                    self.visualization_frame.after_cancel(self.resize_id)
                except ValueError:
                    # Ignora se o ID já for inválido (ex.: já foi cancelado)
                    pass
                finally:
                    self.resize_id = None  # Reseta o ID para evitar reutilização

            # Agenda uma nova atualização após 100ms
            self.resize_id = self.visualization_frame.after(100, self.update_visualization)

    def close_application(self):
        """
        Fecha a aplicação e notifica com a última malha gerada

        Esta função é chamada ao fechar a janela e garante que
        o callback seja notificado com a última malha gerada.
        """
        # Se houver uma malha gerada, notifique antes de fechar
        if hasattr(self, 'mesh') and self.on_mesh_created:
            self.on_mesh_created(self.mesh)
        self.root.destroy()