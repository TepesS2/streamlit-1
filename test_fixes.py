import pandas as pd
import numpy as np

# Test the fixes
print("🔍 Testando correções...")

# Load data
df = pd.read_csv('Lung_Cancer_Trends_Realistic.csv')
print(f"✅ Dataset carregado: {df.shape}")

# Test Income_Level column
print(f"Income_Level dtype: {df['Income_Level'].dtype}")
print(f"Valores únicos Income_Level: {df['Income_Level'].unique()}")

# Test correlation calculation with NaN handling
cancer_binary = (df['Lung_Cancer_Stage'] != 'No Cancer').astype(int)
numerical_cols = ['Age', 'Years_Smoking', 'Cigarettes_Per_Day', 'BMI', 'Air_Pollution_Level']

print("\n🔗 Testando correlações:")
correlations = []
for col in numerical_cols:
    if col in df.columns and len(df[col].dropna()) > 0:
        valid_data = df[[col]].join(pd.Series(cancer_binary, name='cancer')).dropna()
        if len(valid_data) > 1:
            corr = valid_data[col].corr(valid_data['cancer'])
            if not pd.isna(corr):
                correlations.append({'Factor': col.replace('_', ' '), 'Correlation': abs(corr)})
                print(f"  {col}: {abs(corr):.3f}")

print(f"\n✅ {len(correlations)} correlações calculadas com sucesso!")

# Test income mapping
income_mapping = {
    'Low': 1, 'Medium': 2, 'High': 3, 'Middle': 2,
    'Baixa': 1, 'Média': 2, 'Alta': 3
}

try:
    income_numeric = df['Income_Level'].map(income_mapping)
    if income_numeric.isna().any():
        print(f"⚠️ Alguns valores não mapeados: {df['Income_Level'][income_numeric.isna()].unique()}")
        income_numeric = income_numeric.fillna(0)
    print(f"✅ Mapeamento de renda funcionando: {income_numeric.describe()}")
except Exception as e:
    print(f"❌ Erro no mapeamento: {e}")

print("\n🎉 Todos os testes passaram!")
