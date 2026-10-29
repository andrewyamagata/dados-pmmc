
import requests
import pandas as pd
import sys

from urllib.parse import urljoin
from datetime import datetime
from contextlib import redirect_stdout

# API de equipamentos
URL_INICIAL = (
    "https://dadosadm.mogidascruzes.sp.gov.br/api/equipamentos"
)

sessao = requests.Session()
sessao.headers.update({"Accept": "application/json"})

url = URL_INICIAL
urls_visitadas = set()
registros = []
resumo_paginas = []
erros = []

pagina = 0
total_informado_api = None

while url:
    if url in urls_visitadas:
        erros.append(f"URL repetida na paginação: {url}")
        break

    urls_visitadas.add(url)
    pagina += 1

    try:
        resposta = sessao.get(url, timeout=60)
        resposta.raise_for_status()
        dados = resposta.json()
    except Exception as e:
        erros.append(f"Erro na página {pagina}: {e}")
        break

    # A API pode retornar uma lista diretamente
    if isinstance(dados, list):
        resultados = dados
        proxima_url = None

    # Ou retornar resultados paginados
    elif isinstance(dados, dict) and "results" in dados:
        resultados = dados.get("results") or []
        proxima_url = dados.get("next")

        if pagina == 1:
            total_informado_api = dados.get("count")

    else:
        erros.append(
            f"Formato inesperado na página {pagina}: "
            f"{type(dados).__name__}"
        )
        break

    # Guarda cada registro e sua página de origem
    for registro in resultados:
        if isinstance(registro, dict):
            item = registro.copy()
            item["_pagina_api"] = pagina
            item["_url_pagina"] = url
            registros.append(item)
        else:
            erros.append(
                f"Registro não é um objeto na página {pagina}"
            )

    resumo_paginas.append({
        "pagina": pagina,
        "registros": len(resultados),
        "url": url,
        "proxima_pagina": proxima_url
    })

    print(
        f"Página {pagina}: {len(resultados)} registros"
    )

    # Aceita URLs relativas ou absolutas no campo next
    url = urljoin(url, proxima_url) if proxima_url else None

# Transforma os registros em tabela
df = pd.DataFrame(registros)

print("\n========== RESUMO ==========")
print("Páginas consultadas:", pagina)
print("Total coletado:", len(df))
print("Total informado pela API:", total_informado_api)

# Verifica duplicatas pelo ID
if not df.empty and "id" in df.columns:
    df["id"] = df["id"]

    duplicados = df[
        df["id"].notna()
        & df["id"].duplicated(keep=False)
    ].sort_values(["id", "_pagina_api"])

    print("IDs únicos:", df["id"].nunique())
    print("IDs repetidos distintos:",
          duplicados["id"].nunique())
    print("Linhas com ID repetido:", len(duplicados))

    if not duplicados.empty:
        print("\n========== IDs REPETIDOS ==========")
        print(
            duplicados[
                ["id", "_pagina_api", "_url_pagina"]
            ].sort_values(["id", "_pagina_api"]).to_string(index=False)
        )

        print("\n========== RESUMO POR ID ==========")
        print(
            duplicados.groupby("id").agg(
                quantidade=("id", "size"),
                paginas=("_pagina_api",
                         lambda x: list(sorted(set(x))))
            ).reset_index().to_string(index=False)
        )
else:
    print("A coluna 'id' não foi encontrada.")

print("\n========== RESUMO POR PÁGINA ==========")
print(pd.DataFrame(resumo_paginas).to_string(index=False))

if erros:
    print("\n========== ERROS ==========")
    for erro in erros:
        print(erro)

# Exporta os dados completos, sem remover duplicatas
df.to_csv(
    "equipamentos_diagnostico.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivo gerado: equipamentos_diagnostico.csv")

nome_arquivo = (
    "relatorio_equipamentos_"
    + datetime.now().strftime("%Y%m%d_%H%M%S")
    + ".txt"
)

with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
    with redirect_stdout(arquivo):
        print("========== RESUMO ==========")
        print("Páginas consultadas:", pagina)
        print("Total coletado:", len(df))
        print("Total informado pela API:", total_informado_api)

        if not df.empty and "id" in df.columns:
            duplicados = df[
                df["id"].notna()
                & df["id"].duplicated(keep=False)
            ].sort_values(["id", "_pagina_api"])

            print("IDs únicos:", df["id"].nunique())
            print("IDs repetidos distintos:", duplicados["id"].nunique())
            print("Linhas com ID repetido:", len(duplicados))

            print("\n========== IDs REPETIDOS ==========")
            print(
                duplicados[
                    ["id", "_pagina_api", "_url_pagina"]
                ].to_string(index=False)
            )

            print("\n========== RESUMO POR ID ==========")
            print(
                duplicados.groupby("id").agg(
                    quantidade=("id", "size"),
                    paginas=(
                        "_pagina_api",
                        lambda x: sorted(set(x))
                    )
                ).reset_index().to_string(index=False)
            )




        print("\n========== REGISTROS COM TODOS OS CAMPOS VAZIOS ==========")

        colunas_dados = [
            coluna for coluna in df.columns
            if coluna not in ["_pagina_api", "_url_pagina"]
        ]

        if colunas_dados:
            # Considera nulos, textos vazios e espaços como vazios
            dados_vazios = df[colunas_dados].apply(
                lambda coluna: coluna.map(
                    lambda valor: (
                        pd.isna(valor)
                        or (
                            isinstance(valor, str)
                            and valor.strip() == ""
                        )
                    )
                )
            )

            mascara_vazios = dados_vazios.all(axis=1)
            registros_vazios = df[mascara_vazios]

            if registros_vazios.empty:
                print("Nenhum registro totalmente vazio encontrado.")
            else:
                print("Total de registros vazios:", len(registros_vazios))

                print(
                    registros_vazios[
                        ["_pagina_api", "_url_pagina"]
                    ].to_string(index=False)
                )

                print("\nQuantidade por página:")
                print(
                    registros_vazios.groupby("_pagina_api")
                    .size()
                    .reset_index(name="quantidade")
                    .to_string(index=False)
                )
        else:
            print("Não há colunas de dados para verificar.")



        print("\n========== RESUMO POR PÁGINA ==========")
        print(pd.DataFrame(resumo_paginas).to_string(index=False))

        if erros:
            print("\n========== ERROS ==========")
            for erro in erros:
                print(erro)

print("Relatório salvo em:", nome_arquivo)

