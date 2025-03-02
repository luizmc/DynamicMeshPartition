import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definição da matriz de inércia tridimensional (exemplo)
I = np.array([[4, 1, 0],  # Ixx, Ixy, Ixz
              [1, 3, 0],  # Ixy, Iyy, Iyz
              [0, 0, 2]]) # Ixz, Iyz, Izz

# Cálculo dos valores próprios (momentos principais de inércia) e vetores próprios (eixos principais)
eigvals, eigvecs = np.linalg.eig(I)

# Criação da esfera unitária (malha de pontos)
theta = np.linspace(0, np.pi, 20)  # Ângulo polar
phi = np.linspace(0, 2*np.pi, 40)  # Ângulo azimutal
theta, phi = np.meshgrid(theta, phi)

# Coordenadas da esfera unitária
x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)

# Transformação da esfera pela matriz de inércia
sphere = np.array([x.flatten(), y.flatten(), z.flatten()])  # Vetores coluna de coordenadas
ellipsoid = I @ sphere  # Multiplicação matricial

# Extração das novas coordenadas
x_transf = ellipsoid[0].reshape(x.shape)
y_transf = ellipsoid[1].reshape(y.shape)
z_transf = ellipsoid[2].reshape(z.shape)

# Configuração da figura 3D
fig = plt.figure(figsize=(10, 5))

# Subplot da esfera original
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(x, y, z, color='b', alpha=0.5)
ax1.set_title("Esfera Unitária")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")

# Subplot do elipsoide transformado
ax2 = fig.add_subplot(122, projection='3d')
ax2.plot_surface(x_transf, y_transf, z_transf, color='r', alpha=0.5)

# Adiciona os vetores próprios (eixos principais do elipsoide)
for i in range(3):
    vec = eigvecs[:, i] * eigvals[i]  # Escalando os vetores pelos valores próprios
    ax2.plot([0, vec[0]], [0, vec[1]], [0, vec[2]], 'k', lw=2, label=f"Eixo {i+1}")

ax2.set_title("Elipsoide Transformado")
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_zlabel("Z")
ax2.legend()
ax2.set_box_aspect([1,1,1])  # Mantém a proporção correta dos eixos

plt.show()
