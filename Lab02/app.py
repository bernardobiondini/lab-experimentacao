import os
import requests
import csv
import subprocess
from dotenv import load_dotenv
from utils import get_current_folder

script_dir = get_current_folder()
dotenv_path = os.path.join(script_dir, ".env")

load_dotenv(dotenv_path)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

# Obter os 1000 repositórios Java mais populares
def get_top_repositories():
    repos = []
    url = "https://api.github.com/search/repositories?q=language:java&sort=stars&order=desc&per_page=100"
    
    for page in range(1, 11):  # Paginação
        response = requests.get(f"{url}&page={page}", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            repos.extend([(repo["full_name"], repo["stargazers_count"], repo["created_at"], repo["pushed_at"], repo["size"], repo["forks_count"]) for repo in data["items"]])
        else:
            print("Erro ao buscar repositórios", response.status_code)
            break
    return repos

# Clonar um repositório de teste
def clone_repository(repo_name):
    os.system(f"git clone https://github.com/{repo_name}.git")

# Executar ferramenta CK e coletar métricas
def run_ck_tool(repo_name):
    print("Executando analise")

# Salvar dados coletados em CSV
def save_to_csv(filename, data):
    path = get_current_folder() + f"/{filename}"
    with open(path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Repo Name", "Stars", "Created At", "Last Push", "Size (KB)", "Forks"])
        writer.writerows(data)

if __name__ == "__main__":
    repos = get_top_repositories()
    save_to_csv("top_java_repositories.csv", repos)
    
    # Clonando e analisando um repositório de teste
    if repos:
        test_repo = repos[0][0]
        print(f"Clonando repositório: {test_repo}")
        clone_repository(test_repo)
        print(f"Executando análise CK no {test_repo}")
        run_ck_tool(test_repo)
