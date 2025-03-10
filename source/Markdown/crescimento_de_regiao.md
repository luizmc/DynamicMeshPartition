# Teoria e Racional do Algoritmo de Crescimento de Região

Este documento explica o racional e a teoria por trás do algoritmo implementado na função `region_growing_partition`, que utiliza a técnica de crescimento de região para dividir um conjunto de pontos em dois subconjuntos conectados e balanceados por peso.

## Racional do Algoritmo

O algoritmo de crescimento de região é uma técnica de segmentação espacial que começa com "sementes" iniciais e expande regiões a partir delas, anexando pontos vizinhos que satisfaçam determinados critérios. O racional por trás deste algoritmo é:

1. **Garantir conectividade**: A principal força deste método é que ele naturalmente cria subconjuntos conectados, pois os pontos só são adicionados se forem adjacentes a pontos já na região.

2. **Balanceamento por peso**: O algoritmo busca criar duas partições que tenham peso total próximo a valores-alvo calculados com base nas proporções desejadas (n1:n2).

3. **Abordagem gulosa**: O algoritmo toma decisões locais ótimas a cada iteração, expandindo a região que mais "precisa" do próximo ponto de acordo com o déficit de peso normalizado.

## Código Fonte

```python
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
```

## Teoria Subjacente

Do ponto de vista teórico, este algoritmo relaciona-se com:

### 1. Teoria dos Grafos

O espaço de coordenadas 2D pode ser modelado como um grafo de grade, onde cada coordenada é um nó e existem arestas entre células adjacentes. O algoritmo essencialmente realiza uma busca em largura modificada neste grafo.

> Referência: Shi, J., & Malik, J. (2000). Normalized cuts and image segmentation. IEEE Transactions on Pattern Analysis and Machine Intelligence, 22(8), 888-905.

### 2. Otimização com Restrições

O problema sendo resolvido é uma variação do problema de particionamento de grafos com restrições de balanceamento de peso e conectividade, que é NP-difícil na forma geral.

> Referência: Karypis, G., & Kumar, V. (1998). A fast and high quality multilevel scheme for partitioning irregular graphs. SIAM Journal on Scientific Computing, 20(1), 359-392.

### 3. Processos de Difusão

O crescimento das regiões pode ser visto como um processo de difusão controlada, onde as fronteiras das regiões se expandem em direções que minimizam o desequilíbrio de peso.

> Referência: Perona, P., & Malik, J. (1990). Scale-space and edge detection using anisotropic diffusion. IEEE Transactions on Pattern Analysis and Machine Intelligence, 12(7), 629-639.

### 4. Mecânica Estatística

A modificação feita para usar apenas o peso (removendo considerações de tamanho) aproxima-se de métodos que consideram a distribuição de massa em sistemas físicos, similar a problemas de minimização de energia.

> Referência: Mumford, D., & Shah, J. (1989). Optimal approximations by piecewise smooth functions and associated variational problems. Communications on Pure and Applied Mathematics, 42(5), 577-685.

## Fluxo do Algoritmo

O algoritmo segue o seguinte fluxo:

1. **Inicialização com sementes**: O algoritmo começa selecionando sementes nos extremos opostos do conjunto ordenado por projeção (primeiro e último ponto).

2. **Crescimento iterativo**: Em cada passo, identifica todos os vizinhos não atribuídos de cada região.

3. **Decisão gulosa**: Escolhe adicionar o ponto à região com maior déficit normalizado de peso.

4. **Finalização e tratamento de resíduos**: Trata pontos que podem ficar desconectados, atribuindo-os à região que minimiza o desequilíbrio.

## Modificações e Evolução

As modificações marcadas no código (MODIFICAÇÃOs) mostram uma evolução do algoritmo para priorizar apenas o balanceamento de peso, em vez de considerar tanto peso quanto tamanho dos conjuntos, simplificando o critério de otimização.

Esta abordagem tem conexões com algoritmos de particionamento espectral, mas utiliza um método construtivo que garante conectividade espacial.

> Referência: Adams, R., & Bischof, L. (1994). Seeded region growing. IEEE Transactions on Pattern Analysis and Machine Intelligence, 16(6), 641-647.

## Aplicações

Este tipo de algoritmo é particularmente útil em:

- Segmentação de imagens
- Zoneamento territorial
- Planejamento de redes
- Divisão de recursos espaciais
- Agrupamento de dados com restrições de conectividade

## Limitações

- Sensibilidade à escolha inicial das sementes
- Pode ficar preso em ótimos locais
- Não garante a solução ótima global
- Dependência da ordem de processamento dos vizinhos