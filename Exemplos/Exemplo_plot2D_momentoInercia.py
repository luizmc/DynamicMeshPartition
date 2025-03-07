"""
Visualização da transformação de um círculo unitário por uma matriz de inércia 2D.

Este script demonstra como uma matriz de inércia deforma um círculo unitário em uma elipse,
exibindo os eixos principais calculados a partir dos autovetores da matriz.

Módulos utilizados:
- numpy: Cálculos numéricos e álgebra linear
- matplotlib: Visualização gráfica
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
# Obtém o caminho absoluto do diretório atual do arquivo
current_dir = os.path.dirname(os.path.abspath(__file__))
# Sobe um nível para acessar o diretório pai
parent_dir = os.path.dirname(current_dir)
# Define o caminho do diretório 'source'
source_dir = os.path.join(parent_dir, "source")
# Adiciona o diretório 'source' ao sys.path
sys.path.append(source_dir)
# Agora você pode importar os módulos do diretório 'source'
import mesh3d as m3d

"""
Matriz de inércia simétrica 2x2 para exemplo.

:Attributes:
- I[0,0] (float): Momento de inércia em relação ao eixo X (Ixx)
- I[1,1] (float): Momento de inércia em relação ao eixo Y (Iyy)
- I[0,1] (float): Produto de inércia (Ixy)

:Note:
A matriz deve ser simétrica para representar corretamente uma matriz de inércia.
"""
I = np.array([[3, 1], # Ixx e Ixy
[1, 2]]) # Ixy e Iyy

"""
Calcula os momentos principais de inércia e eixos principais.

:Returns:
- eigvals (numpy.ndarray): Array 1D contendo os autovalores (momentos principais).
- eigvecs (numpy.ndarray): Matriz 2x2 onde cada coluna é um autovetor (eixo principal).

:Note:
- Autovalores representam os momentos de inércia máximo e mínimo
- Autovetores definem a orientação dos eixos principais
"""
eigvals, eigvecs = np.linalg.eig(I)

"""
Pontos do círculo unitário parametrizados por ângulo theta.

:Attributes:
- circle[0] (numpy.ndarray): Coordenadas X dos pontos do círculo
- circle[1] (numpy.ndarray): Coordenadas Y dos pontos do círculo
"""
theta = np.linspace(0, 2*np.pi, 100)
circle = np.array([np.cos(theta), np.sin(theta)])

"""
Aplica a transformação linear da matriz de inércia ao círculo unitário.

:Returns:
numpy.ndarray:
Coordenadas da elipse resultante com shape (2, 100).
- Linha 0: Coordenadas X transformadas
- Linha 1: Coordenadas Y transformadas

:Note:
A multiplicação matricial (@) é equivalente a np.dot() para arrays 2D.
"""
ellipse = I @ circle


fig, ax = plt.subplots(figsize=(6,6))
#Plot do círculo e elipse

ax.plot(circle[0], circle[1], 'b--', label="Círculo Unitário")
ax.plot(ellipse[0], ellipse[1], 'r-', label="Elipse Transformada")
#Plot dos eixos principais

for i in range(2):
    vec = eigvecs[:, i] * eigvals[i]
    ax.plot([0, vec[0]], [0, vec[1]], 'k', lw=2, label=f"Eixo {i+1}")
"""
Configurações finais da visualização:

    Limites dos eixos fixos em [-4, 4] para melhor comparação

    Legenda explicativa dos elementos gráficos

    Aspecto igual para evitar distorções na elipse
"""
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Transformação do Círculo pela Matriz de Inércia")
ax.legend()
ax.set_aspect('equal')

plt.show()

