# Resumo dos Documentos

Os documentos abordam técnicas de segmentação de imagens, explorando diferentes abordagens para decompor imagens em regiões significativas. Um dos artigos introduz o algoritmo Seeded Region Growing (SRG), que segmenta imagens com base em pontos iniciais chamados "sementes." Outro texto apresenta um esquema multinível para particionar gráficos irregulares, visando minimizar o número de arestas entre diferentes partições. Um terceiro artigo discute a aproximação ideal por funções suaves por partes, apresentando funcionais para medir a correspondência entre uma imagem e sua segmentação. Finalmente, um dos artigos propõe uma nova definição de espaço de escala e algoritmos baseados em difusão anisotrópica, preservando bordas nítidas durante a suavização.

---

## Referências  


### 1. AdamsBischof1994SeededRegionGrowing_IEEE_TPAMI.pdf

**Tema Principal:** Algoritmo de crescimento de regiões com sementes (seeded region growing).

**Ideias/Fatos Importantes:**
- O algoritmo aloca pixels não alocados (`T`) que fazem fronteira com regiões existentes (`Ai`).
- Avalia a diferença (`b(r)`) entre um pixel não alocado e a região vizinha, geralmente utilizando o valor de cinza do pixel (`g(r)`). A fórmula básica é:  
  `b(r) = |g(r) - mean{g(r') | r' ∈ N(r) ∩ Ai}|`.
- Se um pixel faz fronteira com múltiplas regiões, a região escolhida é aquela que minimiza `b(r)` ou o pixel é classificado como pertencente ao conjunto de fronteira (`ll`).
- O algoritmo itera até que um critério de parada seja satisfeito.
- Menciona o processo de *"flagging"* de pixels de fronteira para exibição ou correção interativa.
- É selecionado um `L ∈ T` tal que `"b(r) is minimized"`.

---

### 2. KarypisKumar1998A Fast and High Quality Multilevel Scheme for Partitioning Irregular Graphs_SISC.pdf

**Tema Principal:** Esquema multinível para particionamento de grafos irregulares.

**Ideias/Fatos Importantes:**
- **Spectral Bisection (SB):**  
  Utiliza o vetor de Fiedler (autovetor da matriz Laplaciana `Q = D − A`) para particionar o grafo.  
  - `D`: Matriz diagonal com `d_i,i = ∑ w(v_i, v_j)`.
  - Partições são definidas comparando valores do vetor de Fiedler com a mediana ponderada (`r`).
- **Fase de Coarsening:**  
  - Contração de grafos via mapeamento `Map`:  
    `Adj(u1) = {Map[x] | x ∈ Adj(v1) ∪ Adj(v2)} - {u1}`.  
    `w(u1, u2) = ∑ w(v1, x) + ∑ w(v2, x)`.
  - Estruturas de dados permitem contração eficiente (tempo proporcional ao número de arestas).
- **Resultados:**  
  - Tabelas comparam *edge-cuts* para partições de 64, 128 e 256 vias.  
  - Estratégias como *MMD*, *SND* e *MLND* são analisadas.

---

### 3. MumfordShah1989Optimal approximations by piecewise_CPAM.pdf

**Tema Principal:** Modelo de Mumford-Shah para segmentação de imagens.

**Ideias/Fatos Importantes:**
- **Funcionais de Energia:**  
  - `E`, `E0`, `E∞` medem a qualidade da segmentação.  
  - Relação com o modelo de Ising e regularidade da fronteira `Γ`.
- **Equações de Euler-Lagrange:**  
  - Condições de contorno em `∂R` e segmentos `γ_i`:  
    `Δf = p²(f - g)` (resolvida via função de Green).  
  - Equação chave:  
    `e(f⁺) - e(f⁻) + ν curv(γ_i) = 0` (curvatura relacionada à densidade de energia).
- **Aproximações:**  
  - Para `p → 0`: `f_r` aproxima-se de uma função constante por partes.  
  - Para `p → ∞`: Analisa ODEs resultantes e aplica estimativas via Lax-Milgram.

---

### 4. PeronaMalik1990Scale-Space and Edge Detection Using AnisotropicDiffusion_IEEE_TPAMI.pdf

**Tema Principal:** Difusão anisotrópica para espaço de escala e detecção de bordas.

**Ideias/Fatos Importantes:**
- **Discretização do Laplaciano:**  
  - Esquema de 4 vizinhos:  
    `I_{t+1} = I_t + λ[CN∇N + CS∇S + CE∇E + CW∇W]`.  
  - Coeficientes de condução atualizados pelo gradiente de brilho.
- **Princípio do Máximo:**  
  - Garantido se `0 ≤ λ ≤ 1/4` e `0 ≤ c ≤ 1`.
- **Borrão Gaussiano:** Caso especial com coeficientes constantes.

---

### 5. ShiMalik2000Normalized Cuts and Image Segmentation_IEEE_TPAMI.pdf

**Tema Principal:** Segmentação via Cortes Normalizados (*Normalized Cuts*).

**Ideias/Fatos Importantes:**
- **Função Objetivo:**  
  Minimizar `Ncut(A, B) = (cut(A, B))/(assoc(A, V)) + (cut(A, B))/(assoc(B, V))`.
- **Relaxamento Autovetorial:**  
  - Problema relaxado para `(D - W)y = λDy`.  
  - `W`: Matriz de similaridade com `w(i, j) = exp(-||F(i) - F(j)||²/σ_I² - ||X(i) - X(j)||²/σ_X²)`.
- **Características:** Intensidade, cor (HSV) ou textura (filtros DOOG).

---

## Conclusão

Os documentos abordam técnicas variadas para segmentação, como crescimento de regiões, particionamento multinível de grafos, difusão anisotrópica e cortes normalizados. A escolha do método depende das características da imagem e dos requisitos da aplicação (e.g., precisão, eficiência ou interatividade).