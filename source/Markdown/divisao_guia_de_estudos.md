# Guia de Estudo: Clustering Espectral e Particionamento de Grafos

## Quiz (Respostas em 2-3 frases)

### 1. O que é clustering espectral e qual a sua vantagem sobre o k-means tradicional?

> Clustering espectral é um algoritmo moderno baseado na teoria dos grafos espectrais, que utiliza autovetores de matrizes Laplacianas para reduzir a dimensionalidade dos dados antes de aplicar métodos como o k-means. Sua principal vantagem sobre o k-means tradicional é a capacidade de identificar clusters não convexos e lidar melhor com estruturas complexas de dados.

### 2. Como o particionamento de problemas não estruturados pode ser formulado como um problema de particionamento de grafos?

> Problemas não estruturados podem ser modelados como grafos, onde vértices representam componentes e arestas representam interações. O objetivo é dividir o grafo em subdomínios minimizando o número de arestas cortadas entre eles, preservando a coesão interna dos clusters.

### 3. Qual a importância do vetor de Fiedler no particionamento espectral de grafos?

> O vetor de Fiedler (autovetor do segundo menor autovalor da matriz Laplaciana) é essencial para encontrar um separador eficiente no grafo. Ele permite particionar o grafo com uma boa relação entre arestas cortadas e o tamanho dos subdomínios, garantindo equilíbrio estrutural.

### 4. Explique o conceito de restrições must-link e cannot-link no contexto do algoritmo COP-KMEANS.

> Restrições **must-link** obrigam pares de dados a pertencerem ao mesmo cluster, enquanto **cannot-link** os impedem de compartilhar clusters. O COP-KMEANS adapta o k-means para respeitar essas restrições, melhorando a precisão em cenários supervisionados.

### 5. Quais são os três tipos de grafos de similaridade mais comuns?

> Os três tipos são:  
> 1. **Grafo de ε-vizinhança** (conecta pontos dentro de uma distância ε).  
> 2. **Grafo k-vizinhos mais próximos** (cada ponto conecta aos k mais próximos).  
> 3. **Grafo k-vizinhos mútuos** (conexão apenas se ambos estão nos k vizinhos do outro).  

### 6. Qual a diferença entre o Laplaciano de grafo não normalizado e os normalizados?

> O Laplaciano não normalizado é definido como **L = D - W**. Os normalizados incluem **Lsym = D⁻¹⸍²LD⁻¹⸍²** (simétrico) e **Lrw = D⁻¹L** (random walk). A normalização ajusta para variações nos graus dos vértices, evitando viés em grafos com densidades heterogêneas.

### 7. Quais são os passos gerais envolvidos nos algoritmos de clustering espectral?

> 1. Construir um grafo de similaridade.  
> 2. Calcular a matriz Laplaciana.  
> 3. Extrair os primeiros *k* autovetores.  
> 4. Projetar os dados nesses autovetores.  
> 5. Aplicar k-means na nova representação.  

### 8. Por que a escolha do número de clusters (k) é um desafio em clustering espectral?

> A escolha de *k* é intrínsecamente complexa em clustering, pois depende da estrutura oculta dos dados. No espectral, métodos como a **heurística do eigengap** (maior salto entre autovalores consecutivos) são usados, mas ainda exigem interpretação subjetiva.

### 9. O que é a distância de comutação e como ela se relaciona com o clustering espectral?

> A distância de comutação mede o tempo médio de um passeio aleatório entre dois vértices e volta. Ela está ligada à matriz Laplaciana, e o clustering espectral aproxima essa métrica para definir clusters baseados em proximidade estrutural.

### 10. Como a teoria da perturbação justifica o uso do clustering espectral?

> A teoria da perturbação mostra que pequenas variações nos dados não afetam drasticamente os autovetores da Laplaciana. Isso permite que o clustering espectral mantenha robustez mesmo quando os clusters não estão perfeitamente separados.

---

## Questões Dissertativas (Formato de Ensaio)

1. **Métodos de Construção de Grafos de Similaridade**: Compare ε-vizinhança, k-vizinhos mais próximos e k-vizinhos mútuos. Discuta vantagens (e.g., simplicidade do ε-vizinhança) e desvantagens (e.g., sensibilidade a parâmetros). Indique cenários ideais para cada método.

2. **Algoritmos de Clustering Espectral Normalizado vs. Não Normalizado**: Detalhe os passos de ambos, enfatizando diferenças teóricas (e.g., tratamento de grafos com graus desbalanceados) e práticas (e.g., desempenho computacional).

3. **Escolha do Número de Clusters (k)**: Analise métodos como eigengap, elbow method e validação externa. Critique a confiabilidade de cada um em diferentes contextos.

4. **Relação com a Teoria dos Grafos Espectrais**: Explore como autovalores da Laplaciana refletem propriedades do grafo (e.g., conectividade) e como autovetores definem cortes ótimos.

5. **Considerações Práticas em Implementação**: Aborde desafios como escalabilidade (autovetores em grafos grandes), escolha de Laplaciano (normalizado ou não) e ajuste de parâmetros (e.g., σ em kernels de similaridade).

---

## Glossário de Termos-Chave

- **Clustering Espectral**: Técnica que usa autovetores da matriz Laplaciana para agrupar dados.  
- **Matriz de Adjacência (W)**: Representa pesos de arestas entre vértices.  
- **Matriz Laplaciana (L)**: Calculada como **L = D - W**; fundamental para análise espectral.  
- **Vetor de Fiedler**: Autovetor do segundo menor autovalor da Laplaciana; usado em particionamento.  
- **Eigengap**: Diferença entre autovalores consecutivos; critério para escolha de *k*.  
- **Rand Index**: Medida de concordância entre agrupamentos.  
- **Bisseção Espectral Recursiva (RSB)**: Algoritmo que divide grafos usando o vetor de Fiedler iterativamente.  
- **Grafo Planar**: Grafo que pode ser desenhado sem cruzamento de arestas.  
- **Isoperimetria**: Princípio que relaciona volume e fronteira de clusters; base para otimização de cortes.  