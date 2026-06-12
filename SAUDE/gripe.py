import pandas as pd

arquivo_gripe = r"C:\Users\Positivo\OneDrive - PRODESP\GIDE - Documentos\PROJETOS\GRIPE - VACINAÇÃO\DADOS\PARQUET\bairro_tratado (1).parquet"

df_gripe = pd.read_parquet(arquivo_gripe)

print(df_gripe.info())
print(len(df_gripe))