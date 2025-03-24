import os
import pandas as pd
from datetime import datetime
from utils import get_current_folder

def process_ck_metrics():
    metrics_folder = f"{get_current_folder()}/metrics"
    repos_file = f"{get_current_folder()}/top_java_repositories.csv"  # Arquivo com dados dos repositórios
    output_file = f"{get_current_folder()}/final_metrics.csv"

    # Carregar informações dos repositórios para cruzar com as métricas
    repos_df = pd.read_csv(repos_file)

    summary_data = []

    # Percorrer todos os arquivos na pasta metrics/
    for file in os.listdir(metrics_folder):
        if file.endswith("_class.csv"):  # Apenas arquivos que terminam com "_class.csv"
            file_path = os.path.join(metrics_folder, file)
            repo_name = file.replace("_metrics_class.csv", "")

            try:
                # Ler CSV e selecionar colunas necessárias
                df = pd.read_csv(file_path, usecols=["loc", "cbo", "lcom", "dit"])

                # Calcular métricas para o repositório
                total_loc = df["loc"].sum()  # Soma das linhas de código
                # total_cloc = df["cloc"].sum()  # Soma das linhas comentadas
                avg_cbo = df["cbo"].mean()  # Média do CBO
                avg_lcom = df["lcom"].mean()  # Média do LCOM
                avg_dit = df["dit"].mean()  # Média do DIT

                # Buscar informações do repositório na tabela original
                repo_info = repos_df[repos_df["Repo Name"].str.contains(repo_name, na=False, case=False)]
                if not repo_info.empty:
                    stars = repo_info["Stars"].values[0]
                    created_at = repo_info["Created At"].values[0]
                    releases = repo_info["Forks"].values[0]
                    size = repo_info["Size (KB)"].values[0]

                    # Calcular idade do repositório
                    repo_age = datetime.now().year - int(created_at[:4])
                else:
                    stars = releases = size = repo_age = None  # Caso não encontre o repositório

                # Adicionar ao conjunto de dados final
                summary_data.append([repo_name, total_loc, avg_cbo, avg_lcom, avg_dit, stars, repo_age, releases, size])

            except Exception as e:
                print(f"Erro ao processar {file}: {e}")

    # Criar DataFrame final
    columns = ["Repo Name", "Total LOC", "Avg CBO", "Avg LCOM", "Avg DIT", "Stars", "Repo Age", "Releases", "Size (KB)"]
    final_df = pd.DataFrame(summary_data, columns=columns)

    # Salvar CSV consolidado
    final_df.to_csv(output_file, index=False)
    print(f"✅ Métricas consolidadas em {output_file}")

if __name__ == "__main__":
    process_ck_metrics()
