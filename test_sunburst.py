import pandas as pd
import plotly.express as px

# Test the sunburst fix
print("🔍 Testando correção do sunburst...")

# Load data
df = pd.read_csv('Lung_Cancer_Trends_Realistic.csv')
print(f"✅ Dataset carregado: {df.shape}")

# Test sunburst data preparation
print("\n📊 Testando preparação dos dados para sunburst:")
sunburst_data = df[['Secondhand_Smoke_Exposure', 'Lung_Cancer_Stage']].dropna()
print(f"Dados limpos: {sunburst_data.shape}")

sunburst_counts = sunburst_data.groupby(['Secondhand_Smoke_Exposure', 'Lung_Cancer_Stage']).size().reset_index(name='Count')
print(f"Contagens agrupadas: {sunburst_counts.shape}")
print("\nPrimeiras 5 linhas:")
print(sunburst_counts.head())

# Test if sunburst can be created
try:
    fig = px.sunburst(
        sunburst_counts,
        path=['Secondhand_Smoke_Exposure', 'Lung_Cancer_Stage'],
        values='Count',
        title="Teste"
    )
    print("\n✅ Sunburst criado com sucesso!")
except Exception as e:
    print(f"\n❌ Erro no sunburst: {e}")

print("\n🎉 Teste concluído!")
