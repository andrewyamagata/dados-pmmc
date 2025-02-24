import os
import pandas as pd
import re
import warnings
warnings.simplefilter("ignore", UserWarning)

# Defina o caminho da pasta onde estão os arquivos
pasta_compilado = r"C:\Users\andre\OneDrive - PRODESP\Documentos - CODATA-GIDE\UNIFICAÇÃO DE BASES\SEGURANÇA PÚBLICA\DADOS\XLSX\COMPILADO"

pasta_final = r"C:\Users\andre\OneDrive - PRODESP\Documentos - CODATA-GIDE\UNIFICAÇÃO DE BASES\SEGURANÇA PÚBLICA\DADOS\XLSX"

# Lista para armazenar os DataFrames processados
dataframes = []

# Percorre os arquivos na pasta
for arquivo in os.listdir(pasta_compilado):
    if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
        caminho_arquivo = os.path.join(pasta_compilado, arquivo)
        
        try:
            # Lê o arquivo sem definir um cabeçalho (para capturar colunas sem nome)
            df = pd.read_excel(caminho_arquivo, engine="openpyxl", header=None)

            # Garante que há pelo menos uma linha para definir como cabeçalho
            if not df.empty and len(df) > 1:
                df.columns = df.iloc[0]  # Usa a primeira linha como cabeçalho real
                df = df[1:].reset_index(drop=True)  # Remove a linha original de cabeçalho

                dataframes.append(df)
            else:
                print(f"Aviso: Arquivo '{arquivo}' está vazio ou não possui dados suficientes.")

        except Exception as e:
            print(f"Erro ao processar '{arquivo}': {e}")

# Concatena os DataFrames se houver arquivos válidos
if dataframes:
    df_final = pd.concat(dataframes, ignore_index=True)
    
    # Salva o resultado consolidado em um arquivo Excel
    output_path = os.path.join(pasta_final,"OcorrenciaMensal_Compilado.xlsx")
    df_final.to_excel(output_path, index=False)

    print(f"Arquivos processados com sucesso! Dados salvos em: {output_path}")
    print(f"Total de linhas processadas: {len(df_final)}")
else:
    print("Nenhum arquivo válido foi encontrado para unificação.")