import requests
import pandas as pd

base_url = "https://apidadosabertos.saude.gov.br/arboviroses/dengue"

limit = 100
offset = 0
dados = []
pagina = 0

while True:
    params = {"nu_ano": 2025, "limit": limit, "offset": offset}
    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        print(f"Erro na requisição: {response.status_code}")
        break

    registros = response.json()

    
    if not registros:
        break

    dados.extend(registros)

    offset += 1

    if offset == 10:
        break

      
df = pd.DataFrame(dados)

df.to_csv("dados_dengue.csv", index=False,  encoding="utf-8")
print("Arquivo salvo: dados_dengue.csv")
print(f"Número de registros retornados: {len(dados)}")