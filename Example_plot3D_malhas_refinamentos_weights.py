import numpy as np
import matplotlib.pyplot as plt
import mesh3d as m3d
import sys

# Funções create_3d_mesh, refine_mesh e compute_weight_array devem estar definidas aqui ou importadas


# Código principal
if __name__ == "__main__":
    # Parâmetros do grid
    # nx, ny, nz = 8, 8, 3 exemplo de valores padrão
    # active_intervals = { 
    #        0: {2: [(3, 4)], 3: [(2, 5)], 4: [(2, 5)], 5: [(3, 4)]},
    #        1: {1: [(2, 5)], 2: [(1, 6)], 3: [(1, 6)], 4: [(1, 6)], 5: [(1, 6)], 6: [(2, 5)]},
    #        2: {0: [(2, 5)], 1: [(1, 6)], 2: [(0, 7)], 3: [(0, 7)], 4: [(0, 7)], 5: [(0, 7)], 6: [(1, 6)], 7: [(2, 5)]}
    #    } exemplo de valores padrão com apenas três níveis na direção Z
    #
    mesh = m3d.create_3d_mesh() # Exemplo sem parâmetros, utiliza os valores padrão, ver documentação para entrada de parâmetros
    
    # 1: {  # refinar apenas na camada Z=1  # Exemplo de refinamento 
    # refinement_regions = {
    #     3: [(2, 4, 2, 2, 1), (5, 6, 3, 1, 1)],  # linha X=3 com dois intervalos de refinamento
    #     4: [(3, 5, 2, 3, 1)]                     # linha X=4 com um intervalo de refinamento
    # },
    # 2: {  # também refinar na camada Z=2
    #     2: [(1, 3, 1, 2, 2)]                     # linha X=2 com um intervalo de refinamento
    # }
    # }
    # refinement_regions : dict
    #     Dicionário definindo as regiões de refinamento. A estrutura do dicionário é:
    #     {k: {i: [(j_start, j_end, factor_i, factor_j, factor_k), ...], ...}, ...} onde:
    #     - k é o índice da camada (direção Z)
    #     - i é o índice da linha (direção X)
    #     - (j_start, j_end, factor_i, factor_j, factor_k) são tuplas definindo:
    #       * j_start, j_end: intervalo de colunas a serem refinadas (direção Y)
    #       * factor_i, factor_j, factor_k: fatores de refinamento nas direções X, Y e Z

    refinement_regions = { # exemplo do artigo
    1: {  # refinar  na camada Z=1
        3: [(3, 4, 2, 2, 1)],  # linha X=3 com um intervalo de refinamento
        4: [(3, 4, 2, 2, 1)]   # linha X=4 com um intervalo de refinamento
    },
    2: {  # também refinar na camada Z=2
        3: [(3, 4, 2, 2, 1)],                    # linha X=3 com um intervalo de refinamento
        4: [(3, 4, 2, 2, 1)],                    # linha X=4 com um intervalo de refinamento    
    }
    }

    refined_mesh = m3d.refine_mesh(mesh, refinement_regions)
    
    # Cálculo do array de pesos
    weight_array = m3d.compute_weight_array(refined_mesh)
    
    print("Malha Refinada:")
    print(refined_mesh[:,:,0])  # Camada inferior
    print(refined_mesh[:,:,1])  # Camada média
    print(refined_mesh[:,:,2])  # Camada superior
    print("Array de Pesos:")
    print(weight_array)
    
    # Plotagem da malha 3D com pesos
   # m3d.plot_3d_mesh_with_weights(refined_mesh,show_refinement=True)
    m3d.plot_both_mesh_views(refined_mesh)
    m3d.plot_weights(weight_array)
    plt.show()
