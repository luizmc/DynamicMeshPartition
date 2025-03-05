import math
import random
import itertools
import numpy as np

def generate_input_dictionary_old(m, p):
    """
    Gera um dicionário com coordenadas únicas e pesos aleatórios.
    
    Parameters
    ----------
    m : int
        Primeira dimensão (variação de 0 a m-1).
    p : int
        Segunda dimensão (variação de 0 a p-1).
    
    Returns
    -------
    dict
        Dicionário com coordenadas como chaves (tuplas (i,j)) e pesos aleatórios como valores.
    """
    # Gera todas as combinações possíveis de coordenadas
    all_coordinates = list(itertools.product(range(m), range(p)))
    
    # Escolhe um número aleatório de coordenadas (entre metade e todas)
    num_coords = random.randint(len(all_coordinates) // 2, len(all_coordinates))
    coordinates = random.sample(all_coordinates, num_coords)
    
    # Cria o dicionário com coordenadas e pesos aleatórios
    input_dict = {coord: random.randint(1, 8) for coord in coordinates}
    
    return input_dict

def generate_input_dictionary(m, p):
    """
    Gera um dicionário com todas as coordenadas possíveis e pesos aleatórios.
    
    Parameters
    ----------
    m : int
        Primeira dimensão (variação de 0 a m-1).
    p : int
        Segunda dimensão (variação de 0 a p-1).
    
    Returns
    -------
    dict
        Dicionário com coordenadas como chaves (tuplas (i,j)) e pesos como valores.
        Aproximadamente 60% dos pesos serão aleatórios (1-8) e 40% serão zero.
    """
    # Gera todas as combinações possíveis de coordenadas
    all_coordinates = list(itertools.product(range(m), range(p)))
    
    # Inicializa o dicionário com todas as coordenadas tendo peso zero
    input_dict = {coord: 0 for coord in all_coordinates}
    
    # Preenche aproximadamente 70% das entradas do dicionário com pesos aleatórios
    for coord in all_coordinates:
        if random.random() < 0.6:  # 70% de chance de alterar o peso
            input_dict[coord] = random.randint(1, 8)
    
    return input_dict

def compute_inertia_matrix_from_points(points):
    """
    Calcula a matriz de inércia e o centro de massa a partir de um conjunto de pontos 2D com pesos.
    
    Parameters
    ----------
    points : array-like
        Array de formato (n, 3) onde cada linha representa um ponto [x, y, peso].
    
    Returns
    -------
    tuple
        (I, center_of_mass) onde:
            - I: Matriz de inércia 2x2.
            - center_of_mass: Tupla (x_bar, y_bar) com as coordenadas do centro de massa.
    """
    points = np.array(points)  # Garante que os pontos estão como um array NumPy
    
    # Extrai as coordenadas x, y e os pesos
    x_coords = points[:, 0]
    y_coords = points[:, 1]
    weights = points[:, 2]
    
    # Calcula o centro de massa
    total_weight = np.sum(weights)
    if total_weight == 0:
        x_bar, y_bar = 0, 0  # Valor padrão apropriado
    else:
        x_bar = np.sum(weights * x_coords) / total_weight
        y_bar = np.sum(weights * y_coords) / total_weight
    
    # Construção da matriz de inércia
    I_xx = np.sum(weights * (y_coords - y_bar) ** 2)  # Momento de inércia em relação ao eixo x
    I_yy = np.sum(weights * (x_coords - x_bar) ** 2)  # Momento de inércia em relação ao eixo y
    I_xy = -np.sum(weights * (x_coords - x_bar) * (y_coords - y_bar))  # Produto de inércia
    
    I = np.array([[I_xx, I_xy],
                  [I_xy, I_yy]])
    
    return I, (x_bar, y_bar)

def calculate_principal_moments(inertia_matrix):
    """
    Calcula os momentos principais de inércia e os eixos principais a partir de uma matriz de inércia.
    
    Esta função decompõe a matriz de inércia em seus valores próprios (momentos principais) 
    e vetores próprios (eixos principais).
    
    Parameters
    ----------
    inertia_matrix : numpy.ndarray
        Matriz de inércia simétrica (2x2 ou 3x3).
    
    Returns
    -------
    tuple
        (principal_moments, principal_axes) onde:
            - principal_moments: numpy.ndarray - Momentos principais de inércia (valores próprios).
            - principal_axes: numpy.ndarray - Eixos principais (vetores próprios), cada coluna é um eixo.
    """
    # Verifica se a matriz é simétrica (propriedade importante para matrizes de inércia)
    if not np.allclose(inertia_matrix, inertia_matrix.T):
        raise ValueError("A matriz de inércia deve ser simétrica")
    
    # Calcula os valores próprios (momentos principais) e vetores próprios (eixos principais)
    principal_moments, principal_axes = np.linalg.eig(inertia_matrix)
    
    return principal_moments, principal_axes

def normalize_vectors(vectors):
    """
    Normaliza os vetores para que tenham norma unitária.
    
    Parameters
    ----------
    vectors : numpy.ndarray
        Matriz onde cada coluna é um vetor a ser normalizado.
    
    Returns
    -------
    numpy.ndarray
        Matriz com os vetores normalizados.
    """
    # Calcula as normas de cada vetor
    norms = np.sqrt(np.sum(vectors**2, axis=0))
    
    # Normaliza cada vetor dividindo pela sua norma
    # Adiciona pequeno valor para evitar divisão por zero
    normalized_vectors = vectors / (norms + 1e-10)
    
    return normalized_vectors

def project_points_on_eigenvector(points, center_of_mass, eigenvector):
    """
    Projeta pontos na direção do autovetor a partir do centro de massa.
    
    Parameters
    ----------
    points : array-like
        Array de formato (n, 3) onde cada linha representa um ponto [x, y, peso].
    center_of_mass : tuple
        Tupla (x_center, y_center) com as coordenadas do centro de massa.
    eigenvector : array-like
        Vetor unitário representando o autovetor [a, b].
    
    Returns
    -------
    numpy.ndarray
        Array com as projeções dos pontos.
    """
    # Extrai coordenadas do centro de massa
    xc, yc = center_of_mass
    
    # Extrai coordenadas x e y dos pontos
    x_coords = points[:, 0]
    y_coords = points[:, 1]
    weights = points[:, 2]
    
    # Extrai componentes do autovetor
    a, b = eigenvector
    
    # Calcula projeções
    projections = np.column_stack([
        x_coords,
        y_coords,
        weights,
        (a * (x_coords - xc) + b * (y_coords - yc)) * a + x_coords,
        (a * (x_coords - xc) + b * (y_coords - yc)) * b + y_coords
    ])
    
    return projections

def calculate_max_distance(projections):
    """
    Calcula a distância máxima entre quaisquer dois pontos projetados.
    
    Parameters
    ----------
    projections : numpy.ndarray
        Array com as projeções dos pontos, onde as colunas 3 e 4 são as coordenadas
        x e y das projeções.
    
    Returns
    -------
    float
        Maior distância encontrada entre os pontos projetados.
    """
    max_distance = 0
    n = projections.shape[0]
    
    # Compara cada ponto com todos os outros
    for i in range(n):
        for j in range(i+1, n):
            # Calcula distância euclidiana entre os pontos projetados
            dist = np.sqrt((projections[i, 3] - projections[j, 3])**2 + 
                         (projections[i, 4] - projections[j, 4])**2)
            max_distance = max(max_distance, dist)
    
    return max_distance


def find_best_projection_and_division_balanced(input_dict, n1, n2):
    """
    Finds the best projection for dividing a set into two balanced, connected subsets.
    
    Parameters
    ----------
    input_dict : dict
        Dictionary with coordinates as keys and weights as values.
    n1 : int
        Target number of elements in the first subset.
    n2 : int
        Target number of elements in the second subset.
    
    Returns
    -------
    tuple
        (first_subset, second_subset) both are dictionaries.
    """
    # Convert dictionary to array
    points = np.array([[coord[0], coord[1], weight] for coord, weight in input_dict.items()])
    
    # Calculate inertia matrix and center of mass
    inertia_matrix, center_of_mass = compute_inertia_matrix_from_points(points)
    
    # Calculate principal moments and principal axes
    principal_moments, principal_axes = calculate_principal_moments(inertia_matrix)
    
    # Normalize eigenvectors
    principal_axes = normalize_vectors(principal_axes)
    
    # Project points onto eigenvectors
    projections1 = project_points_on_eigenvector(points, center_of_mass, principal_axes[:, 0])
    projections2 = project_points_on_eigenvector(points, center_of_mass, principal_axes[:, 1])
    
    # Calculate max distance for each projection
    max_dist1 = calculate_max_distance(projections1)
    max_dist2 = calculate_max_distance(projections2)
    
    # Choose projection with less dispersion
    chosen_projections = projections1 if max_dist1 <= max_dist2 else projections2
    chosen_axis = principal_axes[:, 0] if max_dist1 <= max_dist2 else principal_axes[:, 1]
    
    # Calculate projection value for each point (distance along the chosen axis)
    projection_values = np.zeros(chosen_projections.shape[0])
    for i in range(chosen_projections.shape[0]):
        x, y = chosen_projections[i, 0], chosen_projections[i, 1]
        # Calculate projection value as the dot product with the axis
        projection_values[i] = (x - center_of_mass[0]) * chosen_axis[0] + (y - center_of_mass[1]) * chosen_axis[1]
    
    # Convert coordinates to tuples for dict keys
    coords = [(int(chosen_projections[i, 0]), int(chosen_projections[i, 1])) for i in range(chosen_projections.shape[0])]
    
    # Sort points by projection value
    sorted_indices = np.argsort(projection_values)
    sorted_coords = [coords[i] for i in sorted_indices]
    
    # Calculate total weight
    total_weight = sum(input_dict.values())
    target_weight1 = (total_weight * n1) / (n1 + n2)
    
    # Helper functions for connectivity
    def is_connected(subset):
        """Check if a subset of coordinates forms a connected component"""
        if not subset:
            return True
        
        coords = list(subset.keys())
        visited = set()
        queue = [coords[0]]
        visited.add(coords[0])
        
        while queue:
            current = queue.pop(0)
            i, j = current
            neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
            
            for neighbor in neighbors:
                if neighbor in subset and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited) == len(subset)
    
    # Try different cut points to find a balanced division that maintains connectivity
    best_imbalance = float('inf')
    best_first_subset = {}
    best_second_subset = {}
    
 
    # Modificar esta parte:
    for cut_index in range(1, len(sorted_coords)):
        # Create two potential subsets
        first_subset = {sorted_coords[i]: input_dict[sorted_coords[i]] for i in range(cut_index)}
        second_subset = {sorted_coords[i]: input_dict[sorted_coords[i]] for i in range(cut_index, len(sorted_coords))}
        
        # Check connectivity
        if is_connected(first_subset) and is_connected(second_subset):
            # Calculate weight imbalance
            weight1 = sum(first_subset.values())
            weight2 = sum(second_subset.values())
            
            # MODIFICAÇÃO: Remover o cálculo do size_imbalance e usar apenas weight_imbalance
            weight_imbalance = abs(weight1 - target_weight1)
            
            # MODIFICAÇÃO: Usar apenas normalized_weight_imb como métrica de imbalance 
            normalized_weight_imb = weight_imbalance / total_weight
            
            # MODIFICAÇÃO: imbalance agora considera apenas o peso
            imbalance = normalized_weight_imb
            
            if imbalance < best_imbalance:
                best_imbalance = imbalance
                best_first_subset = first_subset
                best_second_subset = second_subset

    # If we couldn't find connected subsets with the direct approach, use region growing
    if not best_first_subset or not best_second_subset:
        return region_growing_partition(input_dict, n1, n2, sorted_coords)
    
    return best_first_subset, best_second_subset

def region_growing_partition(input_dict, n1, n2, sorted_coords):
    """
    Uses region growing to create connected, balanced partitions.
    
    Parameters
    ----------
    input_dict : dict
        Dictionary with coordinates as keys and weights as values.
    n1, n2 : int
        Target sizes for the subsets.
    sorted_coords : list
        Coordinates sorted by projection value.
    
    Returns
    -------
    tuple
        (first_subset, second_subset) both are dictionaries.
    """
    # Initialize with seeds at opposite ends
    first_seed = sorted_coords[0]
    second_seed = sorted_coords[-1]
    
    first_subset = {first_seed: input_dict[first_seed]}
    second_subset = {second_seed: input_dict[second_seed]}
    assigned = {first_seed, second_seed}
    
    total_weight = sum(input_dict.values())
    target_weight1 = (total_weight * n1) / (n1 + n2)
    target_weight2 = total_weight - target_weight1
    
    target_size1 = (len(input_dict) * n1) // (n1 + n2)
    target_size2 = len(input_dict) - target_size1
    
    # Helper function to find unassigned neighbors
    def get_unassigned_neighbors(subset):
        neighbors = set()
        for coord in subset:
            i, j = coord
            for neighbor in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
                if neighbor in input_dict and neighbor not in assigned:
                    neighbors.add(neighbor)
        return neighbors
    
    # Grow regions until all points are assigned
    while len(assigned) < len(input_dict):
        first_neighbors = get_unassigned_neighbors(first_subset)
        second_neighbors = get_unassigned_neighbors(second_subset)
        
        if not first_neighbors and not second_neighbors:
            break
        
        # Calculate current weights
        weight1 = sum(first_subset.values())
        weight2 = sum(second_subset.values())
        
        # Calculate how far each subset is from its target weight
        weight_deficit1 = target_weight1 - weight1
        weight_deficit2 = target_weight2 - weight2
        
        # MODIFICAÇÃO: Remover o cálculo dos déficits de tamanho (size_deficit)
        
        # Normalize weight deficits
        weight_deficit_norm1 = weight_deficit1 / target_weight1 if target_weight1 > 0 else 0
        weight_deficit_norm2 = weight_deficit2 / target_weight2 if target_weight2 > 0 else 0
        
        # MODIFICAÇÃO: Usar apenas os déficits de peso como critério
        deficit1 = weight_deficit_norm1
        deficit2 = weight_deficit_norm2
 
    # Handle remaining unassigned points
    unassigned = [coord for coord in input_dict if coord not in assigned]
    
    # MODIFICAÇÃO: Atribuir pontos restantes apenas com base no déficit de peso
    for coord in unassigned:
        weight1 = sum(first_subset.values())
        weight2 = sum(second_subset.values())
        
        # Determine which subset needs this point more based only on weight
        if abs(weight1 + input_dict[coord] - target_weight1) < abs(weight1 - target_weight1):
            first_subset[coord] = input_dict[coord]
        else:
            second_subset[coord] = input_dict[coord]
  
    return first_subset, second_subset

def find_best_projection_and_division_old(input_dict, n1, n2):
    """
    Encontra a melhor projeção para divisão do conjunto em dois subconjuntos.
    
    Parameters
    ----------
    input_dict : dict
        Dicionário com coordenadas como chaves e pesos como valores.
    n1 : int
        Número de elementos desejados no primeiro subconjunto.
    n2 : int
        Número de elementos desejados no segundo subconjunto.
    
    Returns
    -------
    tuple
        (first_subset, second_subset) ambos são dicionários.
    """
    # Converte o dicionário em um array
    points = np.array([[coord[0], coord[1], weight] for coord, weight in input_dict.items()])
    
    # Calcular matriz de inércia e centro de massa
    inertia_matrix, center_of_mass = compute_inertia_matrix_from_points(points)
    
    # Calcula momentos principais e eixos principais
    principal_moments, principal_axes = calculate_principal_moments(inertia_matrix)
    
    # Normaliza os autovetores
    principal_axes = normalize_vectors(principal_axes)
    
    # Projeta os pontos nos dois autovetores
    projections1 = project_points_on_eigenvector(points, center_of_mass, principal_axes[:, 0])
    projections2 = project_points_on_eigenvector(points, center_of_mass, principal_axes[:, 1])
    
    # Calcula a distância máxima para cada projeção
    max_dist1 = calculate_max_distance(projections1)
    max_dist2 = calculate_max_distance(projections2)
    
    # Escolhe a projeção com menor dispersão
    if max_dist1 <= max_dist2:
        chosen_projections = projections1
    else:
        chosen_projections = projections2
    
    # Ordena as projeções
    # Primeiro calcula um valor escalar para ordenação (distância projetada do centro de massa)
    sort_values = np.sqrt((chosen_projections[:, 3] - center_of_mass[0])**2 + 
                          (chosen_projections[:, 4] - center_of_mass[1])**2)
    
    # Ordena os índices baseados nos valores de ordenação
    sorted_indices = np.argsort(sort_values)
    sorted_projections = chosen_projections[sorted_indices]
    
    # Recalcula mapeamento para o dicionário original
    sorted_coords = [(int(sorted_projections[i, 0]), int(sorted_projections[i, 1])) 
                      for i in range(sorted_projections.shape[0])]
    
    # Calcula os pesos acumulados
    total_weight = np.sum([input_dict[coord] for coord in sorted_coords])
    target_weight = (total_weight * n1) / (n1 + n2)
    
    # Encontra o índice de corte ótimo
    cumulative_weights = np.zeros(len(sorted_coords))
    for i in range(len(sorted_coords)):
        cumulative_weights[i] = input_dict[sorted_coords[i]]
        if i > 0:
            cumulative_weights[i] += cumulative_weights[i-1]
    
    # Encontra o índice que minimiza a diferença com o peso alvo
    weight_diffs = np.abs(cumulative_weights - target_weight)
    cut_index = np.argmin(weight_diffs)
    
    # Divide os pontos em dois grupos
    first_subset = {sorted_coords[i]: input_dict[sorted_coords[i]] for i in range(cut_index + 1)}
    second_subset = {sorted_coords[i]: input_dict[sorted_coords[i]] for i in range(cut_index + 1, len(sorted_coords))}
    
    return first_subset, second_subset


def recursive_binary_subset_division_balanced(input_dict, n_subsets=2, current_depth=0, binary_prefix=''):
    """
    Recursively divides a set of weighted coordinates into balanced, connected subsets.
    
    Parameters
    ----------
    input_dict : dict
        Dictionary of coordinates and weights.
    n_subsets : int
        Total number of desired subsets.
    current_depth : int
        Current recursion depth.
    binary_prefix : str
        Current binary prefix for subset identification.
    
    Returns
    -------
    dict
        Dictionary of subsets identified by binary strings.
    """
    # Base case: if n_subsets=1 or empty dictionary
    if n_subsets <= 1 or len(input_dict) <= 1:
        return {binary_prefix: input_dict}
    
    # Calculate balanced numbers for each branch
    n1 = n_subsets // 2
    n2 = n_subsets - n1
    
    # Divide set into two balanced, connected subsets
    first_subset, second_subset = find_best_projection_and_division_balanced(input_dict, n1, n2)
    
    # Recursive calls for each subset
    result = {}
    
    if first_subset:
        result.update(recursive_binary_subset_division_balanced(
            first_subset, 
            n1, 
            current_depth + 1, 
            binary_prefix + '0'
        ))
    
    if second_subset:
        result.update(recursive_binary_subset_division_balanced(
            second_subset, 
            n2, 
            current_depth + 1, 
            binary_prefix + '1'
        ))
    
    return result
def recursive_binary_subset_division(input_dict, n_subsets=2, current_depth=0, binary_prefix=''):
    """
    Divide recursivamente um conjunto de coordenadas com pesos em subconjuntos baseados
    em centro de massa e autovetores.
    
    Parameters
    ----------
    input_dict : dict
        Dicionário de coordenadas e pesos.
    n_subsets : int
        Número total de subconjuntos desejados.
    current_depth : int
        Profundidade atual da recursão.
    binary_prefix : str
        Prefixo binário atual para identificação dos subconjuntos.
    
    Returns
    -------
    dict
        Dicionário de subconjuntos identificados por strings binárias.
    """
    # Condição de parada: se n_subsets=1 ou profundidade máxima atingida
    if n_subsets <= 1 or len(input_dict) <= 1:
        return {binary_prefix: input_dict}
    
    # Calcula n1 e n2 (número de subconjuntos para cada metade)
    if n_subsets % 2 == 0:
        n1 = n2 = n_subsets // 2
    else:
        n1 = n_subsets // 2
        n2 = n_subsets // 2 + 1
    
    # Divide o conjunto em dois subconjuntos baseados na matriz de inércia
    first_subset, second_subset = find_best_projection_and_division(input_dict, n1, n2)
    
    # Chamadas recursivas para cada metade
    result = {}
    
    # Só faz a chamada recursiva se o subconjunto tiver elementos
    if first_subset:
        result.update(recursive_binary_subset_division(
            first_subset, 
            n1, 
            current_depth + 1, 
            binary_prefix + '0'
        ))
    
    if second_subset:
        result.update(recursive_binary_subset_division(
            second_subset, 
            n2, 
            current_depth + 1, 
            binary_prefix + '1'
        ))
    
    return result

def evaluate_partition_quality(result, original_dict):
    """
    Avalia a qualidade da partição considerando equilibrio de pesos.
    
    Parameters
    ----------
    result : dict
        Dicionário de subconjuntos gerados pelo algoritmo.
    original_dict : dict
        Dicionário original de coordenadas e pesos.
    
    Returns
    -------
    dict
        Estatísticas da partição.
    """
    # Calcula pesos totais de cada subconjunto
    subset_weights = [sum(subset.values()) for subset in result.values()]
    
    # Calcula estatísticas
    total_weight = sum(original_dict.values())
    mean_weight = total_weight / len(result)
    max_weight = max(subset_weights)
    min_weight = min(subset_weights)
    weight_variance = np.var(subset_weights)
    weight_range = max_weight - min_weight
    weight_percentage_range = (weight_range / mean_weight) * 100
    
    # Número de pontos em cada subconjunto
    subset_sizes = [len(subset) for subset in result.values()]
    
    return {
        'total_weight': total_weight,
        'mean_weight': mean_weight,
        'max_weight': max_weight,
        'min_weight': min_weight,
        'weight_variance': weight_variance,
        'weight_range': weight_range,
        'weight_percentage_range': weight_percentage_range,
        'subset_weights': subset_weights,
        'subset_sizes': subset_sizes
    }

def convert_result_to_domain_assignment(result, m, p):
    """
    Converte os subconjuntos resultantes em um array 2D de atribuições de domínio.
    
    Parameters
    ----------
    result : dict
        Dicionário com os subconjuntos particionados.
    m : int
        Primeira dimensão da grade.
    p : int
        Segunda dimensão da grade.
    
    Returns
    -------
    numpy.ndarray
        Array 2D onde cada célula contém seu código binário de subconjunto.
    """
    # Inicializa com valor padrão
    domain_assignment = np.full((m, p), "", dtype=object)
    
    # Preenche com as designações corretas
    for domain_id, subset in result.items():
        for coord in subset:
            i, j = coord
            domain_assignment[i, j] = domain_id
    
    return domain_assignment

def main():
    """
    Função principal para teste do algoritmo de divisão de subconjuntos.
    """
    # Casos de teste com diferentes números de subconjuntos, m e p
    test_cases = [
        (4, 3, 3),   # m = 4, p = 3, n_subsets = 3
        (5, 6, 4),   # m = 5, p = 6, n_subsets = 4
        (3, 4, 2),    # m = 3, p = 4, n_subsets = 2
        (20, 21, 6)    # m = 10, p = 13, n_subsets = 8

    ]
    
    for m, p, n_subsets in test_cases:
        print(f"\nDividindo coordenadas {m}x{p} em {n_subsets} subconjuntos:")
        
        # Gera o dicionário de entrada
        input_dict = generate_input_dictionary(m, p)
        # print(f"\n O dicionário original \n")
        # # Ordenar as coordenadas
        # sorted_coords = sorted(input_dict.keys())

        # # Agrupar por i (primeira coordenada) e formatar a saída
        # for i, group in itertools.groupby(sorted_coords, key=lambda coord: coord[0]):
        #     linha = []
        #     for coord in group:
        #         j = coord[1]
        #         valor = input_dict[coord]
        #         linha.append(f"(({i}, {j}), {valor})")  # Formato desejado
        #     print(", ".join(linha))  # Junta os elementos da linha com vírgulas    

        # Algoritmo de divisão baseado em centro de massa e autovetores
        result = recursive_binary_subset_division_balanced(input_dict, n_subsets)
        
        # Avalia a qualidade da partição
        quality = evaluate_partition_quality(result, input_dict)
        
        # Impressão formatada dos resultados
        print("\nSubconjuntos:")
        for binary_key, subset in sorted(result.items()):
            print(f"Subconjunto {binary_key}: {subset}")
            print(f"Peso total do subconjunto: {sum(subset.values())}")
            print(f"Número de pontos: {len(subset)}\n")
        
        # Imprime estatísticas
        print("\n\nEstatísticas:")
        print(f"Peso total: {quality['total_weight']}")
        print(f"Peso médio por subconjunto: {quality['mean_weight']:.2f}")
        print(f"Variação de peso: {quality['weight_range']:.2f} ({quality['weight_percentage_range']:.2f}%)")
        print(f"Pesos dos subconjuntos: {quality['subset_weights']}")
        print(f"Tamanhos dos subconjuntos: {quality['subset_sizes']}")
        
        # Converte resultado para mapa de domínios
        domain_map = convert_result_to_domain_assignment(result, m, p)
        print("\nMapa de domínios:")
        print(domain_map)
        
        # Validação dos resultados
        total_items = sum(len(subset) for subset in result.values())
        assert total_items == len(input_dict), "Nem todos os elementos foram distribuídos"

if __name__ == "__main__":
    main()