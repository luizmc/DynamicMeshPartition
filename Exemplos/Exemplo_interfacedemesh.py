import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import json
import ast
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap
import sys
import os

# Obtém o caminho absoluto do diretório atual do arquivo
current_dir = os.path.dirname(os.path.abspath(__file__))
# Sobe um nível para acessar o diretório pai
parent_dir = os.path.dirname(current_dir)
# Define o caminho do diretório 'source'
source_dir = os.path.join(parent_dir, "source")
# Adiciona o diretório 'source' ao sys.path
sys.path.append(source_dir)
# Agora você pode importar os módulos do diretório 'source'

# Importando o módulo que contém a classe MeshInterfaceApp

from mesh_interface import MeshInterfaceApp, open_mesh_interface
from refined_mesh_interface import RefinementInterfaceApp, open_refinement_interface
from mesh3d import refine_mesh


# Nota: Esta função seria sua função original
# Incluída apenas como referência - não duplicar se já existe no seu código

# Exemplo de uso:
if __name__ == "__main__":
    # Obter a malha da interface
    mesh = open_mesh_interface()
    
    # Verificar se a malha foi criada
    if mesh is not None:
        print(f"Malha retornada com dimensões: {mesh.shape}")
        print(f"Células ativas: {np.sum(mesh)}")
    else:
        print("Nenhuma malha foi gerada ou a operação foi cancelada.")

    # Refinar a malha
    refined_mesh = open_refinement_interface(
        mesh,
        refine_mesh
    )

    # Visualizar resultados
    print("Dimensões da malha refinada:", refined_mesh.shape)        