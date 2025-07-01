#!/usr/bin/env python3
"""
Script de configuração rápida para o Dashboard de Análise de Câncer de Pulmão
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Execute um comando e mostre o resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Concluído!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e}")
        print(f"Saída: {e.stdout}")
        print(f"Erro: {e.stderr}")
        return False

def main():
    print("🫁 Dashboard de Análise de Fatores de Risco do Câncer de Pulmão")
    print("=" * 60)
    print("Este script irá configurar automaticamente o ambiente e executar o dashboard.")
    
    # Verificar se Python está instalado
    print(f"\n📋 Python version: {sys.version}")
    
    # Instalar dependências
    if not run_command("pip install -r requirements.txt", "Instalando dependências"):
        print("❌ Falha na instalação das dependências. Verifique o requirements.txt")
        return
    
    # Verificar se o dataset existe
    if not os.path.exists("Lung_Cancer_Trends_Realistic.csv"):
        print("\n📥 Dataset não encontrado. Baixando...")
        if not run_command("python download_dataset.py", "Baixando dataset do Kaggle"):
            print("❌ Falha no download do dataset. Verifique sua conexão e configuração do Kaggle.")
            return
    else:
        print("\n✅ Dataset já existe!")
    
    # Executar o dashboard
    print("\n🚀 Iniciando o dashboard...")
    print("📱 O dashboard será aberto em: http://localhost:8501")
    print("⏹️  Para parar o servidor, pressione Ctrl+C")
    
    try:
        subprocess.run("streamlit run app.py", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard encerrado pelo usuário.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao executar o dashboard: {e}")

if __name__ == "__main__":
    main()
