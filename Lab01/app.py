import requests
import json
import pandas as pd
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

graphql_query = """
query ($cursor: String) {
  search(query: "stars:>1", type: REPOSITORY, first: 100, after: $cursor) {
    pageInfo {
      endCursor
      hasNextPage
    }
    nodes {
      ... on Repository {
        nameWithOwner
        createdAt
        updatedAt
        primaryLanguage { name }
        releases { totalCount }
        pullRequests(states: MERGED) { totalCount }
        issues { totalCount }
        closedIssues: issues(states: CLOSED) { totalCount }
      }
    }
  }
}
"""

def fetch_repositories():
    repositories = []
    cursor = None
    
    while len(repositories) < 100:
        variables = {"cursor": cursor}
        response = requests.post(
            "https://api.github.com/graphql", 
            headers=HEADERS, 
            json={"query": graphql_query, "variables": variables}
        )
        
        if response.status_code != 200:
            print("Erro na requisição:", response.text)
            break
        
        data = response.json()
        search_results = data["data"]["search"]
        repositories.extend(search_results["nodes"])
        
        if not search_results["pageInfo"]["hasNextPage"]:
            break
        
        cursor = search_results["pageInfo"]["endCursor"]
    
    return repositories[:100]

def process_data(repos):
    processed = []
    for repo in repos:
        created_at = repo["createdAt"]
        updated_at = repo["updatedAt"]
        age = (pd.Timestamp.now() - pd.Timestamp(created_at)).days // 365
        last_update_days = (pd.Timestamp.now() - pd.Timestamp(updated_at)).days
        
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

def main():
    repos = fetch_repositories()
    processed_data = process_data(repos)
    with open("github_data.json", "w") as f:
        json.dump(processed_data, f, indent=4)
    print("Dados coletados e salvos com sucesso!")

if __name__ == "__main__":
    main()