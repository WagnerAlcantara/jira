Este script se conecta à API do Jira Cloud para buscar issues a partir de uma jql específico, extrai dados relevantes (como responsável, criador, resumo e campo customizado), organiza essas informações em uma tabela (usando pandas) e salva o resultado em uma planilha .xlsx dentro de uma pasta chamada Relatorio-excel.

PRÉ REQUISITOS PARA QUE O SCRIPT FUNCIONE
Python instalado (recomendado: Python 3.8+)

INSTALAR BIBLIOTECAS NECESSARIAS:
Execute no terminal:
pip install requests pandas python-dotenv openpyxl
Criar os seguintes arquivos no mesmo diretório do script:
Config.json  
{
  "JIRA_EMAIL": "seu-email@empresa.com",
  "JIRA_API_TOKEN": "seu-token-api"
}

ESTRUTURA DE ARQUIVOS
seu_projeto/
├── relatorio.py
├── config.json
└── Relatorio-excel/    ← será criada automaticamente, se não existir

| Item                  | Obrigatório  | Observações                                       |
| --------------------- | ------------ | ------------------------------------------------- |
| Python instalado      | ✅            | Versão 3.8 ou superior                            |
| Bibliotecas via `pip` | ✅            | `requests`, `pandas`, `openpyxl`, `python-dotenv` |
| `config.json`         | ✅            | Com email e token do Jira                         |
| Permissões no Jira    | ✅            | Token com acesso de leitura                       |
| Internet ativa        | ✅            | Necessária para acessar a API                     |


