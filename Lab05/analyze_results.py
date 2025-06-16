
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os resultados do experimento
df = pd.read_csv("experiment_results.csv")

# Análise para RQ1: Respostas às consultas GraphQL são mais rápidas que respostas às consultas REST?
print("\n--- Análise de Tempo de Resposta (RQ1) ---")
response_time_summary = df.groupby("API_Type")["Response_Time_ms"].describe()
print(response_time_summary)

# Visualização para RQ1
plt.figure(figsize=(10, 6))
sns.boxplot(x="API_Type", y="Response_Time_ms", data=df)
plt.title("Tempo de Resposta: GraphQL vs REST")
plt.xlabel("Tipo de API")
plt.ylabel("Tempo de Resposta (ms)")
plt.savefig("response_time_boxplot.png")
plt.close()

# Análise para RQ2: Respostas às consultas GraphQL tem tamanho menor que respostas às consultas REST?
print("\n--- Análise de Tamanho de Resposta (RQ2) ---")
response_size_summary = df.groupby("API_Type")["Response_Size_bytes"].describe()
print(response_size_summary)

# Visualização para RQ2
plt.figure(figsize=(10, 6))
sns.boxplot(x="API_Type", y="Response_Size_bytes", data=df)
plt.title("Tamanho da Resposta: GraphQL vs REST")
plt.xlabel("Tipo de API")
plt.ylabel("Tamanho da Resposta (bytes)")
plt.savefig("response_size_boxplot.png")
plt.close()

print("\nAnálise concluída. Gráficos salvos como response_time_boxplot.png e response_size_boxplot.png")


