import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from datetime import datetime
import json
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Verifica se o arquivo config.json existe antes de tentar abri-lo
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, "config.json")

if not os.path.exists(config_file):
    print(f"Erro: Arquivo '{config_file}' não encontrado!")
    exit()

# Carrega as configurações do JSON
with open(config_file, "r") as file:
    config = json.load(file)

# Configurações do Jira
JIRA_DOMAIN = "https://wagner-alcantara.atlassian.net/"
JIRA_EMAIL = config.get("JIRA_EMAIL")
JIRA_API_TOKEN = config.get("JIRA_API_TOKEN")
JQL_QUERY = "project = ES"

# Se alguma credencial estiver faltando, exibe erro e encerra
if not JIRA_EMAIL or not JIRA_API_TOKEN:
    print("Erro: Credenciais do Jira não encontradas no config.json!")
    exit()

SEARCH_URL = f"{JIRA_DOMAIN}/rest/api/3/search"
HEADERS = {"Accept": "application/json"}
params = {
    "jql": JQL_QUERY,
    "maxResults": 100,
    "fields": "reporter,assignee,created,summary,customfield_10044"
}

response = requests.get(
    SEARCH_URL,
    headers=HEADERS,
    params=params,
    auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
)

if response.status_code != 200:
    print(f"Erro ao consultar Jira: {response.status_code}")
    print(response.text)
    exit()

issues = response.json().get("issues", [])
dados = []

# Processa os dados das issues do Jira
for issue in issues:
    fields = issue["fields"]
    key = issue["key"]
    reporter_info = fields.get("reporter")
    reporter = reporter_info.get(
        "displayName") if reporter_info else "Sem reporter"
    assignee_info = fields.get("assignee")
    assignee = assignee_info.get(
        "displayName") if assignee_info else "Sem assignee"

    created = fields["created"]
    summary = fields["summary"]

    # Campo customizado
    custom_field = fields.get("customfield_10044", "Não preenchido")
    if isinstance(custom_field, dict):
        custom_value = custom_field.get("value") or custom_field.get(
            "displayName") or str(custom_field)
    elif isinstance(custom_field, list):
        custom_value = ", ".join([item.get("value") or str(
            item) for item in custom_field if isinstance(item, dict)])
    else:
        custom_value = custom_field

    dados.append({
        "Key": key,
        "Resumo": summary,
        "Reporter": reporter,
        "Assignee": assignee,
        "Data de Criação": created,
        "Affected hardware": custom_value
    })

# Criar DataFrame
df = pd.DataFrame(dados)

# Formatar data de criação
df["Data de Criação"] = pd.to_datetime(
    df["Data de Criação"]).dt.strftime("%d/%m/%Y %H:%M")

# Criar nome único para o arquivo com timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"relatorio_{timestamp}.xlsx"

# Caminho da pasta Relatorio-excel
output_dir = os.path.join(script_dir, "Relatorio-excel")

# Criar a pasta se não existir
os.makedirs(output_dir, exist_ok=True)

# Caminho completo do arquivo
file_path = os.path.join(output_dir, filename)

# Exportar para Excel
df.to_excel(file_path, index=False)

print(f"Planilha gerada com sucesso: {file_path}")
