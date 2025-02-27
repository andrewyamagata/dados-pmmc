import pandas as pd

arquivo = "alertas_estado_sp.csv"

df = pd.read_csv(arquivo)

df_mogi = df[df['city'].str.contains("Mogi das Cruzes",na=False,case=False)]

df_mogi.to_csv("alertas_mogi.csv", index=False, encoding="UTF-8")

print("Arquivo Gerado com Sucesso")