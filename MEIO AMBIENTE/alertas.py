import pandas as pd

arquivo = "alert_report.csv"

df = pd.read_csv(arquivo)

df_mogi = df[df['state'].str.contains("São Paulo",na=False,case=False)]

df_mogi.to_csv("alertas_estado_sp.csv", index=False, encoding="UTF-8")

print("Arquivo Gerado com Sucesso")