"""
Demonstração de criação, refinamento e visualização de malhas 3D com documentação Sphinx.

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
# Adiciona o diretório pai ao sys.path
sys.path.append(parent_dir)
# Agora você pode importar os módulos do diretório pai
import mesh3d as m3d

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

# Criação da malha base ====================================================
    mesh = m3d.create_3d_mesh()
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

    # Definição de refinamentos ================================================
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

    # Aplicação dos refinamentos ===============================================
    refined_mesh = m3d.refine_mesh(mesh, refinement_regions)
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

    # Cálculo dos pesos ========================================================
    weight_array = m3d.compute_weight_array(refined_mesh)
    """
    Calcula projeção 2D dos pesos por soma ao longo do eixo Z.

    :Returns:
        numpy.ndarray:
            Matriz 2D (8x8) onde cada célula contém a soma dos valores
            das camadas Z correspondentes
            
    Ver também:
        :func:`mesh3d.compute_weight_array` para detalhes matemáticos
    """

    # Saída de dados ===========================================================
    print("Malha Refinada (Camada Z=0):")
    print(refined_mesh[:,:,0])
    print("\nArray de Pesos:")
    print(weight_array)

    # Visualização gráfica =====================================================
    m3d.plot_both_mesh_views(refined_mesh)
    """
    Gera visualização comparativa da malha:

    - Subplot esquerdo: Visualização binária (ativa/inativa)
    - Subplot direito: Visualização com cores por nível de refinamento

    Ver também:
        :func:`mesh3d.plot_both_mesh_views` para detalhes de implementação gráfica
    """

    m3d.plot_weights(weight_array)
    """
    Exibe matriz de pesos como heatmap 2D com valores numéricos

    Ver também:
        :func:`mesh3d.plot_weights` para opções de customização visual
    """

    plt.show()

if __name__ == "__main__":
    main()
