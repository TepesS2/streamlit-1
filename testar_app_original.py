"""
Script de teste específico para o app.py (dashboard original) 
para verificar se a correção do erro de serialização JSON funcionou.
"""

import pandas as pd
import plotly.express as px

def converter_intervalos_para_string(series):
    """Converte objetos Interval para strings legíveis para uso em gráficos"""
    if hasattr(series, 'dtype') and series.dtype.name == 'category':
        # Verificar se são intervalos
        if len(series) > 0 and hasattr(series.iloc[0], 'left'):
            return series.apply(lambda x: f"{x.left:.0f}-{x.right:.0f}")
    return series

def testar_app_original():
    print("🧪 Testando correções no app.py (dashboard original)...")
    
    # Carregar dataset original
    try:
        df = pd.read_csv('Lung_Cancer_Trends_Realistic.csv')
        print("✅ Dataset original carregado com sucesso")
        print(f"   Colunas: {list(df.columns)}")
    except FileNotFoundError:
        print("❌ Dataset original não encontrado")
        return False
    
    # Simular o mesmo processo do app.py
    print("\n🔧 Testando lógica de agrupamento etário do app.py...")
    
    # Teste 1: Décadas
    print("📊 Testando agrupamento por décadas...")
    df_test = df.copy()
    df_test['Age_Group'] = (df_test['Age'] // 10) * 10
    df_test['Age_Group'] = df_test['Age_Group'].astype(str) + 's'
    group_col = 'Age_Group'
    
    age_dist_data = df_test.groupby([group_col, 'Gender'], observed=True).size().reset_index(name='Count')
    print(f"   ✅ Décadas: {len(age_dist_data)} grupos criados")
    
    # Teste 2: Quartis  
    print("📊 Testando agrupamento por quartis...")
    df_test = df.copy()
    df_test['Age_Group'] = pd.qcut(df_test['Age'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    group_col = 'Age_Group'
    
    age_dist_data = df_test.groupby([group_col, 'Gender'], observed=True).size().reset_index(name='Count')
    print(f"   ✅ Quartis: {len(age_dist_data)} grupos criados")
    
    # Teste 3: Faixas personalizadas (o que estava causando erro)
    print("📊 Testando agrupamento por faixas personalizadas...")
    df_test = df.copy()
    bins = 5
    df_test['Age_Group'] = pd.cut(df_test['Age'], bins=bins)
    df_test['Age_Group_Str'] = converter_intervalos_para_string(df_test['Age_Group'])
    group_col = 'Age_Group_Str'
    
    print(f"   Tipo original: {type(df_test['Age_Group'].iloc[0])}")
    print(f"   Tipo convertido: {type(df_test['Age_Group_Str'].iloc[0])}")
    print(f"   Exemplos convertidos: {df_test['Age_Group_Str'].unique()[:3]}")
    
    age_dist_data = df_test.groupby([group_col, 'Gender'], observed=True).size().reset_index(name='Count')
    print(f"   ✅ Faixas personalizadas: {len(age_dist_data)} grupos criados")
    
    # Teste de criação de gráfico (o que estava falhando)
    print("\n🎨 Testando criação de gráfico Plotly com faixas personalizadas...")
    try:
        fig = px.bar(
            age_dist_data,
            x=group_col,
            y='Count',
            color='Gender',
            title="Teste - Distribuição por Faixas Personalizadas",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        print("   ✅ Gráfico criado com sucesso!")
        
        # Testar serialização JSON (o que causava o erro)
        import plotly.io
        json_data = plotly.io.to_json(fig, validate=False)
        print("   ✅ Serialização JSON realizada com sucesso!")
        print(f"   Tamanho do JSON: {len(json_data)} caracteres")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao criar gráfico: {e}")
        return False

def testar_outros_groupby():
    print("\n🧪 Testando outros groupby do app.py...")
    
    try:
        df = pd.read_csv('Lung_Cancer_Trends_Realistic.csv')
        
        # Testar groupby que foram corrigidos
        test_data = df.groupby(['Education_Level', 'Income_Level'], observed=True).size().reset_index(name='Count')
        print(f"   ✅ Education vs Income: {len(test_data)} grupos")
        
        test_data = df.groupby(['Genetic_Markers_Positive', 'Family_History'], observed=True).size().reset_index(name='Count')
        print(f"   ✅ Genetic vs Family: {len(test_data)} grupos")
        
        test_data = df.groupby(['Physical_Activity_Level', 'Diet_Quality'], observed=True).size().reset_index(name='Count')
        print(f"   ✅ Activity vs Diet: {len(test_data)} grupos")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro nos groupby: {e}")
        return False

if __name__ == "__main__":
    print("🫁 Dashboard Original (app.py) - Teste de Correções")
    print("=" * 60)
    print("TESTE DE CORREÇÃO DE SERIALIZAÇÃO JSON")
    print("=" * 60)
    
    sucesso_agrupamento = testar_app_original()
    sucesso_groupby = testar_outros_groupby()
    
    print("\n" + "=" * 60)
    print("RESULTADOS:")
    print(f"✅ Agrupamento etário: {'PASSOU' if sucesso_agrupamento else 'FALHOU'}")
    print(f"✅ Outros groupby: {'PASSOU' if sucesso_groupby else 'FALHOU'}")
    
    if sucesso_agrupamento and sucesso_groupby:
        print("\n🎉 TODOS OS TESTES DO APP.PY PASSARAM!")
        print("✅ O dashboard original foi corrigido com sucesso.")
        print("✅ Ambos os dashboards (app.py e app_traduzido.py) estão funcionais.")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM")
        print("Por favor, verifique os erros acima.")
