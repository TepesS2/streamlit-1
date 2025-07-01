"""
Script de teste para verificar se a correção do erro de serialização JSON funcionou.
Este script testa especificamente a funcionalidade de faixas etárias personalizadas.
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

def testar_faixas_etarias():
    print("🧪 Testando correção de serialização JSON para faixas etárias...")
    
    # Carregar dataset traduzido
    try:
        df = pd.read_csv('Dataset_Cancer_Pulmao_Traduzido.csv')
        print("✅ Dataset carregado com sucesso")
    except FileNotFoundError:
        print("❌ Dataset não encontrado")
        return False
    
    # Testar pd.cut
    print("\n🔧 Testando pd.cut...")
    df['Grupo_Idade'] = pd.cut(df['Idade'], bins=5)
    df['Grupo_Idade_Str'] = converter_intervalos_para_string(df['Grupo_Idade'])
    
    print(f"Tipo original: {type(df['Grupo_Idade'].iloc[0])}")
    print(f"Tipo convertido: {type(df['Grupo_Idade_Str'].iloc[0])}")
    print(f"Exemplos de intervalos originais: {df['Grupo_Idade'].head(3).tolist()}")
    print(f"Exemplos de intervalos convertidos: {df['Grupo_Idade_Str'].head(3).tolist()}")
    
    # Testar agrupamento
    print("\n📊 Testando agrupamento...")
    dados_teste = df.groupby(['Grupo_Idade_Str', 'Genero'], observed=True).size().reset_index(name='Contagem')
    print(f"Dados agrupados criados: {len(dados_teste)} linhas")
    
    # Testar criação de gráfico
    print("\n🎨 Testando criação de gráfico Plotly...")
    try:
        fig = px.bar(
            dados_teste,
            x='Grupo_Idade_Str',
            y='Contagem',
            color='Genero',
            title="Teste de Faixas Etárias",
        )
        print("✅ Gráfico criado com sucesso!")
        
        # Testar serialização JSON
        import plotly.io
        json_data = plotly.io.to_json(fig, validate=False)
        print("✅ Serialização JSON realizada com sucesso!")
        print(f"Tamanho do JSON: {len(json_data)} caracteres")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar gráfico: {e}")
        return False

def testar_quartis():
    print("\n🧪 Testando pd.qcut (quartis)...")
    
    try:
        df = pd.read_csv('Dataset_Cancer_Pulmao_Traduzido.csv')
        df['Grupo_Idade_Quartis'] = pd.qcut(df['Idade'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
        
        dados_quartis = df.groupby(['Grupo_Idade_Quartis', 'Genero'], observed=True).size().reset_index(name='Contagem')
        
        fig = px.bar(
            dados_quartis,
            x='Grupo_Idade_Quartis',
            y='Contagem',
            color='Genero',
            title="Teste de Quartis",
        )
        
        import plotly.io
        json_data = plotly.io.to_json(fig, validate=False)
        print("✅ Quartis testados com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar quartis: {e}")
        return False

if __name__ == "__main__":
    print("🫁 Dashboard de Análise de Fatores de Risco do Câncer de Pulmão")
    print("=" * 60)
    print("TESTE DE CORREÇÃO DE SERIALIZAÇÃO JSON")
    print("=" * 60)
    
    sucesso_faixas = testar_faixas_etarias()
    sucesso_quartis = testar_quartis()
    
    print("\n" + "=" * 60)
    print("RESULTADOS:")
    print(f"✅ Faixas personalizadas: {'PASSOU' if sucesso_faixas else 'FALHOU'}")
    print(f"✅ Quartis: {'PASSOU' if sucesso_quartis else 'FALHOU'}")
    
    if sucesso_faixas and sucesso_quartis:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O erro de serialização JSON foi corrigido com sucesso.")
        print("✅ As faixas etárias personalizadas agora funcionam corretamente.")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM")
        print("Por favor, verifique os erros acima.")
