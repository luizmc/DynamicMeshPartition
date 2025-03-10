import math
import random
import itertools
import numpy as np
import mesh3d as m3d

def generate_input_synthetic_dictionary(m, p):
    """
    Gera um dicionário sintético com todas as coordenadas possíveis e pesos aleatórios.
    Ele representa um mapas bidimensional de pesos vindos de uma malha tridimensional projetada neste mapa
    
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
    
    # Preenche aproximadamente 60% das entradas do dicionário com pesos aleatórios
    for coord in all_coordinates:
        if random.random() < 0.6:  # 60% de chance de alterar o peso
            input_dict[coord] = random.randint(1, 8)
    
    return input_dict

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
    inertia_matrix, center_of_mass = m3d.compute_inertia_matrix_from_points(points)
    
    # Calculate principal moments and principal axes
    principal_moments, principal_axes = m3d.calculate_principal_moments(inertia_matrix)
    
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
        """
        Verifica se um subconjunto de coordenadas forma um componente conectado.
        
        Esta função determina se todas as coordenadas no subconjunto fornecido
        podem ser alcançadas a partir de qualquer outra coordenada, movendo-se
        apenas entre vizinhos adjacentes (acima, abaixo, esquerda, direita).

        Esta função implementa um algoritmo de busca em largura (BFS) para verificar a conectividade de um conjunto de coordenadas. A ideia principal é começar em um ponto e verificar se todos os outros pontos podem ser alcançados seguindo apenas movimentos adjacentes.
       
        Args:
            subset: Um dicionário onde as chaves são tuplas (i, j) representando coordenadas.
                    Os valores do dicionário não são utilizados nesta função.
        
        Returns:
            bool: True se o subconjunto forma um componente conectado, False caso contrário.
        """
        # Caso base: um conjunto vazio é considerado conectado por definição
        if not subset:
            return True
        
        # Extrai todas as coordenadas do subconjunto
        coords = list(subset.keys())
        
        # Inicializa estruturas para o algoritmo de busca em largura (BFS)
        visited = set()  # Conjunto para rastrear coordenadas já visitadas
        queue = [coords[0]]  # Fila começa com a primeira coordenada
        visited.add(coords[0])  # Marca a primeira coordenada como visitada
        
        # Implementação do algoritmo BFS para explorar o componente conectado
        while queue:
            # Remove e processa a próxima coordenada da fila
            current = queue.pop(0)
            i, j = current
            
            # Gera as quatro coordenadas adjacentes (vizinhos)
            # Vizinhos: direita, esquerda, abaixo, acima
            neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
            
            # Processa cada vizinho
            for neighbor in neighbors:
                # Verifica se o vizinho está no subconjunto e ainda não foi visitado
                if neighbor in subset and neighbor not in visited:
                    visited.add(neighbor)  # Marca o vizinho como visitado
                    queue.append(neighbor)  # Adiciona o vizinho à fila para processamento posterior
        
        # Um componente é conectado se todas as coordenadas foram visitadas
        # durante a busca em largura a partir da primeira coordenada
        return len(visited) == len(subset)    
        
    # Try different cut points to find a balanced division that maintains connectivity
    best_imbalance = float('inf')
    best_first_subset = {}
    best_second_subset = {}
    
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
    
    Este algoritmo implementa uma técnica de "crescimento de região" para dividir um conjunto de pontos
    em duas partições conectadas e balanceadas. O processo começa com duas "sementes" (pontos iniciais)
    nas extremidades opostas e vai crescendo cada região de forma balanceada.
    
    Parameters
    ----------
    input_dict : dict
        Dictionary with coordinates as keys and weights as values.
        Um dicionário onde as chaves são coordenadas (tuplas) e os valores são os pesos de cada ponto.
    n1, n2 : int
        Target sizes for the subsets.
        Tamanhos alvo para cada subconjunto, usados para calcular as proporções desejadas.
    sorted_coords : list
        Coordinates sorted by projection value.
        Lista de coordenadas ordenadas por algum valor de projeção (geralmente ordenadas ao longo
        de algum eixo principal para maximizar a separação espacial).
    
    Returns
    -------
    tuple
        (first_subset, second_subset) both are dictionaries.
        Dois dicionários representando as partições resultantes, mantendo a estrutura do input_dict.
    """
    # Initialize with seeds at opposite ends
    # Inicializa os subconjuntos com as sementes nos extremos opostos da lista ordenada
    first_seed = sorted_coords[0]  # Primeira semente (início da lista ordenada)
    second_seed = sorted_coords[-1]  # Segunda semente (final da lista ordenada)
    
    # Cria os subconjuntos iniciais com as sementes e seus respectivos pesos
    first_subset = {first_seed: input_dict[first_seed]}
    second_subset = {second_seed: input_dict[second_seed]}
    assigned = {first_seed, second_seed}  # Conjunto de pontos já atribuídos a algum subconjunto
    
    # Calcula o peso total e os pesos alvo para cada subconjunto baseado nas proporções n1 e n2
    total_weight = sum(input_dict.values())
    target_weight1 = (total_weight * n1) / (n1 + n2)  # Peso alvo para o primeiro subconjunto
    target_weight2 = total_weight - target_weight1  # Peso alvo para o segundo subconjunto
    
    # Calcula o número de pontos alvo para cada subconjunto
    target_size1 = (len(input_dict) * n1) // (n1 + n2)
    target_size2 = len(input_dict) - target_size1
    
    # Helper function to find unassigned neighbors
    # Função auxiliar que encontra vizinhos não atribuídos de um subconjunto
    def get_unassigned_neighbors(subset):
        """
        Identifica todos os pontos vizinhos não atribuídos dos pontos em um subconjunto.
        
        Um ponto é considerado vizinho se estiver adjacente em uma das quatro direções
        (acima, abaixo, esquerda, direita) a qualquer ponto do subconjunto.
        
        Args:
            subset: Dicionário representando um subconjunto de pontos
            
        Returns:
            Set contendo todos os vizinhos não atribuídos do subconjunto
        """
        neighbors = set()
        for coord in subset:
            i, j = coord  # Coordenadas do ponto atual
            # Verifica os quatro vizinhos adjacentes (vizinhança de Von Neumann)
            for neighbor in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
                # Adiciona apenas se o vizinho existir no dicionário original e não estiver atribuído
                if neighbor in input_dict and neighbor not in assigned:
                    neighbors.add(neighbor)
        return neighbors
    
    # Grow regions until all points are assigned
    # Cresce as regiões até que todos os pontos sejam atribuídos
    while len(assigned) < len(input_dict):
        # Obtém os vizinhos não atribuídos de cada subconjunto
        first_neighbors = get_unassigned_neighbors(first_subset)
        second_neighbors = get_unassigned_neighbors(second_neighbors)
        
        # Se nenhum dos subconjuntos tiver vizinhos não atribuídos, encerra o loop
        # (pode acontecer se houver regiões desconectadas no espaço)
        if not first_neighbors and not second_neighbors:
            break
        
        # Calcula os pesos atuais de cada subconjunto
        weight1 = sum(first_subset.values())
        weight2 = sum(second_subset.values())
        
        # Calcula quanto cada subconjunto está distante do seu peso alvo
        weight_deficit1 = target_weight1 - weight1
        weight_deficit2 = target_weight2 - weight2
        
        # MODIFICAÇÃO: Remover o cálculo dos déficits de tamanho (size_deficit)
        # Nota: Esta linha indica que o código original considerava também o tamanho dos subconjuntos,
        # mas essa parte foi removida na implementação atual para focar apenas no equilíbrio de pesos.
        
        # Normaliza os déficits de peso para poder compará-los
        weight_deficit_norm1 = weight_deficit1 / target_weight1 if target_weight1 > 0 else 0
        weight_deficit_norm2 = weight_deficit2 / target_weight2 if target_weight2 > 0 else 0
        
        # MODIFICAÇÃO: Usar apenas os déficits de peso como critério
        # Define o déficit total de cada subconjunto usando apenas o déficit de peso normalizado
        deficit1 = weight_deficit_norm1
        deficit2 = weight_deficit_norm2
        
        # PARTE ADICIONADA: Lógica para escolher qual vizinho adicionar a cada subconjunto
        # Decide qual subconjunto deve crescer com base nos déficits calculados
        if first_neighbors and (not second_neighbors or deficit1 > deficit2):
            # Primeiro subconjunto precisa crescer mais (tem maior déficit) ou é o único com vizinhos
            
            # Seleciona o vizinho que mais contribui para equilibrar o peso
            best_neighbor = None
            best_score = float('-inf')
            
            for neighbor in first_neighbors:
                # Calcula quanto esse vizinho aproximaria o subconjunto do seu peso alvo
                new_deficit = deficit1 - (input_dict[neighbor] / target_weight1)
                score = abs(new_deficit) - abs(deficit1)
                
                # Quanto mais negativo o score, melhor (significa maior redução no déficit)
                if score < best_score:
                    best_score = score
                    best_neighbor = neighbor
            
            # Adiciona o melhor vizinho ao primeiro subconjunto
            first_subset[best_neighbor] = input_dict[best_neighbor]
            assigned.add(best_neighbor)
            
        elif second_neighbors:
            # Segundo subconjunto precisa crescer mais (tem maior déficit) ou é o único com vizinhos
            
            # Seleciona o vizinho que mais contribui para equilibrar o peso
            best_neighbor = None
            best_score = float('-inf')
            
            for neighbor in second_neighbors:
                # Calcula quanto esse vizinho aproximaria o subconjunto do seu peso alvo
                new_deficit = deficit2 - (input_dict[neighbor] / target_weight2)
                score = abs(new_deficit) - abs(deficit2)
                
                # Quanto mais negativo o score, melhor (significa maior redução no déficit)
                if score < best_score:
                    best_score = score
                    best_neighbor = neighbor
            
            # Adiciona o melhor vizinho ao segundo subconjunto
            second_subset[best_neighbor] = input_dict[best_neighbor]
            assigned.add(best_neighbor)
 
    # Handle remaining unassigned points
    # Trata os pontos que não foram atribuídos durante o crescimento de região
    # (geralmente pontos que estão desconectados ou isolados)
    unassigned = [coord for coord in input_dict if coord not in assigned]
    
    # MODIFICAÇÃO: Atribuir pontos restantes apenas com base no déficit de peso
    # Para cada ponto não atribuído, verifica qual subconjunto ficaria mais próximo
    # do seu peso alvo ao receber este ponto
    for coord in unassigned:
        weight1 = sum(first_subset.values())
        weight2 = sum(second_subset.values())
        
        # Verifica se adicionar o ponto ao primeiro subconjunto o aproximaria mais
        # do seu peso alvo do que deixá-lo como está
        if abs(weight1 + input_dict[coord] - target_weight1) < abs(weight1 - target_weight1):
            first_subset[coord] = input_dict[coord]
        else:
            # Caso contrário, adiciona ao segundo subconjunto
            second_subset[coord] = input_dict[coord]
  
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
        (3, 4, 2),   # m = 3, p = 4, n_subsets = 2
        (10, 13, 5)  # m = 10, p = 13, n_subsets = 6

    ]
    
    for m, p, n_subsets in test_cases:
        print(f"\nDividindo coordenadas {m}x{p} em {n_subsets} subconjuntos:")
        
        # Gera o dicionário de entrada
        input_dict = generate_input_synthetic_dictionary(m, p)

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