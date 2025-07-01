import pandas as pd
import numpy as np

# Test the improved fixes
print("🔍 Testando correções melhoradas...")

# Load data
df = pd.read_csv('Lung_Cancer_Trends_Realistic.csv')
print(f"✅ Dataset carregado: {df.shape}")

# Test income mapping with correct values
income_mapping = {
    'Low': 1, 'Middle': 2, 'High': 3,
    'Baixa': 1, 'Média': 2, 'Alta': 3
}

try:
    income_numeric = df['Income_Level'].map(income_mapping)
    print(f"✅ Mapeamento de renda: {income_numeric.value_counts()}")
except Exception as e:
    print(f"❌ Erro no mapeamento: {e}")

# Test categorical to numeric conversion
categorical_mappings = {
    'Air_Pollution_Level': {'Low': 1, 'Medium': 2, 'High': 3},
    'Physical_Activity_Level': {'Low': 1, 'Moderate': 2, 'High': 3},
    'Diet_Quality': {'Poor': 1, 'Average': 2, 'Good': 3}
}

print("\n🔢 Testando conversões categóricas:")
for col, mapping in categorical_mappings.items():
    if col in df.columns:
        unique_vals = df[col].unique()
        print(f"  {col}: {unique_vals}")
        mapped = df[col].map(mapping)
        print(f"    Mapeado: {mapped.value_counts().to_dict()}")

# Test only numeric columns
numerical_cols = []
for col in ['Age', 'Years_Smoking', 'Cigarettes_Per_Day', 'BMI']:
    if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
        numerical_cols.append(col)

print(f"\n📊 Colunas numéricas encontradas: {numerical_cols}")

print("\n🎉 Testes concluídos!")
