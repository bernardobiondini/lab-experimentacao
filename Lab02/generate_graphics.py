import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import get_current_folder

# Carregar os dados do CSV consolidado
file_path = f"{get_current_folder()}/final_metrics.csv"
df = pd.read_csv(file_path)

# Configuração do estilo dos gráficos
sns.set_theme(style="whitegrid")

# Gráfico 1: Popularidade (Stars) vs Tamanho (Total LOC)
plt.figure(figsize=(8, 6))
sns.scatterplot(x=df["Stars"], y=df["Total LOC"], alpha=0.6)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Popularidade (Stars)")
plt.ylabel("Tamanho do Repositório (LOC)")
plt.title("Relação entre Popularidade e Tamanho do Repositório")
plt.savefig(f"{get_current_folder()}/graphics/stars_vs_loc.png")

# Gráfico 2: Idade do repositório vs CBO
plt.figure(figsize=(8, 6))
sns.regplot(x=df["Repo Age"], y=df["Avg CBO"])
plt.xlabel("Idade do Repositório (Anos)")
plt.ylabel("Acoplamento entre Objetos (CBO)")
plt.title("Relação entre Idade do Repositório e CBO")
plt.savefig(f"{get_current_folder()}/graphics/age_vs_cbo.png")

# Gráfico 3: Releases vs LCOM
plt.figure(figsize=(8, 6))
sns.scatterplot(x=df["Releases"], y=df["Avg LCOM"], alpha=0.6)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Número de Releases")
plt.ylabel("Falta de Coesão dos Métodos (LCOM)")
plt.title("Relação entre Atividade e Coesão do Código")
plt.savefig(f"{get_current_folder()}/graphics/releases_vs_lcom.png")

# Gráfico 4: LOC vs DIT
plt.figure(figsize=(8, 6))
sns.scatterplot(x=df["Total LOC"], y=df["Avg DIT"], alpha=0.6)
plt.xscale("log")
plt.xlabel("Linhas de Código (LOC)")
plt.ylabel("Profundidade da Árvore de Herança (DIT)")
plt.title("Relação entre Tamanho e Profundidade de Herança")
plt.savefig(f"{get_current_folder()}/graphics/loc_vs_dit.png")

# Matriz de correlação para verificar relações entre variáveis
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Matriz de Correlação entre Métricas")
plt.savefig(f"{get_current_folder()}/graphics/correlation_matrix.png")
