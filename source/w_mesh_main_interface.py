import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap

from w_mesh_interface import MeshInterfaceApp
from w_refined_mesh_interface import RefinementInterfaceApp
from mesh3d import refine_mesh, create_3d_mesh  # Certifique-se de ter mesh3d.py in the same directory

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface Combinada")
        self.root.geometry("1200x800")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.mesh_tab = ttk.Frame(self.notebook)
        self.refined_mesh_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.mesh_tab, text="Malha Inicial")
        self.notebook.add(self.refined_mesh_tab, text="Refinamento da Malha")

        self.mesh = None  # Armazenará a malha gerada na primeira aba
        self.refined_mesh = None # Armazenara a malha refinada na segunda aba

        self.create_mesh_interface()
        self.create_refined_mesh_interface()

    def create_mesh_interface(self):
        # Corrected: Pass self.mesh_tab as root
        self.mesh_app = MeshInterfaceApp(root=self.mesh_tab, mesh_function=create_3d_mesh, on_mesh_created=self.store_mesh)
        # self.mesh_app.root = self.mesh_tab  # No need to reassign

    def create_refined_mesh_interface(self):
         # Corrected: Pass self.refined_mesh_tab as root
        self.refined_mesh_app = RefinementInterfaceApp(root=self.refined_mesh_tab, mesh=np.zeros((5,5,5)), refine_function=refine_mesh, on_refinement_complete=self.store_refined_mesh)
        # self.refined_mesh_app.root = self.refined_mesh_tab # No need to reassign

        # Desabilitar a aba de refinamento no início
        self.notebook.tab(1, state="disabled")


    def store_mesh(self, mesh):
        """
        Armazena a malha gerada e habilita a aba de refinamento.
        """
        self.mesh = mesh
        # Atualizar a malha na aba de refinamento
        self.refined_mesh_app.mesh = self.mesh
        self.refined_mesh_app.nx, self.refined_mesh_app.ny, self.refined_mesh_app.nz = self.mesh.shape

        # Limpar regiões existentes antes de atualizar visualização
        self.refined_mesh_app.clear_regions()

        # Atualizar visualização com a nova malha
        self.refined_mesh_app.update_visualization()

        # Recriar widgets and reload default regions (Not needed, keep existing widgets, just update data and limits)
        # self.refined_mesh_app.create_widgets() # No need to recreate widgets
        self.refined_mesh_app.load_default_regions()
#        self.refined_mesh_app.update_spinbox_limits() # Probably wrong, then commented

        # Habilitar a aba de refinamento
        self.notebook.tab(1, state="normal")

    def store_refined_mesh(self, mesh):
        self.refined_mesh = mesh

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(True, True)  # Garante que a janela principal seja redimensionável em largura e altura
    app = MainApp(root)
    root.mainloop()