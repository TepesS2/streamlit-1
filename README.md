# 🫁 Dashboard de Análise de Fatores de Risco do Câncer de Pulmão

## 📊 Sobre o Projeto

Este dashboard interativo foi desenvolvido com Streamlit para explorar visualmente um conjunto de dados sobre fatores de risco associados ao câncer de pulmão. O objetivo é facilitar a descoberta de padrões, tendências e relações entre diferentes variáveis que podem influenciar o desenvolvimento da doença.

## 🗂️ Dataset

O projeto utiliza o dataset "Smoking and Other Risk Factors Dataset" do Kaggle, que contém:
- **3.000 registros** de pacientes
- **24 variáveis** incluindo dados demográficos, histórico de tabagismo, fatores ambientais e médicos
- Informações sobre diagnóstico, estágios do câncer e status de sobrevivência

### Principais variáveis:
- Dados demográficos (idade, gênero, região, renda, educação)
- Histórico de tabagismo (status, anos fumando, cigarros por dia)
- Fatores ambientais (poluição do ar, exposição ocupacional)
- Fatores médicos (IMC, atividade física, histórico familiar, marcadores genéticos)
- Dados clínicos (estágio do câncer, ano do diagnóstico, status de sobrevivência)

## 🚀 Funcionalidades

### 📱 Páginas Interativas

1. **🏠 Visão Geral**
   - Métricas principais do dataset
   - Distribuições básicas por gênero e status de tabagismo
   - Visão geral dos estágios do câncer

2. **🚬 Análise de Tabagismo**
   - Análise interativa de cigarros por dia
   - Relação entre anos fumando e câncer
   - Exposição ao fumo passivo

3. **👥 Demografia**
   - Distribuição etária com agrupamentos personalizáveis
   - Análise regional e socioeconômica
   - Análise de IMC por categorias

4. **🏥 Análise Médica**
   - Acesso aos cuidados de saúde
   - Correlação entre fatores de risco
   - Análise de marcadores genéticos e estilo de vida

5. **📈 Tendências Temporais**
   - Evolução dos casos de câncer ao longo do tempo
   - Tendências etárias e de tabagismo
   - Análise de sobrevivência temporal

6. **🔍 Análise Detalhada**
   - Filtros avançados multidimensionais
   - Gráfico 3D interativo
   - Ranking de fatores de risco

### 🎛️ Filtros Globais

- **Faixa Etária**: Slider para selecionar idade mínima e máxima
- **Gênero**: Filtro por masculino, feminino ou todos
- **Região**: Seleção de regiões específicas
- **Status de Tabagismo**: Filtro por nunca fumou, fumante atual, ex-fumante

### 📊 Gráficos Interativos

O dashboard inclui mais de **15 visualizações**, sendo **8 interativas**:

1. **Plotly Interactive**:
   - Scatter plot 3D (Idade vs IMC vs Anos Fumando)
   - Scatter plot com filtros dinâmicos (Cigarros vs Idade)
   - Sunburst chart (Exposição ao fumo passivo)
   - Violin plots comparativos
   - Box plots interativos
   - Heatmap de correlação

2. **Widgets Interativos**:
   - Sliders para faixas etárias e quantidade de cigarros
   - Dropdown para seleção de métricas
   - Multiselect para filtros avançados
   - Selectbox para tipos de agrupamento

## 🛠️ Instalação e Execução

### Pré-requisitos
- Python 3.7+
- Conta no Kaggle (para download do dataset)

### Passo a passo:

1. **Clone ou baixe os arquivos**:
   ```bash
   # Arquivos necessários:
   # - app.py
   # - download_dataset.py
   # - requirements.txt
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o Kaggle** (primeira execução):
   ```bash
   # Instale kagglehub se não estiver instalado
   pip install kagglehub
   
   # O sistema solicitará login no Kaggle na primeira execução
   ```

4. **Baixe o dataset**:
   ```bash
   python download_dataset.py
   ```

5. **Execute o dashboard**:
   ```bash
   streamlit run app.py
   ```

6. **Acesse no navegador**:
   - URL: `http://localhost:8501`

## ☁️ Deploy na Nuvem Streamlit

### Preparação para deploy:

1. **Crie um repositório no GitHub** com os arquivos:
   - `app.py`
   - `requirements.txt`
   - `Lung_Cancer_Trends_Realistic.csv` (após download)
   - `README.md`

2. **Acesse [share.streamlit.io](https://share.streamlit.io)**

3. **Conecte seu repositório GitHub**

4. **Configure o deploy**:
   - Repository: seu-usuario/nome-do-repo
   - Branch: main
   - Main file path: app.py

5. **Deploy automático**: O Streamlit Cloud irá instalar as dependências e executar o app automaticamente

### Configurações importantes para a nuvem:

- O arquivo `requirements.txt` já está otimizado para o Streamlit Cloud
- O dataset será carregado automaticamente do arquivo CSV
- Todas as dependências estão fixadas em versões compatíveis

## 📖 Como Usar o Dashboard

### Navegação:
1. Use o menu lateral esquerdo para navegar entre as páginas
2. Aplique filtros globais para focar em grupos específicos de dados
3. Os gráficos são atualizados automaticamente conforme os filtros

### Filtros:
- **Globais**: Aplicam-se a todas as páginas
- **Locais**: Específicos de cada seção
- **Interativos**: Use sliders e dropdowns para explorar os dados

### Interpretação:
- Gráficos vermelhos geralmente indicam maior risco ou incidência de câncer
- Use hover nos gráficos para ver detalhes adicionais
- Compare diferentes grupos usando os filtros

## 📊 Principais Insights Exploráveis

1. **Correlação Tabagismo-Câncer**: Relação entre anos fumando, quantidade de cigarros e desenvolvimento do câncer
2. **Fatores Demográficos**: Como idade, gênero e região influenciam os riscos
3. **Impacto Socioeconômico**: Relação entre renda, educação e acesso à saúde
4. **Tendências Temporais**: Evolução dos casos e mudanças nos padrões ao longo do tempo
5. **Fatores de Proteção**: Identificação de fatores que podem reduzir o risco

## 🎯 Tecnologias Utilizadas

- **Streamlit**: Framework principal para o dashboard
- **Plotly**: Gráficos interativos avançados
- **Pandas**: Manipulação e análise de dados
- **Seaborn/Matplotlib**: Visualizações complementares
- **NumPy**: Operações numéricas
- **KaggleHub**: Download automático do dataset

## 📝 Estrutura do Código

```
├── app.py                 # Aplicação principal do Streamlit
├── download_dataset.py    # Script para download do dataset
├── requirements.txt       # Dependências do projeto
├── README.md             # Documentação
└── Lung_Cancer_Trends_Realistic.csv  # Dataset (após download)
```

## 🤝 Contribuições

Sinta-se à vontade para:
- Sugerir melhorias nas visualizações
- Adicionar novas análises
- Otimizar o código
- Reportar bugs ou problemas

## 📄 Licença

Este projeto é livre para uso educacional e acadêmico.

---

**Desenvolvido com ❤️ usando Streamlit**
