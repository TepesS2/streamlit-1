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

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=RuntimeWarning)
warnings.filterwarnings('ignore', category=UserWarning)
np.seterr(divide='ignore', invalid='ignore')

# Page configuration
st.set_page_config(
    page_title="Dashboard de Análise de Fatores de Risco do Câncer de Pulmão",
    page_icon="🚭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Lung_Cancer_Trends_Realistic.csv')
        return df
    except FileNotFoundError:
        st.error("Dataset não encontrado. Execute o script download_dataset.py primeiro.")
        st.stop()

# Main title
st.markdown('<h1 class="main-header">🫁 Dashboard de Análise de Fatores de Risco do Câncer de Pulmão</h1>', unsafe_allow_html=True)

# Load data
df = load_data()

# Sidebar for navigation and filters
st.sidebar.title("📊 Navegação e Filtros")

# Page navigation
page = st.sidebar.selectbox(
    "Selecione uma página:",
    ["🏠 Visão Geral", "🚬 Análise de Tabagismo", "👥 Demografia", "🏥 Análise Médica", "📈 Tendências Temporais", "🔍 Análise Detalhada"]
)

# Global filters
st.sidebar.markdown("### 🔧 Filtros Globais")

# Age filter
age_range = st.sidebar.slider(
    "Faixa Etária",
    min_value=int(df['Age'].min()),
    max_value=int(df['Age'].max()),
    value=(int(df['Age'].min()), int(df['Age'].max()))
)

# Gender filter
gender_options = ['Todos'] + list(df['Gender'].unique())
selected_gender = st.sidebar.selectbox("Gênero", gender_options)

# Region filter
region_options = ['Todas'] + list(df['Region'].unique())
selected_region = st.sidebar.selectbox("Região", region_options)

# Smoking status filter
smoking_options = ['Todos'] + list(df['Smoking_Status'].unique())
selected_smoking = st.sidebar.selectbox("Status de Tabagismo", smoking_options)

# Apply filters
filtered_df = df[
    (df['Age'] >= age_range[0]) & 
    (df['Age'] <= age_range[1])
]

if selected_gender != 'Todos':
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

if selected_region != 'Todas':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

if selected_smoking != 'Todos':
    filtered_df = filtered_df[filtered_df['Smoking_Status'] == selected_smoking]

# Show filtered data info
st.sidebar.markdown(f"**📋 Dados filtrados:** {len(filtered_df)} de {len(df)} registros")

# Documentation
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

# Page content based on selection
if page == "🏠 Visão Geral":
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
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Pacientes", len(filtered_df))
    
    with col2:
        cancer_rate = (filtered_df['Lung_Cancer_Stage'] != 'No Cancer').mean() * 100
        st.metric("Taxa de Câncer", f"{cancer_rate:.1f}%")
    
    with col3:
        avg_age = filtered_df['Age'].mean()
        st.metric("Idade Média", f"{avg_age:.1f} anos")
    
    with col4:
        smokers_pct = (filtered_df['Smoking_Status'] != 'Never').mean() * 100
        st.metric("% Fumantes/Ex-fumantes", f"{smokers_pct:.1f}%")
    
    # Main overview charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender distribution
        fig_gender = px.pie(
            filtered_df, 
            names='Gender', 
            title="Distribuição por Gênero",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        fig_gender.update_layout(height=400)
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # Smoking status distribution
        fig_smoking = px.pie(
            filtered_df, 
            names='Smoking_Status', 
            title="Status de Tabagismo",
            color_discrete_sequence=['#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        )
        fig_smoking.update_layout(height=400)
        st.plotly_chart(fig_smoking, use_container_width=True)
    
    # Cancer stages distribution
    cancer_data = filtered_df[filtered_df['Lung_Cancer_Stage'] != 'No Cancer']
    if len(cancer_data) > 0:
        fig_stages = px.histogram(
            cancer_data,
            x='Lung_Cancer_Stage',
            title="Distribuição dos Estágios de Câncer",
            color='Lung_Cancer_Stage',
            color_discrete_sequence=['#FF9999', '#FF6666', '#FF3333', '#CC0000']
        )
        fig_stages.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_stages, use_container_width=True)

elif page == "🚬 Análise de Tabagismo":
    st.markdown('<h2 class="section-header">🚬 Análise Detalhada do Tabagismo</h2>', unsafe_allow_html=True)
    
    # Interactive cigarettes per day analysis
    st.subheader("📈 Cigarros por Dia - Análise Interativa")
    
    # Filter for current smokers
    current_smokers = filtered_df[filtered_df['Smoking_Status'] == 'Current']
    
    if len(current_smokers) > 0:
        # Slider for cigarettes per day
        max_cig = int(current_smokers['Cigarettes_Per_Day'].max())
        cig_range = st.slider(
            "Filtrar por quantidade de cigarros por dia:",
            0, max_cig, (0, max_cig),
            key="cig_slider"
        )
        
        cig_filtered = current_smokers[
            (current_smokers['Cigarettes_Per_Day'] >= cig_range[0]) & 
            (current_smokers['Cigarettes_Per_Day'] <= cig_range[1])
        ]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot: Cigarettes vs Age
            fig_scatter = px.scatter(
                cig_filtered,
                x='Age',
                y='Cigarettes_Per_Day',
                color='Gender',
                size='Years_Smoking',
                hover_data=['BMI', 'Income_Level'],
                title="Cigarros por Dia vs Idade",
                color_discrete_sequence=['#FF6B6B', '#4ECDC4']
            )
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            # Box plot: Cigarettes by cancer stage
            cancer_smokers = cig_filtered[cig_filtered['Lung_Cancer_Stage'] != 'No Cancer']
            if len(cancer_smokers) > 0:
                fig_box = px.box(
                    cancer_smokers,
                    x='Lung_Cancer_Stage',
                    y='Cigarettes_Per_Day',
                    title="Cigarros por Dia por Estágio do Câncer",
                    color='Lung_Cancer_Stage'
                )
                fig_box.update_layout(height=400)
                st.plotly_chart(fig_box, use_container_width=True)
    
    # Years smoking analysis
    st.subheader("⏰ Análise de Anos Fumando")
    
    smoking_data = filtered_df[filtered_df['Years_Smoking'] > 0]
    if len(smoking_data) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram of years smoking
            fig_years = px.histogram(
                smoking_data,
                x='Years_Smoking',
                nbins=20,
                title="Distribuição de Anos Fumando",
                color_discrete_sequence=['#74B9FF']
            )
            fig_years.update_layout(height=400)
            st.plotly_chart(fig_years, use_container_width=True)
        
        with col2:
            # Years smoking vs Cancer
            fig_cancer_years = px.violin(
                smoking_data,
                x='Lung_Cancer_Stage',
                y='Years_Smoking',
                title="Anos Fumando por Estágio do Câncer",
                color='Lung_Cancer_Stage'
            )
            fig_cancer_years.update_layout(height=400)
            st.plotly_chart(fig_cancer_years, use_container_width=True)
    
    # Secondhand smoke analysis
    st.subheader("💨 Exposição ao Fumo Passivo")
    
    # Prepare data for sunburst chart
    try:
        # Create a clean dataframe for sunburst
        sunburst_data = filtered_df[['Secondhand_Smoke_Exposure', 'Lung_Cancer_Stage']].dropna()
        
        # Group and count for better hierarchy
        sunburst_counts = sunburst_data.groupby(['Secondhand_Smoke_Exposure', 'Lung_Cancer_Stage']).size().reset_index(name='Count')
        
        if len(sunburst_counts) > 0:
            fig_secondhand = px.sunburst(
                sunburst_counts,
                path=['Secondhand_Smoke_Exposure', 'Lung_Cancer_Stage'],
                values='Count',
                title="Exposição ao Fumo Passivo vs Câncer",
                color='Count',
                color_continuous_scale='Blues'
            )
            fig_secondhand.update_layout(height=500)
            st.plotly_chart(fig_secondhand, use_container_width=True)
        else:
            # Fallback: use bar chart if sunburst fails
            fallback_data = filtered_df.groupby(['Secondhand_Smoke_Exposure', 'Lung_Cancer_Stage']).size().reset_index(name='Count')
            fig_fallback = px.bar(
                fallback_data,
                x='Secondhand_Smoke_Exposure',
                y='Count',
                color='Lung_Cancer_Stage',
                title="Exposição ao Fumo Passivo vs Câncer",
                barmode='stack'
            )
            fig_fallback.update_layout(height=500)
            st.plotly_chart(fig_fallback, use_container_width=True)
    
    except Exception as e:
        # Ultimate fallback: simple bar chart
        try:
            simple_data = filtered_df['Secondhand_Smoke_Exposure'].value_counts().reset_index()
            simple_data.columns = ['Exposição', 'Contagem']
            fig_simple = px.bar(
                simple_data,
                x='Exposição',
                y='Contagem',
                title="Distribuição de Exposição ao Fumo Passivo",
                color='Contagem',
                color_continuous_scale='Blues'
            )
            fig_simple.update_layout(height=500)
            st.plotly_chart(fig_simple, use_container_width=True)
        except:
            st.warning("Não foi possível gerar o gráfico de exposição ao fumo passivo.")

elif page == "👥 Demografia":
    st.markdown('<h2 class="section-header">👥 Análise Demográfica</h2>', unsafe_allow_html=True)
    
    # Age distribution interactive
    st.subheader("📊 Distribuição Etária Interativa")
    
    # Age group selector
    age_group_type = st.selectbox(
        "Selecione o tipo de agrupamento etário:",
        ["Décadas", "Faixas Personalizadas", "Quartis"]
    )
    
    if age_group_type == "Décadas":
        filtered_df['Age_Group'] = (filtered_df['Age'] // 10) * 10
        filtered_df['Age_Group'] = filtered_df['Age_Group'].astype(str) + 's'
    elif age_group_type == "Quartis":
        filtered_df['Age_Group'] = pd.qcut(filtered_df['Age'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    else:
        bins = st.slider("Número de faixas etárias:", 3, 10, 5)
        filtered_df['Age_Group'] = pd.cut(filtered_df['Age'], bins=bins)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age group distribution
        fig_age_dist = px.bar(
            filtered_df.groupby(['Age_Group', 'Gender']).size().reset_index(name='Count'),
            x='Age_Group',
            y='Count',
            color='Gender',
            title=f"Distribuição por {age_group_type}",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        fig_age_dist.update_layout(height=400)
        st.plotly_chart(fig_age_dist, use_container_width=True)
    
    with col2:
        # Cancer rate by age group
        age_cancer = filtered_df.groupby('Age_Group').agg({
            'Lung_Cancer_Stage': lambda x: (x != 'No Cancer').mean() * 100
        }).reset_index()
        age_cancer.columns = ['Age_Group', 'Cancer_Rate']
        
        fig_age_cancer = px.bar(
            age_cancer,
            x='Age_Group',
            y='Cancer_Rate',
            title="Taxa de Câncer por Faixa Etária (%)",
            color='Cancer_Rate',
            color_continuous_scale='Reds'
        )
        fig_age_cancer.update_layout(height=400)
        st.plotly_chart(fig_age_cancer, use_container_width=True)
    
    # Regional analysis
    st.subheader("🗺️ Análise Regional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Region distribution
        region_data = filtered_df.groupby('Region').agg({
            'Patient_ID': 'count',
            'Lung_Cancer_Stage': lambda x: (x != 'No Cancer').mean() * 100
        }).reset_index()
        region_data.columns = ['Region', 'Patient_Count', 'Cancer_Rate']
        
        fig_region = px.bar(
            region_data,
            x='Region',
            y='Patient_Count',
            title="Distribuição de Pacientes por Região",
            color='Cancer_Rate',
            color_continuous_scale='RdYlBu_r'
        )
        fig_region.update_layout(height=400)
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col2:
        # Income vs Education - Tratamento para dados categóricos
        try:
            # Converter Income_Level para numérico se possível
            income_mapping = {
                'Low': 1, 'Middle': 2, 'High': 3,
                'Baixa': 1, 'Média': 2, 'Alta': 3
            }
            
            # Verificar se os dados são categóricos e mapear para numéricos
            if filtered_df['Income_Level'].dtype == 'object':
                # Tentar usar mapeamento, se não funcionar, usar códigos categóricos
                try:
                    income_numeric = filtered_df['Income_Level'].map(income_mapping)
                    if income_numeric.isna().all():
                        income_numeric = pd.Categorical(filtered_df['Income_Level']).codes
                except:
                    income_numeric = pd.Categorical(filtered_df['Income_Level']).codes
            else:
                income_numeric = filtered_df['Income_Level']
            
            # Criar DataFrame temporário para o gráfico
            temp_df = filtered_df.copy()
            temp_df['Income_Level_Numeric'] = income_numeric
            
            fig_income_edu = px.box(
                temp_df,
                x='Education_Level',
                y='Income_Level_Numeric',
                title="Distribuição de Renda por Nível Educacional",
                color='Education_Level'
            )
            fig_income_edu.update_layout(height=400, xaxis_tickangle=45)
            st.plotly_chart(fig_income_edu, use_container_width=True)
            
        except Exception as e:
            # Fallback: usar gráfico de barras se box plot falhar
            income_edu_count = filtered_df.groupby(['Education_Level', 'Income_Level']).size().reset_index(name='Count')
            fig_income_edu_fallback = px.bar(
                income_edu_count,
                x='Education_Level',
                y='Count',
                color='Income_Level',
                title="Distribuição de Renda por Nível Educacional",
                barmode='group'
            )
            fig_income_edu_fallback.update_layout(height=400, xaxis_tickangle=45)
            st.plotly_chart(fig_income_edu_fallback, use_container_width=True)
    
    # BMI analysis
    st.subheader("⚖️ Análise do IMC")
    
    # BMI categories
    def categorize_bmi(bmi):
        if bmi < 18.5:
            return 'Abaixo do peso'
        elif bmi < 25:
            return 'Peso normal'
        elif bmi < 30:
            return 'Sobrepeso'
        else:
            return 'Obesidade'
    
    filtered_df['BMI_Category'] = filtered_df['BMI'].apply(categorize_bmi)
    
    fig_bmi = px.histogram(
        filtered_df,
        x='BMI_Category',
        color='Gender',
        title="Distribuição de Categorias de IMC por Gênero",
        barmode='group',
        color_discrete_sequence=['#FF6B6B', '#4ECDC4']
    )
    fig_bmi.update_layout(height=400)
    st.plotly_chart(fig_bmi, use_container_width=True)

elif page == "🏥 Análise Médica":
    st.markdown('<h2 class="section-header">🏥 Análise de Fatores Médicos</h2>', unsafe_allow_html=True)
    
    # Healthcare access analysis
    st.subheader("🏥 Acesso aos Cuidados de Saúde")
    
    # Interactive healthcare analysis
    healthcare_metric = st.selectbox(
        "Selecione a métrica para análise:",
        ['Access_to_Healthcare', 'Screening_Frequency', 'Chronic_Lung_Disease']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Healthcare metric distribution
        fig_healthcare = px.pie(
            filtered_df,
            names=healthcare_metric,
            title=f"Distribuição: {healthcare_metric.replace('_', ' ')}",
            color_discrete_sequence=['#FF9999', '#66B2FF', '#99FF99', '#FFB366']
        )
        fig_healthcare.update_layout(height=400)
        st.plotly_chart(fig_healthcare, use_container_width=True)
    
    with col2:
        # Healthcare vs Cancer
        healthcare_cancer = filtered_df.groupby(healthcare_metric).agg({
            'Lung_Cancer_Stage': lambda x: (x != 'No Cancer').mean() * 100
        }).reset_index()
        healthcare_cancer.columns = [healthcare_metric, 'Cancer_Rate']
        
        fig_hc_cancer = px.bar(
            healthcare_cancer,
            x=healthcare_metric,
            y='Cancer_Rate',
            title=f"Taxa de Câncer por {healthcare_metric.replace('_', ' ')} (%)",
            color='Cancer_Rate',
            color_continuous_scale='Reds'
        )
        fig_hc_cancer.update_layout(height=400, xaxis_tickangle=45)
        st.plotly_chart(fig_hc_cancer, use_container_width=True)
    
    # Risk factors correlation
    st.subheader("🔗 Correlação entre Fatores de Risco")
    
    # Select risk factors for correlation
    risk_factors = st.multiselect(
        "Selecione fatores de risco para análise de correlação:",
        ['Age', 'Years_Smoking', 'Cigarettes_Per_Day', 'BMI', 'Air_Pollution_Level'],
        default=['Age', 'Years_Smoking', 'BMI']
    )
    
    if len(risk_factors) > 1:
        try:
            # Filter only numeric columns and handle missing values
            numeric_risk_factors = []
            for factor in risk_factors:
                if factor in filtered_df.columns:
                    if pd.api.types.is_numeric_dtype(filtered_df[factor]):
                        numeric_risk_factors.append(factor)
                    else:
                        # Try to convert categorical to numeric
                        if factor == 'Air_Pollution_Level':
                            temp_col = filtered_df[factor].map({'Low': 1, 'Moderate': 2, 'Medium': 2, 'High': 3})
                            if not temp_col.isna().all():
                                filtered_df_temp = filtered_df.copy()
                                filtered_df_temp[factor] = temp_col
                                numeric_risk_factors.append(factor)
            
            if len(numeric_risk_factors) > 1:
                # Create correlation matrix with error handling
                corr_data_clean = filtered_df[numeric_risk_factors].dropna()
                if len(corr_data_clean) > 1:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        corr_data = corr_data_clean.corr()
                    
                    # Create heatmap
                    fig_corr = px.imshow(
                        corr_data,
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
    
    # Genetic markers analysis
    st.subheader("🧬 Análise de Marcadores Genéticos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Genetic markers vs Family history
        fig_genetic = px.bar(
            filtered_df.groupby(['Genetic_Markers_Positive', 'Family_History']).size().reset_index(name='Count'),
            x='Genetic_Markers_Positive',
            y='Count',
            color='Family_History',
            title="Marcadores Genéticos vs Histórico Familiar",
            barmode='group'
        )
        fig_genetic.update_layout(height=400)
        st.plotly_chart(fig_genetic, use_container_width=True)
    
    with col2:
        # Survival status analysis
        fig_survival = px.bar(
            filtered_df.groupby(['Survival_Status', 'Genetic_Markers_Positive']).size().reset_index(name='Count'),
            x='Survival_Status',
            y='Count',
            color='Genetic_Markers_Positive',
            title="Status de Sobrevivência vs Marcadores Genéticos",
            barmode='group'
        )
        fig_survival.update_layout(height=400)
        st.plotly_chart(fig_survival, use_container_width=True)
    
    # Lifestyle factors
    st.subheader("🏃‍♂️ Fatores de Estilo de Vida")
    
    lifestyle_data = filtered_df.groupby(['Physical_Activity_Level', 'Diet_Quality']).agg({
        'Lung_Cancer_Stage': lambda x: (x != 'No Cancer').mean() * 100
    }).reset_index()
    lifestyle_data.columns = ['Physical_Activity_Level', 'Diet_Quality', 'Cancer_Rate']
    
    fig_lifestyle = px.scatter(
        lifestyle_data,
        x='Physical_Activity_Level',
        y='Diet_Quality',
        size='Cancer_Rate',
        color='Cancer_Rate',
        title="Taxa de Câncer por Atividade Física e Qualidade da Dieta",
        color_continuous_scale='Reds',
        size_max=20
    )
    fig_lifestyle.update_layout(height=500)
    st.plotly_chart(fig_lifestyle, use_container_width=True)

elif page == "📈 Tendências Temporais":
    st.markdown('<h2 class="section-header">📈 Análise de Tendências Temporais</h2>', unsafe_allow_html=True)
    
    # Year range selector
    year_range = st.slider(
        "Selecione o período para análise:",
        min_value=int(filtered_df['Diagnosis_Year'].min()),
        max_value=int(filtered_df['Diagnosis_Year'].max()),
        value=(int(filtered_df['Diagnosis_Year'].min()), int(filtered_df['Diagnosis_Year'].max()))
    )
    
    year_filtered_df = filtered_df[
        (filtered_df['Diagnosis_Year'] >= year_range[0]) & 
        (filtered_df['Diagnosis_Year'] <= year_range[1])
    ]
    
    # Cancer trends over time
    st.subheader("📊 Tendências do Câncer ao Longo do Tempo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cancer cases by year
        yearly_cancer = year_filtered_df.groupby('Diagnosis_Year').agg({
            'Patient_ID': 'count',
            'Lung_Cancer_Stage': lambda x: (x != 'No Cancer').sum()
        }).reset_index()
        yearly_cancer.columns = ['Year', 'Total_Cases', 'Cancer_Cases']
        yearly_cancer['Cancer_Rate'] = (yearly_cancer['Cancer_Cases'] / yearly_cancer['Total_Cases']) * 100
        
        fig_yearly = px.line(
            yearly_cancer,
            x='Year',
            y='Cancer_Cases',
            title="Casos de Câncer por Ano",
            markers=True,
            line_shape='spline'
        )
        fig_yearly.update_layout(height=400)
        st.plotly_chart(fig_yearly, use_container_width=True)
    
    with col2:
        # Cancer rate trend
        fig_rate = px.line(
            yearly_cancer,
            x='Year',
            y='Cancer_Rate',
            title="Taxa de Câncer por Ano (%)",
            markers=True,
            line_shape='spline',
            color_discrete_sequence=['#FF6B6B']
        )
        fig_rate.update_layout(height=400)
        st.plotly_chart(fig_rate, use_container_width=True)
    
    # Age trends over time
    st.subheader("👴 Tendências Etárias")
    
    # Calculate average age by year and cancer status
    age_trends = year_filtered_df.groupby(['Diagnosis_Year', 'Lung_Cancer_Stage'])['Age'].mean().reset_index()
    
    fig_age_trends = px.line(
        age_trends,
        x='Diagnosis_Year',
        y='Age',
        color='Lung_Cancer_Stage',
        title="Idade Média por Ano e Estágio do Câncer",
        markers=True
    )
    fig_age_trends.update_layout(height=400)
    st.plotly_chart(fig_age_trends, use_container_width=True)
    
    # Smoking trends
    st.subheader("🚬 Tendências do Tabagismo")
    
    smoking_trends = year_filtered_df.groupby(['Diagnosis_Year', 'Smoking_Status']).size().reset_index(name='Count')
    smoking_trends['Percentage'] = smoking_trends.groupby('Diagnosis_Year')['Count'].transform(lambda x: x / x.sum() * 100)
    
    fig_smoking_trends = px.area(
        smoking_trends,
        x='Diagnosis_Year',
        y='Percentage',
        color='Smoking_Status',
        title="Tendências do Status de Tabagismo ao Longo do Tempo (%)",
        color_discrete_sequence=['#74B9FF', '#A29BFE', '#FD79A8', '#FDCB6E']
    )
    fig_smoking_trends.update_layout(height=400)
    st.plotly_chart(fig_smoking_trends, use_container_width=True)
    
    # Survival analysis over time
    st.subheader("💚 Análise de Sobrevivência")
    
    survival_trends = year_filtered_df.groupby('Diagnosis_Year').agg({
        'Survival_Status': lambda x: (x == 'Alive').mean() * 100
    }).reset_index()
    survival_trends.columns = ['Year', 'Survival_Rate']
    
    fig_survival_trend = px.bar(
        survival_trends,
        x='Year',
        y='Survival_Rate',
        title="Taxa de Sobrevivência por Ano de Diagnóstico (%)",
        color='Survival_Rate',
        color_continuous_scale='RdYlGn'
    )
    fig_survival_trend.update_layout(height=400)
    st.plotly_chart(fig_survival_trend, use_container_width=True)

elif page == "🔍 Análise Detalhada":
    st.markdown('<h2 class="section-header">🔍 Análise Detalhada e Comparativa</h2>', unsafe_allow_html=True)
    
    # Advanced filtering section
    st.subheader("⚙️ Filtros Avançados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bmi_range = st.slider(
            "Faixa de IMC:",
            float(filtered_df['BMI'].min()),
            float(filtered_df['BMI'].max()),
            (float(filtered_df['BMI'].min()), float(filtered_df['BMI'].max()))
        )
    
    with col2:
        income_levels = st.multiselect(
            "Níveis de Renda:",
            options=filtered_df['Income_Level'].unique(),
            default=filtered_df['Income_Level'].unique()
        )
    
    with col3:
        education_levels = st.multiselect(
            "Níveis de Educação:",
            options=filtered_df['Education_Level'].unique(),
            default=filtered_df['Education_Level'].unique()
        )
    
    # Apply advanced filters
    advanced_df = filtered_df[
        (filtered_df['BMI'] >= bmi_range[0]) & 
        (filtered_df['BMI'] <= bmi_range[1]) &
        (filtered_df['Income_Level'].isin(income_levels)) &
        (filtered_df['Education_Level'].isin(education_levels))
    ]
    
    st.info(f"Registros após filtros avançados: {len(advanced_df)}")
    
    # Multi-dimensional analysis
    st.subheader("📊 Análise Multidimensional")
    
    # 3D scatter plot
    if len(advanced_df) > 0:
        fig_3d = px.scatter_3d(
            advanced_df,
            x='Age',
            y='BMI',
            z='Years_Smoking',
            color='Lung_Cancer_Stage',
            size='Cigarettes_Per_Day',
            hover_data=['Gender', 'Region'],
            title="Análise 3D: Idade vs IMC vs Anos Fumando",
            color_discrete_sequence=['#74B9FF', '#A29BFE', '#FD79A8', '#FDCB6E', '#00B894']
        )
        fig_3d.update_layout(height=600)
        st.plotly_chart(fig_3d, use_container_width=True)
    
    # Comparative analysis
    st.subheader("⚖️ Análise Comparativa")
    
    # Compare two groups
    col1, col2 = st.columns(2)
    
    with col1:
        compare_by = st.selectbox(
            "Comparar por:",
            ['Gender', 'Smoking_Status', 'Region', 'Income_Level', 'Education_Level']
        )
    
    with col2:
        metric_to_compare = st.selectbox(
            "Métrica para comparação:",
            ['Age', 'BMI', 'Years_Smoking', 'Cigarettes_Per_Day', 'Air_Pollution_Level']
        )
    
    if compare_by and metric_to_compare:
        # Create comparison violin plot
        fig_compare = px.violin(
            advanced_df,
            x=compare_by,
            y=metric_to_compare,
            box=True,
            title=f"Comparação de {metric_to_compare.replace('_', ' ')} por {compare_by.replace('_', ' ')}",
            color=compare_by
        )
        fig_compare.update_layout(height=400, xaxis_tickangle=45)
        st.plotly_chart(fig_compare, use_container_width=True)
    
    # Risk factor ranking
    st.subheader("🏆 Ranking de Fatores de Risco")
    
    # Calculate correlation with cancer occurrence
    cancer_binary = (advanced_df['Lung_Cancer_Stage'] != 'No Cancer').astype(int)
    
    # Start with basic numerical columns
    basic_numerical_cols = []
    for col in ['Age', 'Years_Smoking', 'Cigarettes_Per_Day', 'BMI']:
        if col in advanced_df.columns and pd.api.types.is_numeric_dtype(advanced_df[col]):
            basic_numerical_cols.append(col)
    
    # Handle categorical columns that should be numeric
    categorical_mappings = {
        'Air_Pollution_Level': {'Low': 1, 'Moderate': 2, 'Medium': 2, 'High': 3},
        'Physical_Activity_Level': {'Low': 1, 'Moderate': 2, 'Medium': 2, 'High': 3},
        'Diet_Quality': {'Poor': 1, 'Average': 2, 'Good': 3}
    }
    
    # Create a working DataFrame for correlations
    corr_df_working = advanced_df[basic_numerical_cols].copy()
    
    # Add converted categorical columns
    for col, mapping in categorical_mappings.items():
        if col in advanced_df.columns:
            try:
                converted_col = advanced_df[col].map(mapping)
                if not converted_col.isna().all():
                    corr_df_working[col] = converted_col
            except Exception:
                continue
    
    # Calculate correlations with robust error handling
    correlations = []
    for col in corr_df_working.columns:
        try:
            # Check if column has enough valid data
            valid_col_data = corr_df_working[col].dropna()
            if len(valid_col_data) < 2:
                continue
                
            # Check if column has variance (not all same values)
            if valid_col_data.nunique() < 2:
                continue
                
            # Create valid dataset for correlation
            col_data = corr_df_working[col].reset_index(drop=True)
            cancer_data = pd.Series(cancer_binary).reset_index(drop=True)
            
            # Ensure same length
            min_len = min(len(col_data), len(cancer_data))
            col_data = col_data[:min_len]
            cancer_data = cancer_data[:min_len]
            
            # Remove NaN values
            valid_indices = pd.notna(col_data) & pd.notna(cancer_data)
            col_clean = col_data[valid_indices]
            cancer_clean = cancer_data[valid_indices]
            
            # Final checks before correlation
            if len(col_clean) > 1 and col_clean.nunique() > 1 and cancer_clean.nunique() > 1:
                # Suppress warnings for this specific calculation
                with pd.option_context('mode.use_inf_as_na', True):
                    corr = col_clean.corr(cancer_clean)
                    
                if pd.notna(corr) and abs(corr) > 1e-10:  # Avoid very small correlations
                    factor_name = col.replace('_', ' ')
                    correlations.append({'Factor': factor_name, 'Correlation': abs(corr)})
                    
        except (ValueError, ZeroDivisionError, RuntimeWarning):
            continue
        except Exception:
            continue
    
    if correlations:
        corr_result_df = pd.DataFrame(correlations).sort_values('Correlation', ascending=True)
        
        fig_ranking = px.bar(
            corr_result_df,
            x='Correlation',
            y='Factor',
            orientation='h',
            title="Ranking de Correlação com Câncer (Valor Absoluto)",
            color='Correlation',
            color_continuous_scale='Reds'
        )
        fig_ranking.update_layout(height=400)
        st.plotly_chart(fig_ranking, use_container_width=True)
    else:
        st.warning("Não foi possível calcular correlações com os dados filtrados atuais.")
    
    # Summary statistics
    st.subheader("📋 Estatísticas Resumo")
    
    if len(advanced_df) > 0:
        # Use only basic numerical columns that exist in original DataFrame
        basic_numerical_cols = []
        for col in ['Age', 'Years_Smoking', 'Cigarettes_Per_Day', 'BMI']:
            if col in advanced_df.columns and pd.api.types.is_numeric_dtype(advanced_df[col]):
                basic_numerical_cols.append(col)
        
        if basic_numerical_cols:
            summary_stats = advanced_df[basic_numerical_cols].describe()
            st.dataframe(summary_stats.round(2))
        else:
            st.warning("Nenhuma coluna numérica disponível para estatísticas resumo.")
        
        # Cancer statistics by group
        if compare_by in advanced_df.columns:
            try:
                cancer_by_group = advanced_df.groupby(compare_by).agg({
                    'Lung_Cancer_Stage': lambda x: (x != 'No Cancer').mean() * 100,
                    'Age': 'mean',
                    'BMI': 'mean'
                }).round(2)
                cancer_by_group.columns = ['Taxa de Câncer (%)', 'Idade Média', 'IMC Médio']
                st.dataframe(cancer_by_group)
            except Exception as e:
                st.warning(f"Não foi possível calcular estatísticas por grupo: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    📊 Dashboard desenvolvido com Streamlit para análise de fatores de risco do câncer de pulmão<br>
    Dados: Smoking and Other Risk Factors Dataset (Kaggle)<br>
    🔄 Os gráficos são atualizados automaticamente conforme os filtros aplicados
</div>
""", unsafe_allow_html=True)
