# Algoritmo de Projeção Principal e Divisão Balanceada

Este documento explica o racional, os algoritmos e as referências para a função `find_best_projection_and_division_balanced`, que divide um conjunto de pontos em dois subconjuntos balanceados e conectados usando análise de componentes principais.

## Racional do Algoritmo

O objetivo principal deste algoritmo é encontrar uma divisão equilibrada de um conjunto de pontos que:
1. Mantenha conectividade espacial em cada subconjunto
2. Balance os pesos entre os subconjuntos de acordo com uma proporção alvo (n1:n2)
3. Produza divisões que sejam naturais em relação à estrutura geométrica dos dados

O algoritmo utiliza princípios de mecânica para identificar os eixos principais de inércia do conjunto de pontos, e então tenta dividir os pontos ao longo destes eixos. Esta abordagem é inspirada em sistemas físicos e como eles naturalmente se dividem ao longo de linhas de menor resistência.

## Fundamentos Teóricos

### 1. Análise de Componentes Principais (PCA)

O algoritmo utiliza conceitos de PCA para encontrar direções de maior variância nos dados. No entanto, em vez de simplesmente calcular a matriz de covariância, o algoritmo calcula a matriz de inércia, que é ponderada pelas massas (pesos) dos pontos.

> Referência: Jolliffe, I. T. (2002). Principal Component Analysis. Springer Series in Statistics.

### 2. Mecânica do Corpo Rígido

O cálculo da matriz de inércia e dos eixos principais é baseado na teoria da mecânica do corpo rígido, onde os momentos e eixos principais são utilizados para descrever como um corpo rígido rota em torno de seu centro de massa.

> Referência: Goldstein, H., Poole, C., & Safko, J. (2002). Classical Mechanics (3rd ed.). Addison Wesley.

### 3. Teoria Espectral de Grafos

A divisão ao longo do eixo principal tem uma relação com métodos de corte espectral em grafos, onde os autovalores e autovetores da matriz Laplaciana são utilizados para particionar grafos.

> Referência: Luxburg, U. von. (2007). A tutorial on spectral clustering. Statistics and Computing, 17(4), 395-416.

## Implementação do Algoritmo

Aqui está a implementação da função principal:

```python
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
```

## Fluxo do Algoritmo

O algoritmo segue estas etapas principais:

### 1. Cálculo da Matriz de Inércia

A matriz de inércia é calculada a partir dos pontos ponderados pelos seus pesos. Esta matriz caracteriza como a "massa" do sistema está distribuída espacialmente.

### 2. Cálculo dos Momentos Principais e Eixos Principais

Os autovalores (momentos principais) e autovetores (eixos principais) da matriz de inércia são calculados. Os eixos principais representam as direções ao longo das quais o sistema tem distribuição máxima e mínima de massa.

### 3. Projeção de Pontos

Os pontos são projetados nos dois eixos principais para identificar potenciais linhas de corte.

### 4. Seleção do Melhor Eixo de Projeção

O algoritmo seleciona o eixo que resulta em menor dispersão dos pontos, o que geralmente leva a separações mais naturais.

### 5. Ordenação e Teste de Cortes

Os pontos são ordenados com base em suas projeções no eixo escolhido, e diferentes pontos de corte são testados para encontrar a divisão ideal que mantenha a conectividade e minimize o desequilíbrio de peso.

### 6. Fallback para Region Growing

Se nenhuma divisão satisfatória for encontrada usando a abordagem de projeção principal, o algoritmo recorre ao método de crescimento de região (region growing) como alternativa, [ver](crescimento_de_regiao.md).

## Mecanismo de Fallback e Detecção de Falha

Um aspecto crucial do algoritmo é o mecanismo de detecção de falha e a estratégia de fallback. No final da função principal, há a seguinte verificação:

```python
# If we couldn't find connected subsets with the direct approach, use region growing
if not best_first_subset or not best_second_subset:
    return region_growing_partition(input_dict, n1, n2, sorted_coords)
```

### Detecção de Falha do Algoritmo Principal

A falha do algoritmo principal é avaliada verificando se `best_first_subset` ou `best_second_subset` estão vazios. Isso pode ocorrer nas seguintes situações:

1. **Problema de Conectividade**: Se todos os possíveis pontos de corte ao longo do eixo principal resultarem em pelo menos um subconjunto desconectado, nenhuma solução válida será encontrada. 

2. **Topologias Complexas**: Formas com entalhes, buracos ou configurações em forma de "C" podem não permitir uma divisão conectada usando um simples corte linear ao longo do eixo principal.

3. **Distribuições Altamente Não-Uniformes**: Em casos onde a distribuição de pesos é extremamente não uniforme, pode ser impossível encontrar um corte que satisfaça tanto as restrições de conectividade quanto as de balanceamento.

Para detectar estas falhas, o algoritmo tenta todos os possíveis pontos de corte após ordenar os pontos pela sua projeção no eixo principal. Se nenhum ponto de corte resultar em dois subconjuntos conectados, ambos `best_first_subset` e `best_second_subset` permanecerão vazios.

### Estratégia de Fallback

Quando o algoritmo principal falha, a função [region_growing_partition](crescimento_de_regiao.md) é chamada como uma estratégia de fallback. Esta função implementa um algoritmo de crescimento de região que:

1. Inicia com duas "sementes" nos extremos opostos da projeção
2. Gradualmente expande cada região anexando vizinhos adjacentes
3. Toma decisões de atribuição com base no déficit de peso normalizado
4. Garante conectividade inerentemente pela natureza do processo de crescimento

Este método é mais robusto para formas complexas, pois não depende de um corte linear e pode criar divisões que seguem contornos naturais da forma. No entanto, é geralmente mais computacionalmente intensivo e pode resultar em fronteiras menos regulares entre os subconjuntos.

A escolha de usar [region_growing_partition](crescimento_de_regiao.md) como fallback é estratégica: tenta-se primeiro o método mais eficiente (corte ao longo do eixo principal), mas havendo falha, recorre-se a um método mais robusto embora potencialmente mais custoso.

## Relação com Algoritmos Clássicos

### 1. Bisseção Recursiva

Este algoritmo pode ser visto como uma variante da bisseção recursiva, porém com a adição de restrições de conectividade e balanceamento de peso.

> Referência: Simon, H. D. (1991). Partitioning of unstructured problems for parallel processing. Computing Systems in Engineering, 2(2-3), 135-148.

### 2. Método de K-means com Restrições

O algoritmo compartilha semelhanças com o k-means restrito, onde o objetivo é encontrar clusters com restrições adicionais.

> Referência: Wagstaff, K., Cardie, C., Rogers, S., & Schrödl, S. (2001). Constrained K-means Clustering with Background Knowledge. ICML, 1, 577-584.

### 3. Particionamento Espectral

A projeção nos eixos principais tem paralelos com o particionamento espectral, mas com uma matriz de inércia em vez de uma matriz Laplaciana.

> Referência: Spielman, D. A., & Teng, S. H. (2007). Spectral partitioning works: Planar graphs and finite element meshes. Linear Algebra and its Applications, 421(2-3), 284-305.

## Aplicações

Este tipo de algoritmo é particularmente útil em:

- Divisão territorial para planejamento urbano
- Particionamento de malhas para simulações de elementos finitos
- Balanceamento de carga em computação paralela
- Zoneamento de recursos com restrições geográficas
- Segmentação de imagens com conservação de características

## Considerações de Implementação

A implementação atual usa várias funções auxiliares:

- `normalize_vectors` - para normalizar os vetores próprios
- `project_points_on_eigenvector` - para projetar pontos nos eixos principais
- `calculate_max_distance` - para medir a dispersão das projeções
- `is_connected` - para verificar a conectividade dos subconjuntos

Estas funções são cruciais para a correta operação do algoritmo e garantem que as propriedades desejadas (conectividade e balanceamento) sejam mantidas.

## Alterações no Algoritmo

As modificações marcadas no código (`MODIFICAÇÃO`) indicam uma evolução do algoritmo para priorizar apenas o balanceamento de peso, removendo considerações de tamanho dos conjuntos. Estas mudanças simplificam o critério de otimização e focam em:

1. Usar apenas o desequilíbrio de peso como métrica para avaliação de partições
2. Normalizar o desequilíbrio de peso pelo peso total para obter uma medida relativa
3. Remover o cálculo de déficit de tamanho no algoritmo de crescimento de região

Esta evolução indica uma escolha deliberada de priorizar o balanceamento de peso sobre o balanceamento de tamanho, possivelmente porque o peso é uma característica mais importante para a aplicação específica.

## Limitações

- O algoritmo assume que existe pelo menos uma divisão viável que satisfaz as restrições de conectividade
- A qualidade da divisão pode depender da distribuição espacial dos pontos
- O tempo de execução pode aumentar significativamente para conjuntos com formas complexas
- Não há garantia de encontrar a divisão globalmente ótima, apenas uma divisão localmente ótima

## Conclusão

O algoritmo `find_best_projection_and_division_balanced` representa uma abordagem sofisticada para o problema de particionamento espacial com restrições, combinando princípios de mecânica, análise espectral e teoria dos grafos. A utilização dos eixos principais de inércia para guiar a divisão permite que o algoritmo identifique partições que respeitam a estrutura natural dos dados, enquanto as verificações de conectividade e os critérios de balanceamento garantem partições práticas e úteis para aplicações do mundo real. O mecanismo de fallback que chama [region_growing_partition](crescimento_de_regiao.md) proporciona robustez adicional, garantindo que o algoritmo funcione mesmo em casos onde a abordagem de corte simples falha.