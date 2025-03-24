# Relatório Final - Análise das Características de Qualidade de Sistemas Java

## 1. Introdução

O objetivo deste estudo é analisar aspectos da qualidade de repositórios desenvolvidos na linguagem Java, correlacionando-os com características do seu processo de desenvolvimento. Para isso, foram coletadas diversas métricas de qualidade utilizando a ferramenta CK, e os dados foram cruzados com informações sobre popularidade, tamanho, atividade e maturidade dos repositórios.

## 2. Metodologia

### 2.1 Coleta de Dados

A coleta de dados seguiu os seguintes passos:

1. Foram extraídos os **1.000 repositórios Java mais populares** do GitHub utilizando a API REST do GitHub.
2. Para cada repositório, foram coletadas informações como:
   * **Popularidade** : número de estrelas.
   * **Tamanho** : linhas de código (LOC) e linhas comentadas (CLOC).
   * **Atividade** : número de releases (aproximado pelo número de forks).
   * **Maturidade** : idade do repositório, calculada com base na data de criação.
3. Os repositórios foram clonados localmente, e a ferramenta **CK** foi utilizada para calcular métricas de qualidade, incluindo:
   * **CBO** (Coupling Between Objects)
   * **DIT** (Depth Inheritance Tree)
   * **LCOM** (Lack of Cohesion of Methods)
4. Os resultados foram consolidados em um arquivo **final_metrics.csv** contendo os valores agregados por repositório.

### 2.2 Perguntas de Pesquisa

As seguintes perguntas de pesquisa foram formuladas para orientar a análise:

* **RQ 01:** Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
* **RQ 02:** Qual a relação entre a maturidade dos repositórios e as suas características de qualidade?
* **RQ 03:** Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
* **RQ 04:** Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?

### 2.3 Hipóteses

Antes da análise dos dados, formulamos as seguintes hipóteses:

1. **Repositórios mais populares (mais estrelas) tendem a ser maiores (mais linhas de código).**
2. **Repositórios mais maduros (mais antigos) apresentam menor acoplamento (CBO) devido a refatorações ao longo do tempo.**
3. **Repositórios com mais releases possuem maior coesão (menor LCOM).**
4. **Projetos com maior profundidade de herança (DIT) são mais difíceis de manter.**

## 3. Resultados

> **Nota:** Os resultados ainda estão em processamento e serão adicionados nesta seção posteriormente.

## 4. Discussão

Com base nos resultados obtidos, discutiremos a validade das hipóteses formuladas e a relação entre as métricas analisadas. Gráficos de correlação serão apresentados para evidenciar padrões e comportamentos entre os repositórios Java.

## 5. Conclusão

A conclusão será formulada com base na análise dos dados obtidos, indicando se as hipóteses foram confirmadas ou refutadas. Além disso, serão sugeridas melhorias na metodologia e possíveis direções para estudos futuros.

---

**Bônus:** Para melhor análise, também serão gerados **gráficos de correlação** e será aplicado um teste estatístico (como Spearman ou Pearson) para validar as relações entre as variáveis.
