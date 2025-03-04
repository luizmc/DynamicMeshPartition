# Casos de Uso

Coleção de scripts para análise e visualização de malhas 3D e transformações de inércia, usa o pacote mesh3d.

---

## 🗂 Arquivos Principais

### `Exemplo_inerciacompontos.py`

**Objetivo**  

Calcular a **matriz de inércia**, **centro de massa**, **momentos principais** e **eixos principais** para um conjunto de pontos com pesos.

**Funcionalidades**:

- Cálculo numérico do centro de massa a partir de coordenadas e pesos.
- Geração da matriz de inércia 3x3 (assumindo pontos no plano XY).
- Diagonalização da matriz para obtenção de autovalores (momentos) e autovetores (eixos).
- Saída formatada dos resultados no console.

**Execução**:

```bash
python Exemplo_inerciacompontos.py
```

### `Exemplo_plot2D_momentoInercia.py`

**Objetivo**

Ilustrar a transformação de um círculo unitário em elipse usando matriz de inércia 2D.

**Funcionalidades**:

- Aplicação de transformação linear à matriz de inércia
- Visualização dos eixos principais da elipse
- Configuração de gráfico com proporção isométrica

**Execução**:

```bash
python Exemplo_plot2D_momentoInercia.py
```

### `Exemplo_plot3D_malhas_refinamentos_weights.py`

**Objetivo**

Manipular e visualizar malhas 3D com refinamentos locais e projeções de peso.

**Funcionalidades**:

- Criação de malha 3D base (8x8x3)
- Refinamento em regiões específicas (camadas Z, linhas X/Y)
- Cálculo de projeção 2D de pesos
- Visualização 3D interativa e heatmap 2D

**Execução**:

```bash

python Exemplo_plot3D_malhas_refinamentos_weights.py
```

### `Exemplo_plot3D_momentoInercia.py`

**Objetivo**

Demonstrar a deformação de uma esfera unitária em um elipsoide via matriz de inércia 3D.

**Funcionalidades**:

- Cálculo de autovalores (momentos principais) e autovetores (eixos)

- Visualização 3D comparativa (esfera original vs. elipsoide transformado)

- Plotagem dos eixos principais escalados

**Execução**:

```bash
python Exemplo_plot3D_momentoInercia.py
```

---

## ⚙️ Pré-requisitos

- **Python 3.7+**

- **Bibliotecas**:

```bash

    pip install numpy matplotlib numpy matplotlib os sys mpl_toolkits
```

- **Módulo customizado**: mesh3d.py (incluído no repositório).

---

## 📊 Saídas Esperadas

| Script | Descrição da Visualização |
|--------|---------------------------|
| `Exemplo_inerciacompontos.py`      | Resultados numéricos no console: centro de massa, matriz de inércia, autovalores e autovetores|
| `Exemplo_plot2D_momentoInercia.py` | Gráfico 2D comparando círculo (linha tracejada) e elipse (linha sólida) |
| `Exemplo_plot3D_malhas_refinamentos_weights.py` | Malha 3D refinada + matriz de pesos colorida |
| `Exemplo_plot3D_momentoInercia.py` | Dois subplots 3D: esfera (azul) e elipsoide (vermelho) com eixos principais |

---

## 💡 Dicas de Uso

1. **Entrada de Dados**: No Exemplo_inerciacompontos.py, modifique o array points para testar diferentes configurações de massa.
2. **Interatividade 3D**: Use os controles do Matplotlib para rotacionar/ampliar as visualizações.
3. **Customização**:

    - Modifique a matriz *I* nos exemplos de inércia para explorar diferentes deformações.

    - Ajuste refinement_regions no script de malhas para testar refinamentos personalizados.

4. **Debug**: Verifique a saída do console para valores numéricos das malhas refinadas.

---

## 📄 Notas Técnicas

- **Cálculo de Inércia**: O script Exemplo_inerciacompontos.py assume pontos no plano XY (z=0) para simplificação.
- **Malhas 3D**: Células ativas são representadas por 1 e refinadas por valores multiplicados (ex: 4 = refinamento 2x2).
- **Inércia**: Matrizes devem ser simétricas para validade física.
- **Performance**: Reduza a resolução da malha (ex: theta/phi) para acelerar renderizações complexas.