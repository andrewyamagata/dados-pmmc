import pandas as pd

df = pd.read_excel(r'C:\Users\andre\OneDrive\Documentos\GitHub\dados-pmmc\MULHER\Notificações de Violência 2019 a 2025.xlsx')

arquivo_csv = 'Notificações de Violência 2019 a 2025.csv'
df.to_csv(arquivo_csv, index=False, encoding='utf-8')

print(f'Arquivo salvo como {arquivo_csv}')