import pandas as pd

arquivo_gripe = r"C:\Users\Positivo\OneDrive - PRODESP\GIDE - Documentos\PROJETOS\GRIPE - VACINAÇÃO\DADOS\CSV\VDIC_PMMC_GRIPOMETRO.CSV"

df_gripe = pd.read_csv(arquivo_gripe)

print(df_gripe.info())