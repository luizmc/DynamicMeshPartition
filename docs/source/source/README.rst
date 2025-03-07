Bisseção Recursiva
==================

Códigos relativos ao artigo *"Dynamic Mesh Partitioning For Improving Linear Solver Load Balancing In Compositional Aim Simulations"* de J.R.P. Rodrigues e L.S. Gasparini.

---

Arquivos do Projeto
===================

`mesh3d.py`
-----------

Módulo principal para criação, refinamento e análise de malhas 3D.

**Rotinas disponíveis**:

- ``create_3d_mesh``: Cria uma malha 3D logicamente retangular, definindo células ativas por intervalos variáveis por linha e camada.
  
- ``refine_mesh``: Refina a malha tridimensional conforme as regiões definidas por intervalos variáveis.
  
- ``compute_weight_array``: Calcula o array de pesos para a projeção 2D ao longo da direção Z.
  
- ``plot_3d_mesh_with_weights_old``: Plota a malha 3D mostrando as células ativas com base nos pesos.
  
- ``plot_weights``: Plota a matriz de pesos como uma imagem 2D colorida com os valores sobrepostos.
  
- ``plot_3d_mesh_with_weights``: Plota a malha 3D mostrando as células ativas com base nos pesos.
  
- ``plot_mesh_in_axis``: Função auxiliar para plotar uma malha 3D em um eixo específico.
  
- ``plot_both_mesh_views``: Cria duas visualizações da malha 3D lado a lado (simples e com células refinadas coloridas).
  
- ``compute_inertia_matrix_from_grid``: Calcula a matriz de inércia e o centro de massa a partir de uma matriz de pesos.
  
- ``compute_inertia_matrix_from_points``: Calcula a matriz de inércia e o centro de massa a partir de um conjunto de pontos 2D com pesos.
  
- ``calculate_principal_moments``: Calcula os momentos principais de inércia e os eixos principais.
  
- ``visualize_inertia_deformation``: Visualiza a deformação de uma esfera/círculo unitário com base nos momentos principais de inércia.
  
---

`particionamento_por_bissecao.py`
---------------------------------

Módulo para particionamento de malhas usando o método de bissecção recursiva.

**Rotinas disponíveis**:

- ``generate_input_synthetic_dictionary``: Gera um dicionário sintético com coordenadas e pesos para testes.

- ``normalize_vectors``: Normaliza vetores para terem norma euclidiana unitária.

- ``project_points_on_eigenvector``: Projeta pontos na direção do autovetor principal, calculando coordenadas projetadas.

- ``calculate_max_distance``: Calcula a distância máxima entre pontos após projeção.

- ``find_best_projection_and_division_balanced``: Encontra a melhor projeção e divisão balanceada para um conjunto de pontos.

- ``convert_result_to_domain_assignment``: Converte o resultado do particionamento em um array 2D de atribuições de domínio.

- ``evaluate_partition_quality``: Avalia a qualidade da partição com métricas como balanceamento de peso e variância.

- ``recursive_binary_subset_division_balanced``: Realiza a divisão recursiva binária de conjuntos para criar partições balanceadas.

---

`Unittest_mesh3d.py`
--------------------

Testes unitários para validar as funcionalidades do módulo ``mesh3d.py``.

**Casos de teste**:

- Criação de malha padrão e customizada
- Refinamento de células
- Cálculo de matriz de pesos
- Geração de gráficos 3D/2D
- Cálculo de inércia e momentos principais
- Validação de ortogonalidade de vetores próprios

---

`Unittest_particionamento_por_bissecao.py`
------------------------------------------

Testes unitários para validar as funcionalidades do módulo ``particionamento_por_bissecao.py``.

**Casos de teste**:

- Geração de dicionários sintéticos de entrada
- Normalização de vetores
- Projeção de pontos em autovetores
- Cálculo de distâncias máximas
- Divisão balanceada de conjuntos
- Conversão de resultados para atribuição de domínios
- Avaliação da qualidade da partição
- Divisão recursiva binária de subconjuntos

---

Diretório `Exemplos`
====================

Contém casos de uso práticos e scripts demonstrativos.  
:ref:`readmeexemplos` neste diretório para instruções detalhadas e exemplos de aplicação.

---

Exemplos de Uso
===============

1. Criação de uma malha 3D básica:

.. code-block:: python

    mesh = create_3d_mesh()
    print(mesh.shape)  # Saída: (8, 8, 3)

2. Criação de uma malha com intervalos customizados:

.. code-block:: python

    custom_intervals = {
    0: {2: [(3, 4)], 3: [(2, 5)]},
    1: {1: [(2, 5)], 2: [(1, 6)]}
    }
    mesh = create_3d_mesh(active_intervals=custom_intervals)

3. Refinamento de uma malha 3D:

.. code-block:: python

    mesh = create_3d_mesh(8, 8, 3)
    regions = {
    1: {  # camada Z=1
    3: [(2, 4, 2, 2, 1), (5, 6, 3, 1, 1)],  # linha X=3 com dois intervalos
    4: [(3, 5, 2, 3, 1)]  # linha X=4 com um intervalo
    }
    }
    refined_mesh = refine_mesh(mesh, regions)

4. Cálculo de matriz de inércia e visualização:

.. code-block:: python

    mesh = create_3d_mesh()
    weights = compute_weight_array(mesh)
    I, cm = compute_inertia_matrix_from_grid(weights)
    moments, axes = calculate_principal_moments(I)
    fig, ax = visualize_inertia_deformation(moments, axes)
    plt.show()


5. Particionamento de uma malha usando bissecção balanceada:

.. code-block:: python

    # Gerar dicionário de entrada
    input_dict = generate_input_synthetic_dictionary(10, 10)
    # Particionar em 4 subconjuntos balanceados
    result = recursive_binary_subset_division_balanced(input_dict, 4)


6.  Avaliar a qualidade da partição

.. code-block:: python

    quality = evaluate_partition_quality(result, input_dict)
    print(f"Desvio de peso: {quality['weight_percentage_range']}%")
    print(f"Variância: {quality['variance']}")

7. Converter para matriz de atribuição

.. code-block:: python

    domain_assignment = convert_result_to_domain_assignment(result, 10, 10)

---

Documentação
============

A documentação detalhada das funções (com parâmetros, retornos e exemplos) pode ser gerada via Sphinx usando os docstrings do código.
