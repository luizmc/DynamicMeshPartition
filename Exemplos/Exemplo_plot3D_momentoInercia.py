"""
Visualização da transformação de uma esfera unitária por uma matriz de inércia 3D.

Este script demonstra como uma matriz de inércia tridimensional deforma uma esfera unitária em um elipsoide,
exibindo os eixos principais calculados a partir dos autovetores da matriz.

Módulos utilizados:
- numpy: Cálculos numéricos e álgebra linear
- matplotlib: Visualização gráfica 2D/3D
- mpl_toolkits.mplot3d: Ferramentas para plotagem 3D
"""

import sys
import os

# Obtém o caminho absoluto do diretório atual do arquivo
current_dir = os.path.dirname(os.path.abspath(__file__))
# Sobe um nível para acessar o diretório pai
parent_dir = os.path.dirname(current_dir)
# Adiciona o diretório pai ao sys.path
sys.path.append(parent_dir)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
Matriz de inércia simétrica 3x3 para exemplo.

:Attributes:
- I[0,0] (float): Momento de inércia em X (Ixx)
- I[1,1] (float): Momento de inércia em Y (Iyy)
- I[2,2] (float): Momento de inércia em Z (Izz)
- I[0,1] (float): Produto de inércia Ixy
- I[0,2] (float): Produto de inércia Ixz
- I[1,2] (float): Produto de inércia Iyz

:Note:
- A matriz deve ser simétrica para representação física válida
- Valores não diagonais representam acoplamentos entre eixos
"""

I = np.array([[4, 1, 0], # Ixx, Ixy, Ixz
[1, 3, 0], # Ixy, Iyy, Iyz
[0, 0, 2]]) # Ixz, Iyz, Izz

"""
Calcula os momentos principais de inércia e eixos principais.

:Returns:
- eigvals (numpy.ndarray): Array 1D com autovalores (momentos principais).
- eigvecs (numpy.ndarray): Matriz 3x3 onde cada coluna é um autovetor.

:Note:
- Autovalores indicam as magnitudes dos eixos do elipsoide
- Autovetores definem a orientação dos eixos principais no espaço 3D
"""

eigvals, eigvecs = np.linalg.eig(I)

"""
Parametrização da esfera unitária em coordenadas esféricas.

:Attributes:
- theta (numpy.ndarray): Ângulo polar (inclinação)
- phi (numpy.ndarray): Ângulo azimutal (rotação)
- x, y, z (numpy.ndarray): Coordenadas cartesianas da malha
"""

theta = np.linspace(0, np.pi, 20) # Ângulo polar (0 a π)
phi = np.linspace(0, 2*np.pi, 40) # Ângulo azimutal (0 a 2π)
theta, phi = np.meshgrid(theta, phi)

x = np.sin(theta) * np.cos(phi) # Coordenada X da esfera
y = np.sin(theta) * np.sin(phi) # Coordenada Y da esfera
z = np.cos(theta) # Coordenada Z da esfera

"""
Transformação da esfera em elipsoide pela matriz de inércia.

:Note:
- A multiplicação matricial (@) aplica a transformação linear
- O reshape mantém a estrutura da malha para plotagem
"""

sphere = np.array([x.flatten(), y.flatten(), z.flatten()])
ellipsoid = I @ sphere # Aplicação da transformação linear

x_transf = ellipsoid[0].reshape(x.shape) # Coordenada X transformada
y_transf = ellipsoid[1].reshape(y.shape) # Coordenada Y transformada
z_transf = ellipsoid[2].reshape(z.shape) # Coordenada Z transformada

fig = plt.figure(figsize=(10, 5))

ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(x, y, z, color='b', alpha=0.5)
ax1.set_title("Esfera Unitária")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")

ax2 = fig.add_subplot(122, projection='3d')
ax2.plot_surface(x_transf, y_transf, z_transf, color='r', alpha=0.5)

for i in range(3):
    vec = eigvecs[:, i] * eigvals[i]
    ax2.plot([0, vec[0]], [0, vec[1]], [0, vec[2]], 'k', lw=2, label=f"Eixo {i+1}")
ax2.set_title("Elipsoide Transformado")
ax2.legend()
ax2.set_box_aspect([1,1,1]) # Mantém proporção isométrica
plt.show()