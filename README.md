# 📋 Banco de Dados ANS - Operadoras de Saúde

Projeto para análise dos dados trimestrais (2023-2024) das operadoras de saúde reguladas pela ANS.

## 🚀 Como Executar

1. **Configure o ambiente**:
   ```bash
   # Instale o PostgreSQL (se necessário)
   sudo apt-get install postgresql postgresql-contrib
   ```

2. **Execute os scripts**:
   ```bash
   # 1. Crie o banco e tabelas
   psql -U seu_usuario -f scripts/01_criar_banco.sql

   # 2. Importe os dados
   psql -U seu_usuario -d ans_db -f scripts/02_importar_dados.sql
   ```

## 🔍 Consultas Disponíveis

Principais análises no arquivo `03_consultas.sql`:
```sql
-- Exemplo: Top 10 operadoras
SELECT o.razao_social, SUM(d.vl_saldo_final) as total
FROM demonstracoes d
JOIN operadoras o ON d.registro_ans = o.registro_ans
GROUP BY o.razao_social
ORDER BY total DESC
LIMIT 10;
```

## 🛠️ Estrutura do Projeto
```
📂 3_Banco_Dados_ANS/
├── 📂 data/          # Arquivos CSV
├── 📂 scripts/       # SQL scripts
└── 📄 README.md      # Este arquivo
```

## 💡 Dicas VS Code

- Use **Ctrl+Shift+V** para pré-visualizar o Markdown
- Instale a extensão **Markdown All in One** para:
  - Auto-formatação
  - Sumário automático
  - Atalhos úteis


