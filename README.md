# Dynamic Mesh Partition

Códigos relativos ao artigo *"Dynamic Mesh Partitioning For Improving Linear Solver Load Balancing In Compositional Aim Simulations"* de J.R.P. Rodrigues e L.S. Gasparini.

---

## Arquivos do Projeto

### `mesh3d.py`

Módulo principal para criação, refinamento e análise de malhas 3D.

**Rotinas disponíveis**:

- `create_3d_mesh`: Cria uma malha 3D com células ativas/inativas baseadas em intervalos definidos.
- `refine_mesh`: Refina regiões específicas da malha usando fatores de refinamento.
- `compute_weight_array`: Calcula pesos 2D pela projeção vertical da malha 3D.
- `plot_3d_mesh_with_weights`: Visualiza a malha 3D com destaque para células ativas/refinadas.
- `plot_weights`: Plota uma matriz 2D de pesos com cores e valores numéricos.
- `plot_both_mesh_views`: Exibe visualizações comparativas da malha (simples vs. refinada).
- `compute_inertia_matrix_from_grid`: Calcula matriz de inércia e centro de massa.
- `calculate_principal_moments`: Determina momentos e eixos principais de inércia.
- `visualize_inertia_deformation`: Plota deformação de um círculo unitário pela matriz de inércia.

---

### `Unittest_mesh3d.py`

Testes unitários para validar as funcionalidades do módulo `mesh3d.py`.  
**Casos de teste**:

- Criação de malha padrão e customizada
- Refinamento de células
- Cálculo de matriz de pesos
- Geração de gráficos 3D/2D
- Cálculo de inércia e momentos principais
- Validação de ortogonalidade de vetores próprios

---

## Diretório `Exemplos`

Contém casos de uso práticos e scripts demonstrativos.  
📄 Consulte o [README.md](Exemplos/README.md) neste diretório para instruções detalhadas e exemplos de aplicação.

---

## Documentação

A documentação detalhada das funções (com parâmetros, retornos e exemplos) pode ser gerada via Sphinx usando os docstrings do código.
