# Linha de tempo relativa ao arquivo `crescimento_de_regiao.py`

## Timeline dos Principais Eventos e Conceitos

### Década de 1980
- **1989**: Publicação do Modelo de Mumford-Shah, que propõe funcionais de energia para segmentação de imagens (*MumfordShah1989*).

### Década de 1990
- **1990**: Introdução da difusão anisotrópica por Perona e Malik para preservação de bordas em operações de suavização de imagens (*PeronaMalik1990*).
- **1998**: Karypis e Kumar desenvolvem um esquema multinível para particionamento de grafos irregulares, utilizando bisseção espectral (Spectral Bisection - SB) e contração de grafos (*KarypisKumar1998*).

### Década de 2000
- **2000**: Shi e Malik introduzem o conceito de "Normalized Cuts" (Ncuts) para segmentação de imagens, baseado na teoria espectral de grafos (*ShiMalik2000*).

---

## Elenco de Personagens e Conceitos Chave (com mini-biografias)

### Pesquisadores

- **David Mumford**: Matemático conhecido por seu trabalho em visão computacional, incluindo o modelo de Mumford-Shah para segmentação de imagens.
- **Jitendra Shah**: Colaborador de David Mumford no desenvolvimento do modelo de Mumford-Shah.
- **Pietro Perona**: Pesquisador em visão computacional que, juntamente com Malik, propôs a difusão anisotrópica.
- **Jitendra Malik**: Pesquisador em visão computacional, conhecido por seu trabalho em difusão anisotrópica (com Perona) e segmentação de imagens (com Shi).
- **George Karypis**: Pesquisador especializado em algoritmos de particionamento de grafos, incluindo métodos multiníveis.
- **Vipin Kumar**: Colaborador de George Karypis no desenvolvimento de técnicas de particionamento de grafos.
- **Jianbo Shi**: Pesquisador que, em colaboração com Malik, introduziu o método de Normalized Cuts para segmentação de imagens.

### Conceitos Matemáticos e Variáveis

- **f**: Função que representa a imagem ou sinal a ser segmentado (Mumford-Shah). Pode ser a densidade em um CAT scan ou a distância em dados de sonar.
- **Γ** (*Gamma*): A fronteira ou curva que separa diferentes regiões segmentadas na imagem (*Mumford-Shah, Guia de Estudos*).
- **g(x, y)**: A imagem original ou dados de entrada, como valores de brilho ou intensidade (*Mumford-Shah, AdamsBischof1994, PeronaMalik1990*).
- **T**: O conjunto de todos os pixels ainda não alocados que fazem fronteira com pelo menos uma das regiões (*AdamsBischof1994, Guia de Estudos*).
- **Q**: A matriz Laplaciana, usada na bisseção espectral de grafos (*KarypisKumar1998, Guia de Estudos*). Calculada como `Q = D - A`, onde *D* é a matriz de grau e *A* é a matriz de adjacência.
- **y**: O vetor de Fiedler, o autovetor correspondente ao segundo menor autovalor da matriz Laplaciana (*KarypisKumar1998, Guia de Estudos*).
- **E, E0, E∞**: Funcionais de energia usados no modelo de Mumford-Shah para medir a qualidade de uma segmentação (*MumfordShah1989, Guia de Estudos*).
- **p, v**: Parâmetros dos funcionais de energia (*MumfordShah1989, Guia de Estudos*).

### Algoritmos e Técnicas

- **Ncuts** (*Normalized Cuts*): Critério para segmentação de imagens que busca minimizar o corte normalizado entre grupos de pixels (*ShiMalik2000*).
- **A** (*Matriz de Adjacência*): Utilizada no contexto de partição de grafos, onde elementos `aᵢⱼ` descrevem a conexão (ou ausência) entre vértices (*KarypisKumar1998, Guia de Estudos*).
- **D** (*Matriz Diagonal*): No contexto de partição de grafos, é utilizada para representar os graus dos vértices, onde `dᵢᵢ` é a soma dos pesos das arestas incidentes ao vértice *i* (*KarypisKumar1998, Guia de Estudos*).
- **Adj(v)** (*Vizinhança*): Função que retorna o conjunto de vértices adjacentes a um vértice *v* em um grafo (*KarypisKumar1998*).

---

## Conceitos e Termos Chave

- **Segmentação de Imagens**: O processo de particionar uma imagem em múltiplas regiões (*MumfordShah1989*).
- **Crescimento de Regiões** (*Seeded Region Growing*): Um método de segmentação que começa com pixels "semente" e adiciona pixels vizinhos com base em critérios de similaridade (*AdamsBischof1994*).
- **Bisseção Espectral**: Uma técnica para particionar grafos usando o vetor de Fiedler da matriz Laplaciana (*KarypisKumar1998, Guia de Estudos*).
- **Difusão Anisotrópica**: Uma técnica de suavização de imagens que preserva bordas, utilizando coeficientes de condução variáveis (*PeronaMalik1990*).
- **Funcionais de Energia**: Funções que medem a qualidade de uma segmentação, frequentemente usadas em modelos variacionais (*MumfordShah1989*).
- **Matriz Laplaciana**: Uma representação matricial de um grafo que captura sua estrutura de conectividade (*KarypisKumar1998, Guia de Estudos*).
- **Vetor de Fiedler**: O autovetor associado ao segundo menor autovalor da matriz Laplaciana, usado para particionar grafos (*KarypisKumar1998, Guia de Estudos*).
- **Contração de Grafos**: O processo de reduzir um grafo combinando vértices e arestas (*KarypisKumar1998*).
- **Espaço de Escala**: Uma representação de uma imagem em múltiplas escalas de detalhe, obtida por suavização (*PeronaMalik1990*).