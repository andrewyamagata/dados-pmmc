import requests
import pandas as pd

# URL da API (pegando só 100 registros)
url = "https://apidadosabertos.saude.gov.br/arboviroses/dengue?nu_ano=2024&limit=100&offset=0"

# Fazendo a requisição
response = requests.get(url)

# Verifica se a resposta foi bem-sucedida
if response.status_code == 200:
    dados = response.json()  # Converte para JSON
    
    # Verifica se a chave "parametros" está nos dados
    if "parametros" in dados:
        lista_dados = dados["parametros"]  # Lista de registros
        
        # Criar DataFrame
        df = pd.DataFrame(lista_dados)

        # Mostrar as primeiras linhas
        print(df.head(10))  # Para evitar poluir o terminal, exibindo só 10 linhas
        
        # Opcional: Salvar em CSV para análise
        df.to_csv("dengue.csv", index=False)
        print("Arquivo salvo: dengue.csv")
    else:
        print("Chave 'parametros' não encontrada na resposta da API.")

else:
    print(f"Erro na requisição: {response.status_code}")

print(f"Número de registros retornados: {len(lista_dados)}")


