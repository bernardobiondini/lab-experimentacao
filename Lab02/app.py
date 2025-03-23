import os
import requests
import csv
import subprocess
from dotenv import load_dotenv
from utils import get_current_folder
import time

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
        time.sleep(1)
    return repos

# Clonar um repositório
def clone_repository(repo_name):
    folder = get_current_folder()
    repo_path = f"{folder}/repos/{repo_name.split('/')[-1]}"
    
    if os.path.exists(repo_path):
        print(f"Repositório {repo_name} já clonado")
        return repo_path
    
    os.system(f"git clone https://github.com/{repo_name}.git {repo_path}")
    return repo_path

# Executar ferramenta CK e coletar métricas
def run_ck_tool(repo_path, repo_name):
    current_folder = get_current_folder()
    metrics_dir = f"{current_folder}/metrics"

    ck_output_file = f"{metrics_dir}/{repo_name.split('/')[-1]}_metrics_"

    command = subprocess.run(
        ["java", "-jar", "ck.jar", repo_path, "true", "0", "false", ck_output_file],
        capture_output=True,
        text=True,
    )

    if command.returncode != 0:
        print(f"Erro ao executar CK para {repo_name}: {command.stderr}")
        return None

    print(f"✅ CK executado com sucesso! Métricas salvas em {ck_output_file}")
    return ck_output_file

# Deleta o repositório clonado após a análise
def delete_repository(repo_path):
    if not os.path.exists(repo_path):
        print(f"O repositório {repo_path} não existe.")
        return
    
    try:
        if os.name == "nt":
            os.system(f"rmdir /s /q {repo_path}")
            return
        os.system(f"rm -rf {repo_path}")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao tentar deletar o repositório: {e}")

# Salvar dados coletados em CSV
def save_to_csv(filename, data):
    path = get_current_folder() + f"/{filename}"
    with open(path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Repo Name", "Stars", "Created At", "Last Push", "Size (KB)", "Forks"])
        writer.writerows(data)

if __name__ == "__main__":
    os.makedirs(get_current_folder() + "/repos", exist_ok=True)
    os.makedirs(get_current_folder() + "/metrics", exist_ok=True)

    repos = get_top_repositories()
    save_to_csv("top_java_repositories.csv", repos)
    
    for repo in repos:
        repo_name = repo[0]
        print(f"Clonando repositório: {repo_name}")
        repo_path = clone_repository(repo_name)
        print(f"Executando análise CK no {repo_name}")
        ck_file = run_ck_tool(repo_path, repo_name)
        delete_repository(repo_path)
        print(f"Métricas salvas em {ck_file}")
        time.sleep(2)
