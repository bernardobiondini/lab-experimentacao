from writer import write, process_data
from github_api import fetch_repositories

def main():
    repos = fetch_repositories()
    processed_data = process_data(repos)
    write(processed_data)
    print("Dados coletados e salvos com sucesso!")

if __name__ == "__main__":
    main()