import numpy as np
import matplotlib.pyplot as plt

# Definição da matriz de inércia bidimensional (exemplo)
I = np.array([[3, 1],  # Ixx e Ixy
              [1, 2]]) # Ixy e Iyy

# Cálculo dos valores próprios (momentos principais de inércia) e vetores próprios (eixos principais)
eigvals, eigvecs = np.linalg.eig(I)

# Criação do círculo unitário (pontos uniformemente distribuídos)
theta = np.linspace(0, 2*np.pi, 100)
circle = np.array([np.cos(theta), np.sin(theta)])  # Ponto (x, y) no círculo unitário

# Aplicação da matriz de inércia ao círculo para obter a elipse transformada
ellipse = I @ circle  # Multiplicação matricial

# Plotando o círculo original e a elipse transformada
fig, ax = plt.subplots(figsize=(6,6))
ax.plot(circle[0], circle[1], 'b--', label="Círculo Unitário")  # Círculo antes da transformação
ax.plot(ellipse[0], ellipse[1], 'r-', label="Elipse Transformada")  # Elipse depois da transformação

# Plotando os vetores próprios (eixos principais da elipse)
for i in range(2):
    vec = eigvecs[:, i] * eigvals[i]  # Escalando os vetores pelos valores próprios
    ax.plot([0, vec[0]], [0, vec[1]], 'k', lw=2, label=f"Eixo {i+1}")

# Configurações do gráfico
ax.axhline(0, color='gray', linewidth=0.5)  # Linha horizontal no zero
ax.axvline(0, color='gray', linewidth=0.5)  # Linha vertical no zero
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Transformação do Círculo pela Matriz de Inércia")
ax.legend()
ax.set_aspect('equal')  # Mantém a escala igual nos eixos

plt.show()
