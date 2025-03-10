```yaml
lang: pt-BR
```


# Análise e Melhorias do Algoritmo de Partição por Crescimento de Regiões (`region_growing_partition`)

Este documento consolida as análises e sugestões de melhoria para o código `region_growing_partition`.

## 1. Código Original (Referência)

```python
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
    def get_unassigned_neighbors(subset):
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
    while len(assigned) < len(input_dict):
        # Obtém os vizinhos não atribuídos de cada subconjunto
        first_neighbors = get_unassigned_neighbors(first_subset)
        second_neighbors = get_unassigned_neighbors(second_subset)

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

        # Normaliza os déficits de peso para poder compará-los
        weight_deficit_norm1 = weight_deficit1 / target_weight1 if target_weight1 > 0 else 0
        weight_deficit_norm2 = weight_deficit2 / target_weight2 if target_weight2 > 0 else 0

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
    unassigned = [coord for coord in input_dict if coord not in assigned]

    # MODIFICAÇÃO: Atribuir pontos restantes apenas com base no déficit de peso
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
```

## 2. Principais Aspectos e Técnicas

### 2.1. Inicialização com Sementes Opostas

- **Technique**: Initial seed selection at list endpoints (`sorted_coords[0]` and `sorted_coords[-1]`).
- **Goal**: Maximize initial spatial separation between partitions.
- **Advantage**: Ensures growth starts from distant regions, useful for projected/ordered data.

### 2.2. Von Neumann Neighborhood

- **Implementation**: Check 4 adjacent neighbors (up, down, left, right).
- **Purpose**: Maintain region connectivity during growth.

### 2.3. Weight Deficit Balancing

- **Method**: Normalized `weight_deficit` calculation to compare expansion needs between partitions.
- **Selection Criterion**: Choose neighbor that most reduces deficit relative to target weight.
- **Optimization**: Focus on minimizing percentage difference relative to total weight.

### 2.4. Fallback for Non-Connected Points

- **Residual Logic**: Assignment of remaining points to subset that best balances total weight.
- **Limitation**: May compromise connectivity if points are disconnected.

## 3. Critical Points

### 3.1. Non-Guaranteed Connectivity

- Main loop may end prematurely if no neighbors available (e.g., islands of points).
- Final residual assignment step ignores connectivity.

### 3.2. Neighbor Complexity

- Function `get_unassigned_neighbors` called multiple times per iteration, with *O(N)* complexity.
- No efficient data structure to track boundaries.

### 3.3. Simplistic Balancing Criterion

- Ignores balancing of **point count** (`target_size1`/`target_size2` calculated but unused).
- Prioritizes weight only, can lead to disproportionate partition sizes.

### 3.4. Fixed Seed Selection

- Fixed seeds at endpoints may be suboptimal if ordering doesn't reflect spatial distribution.

### 3.5. No Tiebreaker

- No criterion for tiebreaking when multiple neighbors have same `score`.

## 4. Improvement Suggestions (With Code)

### 4.1. Ensure Residual Connectivity

- **Before assigning remaining points, verify if they are adjacent to any partition.** (Complex implementation, not shown here, involves graphs and searches).

### 4.2. Neighbor Search Optimization

- **Pre-calculate neighborhood:**

```python
def precompute_neighbors(input_dict):
    """Pré-calcula os vizinhos de cada coordenada."""
    neighbors = {}
    for i, j in input_dict:
        neighbors[(i, j)] = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
    return neighbors

# No início do region_growing_partition:
# def region_growing_partition(input_dict, n1, n2, sorted_coords):
#   neighbor_map = precompute_neighbors(input_dict)  # Mover para fora da função para evitar recalculos

def get_unassigned_neighbors(subset, neighbor_map): #Modificar a assinatura da função
    neighbors = set()
    for coord in subset:
        for neighbor in neighbor_map[coord]:
            if neighbor in input_dict and neighbor not in assigned:
                neighbors.add(neighbor)
    return neighbors
```

*   **Uso de Quadtrees/K-D Trees:** (Implementação mais complexa, requer bibliotecas e lógica adicionais para construção e consulta das árvores). Não exemplificado com código aqui.

### 4.3. Balanceamento Híbrido (Peso + Tamanho)

*   **Reintroduzir o cálculo de `size_deficit` e ponderar com `weight_deficit`:**

```python
#Dentro do Loop While, antes de calcular deficit1 e deficit2
        size1 = len(first_subset)
        size2 = len(second_subset)
        size_deficit1 = target_size1 - size1
        size_deficit2 = target_size2 - size2

        size_deficit_norm1 = size_deficit1 / target_size1 if target_size1 > 0 else 0
        size_deficit_norm2 = size_deficit2 / target_size2 if target_size2 > 0 else 0

        alpha = 0.5  # Ajustar o peso entre peso e tamanho (0 a 1)
        deficit1 = alpha * weight_deficit_norm1 + (1 - alpha) * size_deficit_norm1
        deficit2 = alpha * weight_deficit_norm2 + (1 - alpha) * size_deficit_norm2

```

### 4.4. Seleção Adaptativa de Sementes

*   **Função `select_seeds` para escolher sementes baseadas em critérios como maior distância espacial:**

```python
def select_seeds(input_dict):
    """Seleciona sementes nos extremos da bounding box."""
    coords = list(input_dict.keys())
    if not coords:
        return None, None  # Lidar com dicionário vazio

    min_x = min(coords, key=lambda c: c[0])[0]
    max_x = max(coords, key=lambda c: c[0])[0]
    min_y = min(coords, key=lambda c: c[1])[1]
    max_y = max(coords, key=lambda c: c[1])[1]

    seed1 = min(coords, key=lambda c: (c[0] - min_x)**2 + (c[1] - min_y)**2) # canto inferior esquerdo
    seed2 = min(coords, key=lambda c: (c[0] - max_x)**2 + (c[1] - max_y)**2) # canto superior direito

    return seed1, seed2

#Dentro do region_growing_partition, substituir as linhas iniciais:
#first_seed = sorted_coords[0]
#second_seed = sorted_coords[-1]
#Pelas seguintes:
#first_seed, second_seed = select_seeds(input_dict)
#if first_seed is None or second_seed is None:
#   return {},{} #Lidar com caso de input vazio.

```

### 4.5. Tratamento de Casos Especiais

*   **Adicionar verificações de input no início da função `region_growing_partition`:**

```python
# No início de region_growing_partition:
# def region_growing_partition(input_dict, n1, n2, sorted_coords):
    if not input_dict:
        return {}, {}  # Dicionário vazio
    if n1 + n2 == 0:
        return {}, {}  # Evitar divisão por zero
    if not sorted_coords:
        sorted_coords = list(input_dict.keys())  # Usar as chaves como coords se não fornecidas.  Pode não ser ideal.
```

### 4.6. Empates e Aleatoriedade Controlada

*   **Introduzir aleatoriedade para desempatar vizinhos com o mesmo `score`:**

```python
import random

# ... Dentro do loop de crescimento (exemplo para o primeiro subconjunto):

            best_neighbors = [neighbor for neighbor in first_neighbors if abs(deficit1 - (input_dict[neighbor] / target_weight1)) == abs(deficit1 - (input_dict[best_neighbor] / target_weight1) if best_neighbor is not None else deficit1) ]
            #Desempata a lista best_neighbors
            if best_neighbors:
                best_neighbor = random.choice(best_neighbors)  # Escolha aleatória

            # Adiciona o melhor vizinho ao primeiro subconjunto
            first_subset[best_neighbor] = input_dict[best_neighbor]
            assigned.add(best_neighbor)
```

## 5. Análise Final

O algoritmo original é adequado para cenários simples com dados bem comportados, mas carece de robustez para casos complexos. Melhorias na eficiência, balanceamento híbrido e garantia de conectividade residual são essenciais para aplicações práticas.  A implementação das sugestões acima, especialmente a otimização da busca por vizinhos e o balanceamento híbrido, deve melhorar significativamente o desempenho e a qualidade dos resultados.

## 6. Comentários Adicionais

Este documento markdown contém:

1. O código original da função `region_growing_partition` para referência em português do Brasil.
2. Um resumo dos principais aspectos e técnicas utilizadas pelo algoritmo.
3. Uma identificação detalhada dos pontos críticos e limitações.
4. Sugestões de melhoria concretas, com trechos de código exemplificando como implementar algumas dessas melhorias. As melhorias mais complexas (ex: uso de quadtrees, imposição de conectividade forte) são descritas conceitualmente, mas não implementadas em código devido à sua complexidade.
5. Uma análise final resumindo os benefícios esperados das melhorias propostas.

Este documento deve servir como um guia completo para entender, analisar e melhorar o algoritmo de partição por crescimento de regiões.
