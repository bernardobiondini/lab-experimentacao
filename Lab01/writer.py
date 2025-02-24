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
            "primary_language": repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "Unknown",
            "releases": repo["releases"]["totalCount"],
            "merged_pull_requests": repo["pullRequests"]["totalCount"],
            "closed_issues_ratio": repo["closedIssues"]["totalCount"] / repo["issues"]["totalCount"] if repo["issues"]["totalCount"] > 0 else 0,
            "last_update_days": last_update_days
        })
    
    return processed

def write(processed_data):
    output_path = os.path.join(get_current_folder(), "github_data.csv")
    
    # Definir cabeçalhos do CSV
    fieldnames = ["repo", "age", "primary_language", "releases", "merged_pull_requests", "closed_issues_ratio", "last_update_days"]
    
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(processed_data)

    print(f"Arquivo salvo em {output_path}")