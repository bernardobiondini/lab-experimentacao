import requests
import os
from dotenv import load_dotenv
from utils import get_current_folder

script_dir = get_current_folder()
dotenv_path = os.path.join(script_dir, ".env")

load_dotenv(dotenv_path)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

print(GITHUB_TOKEN)

def get_query():
    return """
        query ($cursor: String) {
            search(query: "stars:>10000", type: REPOSITORY, first: 10, after: $cursor) {
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
                    stargazerCount
                    forkCount
                    watchers { totalCount }
                    collaborators { totalCount }
                }
                }
            }
        }
    """


def fetch_repositories(size = 1000):
    repositories = []
    cursor = None
    
    while len(repositories) < size:
        variables = {"cursor": cursor}
        response = requests.post(
            "https://api.github.com/graphql", 
            headers=HEADERS, 
            json={"query": get_query(), "variables": variables}
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
    
    return repositories[:size]