import pandas as pd
import numpy as np

def translate_dataset():
    """Traduz o dataset para português"""
    print("🔄 Carregando dataset...")
    df = pd.read_csv('Lung_Cancer_Trends_Realistic.csv')
    
    print("🔄 Traduzindo colunas...")
    # Dicionário de tradução das colunas
    column_translation = {
        'Patient_ID': 'ID_Paciente',
        'Age': 'Idade',
        'Gender': 'Genero',
        'Smoking_Status': 'Status_Tabagismo',
        'Years_Smoking': 'Anos_Fumando',
        'Cigarettes_Per_Day': 'Cigarros_Por_Dia',
        'Secondhand_Smoke_Exposure': 'Exposicao_Fumo_Passivo',
        'Occupation_Exposure': 'Exposicao_Ocupacional',
        'Air_Pollution_Level': 'Nivel_Poluicao_Ar',
        'Family_History': 'Historico_Familiar',
        'Genetic_Markers_Positive': 'Marcadores_Geneticos_Positivos',
        'BMI': 'IMC',
        'Physical_Activity_Level': 'Nivel_Atividade_Fisica',
        'Alcohol_Consumption': 'Consumo_Alcool',
        'Diet_Quality': 'Qualidade_Dieta',
        'Region': 'Regiao',
        'Income_Level': 'Nivel_Renda',
        'Education_Level': 'Nivel_Educacao',
        'Access_to_Healthcare': 'Acesso_Cuidados_Saude',
        'Screening_Frequency': 'Frequencia_Exames',
        'Chronic_Lung_Disease': 'Doenca_Pulmonar_Cronica',
        'Lung_Cancer_Stage': 'Estagio_Cancer_Pulmao',
        'Diagnosis_Year': 'Ano_Diagnostico',
        'Survival_Status': 'Status_Sobrevivencia'
    }
    
    # Renomear colunas
    df_translated = df.rename(columns=column_translation)
    
    print("🔄 Traduzindo valores categóricos...")
    
    # Traduzir valores categóricos
    value_translations = {
        'Genero': {
            'Male': 'Masculino',
            'Female': 'Feminino'
        },
        'Status_Tabagismo': {
            'Never': 'Nunca',
            'Current': 'Atual',
            'Former': 'Ex-fumante'
        },
        'Exposicao_Fumo_Passivo': {
            'Low': 'Baixa',
            'Medium': 'Média',
            'High': 'Alta'
        },
        'Exposicao_Ocupacional': {
            'Asbestos': 'Amianto',
            'Silica': 'Sílica',
            'Diesel Fumes': 'Gases Diesel',
            'Coal Dust': 'Poeira de Carvão',
            'Chemical Fumes': 'Gases Químicos'
        },
        'Nivel_Poluicao_Ar': {
            'Low': 'Baixo',
            'Moderate': 'Moderado',
            'High': 'Alto'
        },
        'Historico_Familiar': {
            'Yes': 'Sim',
            'No': 'Não'
        },
        'Marcadores_Geneticos_Positivos': {
            'Yes': 'Sim',
            'No': 'Não'
        },
        'Nivel_Atividade_Fisica': {
            'Low': 'Baixo',
            'Moderate': 'Moderado',
            'High': 'Alto'
        },
        'Consumo_Alcool': {
            'Low': 'Baixo',
            'Moderate': 'Moderado',
            'High': 'Alto'
        },
        'Qualidade_Dieta': {
            'Poor': 'Ruim',
            'Average': 'Média',
            'Good': 'Boa'
        },
        'Regiao': {
            'North': 'Norte',
            'South': 'Sul',
            'East': 'Leste',
            'West': 'Oeste'
        },
        'Nivel_Renda': {
            'Low': 'Baixa',
            'Middle': 'Média',
            'High': 'Alta'
        },
        'Nivel_Educacao': {
            'Primary': 'Fundamental',
            'Secondary': 'Médio',
            'Tertiary': 'Superior'
        },
        'Acesso_Cuidados_Saude': {
            'Poor': 'Ruim',
            'Average': 'Médio',
            'Good': 'Bom'
        },
        'Frequencia_Exames': {
            'Never': 'Nunca',
            'Occasionally': 'Ocasionalmente',
            'Regularly': 'Regularmente'
        },
        'Doenca_Pulmonar_Cronica': {
            'Yes': 'Sim',
            'No': 'Não'
        },
        'Estagio_Cancer_Pulmao': {
            'No Cancer': 'Sem Câncer',
            'None': 'Sem Câncer',
            'Stage I': 'Estágio I',
            'Stage II': 'Estágio II',
            'Stage III': 'Estágio III',
            'Stage IV': 'Estágio IV'
        },
        'Status_Sobrevivencia': {
            'Alive': 'Vivo',
            'Deceased': 'Falecido'
        }
    }
    
    # Aplicar traduções
    for column, translations in value_translations.items():
        if column in df_translated.columns:
            df_translated[column] = df_translated[column].replace(translations)
    
    print("💾 Salvando dataset traduzido...")
    df_translated.to_csv('Dataset_Cancer_Pulmao_Traduzido.csv', index=False, encoding='utf-8')
    
    print("✅ Dataset traduzido salvo como 'Dataset_Cancer_Pulmao_Traduzido.csv'")
    print(f"📊 Shape: {df_translated.shape}")
    print(f"📋 Colunas traduzidas: {list(df_translated.columns)}")
    
    return df_translated

if __name__ == "__main__":
    translate_dataset()
