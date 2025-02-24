import os
import pandas as pd
import re
import warnings
warnings.simplefilter("ignore", UserWarning)

# Defina o caminho da pasta onde estão os arquivos
pasta = r"C:\Users\andre\OneDrive - PRODESP\Documentos - CODATA-GIDE\UNIFICAÇÃO DE BASES\SEGURANÇA PÚBLICA\DADOS\XLSX\2024"

# Extrai o ano da pasta (última parte do caminho)
ano = os.path.basename(pasta)

# Lista para armazenar os DataFrames processados
dataframes = []

# Percorre os arquivos na pasta
for arquivo in os.listdir(pasta):
    if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
        caminho_arquivo = os.path.join(pasta, arquivo)
        
        try:
            # Lê o arquivo sem definir um cabeçalho (para capturar colunas sem nome)
            df = pd.read_excel(caminho_arquivo, engine="openpyxl", header=None)

            # Garante que há pelo menos uma linha para definir como cabeçalho
            if not df.empty and len(df) > 1:
                df.columns = df.iloc[0]  # Usa a primeira linha como cabeçalho real
                df = df[1:].reset_index(drop=True)  # Remove a linha original de cabeçalho

                # 🔹 Extrai informações do nome do arquivo
                categoria_match = re.search(r'\((.*?)\)', arquivo)  # Pega o que está entre parênteses
                unidade_match = re.search(r'-(.*?)_', arquivo)  # Pega o que está entre "-" e "_"

                categoria = categoria_match.group(1) if categoria_match else "Desconhecido"
                unidade = unidade_match.group(1).strip() if unidade_match else "Desconhecido"

                # 🔹 Adiciona as novas colunas ao DataFrame
                df["Categoria"] = categoria
                df["Unidade"] = unidade
                df["Ano"] = ano

                dataframes.append(df)
            else:
                print(f"Aviso: Arquivo '{arquivo}' está vazio ou não possui dados suficientes.")

        except Exception as e:
            print(f"Erro ao processar '{arquivo}': {e}")

# Concatena os DataFrames se houver arquivos válidos
if dataframes:
    df_final = pd.concat(dataframes, ignore_index=True)
    
    # Salva o resultado consolidado em um arquivo Excel
    output_path = os.path.join(pasta, f"OcorrenciaMensal_{ano}.xlsx")
    df_final.to_excel(output_path, index=False)

    print(f"Arquivos processados com sucesso! Dados salvos em: {output_path}")
    print(df_final)
else:
    print("Nenhum arquivo válido foi encontrado para unificação.")