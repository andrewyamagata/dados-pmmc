import pandas as pd

imob = r"C:\Users\Positivo\Downloads\SIC\pmmc_imobiliario_2024.CSV"
imobiliario = "/mnt/c/Users/Positivo/Downloads/SIC/pmmc_imobiliario_2024.CSV"

df = pd.read_csv(imobiliario,sep=';',encoding='latin-1')

print(df.head())