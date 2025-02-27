import csv
import pandas as pd
from utils import get_current_folder
import os

def process_data(repos):
    processed = []
    for repo in repos:
        created_at = repo["createdAt"]
        updated_at = repo["updatedAt"]
        age = (pd.Timestamp.now(tz="UTC") - pd.Timestamp(created_at).tz_convert("UTC")).days // 365
        last_update_days = (pd.Timestamp.now(tz="UTC") - pd.Timestamp(updated_at).tz_convert("UTC")).days
        
        processed.append({
            "repo": repo["nameWithOwner"],
            "age": age,
            "language": repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "Unknown",
            "releases": repo["releases"]["totalCount"],
            "pull_requests": repo["pullRequests"]["totalCount"],  # Ajuste no nome
            "closed_issues": repo["closedIssues"]["totalCount"],  # Agora temos esse campo
            "total_issues": repo["issues"]["totalCount"],  # Adicionado para evitar erro de divisão
            "closed_issues_ratio": repo["closedIssues"]["totalCount"] / repo["issues"]["totalCount"] if repo["issues"]["totalCount"] > 0 else 0,
            "last_update_days": last_update_days,
            "pushed_at": updated_at,  # Renomeado para bater com o código dos gráficos
            "created_at": created_at,
            "stars": repo["stargazerCount"],  # ⭐ Adicionando estrelas
            "forks": repo["forkCount"],  # 🍴 Adicionando forks
            "watchers": repo["watchers"]["totalCount"],  # 👀 Adicionando watchers
            "collaborators": repo["collaborators"]["totalCount"] if repo["collaborators"] else 0  # 👥 Adicionando contribuidores
        })

    return processed

def write(processed_data):
    output_path = os.path.join(get_current_folder(), "github_data.csv")
    
    # Definir cabeçalhos do CSV
    fieldnames = ["repo", "age", "language", "releases", "pull_requests", "closed_issues", "total_issues", "closed_issues_ratio", "last_update_days", "pushed_at", "created_at", "stars", "forks", "watchers", "collaborators"]
    
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(processed_data)

    print(f"Arquivo salvo em {output_path}")