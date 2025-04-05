import requests
import csv
from datetime import datetime, timezone
import time
from dotenv import load_dotenv
import os
from utils import get_current_folder

script_dir = get_current_folder()
dotenv_path = os.path.join(script_dir, ".env")


load_dotenv(dotenv_path)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# ==== FUNCOES ====
def get_top_repositories(top_n=200):
    repos = []
    per_page = 100
    pages = (top_n // per_page) + (1 if top_n % per_page else 0)

    for page in range(1, pages + 1):
        url = f"https://api.github.com/search/repositories?q=stars:>1&sort=stars&order=desc&per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Erro ao buscar repositórios populares: {response.status_code}")
            break

        data = response.json()
        items = data.get('items', [])
        for item in items:
            repos.append(item['full_name'])

        time.sleep(1)  # Evitar limite de rate

    return repos[:top_n]

def get_pull_requests(repo):
    pulls = []
    page = 1
    per_page = 50  # Ajuste conforme necessário

    while True:
        url = f"https://api.github.com/repos/{repo}/pulls?state=all&per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Erro ao buscar PRs de {repo}: {response.status_code}")
            break

        data = response.json()
        if not data:
            break
        
        if page >= 4:
            break;

        pulls.extend(data)
        page += 1
        time.sleep(1)  # Evitar limite de rate

    return pulls

def get_reviews_count(repo, pr_number):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/reviews"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return 0

    reviews = response.json()
    return len(reviews)

def calculate_hours_difference(start, end):
    if not end:
        return 0
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    start_dt = datetime.strptime(start, fmt).replace(tzinfo=timezone.utc)
    end_dt = datetime.strptime(end, fmt).replace(tzinfo=timezone.utc)
    diff = end_dt - start_dt
    return diff.total_seconds() / 3600

# ==== SCRIPT PRINCIPAL ====

def main():
    results = []

    repositories = get_top_repositories(top_n=200)
    print(f"{len(repositories)} repositórios populares encontrados!")

    for repo in repositories:
        print(f"Buscando PRs do repositório: {repo}")
        prs = get_pull_requests(repo)

        for pr in prs:
            pr_number = pr['number']
            state = pr['state']
            merged = pr.get('merged_at') is not None

            if not (state in ['closed'] or merged):
                continue

            created_at = pr['created_at']
            closed_at = pr['closed_at'] or pr['merged_at']

            hours_diff = calculate_hours_difference(created_at, closed_at)
            if hours_diff < 1:
                continue

            review_count = get_reviews_count(repo, pr_number)
            if review_count == 0:
                continue

            body_length = len(pr['body']) if pr['body'] else 0

            result = {
                "repository": repo,
                "pr_number": pr_number,
                "state": "merged" if merged else "closed",
                "created_at": created_at,
                "closed_at": closed_at,
                "changed_files": pr.get('changed_files', 0),
                "additions": pr.get('additions', 0),
                "deletions": pr.get('deletions', 0),
                "review_comments": pr.get('review_comments', 0),
                "comments": pr.get('comments', 0),
                "participants": 0,  # Participantes não é diretamente disponível aqui
                "body_length": body_length,
                "hours_to_close": hours_diff,
                "review_count": review_count
            }

            results.append(result)
            print(f"PR #{pr_number} coletado!")

    # Salvar em CSV
    if results:
        with open("pull_requests_data.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

        print("\nArquivo pull_requests_data.csv gerado com sucesso!")
    else:
        print("\nNenhum PR válido encontrado.")

if __name__ == "__main__":
    main()
