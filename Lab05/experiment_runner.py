
import requests
import time
import json
import csv

# URLs das APIs
REST_API_URL = "http://127.0.0.1:5000"
GRAPHQL_API_URL = "http://127.0.0.1:5001/graphql"

# Número de requisições para cada cenário
NUM_REQUESTS = 100  # Reduzido para teste rápido

def run_rest_experiment(results):
    print("\n--- Executando Experimento REST ---")
    # Consulta Simples: Obter um usuário pelo ID
    for i in range(1, NUM_REQUESTS + 1):
        user_id = (i % 1000) + 1  # Garante que o ID do usuário esteja dentro do range de 1 a 1000
        start_time = time.time()
        try:
            response = requests.get(f"{REST_API_URL}/users/{user_id}")
            response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # em milissegundos
            response_size = len(response.content)  # em bytes
            results.append(["REST", "Simple Query", user_id, response_time, response_size, "Success"])
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição REST (Simple Query) para o usuário {user_id}: {e}")
            results.append(["REST", "Simple Query", user_id, 0, 0, f"Error: {e}"])

    # Consulta com Múltiplos Itens: Obter todos os usuários
    start_time = time.time()
    try:
        response = requests.get(f"{REST_API_URL}/users")
        response.raise_for_status()
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        response_size = len(response.content)
        results.append(["REST", "All Users Query", "N/A", response_time, response_size, "Success"])
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição REST (All Users Query): {e}")
        results.append(["REST", "All Users Query", "N/A", 0, 0, f"Error: {e}"])

    # Consulta com Filtragem: Obter usuários de uma cidade específica
    city_name = "City 1"
    start_time = time.time()
    try:
        response = requests.get(f"{REST_API_URL}/users?city={city_name}")
        response.raise_for_status()
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        response_size = len(response.content)
        results.append(["REST", "Filtered Query", city_name, response_time, response_size, "Success"])
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição REST (Filtered Query) para a cidade {city_name}: {e}")
        results.append(["REST", "Filtered Query", city_name, 0, 0, f"Error: {e}"])

def run_graphql_experiment(results):
    print("\n--- Executando Experimento GraphQL ---")
    headers = {"Content-Type": "application/json"}

    # Consulta Simples: Obter um usuário pelo ID
    for i in range(1, NUM_REQUESTS + 1):
        user_id = (i % 1000) + 1
        query = """
            query GetUser($id: Int!) {
                user(id: $id) {
                    id
                    name
                    email
                    city
                }
            }
        """
        variables = {"id": user_id}
        start_time = time.time()
        try:
            response = requests.post(GRAPHQL_API_URL, headers=headers, json={
                                     "query": query, "variables": variables})
            response.raise_for_status()
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            response_size = len(response.content)
            results.append(["GraphQL", "Simple Query", user_id, response_time, response_size, "Success"])
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição GraphQL (Simple Query) para o usuário {user_id}: {e}")
            results.append(["GraphQL", "Simple Query", user_id, 0, 0, f"Error: {e}"])

    # Consulta com Múltiplos Itens: Obter todos os usuários
    query = """
        query {
            allUsers {
                id
                name
                email
                city
            }
        }
    """
    start_time = time.time()
    try:
        response = requests.post(GRAPHQL_API_URL, headers=headers, json={"query": query})
        response.raise_for_status()
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        response_size = len(response.content)
        results.append(["GraphQL", "All Users Query", "N/A", response_time, response_size, "Success"])
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição GraphQL (All Users Query): {e}")
        results.append(["GraphQL", "All Users Query", "N/A", 0, 0, f"Error: {e}"])

    # Consulta com Filtragem: Obter usuários de uma cidade específica
    city_name = "City 1"
    query = """
        query GetUsersByCity($city: String!) {
            usersByCity(city: $city) {
                id
                name
                email
                city
            }
        }
    """
    variables = {"city": city_name}
    start_time = time.time()
    try:
        response = requests.post(GRAPHQL_API_URL, headers=headers, json={
                                 "query": query, "variables": variables})
        response.raise_for_status()
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        response_size = len(response.content)
        results.append(["GraphQL", "Filtered Query", city_name, response_time, response_size, "Success"])
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição GraphQL (Filtered Query) para a cidade {city_name}: {e}")
        results.append(["GraphQL", "Filtered Query", city_name, 0, 0, f"Error: {e}"])

def main():
    results = []
    headers = ["API_Type", "Query_Type", "Query_Param", "Response_Time_ms", "Response_Size_bytes", "Status"]

    run_rest_experiment(results)
    run_graphql_experiment(results)

    # Salvar resultados em CSV
    with open("experiment_results.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)
        csv_writer.writerows(results)
    print("\nExperimento concluído. Resultados salvos em experiment_results.csv")

if __name__ == "__main__":
    main()


