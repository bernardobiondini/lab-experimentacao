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
    folder = get_current_folder();
    
    if (os.path.exists(f"{folder}/repos/{repo_name.split('/')[-1]}")):
        print("Repositório já clonado")
        return
    
    os.system(f"git clone https://github.com/{repo_name}.git {folder}/repos/{repo_name.split('/')[-1]}")

# Executar ferramenta CK e coletar métricas
def run_ck_tool(repo_name):
    current_folder = get_current_folder()
    repo_dir = repo_name.split('/')[-1]
    ck_output_file = f"{current_folder}/metrics/{repo_dir}_metrics.csv"
    repo_dir = f"{get_current_folder()}/repos/{repo_dir}"
    command = subprocess.run(["java", "-jar", "ck.jar", repo_dir, "true", "0", "false", ck_output_file])
    print(command)
    return ck_output_file

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
    
    # Clonando e analisando um repositório de teste
    if repos:
        test_repo = repos[1][0]
        print(f"Clonando repositório: {test_repo}")
        clone_repository(test_repo)
        ck_file = run_ck_tool(test_repo)
        print(f"Métricas salvas em {ck_file}")
