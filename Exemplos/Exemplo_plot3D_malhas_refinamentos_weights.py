"""
Este script utiliza o módulo mesh3d para operações com malhas tridimensionais, incluindo:

    Criação de malhas lógicas

    Aplicação de refinamentos locais

    Cálculo de projeções de peso

    Visualização gráfica 2D/3D

Módulos utilizados:
- numpy: Manipulação de arrays numéricos
- matplotlib: Visualização gráfica
- mesh3d: Operações especializadas com malhas 3D
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
import mesh_interface as mi


def main():
    """
    Fluxo principal de execução do programa.
    Copy
    
    Sequência de operações:
    1. Criação da malha base
    2. Definição de regiões de refinamento
    3. Aplicação dos refinamentos
    4. Cálculo dos pesos
    5. Visualização dos resultados
    """

    """
    Cria malha 3D inicial usando configurações padrão.

    :Returns:
        numpy.ndarray: 
            Array tridimensional (8x8x3) com células ativas/inativas. Valores:
            - 1: Célula ativa
            - 0: Célula inativa
            
    Ver também:
        :func:`mesh3d.create_3d_mesh` para detalhes de implementação
    """
    mesh = m3d.create_3d_mesh()
 #   mesh = mi.open_mesh_interface()

    """
    Dicionário de refinamentos com estrutura:

    :Dict[int, Dict[int, List[Tuple]]]:
        - Chave primária: Índice da camada Z (0-based)
        - Chave secundária: Índice da linha X (0-based)
        - Valor: Lista de tuplas com parâmetros de refinamento
        
    Formato das tuplas:
        (j_start, j_end, factor_i, factor_j, factor_k)
        
    Onde:
        - j_start: Índice inicial da coluna Y
        - j_end: Índice final da coluna Y
        - factor_i: Fator de refinamento em X
        - factor_j: Fator de refinamento em Y
        - factor_k: Fator de refinamento em Z
    """

    refinement_regions = {
        1: {
            3: [(3, 4, 2, 2, 1)],
            4: [(3, 4, 2, 2, 1)]
        },
        2: {
            3: [(3, 4, 2, 2, 1)],
            4: [(3, 4, 2, 2, 1)]
        }
    }

    """
    Aplica refinamentos na malha original.

    :Parameters:
        - mesh (numpy.ndarray): Malha 3D original
        - refinement_regions (dict): Regiões para refinamento
        
    :Returns:
        numpy.ndarray: 
            Malha refinada com mesma estrutura dimensional. Células refinadas
            têm valores multiplicados pelos fatores especificados
            
    :Note:
        - Apenas células originalmente ativas são refinadas
        - Fatores de refinamento são aplicados multiplicativamente
        
    Ver também:
        :func:`mesh3d.refine_mesh` para detalhes do algoritmo
    """

    refined_mesh = m3d.refine_mesh(mesh, refinement_regions)

    """
    Calcula projeção 2D dos pesos por soma ao longo do eixo Z.

    :Returns:
        numpy.ndarray:
            Matriz 2D (8x8) onde cada célula contém a soma dos valores
            das camadas Z correspondentes
            
    Ver também:
        :func:`mesh3d.compute_weight_array` para detalhes matemáticos
    """
    
    weight_array = m3d.compute_weight_array(refined_mesh)


    # Saída de dados simplificada
    # ===========================================================

    print("Malha Refinada (3 Camadas Z):")
    for i in range(3):
        print("\n Camada Z=",i)
        print(refined_mesh[:,:,0])

    print("\nArray de Pesos:")
    print(weight_array)

    """
    Gera visualização comparativa da malha:

    - Subplot esquerdo: Visualização binária (ativa/inativa)
    - Subplot direito: Visualização com cores por nível de refinamento

    Ver também:
        :func:`mesh3d.plot_both_mesh_views` para detalhes de implementação gráfica
    """   
    
    m3d.plot_both_mesh_views(refined_mesh)

    """
    Exibe matriz de pesos como heatmap 2D com valores numéricos

    Ver também:
        :func:`mesh3d.plot_weights` para opções de customização visual
    """

    m3d.plot_weights(weight_array)


    plt.show()

if __name__ == "__main__":
    main()
