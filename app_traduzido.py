import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import warnings

# Suprimir warnings para saída mais limpa
warnings.filterwarnings('ignore', category=RuntimeWarning)
warnings.filterwarnings('ignore', category=UserWarning)
np.seterr(divide='ignore', invalid='ignore')

def converter_intervalos_para_string(series):
    """Converte objetos Interval para strings legíveis para uso em gráficos"""
    if hasattr(series, 'dtype') and series.dtype.name == 'category':
        # Verificar se são intervalos
        if len(series) > 0 and hasattr(series.iloc[0], 'left'):
            return series.apply(lambda x: f"{x.left:.0f}-{x.right:.0f}")
    return series

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Análise de Fatores de Risco do Câncer de Pulmão",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhor estilização
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #A23B72;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Carregar dados
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv('Dataset_Cancer_Pulmao_Traduzido.csv')
        return df
    except FileNotFoundError:
        st.error("Dataset traduzido não encontrado. Execute o script traduzir_dataset.py primeiro.")
        st.stop()

# Título principal
st.markdown('<h1 class="main-header">🫁 Dashboard de Análise de Fatores de Risco do Câncer de Pulmão</h1>', unsafe_allow_html=True)

# Carregar dados
df = carregar_dados()

# Barra lateral para navegação e filtros
st.sidebar.title("📊 Navegação e Filtros")

# Navegação de páginas
pagina = st.sidebar.selectbox(
    "Selecione uma página:",
    ["🏠 Visão Geral", "🚬 Análise de Tabagismo", "👥 Demografia", "🏥 Análise Médica", "📈 Tendências Temporais", "🔍 Análise Detalhada"]
)

# Filtros globais
st.sidebar.markdown("### 🔧 Filtros Globais")

# Filtro de idade
faixa_idade = st.sidebar.slider(
    "Faixa Etária",
    min_value=int(df['Idade'].min()),
    max_value=int(df['Idade'].max()),
    value=(int(df['Idade'].min()), int(df['Idade'].max()))
)

# Filtro de gênero
opcoes_genero = ['Todos'] + list(df['Genero'].unique())
genero_selecionado = st.sidebar.selectbox("Gênero", opcoes_genero)

# Filtro de região
opcoes_regiao = ['Todas'] + list(df['Regiao'].unique())
regiao_selecionada = st.sidebar.selectbox("Região", opcoes_regiao)

# Filtro de status de tabagismo
opcoes_tabagismo = ['Todos'] + list(df['Status_Tabagismo'].unique())
tabagismo_selecionado = st.sidebar.selectbox("Status de Tabagismo", opcoes_tabagismo)

# Aplicar filtros
df_filtrado = df[
    (df['Idade'] >= faixa_idade[0]) & 
    (df['Idade'] <= faixa_idade[1])
]

if genero_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Genero'] == genero_selecionado]

if regiao_selecionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Regiao'] == regiao_selecionada]

if tabagismo_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Status_Tabagismo'] == tabagismo_selecionado]

# Mostrar informações dos dados filtrados
st.sidebar.markdown(f"**📋 Dados filtrados:** {len(df_filtrado)} de {len(df)} registros")

# Documentação
with st.sidebar.expander("📖 Como usar este dashboard"):
    st.markdown("""
    **Objetivo:** Explorar fatores de risco associados ao câncer de pulmão.
    
    **Navegação:**
    - Use o menu acima para alternar entre seções
    - Aplique filtros para focar em grupos específicos
    
    **Filtros:**
    - Todos os gráficos são atualizados automaticamente
    - Use múltiplos filtros para análises detalhadas
    """)

# Conteúdo das páginas baseado na seleção
if pagina == "🏠 Visão Geral":
    st.markdown('<h2 class="section-header">📊 Visão Geral dos Dados</h2>', unsafe_allow_html=True)
    
    # Documentação do Dashboard
    st.markdown("### 📖 Sobre este Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 Objetivo do Dashboard**
        
        Este dashboard foi desenvolvido para explorar visualmente fatores de risco associados ao câncer de pulmão, facilitando a descoberta de padrões, tendências e relações entre diferentes variáveis que podem influenciar o desenvolvimento da doença.
        
        **📊 Dataset:** 3.000 pacientes com 24 variáveis incluindo dados demográficos, histórico de tabagismo, fatores ambientais e médicos.
        """)
    
    with col2:
        st.markdown("""
        **🧭 Como Navegar**
        
        - **Menu Lateral:** Use o seletor de páginas para navegar entre as diferentes seções de análise
        - **6 Páginas Temáticas:** Cada página foca em um aspecto específico dos dados
        - **Filtros Globais:** Aplicam-se a todas as páginas automaticamente
        - **Interatividade:** Clique, arraste e use widgets para explorar os dados
        """)
    
    with col3:
        st.markdown("""
        **🔧 Como os Filtros Funcionam**
        
        - **Atualizações Automáticas:** Todos os gráficos são atualizados em tempo real
        - **Combinação de Filtros:** Use múltiplos filtros simultaneamente para análises específicas
        - **Indicador de Dados:** Veja quantos registros estão sendo analisados após a filtragem
        - **Reset:** Ajuste os filtros a qualquer momento para explorar diferentes cenários
        """)
    
    st.markdown("---")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Pacientes", len(df_filtrado))
    
    with col2:
        taxa_cancer = (df_filtrado['Estagio_Cancer_Pulmao'] != 'Sem Câncer').mean() * 100
        st.metric("Taxa de Câncer", f"{taxa_cancer:.1f}%")
    
    with col3:
        idade_media = df_filtrado['Idade'].mean()
        st.metric("Idade Média", f"{idade_media:.1f} anos")
    
    with col4:
        pct_fumantes = (df_filtrado['Status_Tabagismo'] != 'Nunca').mean() * 100
        st.metric("% Fumantes/Ex-fumantes", f"{pct_fumantes:.1f}%")
    
    # Gráficos principais de visão geral
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por gênero
        fig_genero = px.pie(
            df_filtrado, 
            names='Genero', 
            title="Distribuição por Gênero",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        fig_genero.update_layout(height=400)
        st.plotly_chart(fig_genero, use_container_width=True)
    
    with col2:
        # Distribuição do status de tabagismo
        fig_tabagismo = px.pie(
            df_filtrado, 
            names='Status_Tabagismo', 
            title="Status de Tabagismo",
            color_discrete_sequence=['#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        )
        fig_tabagismo.update_layout(height=400)
        st.plotly_chart(fig_tabagismo, use_container_width=True)
    
    # Distribuição dos estágios de câncer
    dados_cancer = df_filtrado[df_filtrado['Estagio_Cancer_Pulmao'] != 'Sem Câncer']
    if len(dados_cancer) > 0:
        fig_estagios = px.histogram(
            dados_cancer,
            x='Estagio_Cancer_Pulmao',
            title="Distribuição dos Estágios de Câncer",
            color='Estagio_Cancer_Pulmao',
            color_discrete_sequence=['#FF9999', '#FF6666', '#FF3333', '#CC0000']
        )
        fig_estagios.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_estagios, use_container_width=True)

elif pagina == "🚬 Análise de Tabagismo":
    st.markdown('<h2 class="section-header">🚬 Análise Detalhada do Tabagismo</h2>', unsafe_allow_html=True)
    
    # Análise interativa de cigarros por dia
    st.subheader("📈 Cigarros por Dia - Análise Interativa")
    
    # Filtrar fumantes atuais
    fumantes_atuais = df_filtrado[df_filtrado['Status_Tabagismo'] == 'Atual']
    
    if len(fumantes_atuais) > 0:
        # Slider para cigarros por dia
        max_cig = int(fumantes_atuais['Cigarros_Por_Dia'].max())
        faixa_cig = st.slider(
            "Filtrar por quantidade de cigarros por dia:",
            0, max_cig, (0, max_cig),
            key="cig_slider"
        )
        
        cig_filtrado = fumantes_atuais[
            (fumantes_atuais['Cigarros_Por_Dia'] >= faixa_cig[0]) & 
            (fumantes_atuais['Cigarros_Por_Dia'] <= faixa_cig[1])
        ]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de dispersão: Cigarros vs Idade
            fig_scatter = px.scatter(
                cig_filtrado,
                x='Idade',
                y='Cigarros_Por_Dia',
                color='Genero',
                size='Anos_Fumando',
                hover_data=['IMC', 'Nivel_Renda'],
                title="Cigarros por Dia vs Idade",
                color_discrete_sequence=['#FF6B6B', '#4ECDC4']
            )
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            # Box plot: Cigarros por estágio do câncer
            fumantes_cancer = cig_filtrado[cig_filtrado['Estagio_Cancer_Pulmao'] != 'Sem Câncer']
            if len(fumantes_cancer) > 0:
                fig_box = px.box(
                    fumantes_cancer,
                    x='Estagio_Cancer_Pulmao',
                    y='Cigarros_Por_Dia',
                    title="Cigarros por Dia por Estágio do Câncer",
                    color='Estagio_Cancer_Pulmao'
                )
                fig_box.update_layout(height=400)
                st.plotly_chart(fig_box, use_container_width=True)
    
    # Análise de anos fumando
    st.subheader("⏰ Análise de Anos Fumando")
    
    dados_tabagismo = df_filtrado[df_filtrado['Anos_Fumando'] > 0]
    if len(dados_tabagismo) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Histograma de anos fumando
            fig_anos = px.histogram(
                dados_tabagismo,
                x='Anos_Fumando',
                nbins=20,
                title="Distribuição de Anos Fumando",
                color_discrete_sequence=['#74B9FF']
            )
            fig_anos.update_layout(height=400)
            st.plotly_chart(fig_anos, use_container_width=True)
        
        with col2:
            # Anos fumando vs Câncer
            fig_cancer_anos = px.violin(
                dados_tabagismo,
                x='Estagio_Cancer_Pulmao',
                y='Anos_Fumando',
                title="Anos Fumando por Estágio do Câncer",
                color='Estagio_Cancer_Pulmao'
            )
            fig_cancer_anos.update_layout(height=400)
            st.plotly_chart(fig_cancer_anos, use_container_width=True)
    
    # Análise de exposição ao fumo passivo
    st.subheader("💨 Exposição ao Fumo Passivo")
    
    # Preparar dados para sunburst - remover valores nulos
    dados_sunburst = df_filtrado[['Exposicao_Fumo_Passivo', 'Estagio_Cancer_Pulmao']].dropna()
    
    if len(dados_sunburst) > 0:
        fig_fumo_passivo = px.sunburst(
            dados_sunburst,
            path=['Exposicao_Fumo_Passivo', 'Estagio_Cancer_Pulmao'],
            title="Exposição ao Fumo Passivo vs Câncer",
            color_discrete_sequence=['#A8E6CF', '#FFD93D', '#FF6B6B', '#6C5CE7']
        )
        fig_fumo_passivo.update_layout(height=500)
        st.plotly_chart(fig_fumo_passivo, use_container_width=True)

elif pagina == "👥 Demografia":
    st.markdown('<h2 class="section-header">👥 Análise Demográfica</h2>', unsafe_allow_html=True)
    
    # Distribuição etária interativa
    st.subheader("📊 Distribuição Etária Interativa")
    
    # Seletor de tipo de agrupamento etário
    tipo_grupo_idade = st.selectbox(
        "Selecione o tipo de agrupamento etário:",
        ["Décadas", "Faixas Personalizadas", "Quartis"]
    )
    
    if tipo_grupo_idade == "Décadas":
        df_filtrado['Grupo_Idade'] = (df_filtrado['Idade'] // 10) * 10
        df_filtrado['Grupo_Idade'] = df_filtrado['Grupo_Idade'].astype(str) + 's'
        grupo_col = 'Grupo_Idade'
    elif tipo_grupo_idade == "Quartis":
        df_filtrado['Grupo_Idade'] = pd.qcut(df_filtrado['Idade'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
        grupo_col = 'Grupo_Idade'
    else:
        bins = st.slider("Número de faixas etárias:", 3, 10, 5)
        df_filtrado['Grupo_Idade'] = pd.cut(df_filtrado['Idade'], bins=bins)
        # Converter intervalos para strings para evitar erro de serialização JSON
        df_filtrado['Grupo_Idade_Str'] = converter_intervalos_para_string(df_filtrado['Grupo_Idade'])
        grupo_col = 'Grupo_Idade_Str'
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por grupo de idade
        dados_dist = df_filtrado.groupby([grupo_col, 'Genero'], observed=True).size().reset_index(name='Contagem')
        fig_dist_idade = px.bar(
            dados_dist,
            x=grupo_col,
            y='Contagem',
            color='Genero',
            title=f"Distribuição por {tipo_grupo_idade}",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        fig_dist_idade.update_layout(height=400)
        st.plotly_chart(fig_dist_idade, use_container_width=True)
    
    with col2:
        # Taxa de câncer por grupo de idade
        cancer_idade = df_filtrado.groupby(grupo_col, observed=True).agg({
            'Estagio_Cancer_Pulmao': lambda x: (x != 'Sem Câncer').mean() * 100
        }).reset_index()
        cancer_idade.columns = [grupo_col, 'Taxa_Cancer']
        
        fig_cancer_idade = px.bar(
            cancer_idade,
            x=grupo_col,
            y='Taxa_Cancer',
            title="Taxa de Câncer por Faixa Etária (%)",
            color='Taxa_Cancer',
            color_continuous_scale='Reds'
        )
        fig_cancer_idade.update_layout(height=400)
        st.plotly_chart(fig_cancer_idade, use_container_width=True)
    
    # Análise regional
    st.subheader("🗺️ Análise Regional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por região
        dados_regiao = df_filtrado.groupby('Regiao').agg({
            'ID_Paciente': 'count',
            'Estagio_Cancer_Pulmao': lambda x: (x != 'Sem Câncer').mean() * 100
        }).reset_index()
        dados_regiao.columns = ['Regiao', 'Contagem_Pacientes', 'Taxa_Cancer']
        
        fig_regiao = px.bar(
            dados_regiao,
            x='Regiao',
            y='Contagem_Pacientes',
            title="Distribuição de Pacientes por Região",
            color='Taxa_Cancer',
            color_continuous_scale='RdYlBu_r'
        )
        fig_regiao.update_layout(height=400)
        st.plotly_chart(fig_regiao, use_container_width=True)
    
    with col2:
        # Renda vs Educação - Tratamento para dados categóricos
        try:
            # Converter Nivel_Renda para numérico
            mapeamento_renda = {
                'Baixa': 1, 'Média': 2, 'Alta': 3
            }
            
            # Verificar se os dados são categóricos e mapear para numéricos
            if df_filtrado['Nivel_Renda'].dtype == 'object':
                try:
                    renda_numerica = df_filtrado['Nivel_Renda'].map(mapeamento_renda)
                    if renda_numerica.isna().all():
                        renda_numerica = pd.Categorical(df_filtrado['Nivel_Renda']).codes
                except:
                    renda_numerica = pd.Categorical(df_filtrado['Nivel_Renda']).codes
            else:
                renda_numerica = df_filtrado['Nivel_Renda']
            
            # Criar DataFrame temporário para o gráfico
            df_temp = df_filtrado.copy()
            df_temp['Nivel_Renda_Numerico'] = renda_numerica
            
            fig_renda_edu = px.box(
                df_temp,
                x='Nivel_Educacao',
                y='Nivel_Renda_Numerico',
                title="Distribuição de Renda por Nível Educacional",
                color='Nivel_Educacao'
            )
            fig_renda_edu.update_layout(height=400, xaxis_tickangle=45)
            st.plotly_chart(fig_renda_edu, use_container_width=True)
            
        except Exception as e:
            # Fallback: usar gráfico de barras se box plot falhar
            contagem_renda_edu = df_filtrado.groupby(['Nivel_Educacao', 'Nivel_Renda'], observed=True).size().reset_index(name='Contagem')
            fig_renda_edu_fallback = px.bar(
                contagem_renda_edu,
                x='Nivel_Educacao',
                y='Contagem',
                color='Nivel_Renda',
                title="Distribuição de Renda por Nível Educacional",
                barmode='group'
            )
            fig_renda_edu_fallback.update_layout(height=400, xaxis_tickangle=45)
            st.plotly_chart(fig_renda_edu_fallback, use_container_width=True)
    
    # Análise do IMC
    st.subheader("⚖️ Análise do IMC")
    
    # Categorias de IMC
    def categorizar_imc(imc):
        if imc < 18.5:
            return 'Abaixo do peso'
        elif imc < 25:
            return 'Peso normal'
        elif imc < 30:
            return 'Sobrepeso'
        else:
            return 'Obesidade'
    
    df_filtrado['Categoria_IMC'] = df_filtrado['IMC'].apply(categorizar_imc)
    
    fig_imc = px.histogram(
        df_filtrado,
        x='Categoria_IMC',
        color='Genero',
        title="Distribuição de Categorias de IMC por Gênero",
        barmode='group',
        color_discrete_sequence=['#FF6B6B', '#4ECDC4']
    )
    fig_imc.update_layout(height=400)
    st.plotly_chart(fig_imc, use_container_width=True)

elif pagina == "🏥 Análise Médica":
    st.markdown('<h2 class="section-header">🏥 Análise de Fatores Médicos</h2>', unsafe_allow_html=True)
    
    # Análise de acesso aos cuidados de saúde
    st.subheader("🏥 Acesso aos Cuidados de Saúde")
    
    # Análise interativa de cuidados de saúde
    metrica_saude = st.selectbox(
        "Selecione a métrica para análise:",
        ['Acesso_Cuidados_Saude', 'Frequencia_Exames', 'Doenca_Pulmonar_Cronica']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição da métrica de saúde
        fig_saude = px.pie(
            df_filtrado,
            names=metrica_saude,
            title=f"Distribuição: {metrica_saude.replace('_', ' ')}",
            color_discrete_sequence=['#FF9999', '#66B2FF', '#99FF99', '#FFB366']
        )
        fig_saude.update_layout(height=400)
        st.plotly_chart(fig_saude, use_container_width=True)
    
    with col2:
        # Saúde vs Câncer
        saude_cancer = df_filtrado.groupby(metrica_saude).agg({
            'Estagio_Cancer_Pulmao': lambda x: (x != 'Sem Câncer').mean() * 100
        }).reset_index()
        saude_cancer.columns = [metrica_saude, 'Taxa_Cancer']
        
        fig_sc_cancer = px.bar(
            saude_cancer,
            x=metrica_saude,
            y='Taxa_Cancer',
            title=f"Taxa de Câncer por {metrica_saude.replace('_', ' ')} (%)",
            color='Taxa_Cancer',
            color_continuous_scale='Reds'
        )
        fig_sc_cancer.update_layout(height=400, xaxis_tickangle=45)
        st.plotly_chart(fig_sc_cancer, use_container_width=True)
    
    # Correlação entre fatores de risco
    st.subheader("🔗 Correlação entre Fatores de Risco")
    
    # Selecionar fatores de risco para correlação
    fatores_risco = st.multiselect(
        "Selecione fatores de risco para análise de correlação:",
        ['Idade', 'Anos_Fumando', 'Cigarros_Por_Dia', 'IMC', 'Nivel_Poluicao_Ar'],
        default=['Idade', 'Anos_Fumando', 'IMC']
    )
    
    if len(fatores_risco) > 1:
        try:
            # Filtrar apenas colunas numéricas e tratar valores ausentes
            fatores_numericos = []
            for fator in fatores_risco:
                if fator in df_filtrado.columns:
                    if pd.api.types.is_numeric_dtype(df_filtrado[fator]):
                        fatores_numericos.append(fator)
                    else:
                        # Tentar converter categórico para numérico
                        if fator == 'Nivel_Poluicao_Ar':
                            col_temp = df_filtrado[fator].map({'Baixo': 1, 'Moderado': 2, 'Alto': 3})
                            if not col_temp.isna().all():
                                df_filtrado_temp = df_filtrado.copy()
                                df_filtrado_temp[fator] = col_temp
                                fatores_numericos.append(fator)
            
            if len(fatores_numericos) > 1:
                # Criar matriz de correlação com tratamento de erro
                dados_corr_limpos = df_filtrado[fatores_numericos].dropna()
                if len(dados_corr_limpos) > 1:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        dados_corr = dados_corr_limpos.corr()
                    
                    # Criar heatmap
                    fig_corr = px.imshow(
                        dados_corr,
                        text_auto=True,
                        aspect="auto",
                        title="Matriz de Correlação entre Fatores de Risco",
                        color_continuous_scale='RdBu'
                    )
                    fig_corr.update_layout(height=500)
                    st.plotly_chart(fig_corr, use_container_width=True)
                else:
                    st.warning("Dados insuficientes para calcular correlações após remoção de valores ausentes.")
            else:
                st.warning("Selecione pelo menos 2 fatores numéricos para análise de correlação.")
        except Exception as e:
            st.warning("Não foi possível calcular a matriz de correlação com os fatores selecionados.")
    
    # Análise de marcadores genéticos
    st.subheader("🧬 Análise de Marcadores Genéticos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Marcadores genéticos vs Histórico familiar
        fig_genetico = px.bar(
            df_filtrado.groupby(['Marcadores_Geneticos_Positivos', 'Historico_Familiar'], observed=True).size().reset_index(name='Contagem'),
            x='Marcadores_Geneticos_Positivos',
            y='Contagem',
            color='Historico_Familiar',
            title="Marcadores Genéticos vs Histórico Familiar",
            barmode='group'
        )
        fig_genetico.update_layout(height=400)
        st.plotly_chart(fig_genetico, use_container_width=True)
    
    with col2:
        # Análise de status de sobrevivência
        fig_sobrevivencia = px.bar(
            df_filtrado.groupby(['Status_Sobrevivencia', 'Marcadores_Geneticos_Positivos'], observed=True).size().reset_index(name='Contagem'),
            x='Status_Sobrevivencia',
            y='Contagem',
            color='Marcadores_Geneticos_Positivos',
            title="Status de Sobrevivência vs Marcadores Genéticos",
            barmode='group'
        )
        fig_sobrevivencia.update_layout(height=400)
        st.plotly_chart(fig_sobrevivencia, use_container_width=True)
    
    # Fatores de estilo de vida
    st.subheader("🏃‍♂️ Fatores de Estilo de Vida")
    
    dados_estilo_vida = df_filtrado.groupby(['Nivel_Atividade_Fisica', 'Qualidade_Dieta'], observed=True).agg({
        'Estagio_Cancer_Pulmao': lambda x: (x != 'Sem Câncer').mean() * 100
    }).reset_index()
    dados_estilo_vida.columns = ['Nivel_Atividade_Fisica', 'Qualidade_Dieta', 'Taxa_Cancer']
    
    fig_estilo_vida = px.scatter(
        dados_estilo_vida,
        x='Nivel_Atividade_Fisica',
        y='Qualidade_Dieta',
        size='Taxa_Cancer',
        color='Taxa_Cancer',
        title="Taxa de Câncer por Atividade Física e Qualidade da Dieta",
        color_continuous_scale='Reds',
        size_max=20
    )
    fig_estilo_vida.update_layout(height=500)
    st.plotly_chart(fig_estilo_vida, use_container_width=True)

elif pagina == "📈 Tendências Temporais":
    st.markdown('<h2 class="section-header">📈 Análise de Tendências Temporais</h2>', unsafe_allow_html=True)
    
    # Seletor de faixa de anos
    faixa_anos = st.slider(
        "Selecione o período para análise:",
        min_value=int(df_filtrado['Ano_Diagnostico'].min()),
        max_value=int(df_filtrado['Ano_Diagnostico'].max()),
        value=(int(df_filtrado['Ano_Diagnostico'].min()), int(df_filtrado['Ano_Diagnostico'].max()))
    )
    
    df_anos_filtrado = df_filtrado[
        (df_filtrado['Ano_Diagnostico'] >= faixa_anos[0]) & 
        (df_filtrado['Ano_Diagnostico'] <= faixa_anos[1])
    ]
    
    # Tendências do câncer ao longo do tempo
    st.subheader("📊 Tendências do Câncer ao Longo do Tempo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Casos de câncer por ano
        cancer_anual = df_anos_filtrado.groupby('Ano_Diagnostico').agg({
            'ID_Paciente': 'count',
            'Estagio_Cancer_Pulmao': lambda x: (x != 'Sem Câncer').sum()
        }).reset_index()
        cancer_anual.columns = ['Ano', 'Total_Casos', 'Casos_Cancer']
        cancer_anual['Taxa_Cancer'] = (cancer_anual['Casos_Cancer'] / cancer_anual['Total_Casos']) * 100
        
        fig_anual = px.line(
            cancer_anual,
            x='Ano',
            y='Casos_Cancer',
            title="Casos de Câncer por Ano",
            markers=True,
            line_shape='spline'
        )
        fig_anual.update_layout(height=400)
        st.plotly_chart(fig_anual, use_container_width=True)
    
    with col2:
        # Tendência da taxa de câncer
        fig_taxa = px.line(
            cancer_anual,
            x='Ano',
            y='Taxa_Cancer',
            title="Taxa de Câncer por Ano (%)",
            markers=True,
            line_shape='spline',
            color_discrete_sequence=['#FF6B6B']
        )
        fig_taxa.update_layout(height=400)
        st.plotly_chart(fig_taxa, use_container_width=True)
    
    # Tendências etárias ao longo do tempo
    st.subheader("👴 Tendências Etárias")
    
    # Calcular idade média por ano e status de câncer
    tendencias_idade = df_anos_filtrado.groupby(['Ano_Diagnostico', 'Estagio_Cancer_Pulmao'], observed=True)['Idade'].mean().reset_index()
    
    fig_tendencias_idade = px.line(
        tendencias_idade,
        x='Ano_Diagnostico',
        y='Idade',
        color='Estagio_Cancer_Pulmao',
        title="Idade Média por Ano e Estágio do Câncer",
        markers=True
    )
    fig_tendencias_idade.update_layout(height=400)
    st.plotly_chart(fig_tendencias_idade, use_container_width=True)
    
    # Tendências do tabagismo
    st.subheader("🚬 Tendências do Tabagismo")
    
    tendencias_tabagismo = df_anos_filtrado.groupby(['Ano_Diagnostico', 'Status_Tabagismo'], observed=True).size().reset_index(name='Contagem')
    tendencias_tabagismo['Porcentagem'] = tendencias_tabagismo.groupby('Ano_Diagnostico')['Contagem'].transform(lambda x: x / x.sum() * 100)
    
    fig_tendencias_tabagismo = px.area(
        tendencias_tabagismo,
        x='Ano_Diagnostico',
        y='Porcentagem',
        color='Status_Tabagismo',
        title="Tendências do Status de Tabagismo ao Longo do Tempo (%)",
        color_discrete_sequence=['#74B9FF', '#A29BFE', '#FD79A8', '#FDCB6E']
    )
    fig_tendencias_tabagismo.update_layout(height=400)
    st.plotly_chart(fig_tendencias_tabagismo, use_container_width=True)
    
    # Análise de sobrevivência ao longo do tempo
    st.subheader("💚 Análise de Sobrevivência")
    
    tendencias_sobrevivencia = df_anos_filtrado.groupby('Ano_Diagnostico').agg({
        'Status_Sobrevivencia': lambda x: (x == 'Vivo').mean() * 100
    }).reset_index()
    tendencias_sobrevivencia.columns = ['Ano', 'Taxa_Sobrevivencia']
    
    fig_tendencia_sobrevivencia = px.bar(
        tendencias_sobrevivencia,
        x='Ano',
        y='Taxa_Sobrevivencia',
        title="Taxa de Sobrevivência por Ano de Diagnóstico (%)",
        color='Taxa_Sobrevivencia',
        color_continuous_scale='RdYlGn'
    )
    fig_tendencia_sobrevivencia.update_layout(height=400)
    st.plotly_chart(fig_tendencia_sobrevivencia, use_container_width=True)

elif pagina == "🔍 Análise Detalhada":
    st.markdown('<h2 class="section-header">🔍 Análise Detalhada e Comparativa</h2>', unsafe_allow_html=True)
    
    # Seção de filtros avançados
    st.subheader("⚙️ Filtros Avançados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        faixa_imc = st.slider(
            "Faixa de IMC:",
            float(df_filtrado['IMC'].min()),
            float(df_filtrado['IMC'].max()),
            (float(df_filtrado['IMC'].min()), float(df_filtrado['IMC'].max()))
        )
    
    with col2:
        niveis_renda = st.multiselect(
            "Níveis de Renda:",
            options=df_filtrado['Nivel_Renda'].unique(),
            default=df_filtrado['Nivel_Renda'].unique()
        )
    
    with col3:
        niveis_educacao = st.multiselect(
            "Níveis de Educação:",
            options=df_filtrado['Nivel_Educacao'].unique(),
            default=df_filtrado['Nivel_Educacao'].unique()
        )
    
    # Aplicar filtros avançados
    df_avancado = df_filtrado[
        (df_filtrado['IMC'] >= faixa_imc[0]) & 
        (df_filtrado['IMC'] <= faixa_imc[1]) &
        (df_filtrado['Nivel_Renda'].isin(niveis_renda)) &
        (df_filtrado['Nivel_Educacao'].isin(niveis_educacao))
    ]
    
    st.info(f"Registros após filtros avançados: {len(df_avancado)}")
    
    # Análise multidimensional
    st.subheader("📊 Análise Multidimensional")
    
    # Gráfico de dispersão 3D
    if len(df_avancado) > 0:
        fig_3d = px.scatter_3d(
            df_avancado,
            x='Idade',
            y='IMC',
            z='Anos_Fumando',
            color='Estagio_Cancer_Pulmao',
            size='Cigarros_Por_Dia',
            hover_data=['Genero', 'Regiao'],
            title="Análise 3D: Idade vs IMC vs Anos Fumando",
            color_discrete_sequence=['#74B9FF', '#A29BFE', '#FD79A8', '#FDCB6E', '#00B894']
        )
        fig_3d.update_layout(height=600)
        st.plotly_chart(fig_3d, use_container_width=True)
    
    # Análise comparativa
    st.subheader("⚖️ Análise Comparativa")
    
    # Comparar dois grupos
    col1, col2 = st.columns(2)
    
    with col1:
        comparar_por = st.selectbox(
            "Comparar por:",
            ['Genero', 'Status_Tabagismo', 'Regiao', 'Nivel_Renda', 'Nivel_Educacao']
        )
    
    with col2:
        metrica_comparar = st.selectbox(
            "Métrica para comparação:",
            ['Idade', 'IMC', 'Anos_Fumando', 'Cigarros_Por_Dia', 'Nivel_Poluicao_Ar']
        )
    
    if comparar_por and metrica_comparar:
        # Criar violin plot de comparação
        fig_comparar = px.violin(
            df_avancado,
            x=comparar_por,
            y=metrica_comparar,
            box=True,
            title=f"Comparação de {metrica_comparar.replace('_', ' ')} por {comparar_por.replace('_', ' ')}",
            color=comparar_por
        )
        fig_comparar.update_layout(height=400, xaxis_tickangle=45)
        st.plotly_chart(fig_comparar, use_container_width=True)
    
    # Ranking de fatores de risco
    st.subheader("🏆 Ranking de Fatores de Risco")
    
    # Calcular correlação com ocorrência de câncer
    cancer_binario = (df_avancado['Estagio_Cancer_Pulmao'] != 'Sem Câncer').astype(int)
    
    # Começar com colunas numéricas básicas
    colunas_numericas_basicas = []
    for col in ['Idade', 'Anos_Fumando', 'Cigarros_Por_Dia', 'IMC']:
        if col in df_avancado.columns and pd.api.types.is_numeric_dtype(df_avancado[col]):
            colunas_numericas_basicas.append(col)
    
    # Tratar colunas categóricas que deveriam ser numéricas
    mapeamentos_categoricos = {
        'Nivel_Poluicao_Ar': {'Baixo': 1, 'Moderado': 2, 'Alto': 3},
        'Nivel_Atividade_Fisica': {'Baixo': 1, 'Moderado': 2, 'Alto': 3},
        'Qualidade_Dieta': {'Ruim': 1, 'Média': 2, 'Boa': 3}
    }
    
    # Criar DataFrame de trabalho para correlações
    df_trabalho_corr = df_avancado[colunas_numericas_basicas].copy()
    
    # Adicionar colunas categóricas convertidas
    for col, mapeamento in mapeamentos_categoricos.items():
        if col in df_avancado.columns:
            try:
                col_convertida = df_avancado[col].map(mapeamento)
                if not col_convertida.isna().all():
                    df_trabalho_corr[col] = col_convertida
            except Exception:
                continue
    
    # Calcular correlações com tratamento robusto de erro
    correlacoes = []
    for col in df_trabalho_corr.columns:
        try:
            # Verificar se a coluna tem dados válidos suficientes
            dados_col_validos = df_trabalho_corr[col].dropna()
            if len(dados_col_validos) < 2:
                continue
                
            # Verificar se a coluna tem variância (não todos os mesmos valores)
            if dados_col_validos.nunique() < 2:
                continue
                
            # Criar dataset válido para correlação
            dados_col = df_trabalho_corr[col].reset_index(drop=True)
            dados_cancer = pd.Series(cancer_binario).reset_index(drop=True)
            
            # Garantir mesmo comprimento
            comprimento_min = min(len(dados_col), len(dados_cancer))
            dados_col = dados_col[:comprimento_min]
            dados_cancer = dados_cancer[:comprimento_min]
            
            # Remover valores NaN
            indices_validos = pd.notna(dados_col) & pd.notna(dados_cancer)
            col_limpa = dados_col[indices_validos]
            cancer_limpo = dados_cancer[indices_validos]
            
            # Verificações finais antes da correlação
            if len(col_limpa) > 1 and col_limpa.nunique() > 1 and cancer_limpo.nunique() > 1:
                # Suprimir warnings para este cálculo específico
                with pd.option_context('mode.use_inf_as_na', True):
                    corr = col_limpa.corr(cancer_limpo)
                    
                if pd.notna(corr) and abs(corr) > 1e-10:  # Evitar correlações muito pequenas
                    nome_fator = col.replace('_', ' ')
                    correlacoes.append({'Fator': nome_fator, 'Correlacao': abs(corr)})
                    
        except (ValueError, ZeroDivisionError, RuntimeWarning):
            continue
        except Exception:
            continue
    
    if correlacoes:
        df_resultado_corr = pd.DataFrame(correlacoes).sort_values('Correlacao', ascending=True)
        
        fig_ranking = px.bar(
            df_resultado_corr,
            x='Correlacao',
            y='Fator',
            orientation='h',
            title="Ranking de Correlação com Câncer (Valor Absoluto)",
            color='Correlacao',
            color_continuous_scale='Reds'
        )
        fig_ranking.update_layout(height=400)
        st.plotly_chart(fig_ranking, use_container_width=True)
    else:
        st.warning("Não foi possível calcular correlações com os dados filtrados atuais.")
    
    # Estatísticas resumo
    st.subheader("📋 Estatísticas Resumo")
    
    if len(df_avancado) > 0:
        # Usar apenas colunas numéricas básicas que existem no DataFrame original
        colunas_numericas_basicas = []
        for col in ['Idade', 'Anos_Fumando', 'Cigarros_Por_Dia', 'IMC']:
            if col in df_avancado.columns and pd.api.types.is_numeric_dtype(df_avancado[col]):
                colunas_numericas_basicas.append(col)
        
        if colunas_numericas_basicas:
            stats_resumo = df_avancado[colunas_numericas_basicas].describe()
            st.dataframe(stats_resumo.round(2))
        else:
            st.warning("Nenhuma coluna numérica disponível para estatísticas resumo.")
        
        # Estatísticas de câncer por grupo
        if comparar_por in df_avancado.columns:
            try:
                cancer_por_grupo = df_avancado.groupby(comparar_por).agg({
                    'Estagio_Cancer_Pulmao': lambda x: (x != 'Sem Câncer').mean() * 100,
                    'Idade': 'mean',
                    'IMC': 'mean'
                }).round(2)
                cancer_por_grupo.columns = ['Taxa de Câncer (%)', 'Idade Média', 'IMC Médio']
                st.dataframe(cancer_por_grupo)
            except Exception as e:
                st.warning(f"Não foi possível calcular estatísticas por grupo: {str(e)}")

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    📊 Dashboard desenvolvido com Streamlit para análise de fatores de risco do câncer de pulmão<br>
    📋 Dados: Dataset de Fatores de Risco de Tabagismo e Câncer de Pulmão (traduzido)<br>
    🔄 Os gráficos são atualizados automaticamente conforme os filtros aplicados<br>
    🇧🇷 Versão Totalmente em Português
</div>
""", unsafe_allow_html=True)
