# 🚀 Instruções para Deploy na Nuvem Streamlit

## 📋 Pré-requisitos
- Conta no GitHub
- Conta no Streamlit Cloud (share.streamlit.io)

## 🔧 Passos para Deploy

### 1. Preparar Repositório GitHub

```bash
# 1. Crie um novo repositório no GitHub
# 2. Clone o repositório localmente
git clone https://github.com/SEU_USUARIO/NOME_DO_REPO.git

# 3. Copie todos os arquivos para o repositório:
# - app.py
# - requirements.txt  
# - Lung_Cancer_Trends_Realistic.csv
# - README.md
# - .gitignore

# 4. Faça commit e push
git add .
git commit -m "Dashboard de Análise de Câncer de Pulmão"
git push origin main
```

### 2. Deploy no Streamlit Cloud

1. **Acesse**: https://share.streamlit.io
2. **Login**: Use sua conta GitHub
3. **New app**: Clique em "New app"
4. **Configure**:
   - Repository: `seu-usuario/nome-do-repo`
   - Branch: `main`
   - Main file path: `app.py`
5. **Deploy**: Clique em "Deploy!"

### 3. Configurações Opcionais

#### Secrets (se necessário)
Se precisar de variáveis de ambiente:
```toml
# .streamlit/secrets.toml
[kaggle]
username = "seu_usuario_kaggle"
key = "sua_api_key"
```

#### Configuração Avançada
```toml
# .streamlit/config.toml
[server]
maxUploadSize = 200

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

## 🔗 URL do Dashboard

Após o deploy, seu dashboard estará disponível em:
`https://NOME_DO_APP-HASH.streamlit.app`

## ⚡ Atualizações Automáticas

- Qualquer push para o branch `main` atualiza automaticamente o app
- O Streamlit Cloud rebuilda o ambiente automaticamente
- Logs de build/erro disponíveis no painel de controle

## 🛠️ Troubleshooting

### Problemas Comuns:

1. **Erro de dependências**:
   - Verifique o `requirements.txt`
   - Use versões específicas das bibliotecas

2. **Dataset não encontrado**:
   - Certifique-se que o CSV está no repositório
   - Verifique o nome do arquivo no código

3. **Timeout na build**:
   - Dataset muito grande (limite: 200MB)
   - Considere usar cache ou repositório separado

4. **Erro de memória**:
   - Use `@st.cache_data` para otimizar
   - Considere amostragem dos dados

### Comandos Úteis:

```bash
# Testar localmente antes do deploy
streamlit run app.py

# Verificar tamanho dos arquivos
du -sh *

# Limpar cache local
streamlit cache clear
```

## 📊 Monitoramento

- **Analytics**: Disponível no painel do Streamlit Cloud
- **Logs**: Acesso em tempo real aos logs de erro
- **Usage**: Métricas de uso e performance

## 🔄 Versionamento

Recomendações para manter o app estável:

1. **Branch strategy**:
   ```bash
   # Desenvolvimento
   git checkout -b feature/nova-funcionalidade
   
   # Deploy apenas do main
   git checkout main
   git merge feature/nova-funcionalidade
   git push origin main
   ```

2. **Tags de versão**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

## 🎯 Próximos Passos

Após o deploy, considere:

1. **Custom domain**: Configurar domínio personalizado
2. **Analytics**: Integrar Google Analytics
3. **Feedback**: Adicionar sistema de feedback
4. **Performance**: Monitorar e otimizar carregamento
5. **Features**: Adicionar novas análises baseadas no feedback

---

**🎉 Parabéns! Seu dashboard está na nuvem!**

Compartilhe a URL com seus usuários e monitore o uso através do painel do Streamlit Cloud.
