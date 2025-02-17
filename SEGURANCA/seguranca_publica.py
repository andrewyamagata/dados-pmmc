import os
import pandas as pd

# Defina o caminho da pasta onde estão os arquivos
pasta = r"C:\Users\andre\OneDrive - PRODESP\Documentos - CODATA-GIDE\UNIFICAÇÃO DE BASES\SEGURANÇA PÚBLICA\DADOS\XLSX"

# Lista para armazenar os DataFrames processados
dataframes = []

# Lista com os meses do ano
meses = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

# Percorre os arquivos na pasta
for arquivo in os.listdir(pasta):
    if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
        caminho_arquivo = os.path.join(pasta, arquivo)

        # Lê o arquivo sem definir um cabeçalho (para capturar colunas sem nome)
        df = pd.read_excel(caminho_arquivo, header=None)

        # Define o nome correto da primeira coluna (antes estava em branco)
        df.iloc[0, 0] = "Categoria"  

        # Usa a primeira linha como cabeçalho real
        df.columns = df.iloc[0]  
        df = df[1:].reset_index(drop=True)  # Remove a linha original de cabeçalho

        # Ajusta o número de colunas conforme o arquivo
        num_colunas = len(df.columns) - 1
        df.columns = ["Categoria"] + meses[:num_colunas]

        # Identifica o tipo do arquivo com base no nome
        nome_base = os.path.splitext(arquivo)[0]
        if "Criminal" in nome_base:
            tipo = "Criminal"
        elif "ProdutividadePolicial" in nome_base:
            tipo = "Produtividade Policial"
        else:
            tipo = "Desconhecido"

        # Extrai a unidade e o ano do nome do arquivo
        partes = nome_base.rsplit("_", 1)
        if len(partes) == 2:
            unidade = partes[0].replace("OcorrenciaMensal(Criminal)-", "").replace("OcorrenciaMensal(ProdutividadePolicial)-", "").strip()
            ano = partes[1]
        else:
            unidade = "Desconhecido"
            ano = "Desconhecido"

        # Transforma o DataFrame de formato largo para longo (melt)
        df_long = df.melt(id_vars=["Categoria"], var_name="Mês", value_name="Valor")

        # Adiciona colunas de unidade, ano e tipo
        df_long["Unidade"] = unidade
        df_long["Ano"] = ano
        df_long["Tipo"] = tipo

        # Adiciona ao conjunto de dados final
        dataframes.append(df_long)

# Concatena todos os DataFrames em um único
df_final = pd.concat(dataframes, ignore_index=True)

# Salva o resultado consolidado em um arquivo Excel
df_final.to_excel("dados_unificados.xlsx", index=False)

print("Arquivos processados com sucesso!")
