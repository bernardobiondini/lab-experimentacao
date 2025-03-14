import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import get_current_folder
import os

def generate_graphics():
    graficos_folder = os.path.join(get_current_folder(), "graficos")
    os.makedirs(graficos_folder, exist_ok=True)
    # Carregar os dados (supondo que o CSV esteja no diretório correto)
    filePath = os.path.join(get_current_folder(), "github_data.csv")
    df = pd.read_csv(filePath)
    
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', utc=True)

    mean_age = (pd.Timestamp.now().tz_localize(None) - df['created_at'].dt.tz_localize(None)).dt.days.mean()
    mode_age = ((pd.Timestamp.now().tz_localize(None) - df['created_at'].dt.tz_localize(None)).dt.days // 365).mode()
    mean_prs = df['pull_requests'].mean()
    mode_prs = df['pull_requests'].mode()
    mean_releases = df['releases'].mean()
    mode_releases = df['releases'].mode()
    mean_updates = df['last_update_days'].mean()
    mode_updates = df['last_update_days'].mode()
    language_counts = df['language'].value_counts()
    mean_closed_issues = (df['closed_issues'] / df['total_issues']).mean()
    mode_closed_issues = (df['closed_issues'] / df['total_issues']).mode()

    # Criar gráficos
    sns.set_theme(style="whitegrid")

    # Gráfico da idade dos repositórios
    plt.figure(figsize=(8,5))
    sns.histplot((pd.Timestamp.now().tz_localize(None) - df['created_at'].dt.tz_localize(None)).dt.days, bins=20, kde=True)
    plt.xlabel("Idade do repositório (dias)")
    plt.ylabel("Frequência")
    plt.title("Distribuição da Idade dos Repositórios Populares")
    plt.savefig(graficos_folder + "/idade_repositorios.png")
    plt.close()

    # Gráfico do número de PRs
    plt.figure(figsize=(8,5))
    sns.boxplot(x=df['pull_requests'])
    plt.xlabel("Número de Pull Requests Aceitas")
    plt.title("Distribuição de Pull Requests por Repositório")
    plt.savefig(graficos_folder + "/pull_requests.png")
    plt.close()

    # Gráfico do número de releases
    plt.figure(figsize=(8,5))
    sns.boxplot(x=df['releases'])
    plt.xlabel("Número de Releases")
    plt.title("Distribuição de Releases por Repositório")
    plt.savefig(graficos_folder + "/releases.png")
    plt.close()

    # Gráfico do tempo desde a última atualização
    plt.figure(figsize=(8,5))
    sns.histplot(df['last_update_days'], bins=20, kde=True)
    plt.xlabel("Dias desde última atualização")
    plt.ylabel("Frequência")
    plt.title("Tempo desde Última Atualização dos Repositórios")
    plt.savefig(graficos_folder + "/ultima_atualizacao.png")
    plt.close()

    # Gráfico de linguagens mais usadas
    plt.figure(figsize=(8,5))
    language_counts[:10].plot(kind='bar', color='c')
    plt.xlabel("Linguagem")
    plt.ylabel("Número de Repositórios")
    plt.title("Top 10 Linguagens em Repositórios Populares")
    plt.xticks(rotation=45)
    plt.savefig(graficos_folder + "/linguagens.png")
    plt.close()

    # Gráfico da porcentagem de issues fechadas
    plt.figure(figsize=(8,5))
    sns.histplot(df['closed_issues'] / df['total_issues'], bins=20, kde=True)
    plt.xlabel("Proporção de Issues Fechadas")
    plt.ylabel("Frequência")
    plt.title("Distribuição da Proporção de Issues Fechadas por Repositório")
    plt.savefig(graficos_folder + "/issues_fechadas.png")
    plt.close()

    # Exibir medianas calculadas
    print(f"Média da Idade dos Repositórios: {mean_age} dias")
    print(f"Moda da Idade dos Repositórios: {mode_age.values[0]} anos")
    print(f"Média de Pull Requests Aceitas: {mean_prs}")
    print(f"Moda de Pull Requests Aceitas: {mode_prs.values[0]}")
    print(f"Média de Releases: {mean_releases}")
    print(f"Moda de Releases: {mode_releases.values[0]}")
    print(f"Média de Tempo desde Última Atualização: {mean_updates} dias")
    print(f"Moda de Tempo desde Última Atualização: {mode_updates.values[0]} dias")
    print(f"Média da Proporção de Issues Fechadas: {mean_closed_issues:.2f}")
    print(f"Moda da Proporção de Issues Fechadas: {mode_closed_issues.values[0]:.2f}")
