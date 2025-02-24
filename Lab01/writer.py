import json
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
    output_path = os.path.join(get_current_folder(), "github_data.json")
    
    with open(output_path, "w") as f:
        json.dump(processed_data, f, indent=4)