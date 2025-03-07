import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import json
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mesh3d as m3d

class MeshGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Malhas 3D")
        self.setup_ui()
        self.stdout_redirector = StdoutRedirector(self.output_text)
        sys.stdout = self.stdout_redirector

    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        # Painel de Controles
        control_frame = ttk.LabelFrame(main_frame, text="Parâmetros de Entrada")
        control_frame.pack(side='left', fill='y', padx=5, pady=5)

        # Configuração de Active Intervals
        ttk.Label(control_frame, text="Active Intervals").grid(row=0, column=0, sticky='w')
        self.active_tree = self.create_active_tree(control_frame)
        self.setup_active_controls(control_frame)

        # Configuração de Refinement Regions
        ttk.Label(control_frame, text="Refinement Regions").grid(row=4, column=0, sticky='w')
        self.refine_tree = self.create_refine_tree(control_frame)
        self.setup_refine_controls(control_frame)

        # Botão de Execução
        ttk.Button(control_frame, text="Executar Simulação", command=self.run_simulation).grid(row=8, column=0, pady=10)

        # Área de Visualização
        view_frame = ttk.Frame(main_frame)
        view_frame.pack(side='right', fill='both', expand=True)
        
        self.notebook = ttk.Notebook(view_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Área de Saída
        self.output_text = scrolledtext.ScrolledText(main_frame, height=10)
        self.output_text.pack(fill='x', side='bottom')

    def create_active_tree(self, parent):
        tree = ttk.Treeview(parent, columns=('k', 'i', 'interval'), show='headings', height=5)
        tree.heading('k', text='Camada (k)')
        tree.heading('i', text='Linha (i)')
        tree.heading('interval', text='Intervalo j')
        tree.grid(row=1, column=0, sticky='ew')
        return tree

    def create_refine_tree(self, parent):
        tree = ttk.Treeview(parent, columns=('k', 'i', 'interval', 'factors'), show='headings', height=5)
        tree.heading('k', text='Camada (k)')
        tree.heading('i', text='Linha (i)')
        tree.heading('interval', text='Intervalo j')
        tree.heading('factors', text='Fatores (i,j,k)')
        tree.grid(row=5, column=0, sticky='ew')
        return tree

    def setup_active_controls(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=2, column=0, pady=5)
        
        ttk.Label(frame, text="k:").pack(side='left')
        self.active_k = ttk.Spinbox(frame, from_=0, to=10, width=5)
        self.active_k.pack(side='left', padx=2)
        
        ttk.Label(frame, text="i:").pack(side='left')
        self.active_i = ttk.Spinbox(frame, from_=0, to=20, width=5)
        self.active_i.pack(side='left', padx=2)
        
        ttk.Label(frame, text="j:").pack(side='left')
        self.j_start = ttk.Spinbox(frame, from_=0, to=20, width=5)
        self.j_start.pack(side='left', padx=2)
        self.j_end = ttk.Spinbox(frame, from_=0, to=20, width=5)
        self.j_end.pack(side='left', padx=2)
        
        ttk.Button(frame, text="Adicionar", command=self.add_active).pack(side='left', padx=5)

    def setup_refine_controls(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=6, column=0, pady=5)
        
        ttk.Label(frame, text="k:").pack(side='left')
        self.refine_k = ttk.Spinbox(frame, from_=0, to=10, width=5)
        self.refine_k.pack(side='left', padx=2)
        
        ttk.Label(frame, text="i:").pack(side='left')
        self.refine_i = ttk.Spinbox(frame, from_=0, to=20, width=5)
        self.refine_i.pack(side='left', padx=2)
        
        ttk.Label(frame, text="j:").pack(side='left')
        self.refine_j_start = ttk.Spinbox(frame, from_=0, to=20, width=5)
        self.refine_j_start.pack(side='left', padx=2)
        self.refine_j_end = ttk.Spinbox(frame, from_=0, to=20, width=5)
        self.refine_j_end.pack(side='left', padx=2)
        
        ttk.Label(frame, text="Fatores:").pack(side='left')
        self.factor_i = ttk.Spinbox(frame, from_=1, to=10, width=3)
        self.factor_i.pack(side='left', padx=2)
        self.factor_j = ttk.Spinbox(frame, from_=1, to=10, width=3)
        self.factor_j.pack(side='left', padx=2)
        self.factor_k = ttk.Spinbox(frame, from_=1, to=10, width=3)
        self.factor_k.pack(side='left', padx=2)
        
        ttk.Button(frame, text="Adicionar", command=self.add_refine).pack(side='left', padx=5)

    def add_active(self):
        try:
            k = int(self.active_k.get())
            i = int(self.active_i.get())
            j_start = int(self.j_start.get())
            j_end = int(self.j_end.get())
            
            if j_end < j_start:
                raise ValueError("Intervalo inválido: j_end deve ser >= j_start")
                
            self.active_tree.insert('', 'end', values=(k, i, f"{j_start}-{j_end}"))
            
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def add_refine(self):
        try:
            k = int(self.refine_k.get())
            i = int(self.refine_i.get())
            j_start = int(self.refine_j_start.get())
            j_end = int(self.refine_j_end.get())
            fi = int(self.factor_i.get())
            fj = int(self.factor_j.get())
            fk = int(self.factor_k.get())
            
            if j_end < j_start:
                raise ValueError("Intervalo inválido: j_end deve ser >= j_start")
                
            self.refine_tree.insert('', 'end', values=(k, i, f"{j_start}-{j_end}", f"{fi},{fj},{fk}"))
            
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def run_simulation(self):
        try:
            # Limpar resultados anteriores
            for tab in self.notebook.tabs():
                self.notebook.forget(tab)
            self.output_text.delete('1.0', tk.END)
            
            # Construir parâmetros
            active_intervals = self.build_active_intervals()
            refinement_regions = self.build_refinement_regions()
            
            # Executar simulação
            mesh = m3d.create_3d_mesh(active_intervals=active_intervals)
            refined_mesh = m3d.refine_mesh(mesh, refinement_regions)
            weights = m3d.compute_weight_array(refined_mesh)
            
            # Gerar visualizações
            self.create_plot_tab(m3d.plot_weights, (weights,), "Matriz de Pesos")
            self.create_plot_tab(m3d.plot_both_mesh_views, (refined_mesh,), "Vistas da Malha")
            
            # Mostrar saída do console
            print("Simulação concluída com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro na Simulação", str(e))
            print(f"ERRO: {str(e)}")

    def build_active_intervals(self):
        intervals = {}
        for item in self.active_tree.get_children():
            k, i, j = self.active_tree.item(item, 'values')
            k = int(k)
            i = int(i)
            j_start, j_end = map(int, j.split('-'))
            
            if k not in intervals:
                intervals[k] = {}
            if i not in intervals[k]:
                intervals[k][i] = []
            intervals[k][i].append((j_start, j_end))
            
        return intervals

    def build_refinement_regions(self):
        regions = {}
        for item in self.refine_tree.get_children():
            k, i, j, factors = self.refine_tree.item(item, 'values')
            k = int(k)
            i = int(i)
            j_start, j_end = map(int, j.split('-'))
            fi, fj, fk = map(int, factors.split(','))
            
            if k not in regions:
                regions[k] = {}
            if i not in regions[k]:
                regions[k][i] = []
            regions[k][i].append((j_start, j_end, fi, fj, fk))
            
        return regions

    def create_plot_tab(self, plot_func, args, title):
        fig = Figure(figsize=(6, 4))
        plot_func(*args)
        
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=title)
        
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert('end', message)
        self.text_widget.see('end')

    def flush(self):
        pass

if __name__ == '__main__':
    root = tk.Tk()
    app = MeshGUI(root)
    root.mainloop()