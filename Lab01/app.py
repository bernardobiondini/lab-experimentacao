from writer import write, process_data
from github_api import fetch_repositories
from data import generate_graphics

def main():
    repos = fetch_repositories()
    processed_data = process_data(repos)
    write(processed_data)
    generate_graphics()
    print("Dados coletados e salvos com sucesso!")

if __name__ == "__main__":
    main()