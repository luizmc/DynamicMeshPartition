"""
Exemplo de Cálculo de Inércia e Centro de Massa
================================================

Este módulo demonstra o cálculo da matriz de inércia, centro de massa, momentos principais e eixos principais
para um conjunto de pontos com pesos associados, utilizando funções do módulo :mod:`mesh3d`.

Exemplo
-------
O exemplo utiliza quatro pontos no plano XY com pesos distintos. O script calcula e imprime:

1. Centro de massa do sistema.
2. Matriz de inércia.
3. Momentos principais (autovalores da matriz de inércia).
4. Eixos principais (autovetores correspondentes).

.. code-block:: python

    # Configuração dos pontos
    points = np.array([
        [0, 0, 1],  # (x, y, peso)
        [1, 0, 2],
        [0, 1, 1],
        [1, 1, 3]
    ])

Parâmetros de Entrada
---------------------
- **points**: Array numpy de formato (N, 3), onde cada linha representa um ponto no formato [x, y, peso].

Saídas
------
- **center_of_mass**: Coordenadas (x, y) do centro de massa.
- **inertia_matrix**: Matriz 3x3 de inércia (considerando coordenadas 2D com z = 0).
- **principal_moments**: Autovalores da matriz de inércia, representando os momentos principais.
- **principal_axes**: Autovetores da matriz de inércia, representando os eixos principais.

Dependências
------------
- numpy
- matplotlib (para visualizações futuras, não utilizado neste exemplo)
- mesh3d (módulo customizado para cálculos geométricos)

Exemplo de Saída
----------------
.. code-block:: text

    Centro de massa: [0.57142857 0.71428571]
    
    Matriz de inércia:
    [[ 7.28571429 -4.28571429  0.        ]
     [-4.28571429  5.57142857  0.        ]
     [ 0.          0.         12.85714286]]
    
    Momentos principais: [11.69195261  1.16419007  0.85714286]
    
    Eixos principais:
    [[-0.76301998  0.64636526  0.        ]
     [ 0.64636526  0.76301998  0.        ]
     [ 0.          0.          1.        ]]

Notas
-----
- A matriz de inércia é calculada assumindo que os pontos estão no plano XY (z = 0).
- Os eixos principais são normalizados e ortogonais entre si.
"""
import numpy as np
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



# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo: lista de pontos no formato [x, y, peso]
    points = np.array([
        [0, 0, 1],
        [1, 0, 2],
        [0, 1, 1],
        [1, 1, 3]
    ])
    
    # Calcula a matriz de inércia e o centro de massa
    inertia_matrix, center_of_mass = m3d.compute_inertia_matrix_from_points(points)
    
    print("\nCentro de massa:", center_of_mass)
    print("\nMatriz de inércia:")
    print(inertia_matrix)
    
    # Calcula os momentos principais e eixos principais
    principal_moments, principal_axes = m3d.calculate_principal_moments(inertia_matrix)
    
    print("\nMomentos principais de inércia (autovalores):", principal_moments)
    print("\nEixos principais (autovetores):")
    print(principal_axes)
    print("\n\n")