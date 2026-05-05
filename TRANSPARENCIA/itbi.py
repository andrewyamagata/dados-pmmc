import pandas as pd
import os

imob = r"C:\Users\Positivo\Downloads\SIC\pmmc_itbi_2016_2018.CSV"

# Leitura
df = pd.read_csv(imob, sep=';', encoding='latin-1')

# (Opcional, mas recomendado) garantir tipo correto
df['exercicio'] = df['exercicio'].astype(int)

# Conferência rápida
print(df['exercicio'].value_counts().sort_index())

# Criar pasta de saída
output_dir = r"C:\Users\Positivo\Downloads\SIC\saida_por_exercicio"
os.makedirs(output_dir, exist_ok=True)

# Separar e salvar
for ano, grupo in df.groupby('exercicio'):
    caminho = os.path.join(output_dir, f"iptu_itbi_{ano}.csv")
    grupo.to_csv(caminho, sep=';', index=False, encoding='latin-1')
    print(f"Arquivo gerado: {caminho}")

# Preview
print(df.head())