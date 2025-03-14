# 3dMesh.py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import Normalize
from matplotlib import colormaps
import tkinter as tk
from tkinter import ttk, messagebox
import json
import ast
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
  
def create_3d_mesh(nx=8, ny=8, nz=3, active_intervals=None):
    """
    Cria uma malha 3D logicamente retangular, definindo células ativas por intervalos variáveis por linha e camada.
    
    A malha é inicializada com zeros (células inativas) e depois são ativadas células específicas de acordo
    com os intervalos definidos no dicionário `active_intervals`.
    
    Parameters
    ----------
    nx : int, optional
        Número de células na direção X. Valor padrão é 8.
    ny : int, optional
        Número de células na direção Y. Valor padrão é 8.
    nz : int, optional
        Número de células na direção Z. Valor padrão é 3.
    active_intervals : dict, optional
        Dicionário definindo os intervalos de células ativas. A estrutura do dicionário é:
        {k: {i: [(j_start, j_end), ...], ...}, ...} onde:
        - k é o índice da camada (direção Z)
        - i é o índice da linha (direção X)
        - (j_start, j_end) são tuplas definindo o intervalo de colunas ativas (direção Y)
        Se None, utiliza um padrão predefinido.
        
    Returns
    -------
    numpy.ndarray
        Array tridimensional de dimensões (nx, ny, nz) representando a malha 3D,
        onde 1 indica células ativas e 0 indica células inativas.
    
    Examples
    --------
    >>> # Exemplo com configuração padrão
    >>> mesh = create_3d_mesh()
    >>> print(mesh.shape)
    (8, 8, 3)
    
    >>> # Exemplo com intervalos customizados
    >>> custom_intervals = {
    ...     0: {2: [(3, 4)], 3: [(2, 5)]},
    ...     1: {1: [(2, 5)], 2: [(1, 6)]}
    ... }
    >>> mesh = create_3d_mesh(active_intervals=custom_intervals)
    """
    # Configuração padrão dos intervalos ativos se não forem fornecidos
    if active_intervals is None:
        active_intervals = {
            0: {2: [(3, 4)], 3: [(2, 5)], 4: [(2, 5)], 5: [(3, 4)]},
            1: {1: [(2, 5)], 2: [(1, 6)], 3: [(1, 6)], 4: [(1, 6)], 5: [(1, 6)], 6: [(2, 5)]},
            2: {0: [(2, 5)], 1: [(1, 6)], 2: [(0, 7)], 3: [(0, 7)], 4: [(0, 7)], 5: [(0, 7)], 6: [(1, 6)], 7: [(2, 5)]}
        }
    
    mesh = np.zeros((nx, ny, nz), dtype=int)  # Inicializa todas as células como vazias
    
    for k, layers in active_intervals.items():
        for i, intervals in layers.items():
            for j_start, j_end in intervals:
                # Verifica se os índices estão dentro dos limites da malha
                if i < nx and k < nz :  #Removed j_end < ny
                    # Ajusta o intervalo final se necessário
                    j_end_adjusted = min(j_end, ny)
                    mesh[i, j_start:j_end_adjusted, k] = 1  # Ativa apenas as células dentro dos intervalos
       
    return mesh


def refine_mesh(mesh, refinement_regions):
    """
    Refina a malha tridimensional conforme as regiões definidas por intervalos variáveis.
    
    Para cada camada e linha especificada, refina as células ativas dentro dos
    intervalos definidos, aplicando os fatores de refinamento correspondentes.
    
    Parameters
    ----------
    mesh : numpy.ndarray
        Array tridimensional representando a malha 3D, onde valores positivos
        indicam células ativas.
    refinement_regions : dict
        Dicionário definindo as regiões de refinamento. A estrutura do dicionário é:
        {k: {i: [(j_start, j_end, factor_i, factor_j, factor_k), ...], ...}, ...} onde:
        - k é o índice da camada (direção Z)
        - i é o índice da linha (direção X)
        - (j_start, j_end, factor_i, factor_j, factor_k) são tuplas definindo:
          * j_start, j_end: intervalo de colunas a serem refinadas (direção Y)
          * factor_i, factor_j, factor_k: fatores de refinamento nas direções X, Y e Z
    
    Returns
    -------
    numpy.ndarray
        Malha refinada com a mesma forma do array de entrada.
    
    Examples
    --------
    >>> mesh = create_3d_mesh(8, 8, 3)
    >>> regions = {
    ...     1: {  # camada Z=1
    ...         3: [(2, 4, 2, 2, 1), (5, 6, 3, 1, 1)],  # linha X=3 com dois intervalos
    ...         4: [(3, 5, 2, 3, 1)]  # linha X=4 com um intervalo
    ...     }
    ... }
    >>> refined_mesh = refine_mesh(mesh, regions)
    """
    refined_mesh = np.zeros_like(mesh)  # Inicializa com células inativas
    
    # Primeiro, mantém as células ativas originais
    for i in range(mesh.shape[0]):
        for j in range(mesh.shape[1]):
            for k in range(mesh.shape[2]):
                if mesh[i, j, k] > 0:
                    refined_mesh[i, j, k] = 1  # Mantém as células ativas
    
    # Aplica o refinamento por intervalos variáveis
    for k, layers in refinement_regions.items():
        for i, intervals in layers.items():
            for interval in intervals:
                # Verifica se é um intervalo válido com 5 elementos (j_start, j_end, factor_i, factor_j, factor_k)
                if len(interval) == 5:
                    j_start, j_end, factor_i, factor_j, factor_k = interval
                    
                    # Verifica se os índices estão dentro dos limites da malha
                    if (0 <= i < mesh.shape[0] and 
                        0 <= k < mesh.shape[2] and 
                        0 <= j_start <= j_end < mesh.shape[1]):
                        
                        # Aplica o refinamento apenas para células ativas dentro do intervalo
                        for j in range(j_start, j_end + 1):
                            if refined_mesh[i, j, k] > 0:
                                refined_mesh[i, j, k] *= factor_i * factor_j * factor_k
                else:
                    print(f"Aviso: Intervalo inválido ignorado: {interval}. Formato esperado: (j_start, j_end, factor_i, factor_j, factor_k)")
    
    return refined_mesh

def compute_weight_array(mesh):
    """
    Calcula o array de pesos para a projeção 2D ao longo da direção Z.
    
    Os pesos são calculados somando os valores das células ao longo do eixo Z.
    
    Parameters
    ----------
    mesh : numpy.ndarray
        Array tridimensional representando a malha 3D.
        
    Returns
    -------
    numpy.ndarray
        Array bidimensional com os pesos calculados, representando
        a projeção da malha 3D no plano XY.
    
    Examples
    --------
    >>> mesh = create_3d_mesh(8, 8, 3)
    >>> weights = compute_weight_array(mesh)
    >>> print(weights.shape)
    (8, 8)
    """
    weight_array = np.sum(mesh, axis=2)  # Soma ao longo do eixo Z
    return weight_array

def plot_weights(weight_array):
    """
    Plota a matriz de pesos como uma imagem 2D colorida com os valores sobrepostos.
    
    Parameters
    ----------
    weight_array : numpy.ndarray
        Array bidimensional com os pesos calculados.
    
    Returns
    -------
    None
        A função cria e exibe um gráfico 2D, mas não retorna nenhum valor.
    
    Notes
    -----
    Esta função usa a biblioteca Matplotlib para criar uma visualização 2D da matriz de pesos.
    A cor de cada célula é determinada pelo valor do peso, e o valor numérico é mostrado
    dentro de cada célula. A cor do texto é ajustada (preto ou branco) para garantir
    a legibilidade de acordo com o brilho da cor de fundo.
    """
    # Função para plotar a matriz de pesos
    fig, ax = plt.subplots()
    cmap = colormaps['viridis']  # Escolha o mapa de cores desejado
    norm = Normalize(vmin=weight_array.min(), vmax=weight_array.max())

    # Exibe a matriz de pesos
    cax = ax.imshow(weight_array, cmap=cmap, norm=norm)

    # Adiciona os valores sobre as células
    for (i, j), val in np.ndenumerate(weight_array):
        # Obtém a cor de fundo da célula
        bg_color = cmap(norm(val))
        # Calcula o brilho percebido da cor de fundo
        brightness = 0.299 * bg_color[0] + 0.587 * bg_color[1] + 0.114 * bg_color[2]
        # Define a cor do texto como branco ou preto, dependendo do brilho
        text_color = 'white' if brightness < 0.5 else 'black'
        ax.text(j, i, f'{val}', ha='center', va='center', color=text_color)

    # Adiciona uma barra de cores para referência
    fig.colorbar(cax)

    # Configurações adicionais
    ax.set_title('Matriz de Pesos')
    ax.set_xlabel('Índice da Coluna')
    ax.set_ylabel('Índice da Linha')

def plot_3d_mesh_with_weights(mesh, show_refinement=False):
    """
    Plota a malha 3D mostrando as células ativas com base nos pesos.
    
    As células ativas não refinadas são mostradas com alta transparência,
    enquanto as células refinadas são destacadas com cores mais visíveis.
    Células inativas são quase invisíveis.
    
    Parameters
    ----------
    mesh : numpy.ndarray
        Array tridimensional representando a malha 3D, onde valores positivos
        indicam células ativas.
    show_refinement : bool, optional
        Se True, mostra as células refinadas com cores distintas. Se False,
        mostra apenas células ativas/inativas. Valor padrão é False.
    
    Returns
    -------
    None
        A função cria e exibe um gráfico 3D, mas não retorna nenhum valor.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Define cores para células inativas, ativas não refinadas e refinadas
    inactive_color = (1, 0, 0, 0.05)  # Vermelho quase invisível
    active_color = (0, 0, 1, 0.2)     # Azul com alta transparência
    
    if show_refinement:
        # Normaliza os valores para coloração
        max_value = np.max(mesh)
        norm = Normalize(vmin=1, vmax=max_value)
        cmap = colormaps['viridis']  # Use viridis colormap for refinement values
        
        title = 'Malha 3D com Células Refinadas'
    else:
        title = 'Malha 3D com Células Ativas/Inativas'

    # Dimensões da malha
    nx, ny, nz = mesh.shape

    # Função para criar vértices de um cubo
    def cubo_vertices(x, y, z):
        """
        Retorna os vértices de um cubo dadas as coordenadas de um dos seus vértices.
        
        Parameters
        ----------
        x : int
            Coordenada X do vértice inicial.
        y : int
            Coordenada Y do vértice inicial.
        z : int
            Coordenada Z do vértice inicial.
            
        Returns
        -------
        list
            Lista com as coordenadas dos 8 vértices do cubo.
        """

        return [
            [x, y, z],
            [x + 1, y, z],
            [x + 1, y + 1, z],
            [x, y + 1, z],
            [x, y, z + 1],
            [x + 1, y, z + 1],
            [x + 1, y + 1, z + 1],
            [x, y + 1, z + 1]
        ]

    # Função para criar faces de um cubo a partir dos vértices
    def cubo_faces(verts):
        """
        Retorna as faces de um cubo a partir dos seus vértices.
        
        Parameters
        ----------
        verts : list
            Lista com as coordenadas dos 8 vértices do cubo.
            
        Returns
        -------
        list
            Lista com as 6 faces do cubo, onde cada face é uma lista de 4 vértices.
        """
   
        return [
            # First face: top face
            [verts[0], verts[1], verts[5], verts[4]],
            # Second face: bottom face
            [verts[7], verts[6], verts[2], verts[3]],
            # Third face: front face
            [verts[0], verts[3], verts[7], verts[4]],
            # Fourth face: back face
            [verts[1], verts[2], verts[6], verts[5]],
            # Fifth face: left face
            [verts[0], verts[1], verts[2], verts[3]],
            # Sixth face: right face
            [verts[4], verts[5], verts[6], verts[7]]
        ]

    # Lista para armazenar todas as células, ordenadas pelo valor de refinamento
    all_cells = []
    
    # Percorre todas as células da malha e armazena para ordenação posterior
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                cell_value = mesh[i, j, k]
                verts = cubo_vertices(i, j, k)
                faces = cubo_faces(verts)
                
                # Define a cor com base no valor da célula
                if cell_value <= 0:
                    color = inactive_color
                    z_order = -1  # Células inativas têm prioridade mais baixa
                elif cell_value == 1:
                    color = active_color
                    z_order = 0   # Células ativas não refinadas têm prioridade média
                else:
                    if show_refinement:
                        # Usa o colormap para células refinadas com transparência ajustada
                        color_rgba = list(cmap(norm(cell_value)))
                        # Células refinadas têm transparência menor (mais visíveis)
                        color_rgba[3] = 0.8  
                        color = tuple(color_rgba)
                        z_order = cell_value  # Células mais refinadas têm prioridade mais alta
                    else:
                        # No modo não-refinamento, usa a cor azul padrão, mas mais opaca
                        color = (0, 0, 1, 0.6)
                        z_order = 1
                
                all_cells.append((z_order, faces, color))
    
    # Ordena as células pela prioridade de desenho (z-order)
    # Células com valores menores (inativas, depois não refinadas) são desenhadas primeiro
    all_cells.sort(key=lambda x: x[0])
    
    # Adiciona as células ao gráfico na ordem correta
    for _, faces, color in all_cells:
        poly3d = Poly3DCollection(faces, facecolors=color, linewidths=0.1, edgecolors='k')
        ax.add_collection3d(poly3d)

    # Configurações do gráfico
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(0, nx)
    ax.set_ylim(0, ny)
    ax.set_zlim(0, nz)
    ax.view_init(elev=20, azim=30)  # Ajusta a visualização 3D
    ax.set_title(title)
    
    # Adiciona uma legenda colorida se estiver mostrando refinamento
    if show_refinement:
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, orientation='vertical', 
                           label='Fator de Refinamento')

def plot_mesh_in_axis(ax, mesh, show_refinement):
    """
    Função auxiliar para plotar uma malha 3D em um eixo específico.
    Células não refinadas são quase transparentes, enquanto células
    refinadas são destacadas.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        O eixo onde a malha será plotada.
    mesh : numpy.ndarray
        Array tridimensional representando a malha 3D.
    show_refinement : bool
        Se True, mostra as células refinadas com cores distintas.
    """
    # Define cores para células inativas, ativas não refinadas
    inactive_color = (1, 0, 0, 0.05)  # Vermelho quase invisível
    active_color = (0, 0, 1, 0.2)     # Azul com alta transparência
    
    if show_refinement:
        # Normaliza os valores para coloração
        max_value = np.max(mesh)
        norm = Normalize(vmin=1, vmax=max_value)
        cmap = colormaps['viridis']  # Use viridis colormap for refinement values
    
    # Dimensões da malha
    nx, ny, nz = mesh.shape
    
    # Função para criar vértices de um cubo
    def cubo_vertices(x, y, z):
        return [
            [x, y, z],
            [x + 1, y, z],
            [x + 1, y + 1, z],
            [x, y + 1, z],
            [x, y, z + 1],
            [x + 1, y, z + 1],
            [x + 1, y + 1, z + 1],
            [x, y + 1, z + 1]
        ]
    
    # Função para criar faces de um cubo a partir dos vértices
    def cubo_faces(verts):
        return [
            [verts[0], verts[1], verts[5], verts[4]],
            [verts[7], verts[6], verts[2], verts[3]],
            [verts[0], verts[3], verts[7], verts[4]],
            [verts[1], verts[2], verts[6], verts[5]],
            [verts[0], verts[1], verts[2], verts[3]],
            [verts[4], verts[5], verts[6], verts[7]]
        ]
    
    # Lista para armazenar todas as células, ordenadas pelo valor de refinamento
    all_cells = []
    
    # Percorre todas as células da malha e armazena para ordenação posterior
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                cell_value = mesh[i, j, k]
                verts = cubo_vertices(i, j, k)
                faces = cubo_faces(verts)
                
                # Define a cor com base no valor da célula
                if cell_value <= 0:
                    color = inactive_color
                    z_order = -1  # Células inativas têm prioridade mais baixa
                elif cell_value == 1:
                    color = active_color
                    z_order = 0   # Células ativas não refinadas têm prioridade média
                else:
                    if show_refinement:
                        # Usa o colormap para células refinadas com transparência ajustada
                        color_rgba = list(cmap(norm(cell_value)))
                        # Células refinadas têm transparência menor (mais visíveis)
                        color_rgba[3] = 0.8  
                        color = tuple(color_rgba)
                        z_order = cell_value  # Células mais refinadas têm prioridade mais alta
                    else:
                        # No modo não-refinamento, usa a cor azul padrão, mas mais opaca
                        color = (0, 0, 1, 0.6)
                        z_order = 1
                
                all_cells.append((z_order, faces, color))
    
    # Ordena as células pela prioridade de desenho (z-order)
    all_cells.sort(key=lambda x: x[0])
    
    # Adiciona as células ao gráfico na ordem correta
    for _, faces, color in all_cells:
        poly3d = Poly3DCollection(faces, facecolors=color, linewidths=0.1, edgecolors='k')
        ax.add_collection3d(poly3d)
    
    # Configurações do gráfico
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(0, nx)
    ax.set_ylim(0, ny)
    ax.set_zlim(0, nz)
    ax.view_init(elev=20, azim=30)  # Ajusta a visualização 3D
    
    # Adiciona uma legenda colorida se estiver mostrando refinamento
    if show_refinement:
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        plt.colorbar(sm, ax=ax, orientation='vertical', 
                     label='Fator de Refinamento')

def plot_both_mesh_views(mesh):
    """
    Cria duas visualizações da malha 3D lado a lado:
    1. Visualização simples (ativa/inativa)
    2. Visualização com células refinadas coloridas
    
    Células não refinadas são quase transparentes para permitir melhor
    visualização das células refinadas no interior da malha.
    
    Parameters
    ----------
    mesh : numpy.ndarray
        Array tridimensional representando a malha 3D.
    
    Returns
    -------
    None
        A função cria e exibe dois gráficos 3D, mas não retorna nenhum valor.
    """
    # Configuração do layout
    fig = plt.figure(figsize=(15, 7))
    
    # Primeiro gráfico: visualização simples
    ax1 = fig.add_subplot(121, projection='3d')
    plot_mesh_in_axis(ax1, mesh, show_refinement=False)
    ax1.set_title('Malha 3D com Células Ativas/Inativas')
    
    # Segundo gráfico: visualização com refinamento
    ax2 = fig.add_subplot(122, projection='3d')
    plot_mesh_in_axis(ax2, mesh, show_refinement=True)
    ax2.set_title('Malha 3D com Células Refinadas')
    
    plt.tight_layout()

def compute_inertia_matrix_from_grid(weight_matrix):
    """
    Calcula a matriz de inércia e o centro de massa a partir de uma matriz de pesos.
    
    Parâmetros:
    - weight_matrix: Matriz bidimensional onde cada entrada representa o peso de um ponto.

    Retorna:
    - I: Matriz de inércia 2x2
    - center_of_mass: Tupla (x_bar, y_bar) com as coordenadas do centro de massa
    """
    weight_matrix = np.array(weight_matrix)  # Garante que os pesos estão como um array NumPy

    # Dimensões da matriz
    nx, ny = weight_matrix.shape

    # Criando listas de coordenadas correspondentes
    x_coords, y_coords = np.meshgrid(np.arange(nx), np.arange(ny), indexing='ij')

    # Achando o centro de massa
    total_weight = np.sum(weight_matrix)
    if total_weight == 0:
        x_bar, y_bar = 0, 0  # Or some other appropriate default value
    else:
        x_bar = np.sum(weight_matrix * x_coords) / total_weight
        y_bar = np.sum(weight_matrix * y_coords) / total_weight


    # Construção da matriz de inércia
    I_xx = np.sum(weight_matrix * (x_coords - x_bar) ** 2)
    I_yy = np.sum(weight_matrix * (y_coords - y_bar) ** 2)
    I_xy = -np.sum(weight_matrix * (x_coords - x_bar) * (y_coords - y_bar))

    I = np.array([[I_xx, I_xy],
                  [I_xy, I_yy]])

    return I, (x_bar, y_bar)    

def compute_inertia_matrix_from_points(points):
    """
    Calcula a matriz de inércia e o centro de massa a partir de um conjunto de pontos 2D com pesos.
    
    Parâmetros:
    - points: Array de formato (n, 3) onde cada linha representa um ponto [x, y, peso]
    
    Retorna:
    - I: Matriz de inércia 2x2
    - center_of_mass: Tupla (x_bar, y_bar) com as coordenadas do centro de massa
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
        Um par contendo:
        - principal_moments: numpy.ndarray
            Momentos principais de inércia (valores próprios da matriz).
        - principal_axes: numpy.ndarray
            Eixos principais (vetores próprios da matriz), cada coluna corresponde a um eixo.
    
    Examples
    --------
    >>> I = np.array([[3, 1], [1, 2]])
    >>> moments, axes = calculate_principal_moments(I)
    """
    # Verifica se a matriz é simétrica (propriedade importante para matrizes de inércia)
    if not np.allclose(inertia_matrix, inertia_matrix.T):
        raise ValueError("A matriz de inércia deve ser simétrica")
    
    # Calcula os valores próprios (momentos principais) e vetores próprios (eixos principais)
    principal_moments, principal_axes = np.linalg.eig(inertia_matrix)
    
    return principal_moments, principal_axes


def visualize_inertia_deformation(principal_moments, principal_axes, fig_size=(6, 6), title=None):
    """
    Visualiza a deformação de uma esfera/círculo unitário com base nos momentos principais de inércia.
    
    Esta função gera um gráfico que mostra como uma esfera/círculo unitário é deformado quando
    transformado pela matriz de inércia, resultando em uma elipse. Também exibe os eixos principais.
    
    Parameters
    ----------
    principal_moments : numpy.ndarray
        Momentos principais de inércia (valores próprios da matriz).
    principal_axes : numpy.ndarray
        Eixos principais (vetores próprios da matriz).
    fig_size : tuple, optional
        Tamanho da figura em polegadas, por padrão (6, 6).
    title : str, optional
        Título do gráfico. Se None, um título padrão é usado.
    
    Returns
    -------
    tuple
        Um par contendo:
        - fig: matplotlib.figure.Figure
            O objeto figura do matplotlib.
        - ax: matplotlib.axes.Axes
            O objeto eixos do matplotlib.
    
    Examples
    --------
    >>> I = np.array([[3, 1], [1, 2]])
    >>> moments, axes = calculate_principal_moments(I)
    >>> fig, ax = visualize_inertia_deformation(moments, axes)
    >>> plt.show()
    """
    # Reconstrução da matriz de inércia a partir dos momentos e eixos principais
    inertia_matrix = principal_axes @ np.diag(principal_moments) @ principal_axes.T
    
    # Criação do círculo unitário (pontos uniformemente distribuídos)
    theta = np.linspace(0, 2*np.pi, 100)
    circle = np.array([np.cos(theta), np.sin(theta)])  # Pontos (x, y) no círculo unitário
    
    # Aplicação da matriz de inércia ao círculo para obter a elipse transformada
    ellipse = inertia_matrix @ circle  # Multiplicação matricial
    
    # Criação da figura e eixos
    fig, ax = plt.subplots(figsize=fig_size)
    
    # Plotando o círculo original e a elipse transformada
    ax.plot(circle[0], circle[1], 'b--', label="Círculo Unitário")
    ax.plot(ellipse[0], ellipse[1], 'r-', label="Elipse Transformada")
    
    # Plotando os vetores próprios (eixos principais da elipse)
    for i in range(len(principal_moments)):
        vec = principal_axes[:, i] * principal_moments[i]  # Escalando os vetores pelos valores próprios
        ax.plot([0, vec[0]], [0, vec[1]], 'k', lw=2, label=f"Eixo {i+1}")
    
    # Configurações do gráfico
    ax.axhline(0, color='gray', linewidth=0.5)  # Linha horizontal no zero
    ax.axvline(0, color='gray', linewidth=0.5)  # Linha vertical no zero
    
    # Determina os limites do gráfico com base na elipse e nos vetores
    max_range = max(np.max(np.abs(ellipse)), np.max(np.abs(principal_moments)))
    limit = max_range * 1.2  # Adiciona uma margem de 20%
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    
    # Define o título do gráfico
    if title is None:
        title = "Transformação do Círculo pela Matriz de Inércia"
    ax.set_title(title)
    
    ax.legend()
    ax.set_aspect('equal')  # Mantém a escala igual nos eixos
    
    return fig, ax
