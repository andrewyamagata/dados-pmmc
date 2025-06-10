import pdfplumber
import pandas as pd

# Abre o PDF
with pdfplumber.open("EMPRESAS RECLAMADAS 2024.pdf") as pdf:
    all_data = []
    
    # Para cada página
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            df = pd.DataFrame(table[1:], columns=table[0])  # Ignora o cabeçalho na primeira linha
            all_data.append(df)

# Junta todas as tabelas
result = pd.concat(all_data, ignore_index=True)

# Exporta para CSV ou Excel
result.to_csv("empresas_reclamadas_2024.csv", encoding="ISO-8859-1", sep=";", index=False)
# ou
# result.to_excel("empresas_reclamadas_2024.xlsx", index=False)
