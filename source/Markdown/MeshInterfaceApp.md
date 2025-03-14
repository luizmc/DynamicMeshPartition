# MeshInterfaceApp: Interface Gráfica para Malhas 3D

## Visão Geral

`MeshInterfaceApp` é uma interface gráfica desenvolvida em Tkinter para criar e visualizar malhas tridimensionais. Esta ferramenta permite aos usuários especificar intervalos ativos em diferentes camadas de uma grade 3D, visualizar a estrutura resultante em tempo real, e gerar malhas 3D baseadas nestes parâmetros.

## Funcionalidades Principais

- **Configuração de Parâmetros da Malha**: Define dimensões básicas (nx, ny, nz) da estrutura tridimensional
- **Criação de Intervalos Ativos**: Especifica áreas ativas em cada camada Z e linha X
- **Visualização em Tempo Real**: Renderiza representações 2D de cada camada Z da malha
- **Gerenciamento de Intervalos**: Interface para adicionar, remover e editar intervalos ativos
- **Restauração de Valores Padrão**: Retorna rapidamente a uma configuração pré-definida
- **Exportação de Resultados**: Retorna a malha gerada para uso em código externo

## Estrutura de Dados

A classe utiliza uma estrutura de dados hierárquica para representar intervalos ativos:

```python
active_intervals = {
    z_layer: {
        x_line: [(y_start1, y_end1), (y_start2, y_end2), ...],
        ...
    },
    ...
}
```

Onde:
- `z_layer`: Índice da camada Z
- `x_line`: Índice da linha X
- `y_start`, `y_end`: Delimitam um intervalo ativo na coordenada Y

## Interface do Usuário

A interface é composta por várias seções:

1. **Painel de Parâmetros**: Controles para as dimensões da malha (nx, ny, nz)
2. **Entrada de Intervalos**: Campos para especificar novos intervalos ativos
3. **Visualização de Intervalos**: Exibição em árvore e representação textual dos intervalos definidos
4. **Controles de Gerenciamento**: Botões para adicionar, remover e limpar intervalos
5. **Visualização da Malha**: Representação gráfica das camadas da malha em tempo real

![Diagrama da Interface](https://via.placeholder.com/800x600)

## Uso Básico

### Inicialização

```python
import tkinter as tk
from mesh_interface import open_mesh_interface

# Usando a função de conveniência
mesh = open_mesh_interface()

# OU inicializando manualmente
def my_mesh_function(nx, ny, nz, active_intervals):
    # Criar malha personalizada
    return mesh_data

root = tk.Tk()
app = MeshInterfaceApp(root, my_mesh_function, on_mesh_created=callback_function)
root.mainloop()
```

### Definição de Intervalos Ativos

Para definir manualmente intervalos ativos sem usar a interface:

```python
# Formato: {z: {x: [(y_start, y_end), ...]}}
active_intervals = {
    0: {2: [(3, 4)], 3: [(2, 5)]},
    1: {1: [(2, 5)], 2: [(1, 6)]}
}

mesh = create_3d_mesh(nx=8, ny=8, nz=3, active_intervals=active_intervals)
```

## Casos de Uso

### 1. Prototipagem de Modelos Estruturais

Ideal para engenheiros e cientistas que precisam definir visualmente áreas ativas em uma estrutura tridimensional antes de aplicar algoritmos complexos.

### 2. Modelagem de Materiais Porosos

Permite definir rapidamente regiões de interesse em materiais porosos ou compósitos para simulações físicas.

### 3. Ensino de Conceitos 3D

Ferramenta educacional para demonstrar conceitos de estruturas tridimensionais, malhas computacionais e visualização de dados.

### 4. Geração de Dados para Simulações

Cria especificações de entrada para simulações que exigem definição de regiões ativas em uma grade 3D.

## Integração com Sistemas Existentes

A interface foi projetada para ser facilmente integrada com sistemas existentes:

1. Aceita qualquer função de geração de malha com a assinatura adequada
2. Retorna a malha gerada para processamento posterior
3. Suporta callbacks para notificação quando uma nova malha é gerada

## Personalização e Extensão

A classe pode ser estendida para:

- Suportar formatos de visualização adicionais
- Integrar algoritmos de validação personalizados
- Adicionar opções de exportação (por exemplo, para formatos como VTK, STL)
- Implementar funcionalidades de recorte ou seções transversais

## Requisitos Técnicos

- Python 3.6+
- Bibliotecas: Tkinter, NumPy, Matplotlib
- Recomendado: Sistema com interface gráfica

## Exemplo de Código Completo

```python
import tkinter as tk
import numpy as np
from mesh_interface import open_mesh_interface, MeshInterfaceApp

# Função personalizada para geração de malha
def custom_mesh_generator(nx, ny, nz, active_intervals):
    # Cria uma malha vazia
    mesh = np.zeros((nx, ny, nz))
    
    # Preenche com base nos intervalos ativos
    for z in active_intervals:
        for x in active_intervals[z]:
            for y_start, y_end in active_intervals[z][x]:
                mesh[x, y_start:y_end+1, z] = 1
    
    return mesh

# Callback para processamento após geração
def process_mesh(mesh):
    print(f"Malha gerada com {np.sum(mesh)} células ativas")
    # Processamento adicional...

# Método 1: Usando a função de conveniência
mesh_result = open_mesh_interface(mesh_function=custom_mesh_generator)

# Método 2: Controlando todo o ciclo de vida
if __name__ == "__main__":
    root = tk.Tk()
    app = MeshInterfaceApp(
        root=root,
        mesh_function=custom_mesh_generator,
        on_mesh_created=process_mesh
    )
    root.mainloop()
```

## Conclusão

A `MeshInterfaceApp` oferece uma solução completa para criação visual e interativa de malhas 3D, combinando facilidade de uso com flexibilidade para integração em fluxos de trabalho existentes. Sua implementação modular permite adaptações para diversos casos de uso em engenharia, ciência de materiais, e modelagem computacional.