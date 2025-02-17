import os
import pandas as pd

pasta = r"C:\Users\andre\OneDrive - PRODESP\Documentos - CODATA-GIDE\UNIFICAÇÃO DE BASES\SEGURANÇA PÚBLICA\DADOS\XLSX"

dataframes = []

meses = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

for arquivo in os.listdir(pasta):
    if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
        caminho_arquivo = os.path.join(pasta,arquivo)

        df = pd.read_excel(caminho_arquivo, header=None)

        df.iloc[0, 0] = "Categoria"
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True) 

        nome_base = os.path.splitext(arquivo)[0]

        if "Criminal" in nome_base:
            tipo = "Criminal"
        elif "ProdutividadePolicial" in nome_base:
            tipo = "Produtividade Policial"
        else:
            tipo = "Desconhecido"

        partes = nome_base.rsplit("_",1)
        if len(partes) == 2:
            unidade = partes[0].replace("OcorrenciaMensal(Criminal)-", "").replace("OcorrenciaMensal(ProdutividadePolicial)-", "").strip()
            ano = partes[1]
        else:
            unidade = "Desconhecido"
            ano = "Desconhecido"

        num_colunas = len(df.columns) - 1
        df.columns = ["Categoria"] + meses[:num_colunas]

        df_long = df.melt(id_vars=["Categoria"], var_name="Mês", value_name="Valor")

        df_long["Unidade"] = unidade
        df_long["Ano"] = ano
        df_long["Tipo"] = tipo

        dataframes.append(df_long)

df_final = pd.concat(dataframes, ignore_index=True)

df_final.to_excel("dados_unificados.xlsx", index=False)

print("Arquivos processados")