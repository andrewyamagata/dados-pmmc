import pandas as pd

imobiliario = r"C:\Users\Positivo\Downloads\SIC\pmmc_imobiliario_2024.CSV"

df = pd.read_csv(imobiliario)

print(df.head())