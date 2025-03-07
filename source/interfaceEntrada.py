import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import mesh3d as m3d
import matplotlib.pyplot as plt

class MeshConfigurator:
    def __init__(self, root):
        self.root = root
        self.root.title("Configurador de Malha 3D")
        
        # Dicionários para armazenar configurações
        self.active_intervals = {}
        self.refinement_regions = {}
        
        # Notebook para separar as configurações
        self.notebook = ttk.Notebook(root)
        self.tab_active = ttk.Frame(self.notebook)
        self.tab_refine = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_active, text="Active Intervals")
        self.notebook.add(self.tab_refine, text="Refinement Regions")
        self.notebook.pack(expand=1, fill="both")
        
        # Widgets para Active Intervals
        self.build_active_interface(self.tab_active)
        
        # Widgets para Refinement Regions
        self.build_refine_interface(self.tab_refine)
        
        # Área de saída e botão de execução
        self.output_area = ScrolledText(root, height=10)
        self.output_area.pack(fill="x")
        
        btn_generate = ttk.Button(root, text="Gerar Malha e Plotar", command=self.generate_mesh)
        btn_generate.pack()

    def build_active_interface(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", padx=5, pady=5)
        
        ttk.Label(frame, text="Camada (k):").grid(row=0, column=0)
        self.active_layer = ttk.Spinbox(frame, from_=0, to=10, width=5)
        self.active_layer.grid(row=0, column=1)
        
        ttk.Label(frame, text="Linha (i):").grid(row=0, column=2)
        self.active_row = ttk.Spinbox(frame, from_=0, to=20, width=5)
        self.active_row.grid(row=0, column=3)
        
        ttk.Label(frame, text="Intervalo j (start, end):").grid(row=0, column=4)
        self.j_start = ttk.Spinbox(frame, from_=0, to=20, width=5)
        self.j_start.grid(row=0, column=5)
        self.j_end = ttk.Spinbox(frame, from_=0, to=20, width=5)
        self.j_end.grid(row=0, column=6)
        
        btn_add = ttk.Button(frame, text="Adicionar Intervalo", command=self.add_active_interval)
        btn_add.grid(row=0, column=7, padx=5)
        
        self.active_tree = ttk.Treeview(parent, columns=("k", "i", "interval"), show="headings")
        self.active_tree.heading("k", text="Camada (k)")
        self.active_tree.heading("i", text="Linha (i)")
        self.active_tree.heading("interval", text="Intervalo j")
        self.active_tree.pack(fill="both", expand=True)

    def build_refine_interface(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", padx=5, pady=5)
        
        ttk.Label(frame, text="Camada (k):").grid(row=0, column=0)
        self.refine_layer = ttk.Spinbox(frame, from_=0, to=10, width=5)
        self.refine_layer.grid(row=0, column=1)
        
        ttk.Label(frame, text="Linha (i):").grid(row=0, column=2)
        self.refine_row = ttk.Spinbox(frame, from_=0, to=20, width=5)
        self.refine_row.grid(row=0, column=3)
        
        ttk.Label(frame, text="Intervalo e fatores:").grid(row=0, column=4)
        self.refine_j_start = ttk.Spinbox(frame, from_=0, to=20, width=5)
        self.refine_j_start.grid(row=0, column=5)
        self.refine_j_end = ttk.Spinbox(frame, from_=0, to=20, width=5)
        self.refine_j_end.grid(row=0, column=6)
        
        ttk.Label(frame, text="Fatores (i,j,k):").grid(row=0, column=7)
        self.factor_i = ttk.Spinbox(frame, from_=1, to=10, width=3)
        self.factor_i.grid(row=0, column=8)
        self.factor_j = ttk.Spinbox(frame, from_=1, to=10, width=3)
        self.factor_j.grid(row=0, column=9)
        self.factor_k = ttk.Spinbox(frame, from_=1, to=10, width=3)
        self.factor_k.grid(row=0, column=10)
        
        btn_add = ttk.Button(frame, text="Adicionar Refinamento", command=self.add_refinement)
        btn_add.grid(row=0, column=11, padx=5)
        
        self.refine_tree = ttk.Treeview(parent, columns=("k", "i", "interval"), show="headings")
        self.refine_tree.heading("k", text="Camada (k)")
        self.refine_tree.heading("i", text="Linha (i)")
        self.refine_tree.heading("interval", text="Intervalo e Fatores")
        self.refine_tree.pack(fill="both", expand=True)

    def add_active_interval(self):
        try:
            k = int(self.active_layer.get())
            i = int(self.active_row.get())
            j_start = int(self.j_start.get())
            j_end = int(self.j_end.get())
            
            if j_end < j_start:
                raise ValueError("j_end deve ser maior ou igual a j_start")
                
            if k not in self.active_intervals:
                self.active_intervals[k] = {}
            
            if i not in self.active_intervals[k]:
                self.active_intervals[k][i] = []
            
            self.active_intervals[k][i].append((j_start, j_end))
            self.active_tree.insert("", "end", values=(k, i, f"({j_start}-{j_end})"))
            
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def add_refinement(self):
        try:
            k = int(self.refine_layer.get())
            i = int(self.refine_row.get())
            j_start = int(self.refine_j_start.get())
            j_end = int(self.refine_j_end.get())
            fi = int(self.factor_i.get())
            fj = int(self.factor_j.get())
            fk = int(self.factor_k.get())
            
            if j_end < j_start:
                raise ValueError("j_end deve ser maior ou igual a j_start")
                
            if k not in self.refinement_regions:
                self.refinement_regions[k] = {}
            
            if i not in self.refinement_regions[k]:
                self.refinement_regions[k][i] = []
            
            self.refinement_regions[k][i].append((j_start, j_end, fi, fj, fk))
            self.refine_tree.insert("", "end", values=(k, i, f"({j_start}-{j_end}) [{fi},{fj},{fk}]"))
            
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def generate_mesh(self):
        try:
            # Criar malha base
            mesh = m3d.create_3d_mesh(active_intervals=self.active_intervals or None)
            
            # Aplicar refinamentos
            refined_mesh = m3d.refine_mesh(mesh, self.refinement_regions)
            
            # Calcular pesos
            weights = m3d.compute_weight_array(refined_mesh)
            
            # Plotar resultados
            m3d.plot_both_mesh_views(refined_mesh)
            m3d.plot_weights(weights)
            plt.show()
            
            self.output_area.insert("end", "Malha gerada com sucesso!\n")
            
        except Exception as e:
            messagebox.showerror("Erro na geração", str(e))
            self.output_area.insert("end", f"Erro: {str(e)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MeshConfigurator(root)
    root.mainloop()