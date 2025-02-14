import requests
import pandas as pd

url = "https://apidadosabertos.saude.gov.br/arboviroses/dengue?nu_ano=2024&limit=100&offset=0"

response = requests.get(url)

if response.status_code == 200:
    dados = response.json()
    
    if "parametros" in dados:
        lista_dados = dados["parametros"]
        
        df = pd.DataFrame(lista_dados)

        print(df.head(10))
        
        df.to_csv("dengue.csv", index=False)
        print("Arquivo salvo: dengue.csv")
    else:
        print("Chave 'parametros' não encontrada na resposta da API.")

else:
    print(f"Erro na requisição: {response.status_code}")

print(f"Número de registros retornados: {len(lista_dados)}")