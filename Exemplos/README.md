# Repositório de Visualização Computacional

Coleção de scripts para análise e visualização de malhas 3D e transformações de inércia, usa o pacote mesh3d.

---

## 🗂 Arquivos Principais

### 1. `Exemplo_plot3D_momentoInercia.py`
**Objetivo**  
Demonstrar a deformação de uma **esfera unitária** em um **elipsoide** via matriz de inércia 3D.

**Funcionalidades**:
- Cálculo de autovalores (momentos principais) e autovetores (eixos)
- Visualização 3D comparativa (esfera original vs. elipsoide transformado)
- Plotagem dos eixos principais escalados

**Execução**:
```bash
python Exemplo_plot3D_momentoInercia.py
```

---

### 2. `Exemplo_plot2D_momentoInercia.py`
**Objetivo**  
Ilustrar a transformação de um **círculo unitário** em **elipse** usando matriz de inércia 2D.

**Funcionalidades**:
- Aplicação de transformação linear à matriz de inércia
- Visualização dos eixos principais da elipse
- Configuração de gráfico com proporção isométrica

**Execução**:
```bash
python Exemplo_plot2D_momentoInercia.py
```

---

### 3. `Example_plot3D_malhas_refinamentos_weights.py`
**Objetivo**  
Manipular e visualizar malhas 3D com refinamentos locais e projeções de peso.

**Funcionalidades**:
- Criação de malha 3D base (8x8x3)
- Refinamento em regiões específicas (camadas Z, linhas X/Y)
- Cálculo de projeção 2D de pesos
- Visualização 3D interativa e heatmap 2D

**Execução**:
```bash
python Example_plot3D_malhas_refinamentos_weights.py
```

---

## ⚙️ Pré-requisitos
- **Python 3.7+**
- **Bibliotecas**:
  ```bash
  pip install numpy matplotlib
  ```
- **Módulo customizado**: `mesh3d.py` (incluído no repositório).

---

## 📊 Saídas Esperadas

| Script | Descrição da Visualização |
|--------|---------------------------|
| `Exemplo_plot3D_momentoInercia.py` | Dois subplots 3D: esfera (azul) e elipsoide (vermelho) com eixos principais |
| `Exemplo_plot2D_momentoInercia.py` | Gráfico 2D comparando círculo (linha tracejada) e elipse (linha sólida) |
| `Example_plot3D_malhas_refinamentos_weights.py` | Malha 3D refinada + matriz de pesos colorida |

---

## 💡 Dicas de Uso
1. **Interatividade 3D**: Use os controles do Matplotlib para rotacionar/ampliar as visualizações.
2. **Customização**:
   - Modifique a matriz `I` nos exemplos de inércia para explorar diferentes deformações.
   - Ajuste `refinement_regions` no script de malhas para testar refinamentos personalizados.
3. **Debug**: Verifique a saída do console para valores numéricos das malhas refinadas.

---

## 📄 Notas Técnicas
- **Malhas 3D**: Células ativas são representadas por `1` e refinadas por valores multiplicados (ex: `4` = refinamento 2x2).
- **Inércia**: Matrizes devem ser simétricas para validade física.
- **Performance**: Reduza a resolução da malha (ex: `theta`/`phi`) para acelerar renderizações complexas.
