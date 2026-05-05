import os

arquivo_entrada = r"C:\Users\Positivo\Downloads\SIC\pmmc_imobiliario_2024.CSV"
output_dir = r"C:\Users\Positivo\Downloads\SIC\imobiliario_dividido"

os.makedirs(output_dir, exist_ok=True)

MAX_SIZE = 10 * 1024 * 1024  # 10 MB

with open(arquivo_entrada, 'r', encoding='latin-1') as f:
    header = f.readline()

    parte = 1
    tamanho_atual = 0

    nome_base = os.path.basename(arquivo_entrada).replace(".CSV", "")

    caminho_saida = os.path.join(output_dir, f"{nome_base}_part{parte}.csv")
    out = open(caminho_saida, 'w', encoding='latin-1')
    out.write(header)
    tamanho_atual += len(header.encode('latin-1'))

    for linha in f:
        tamanho_linha = len(linha.encode('latin-1'))

        if tamanho_atual + tamanho_linha > MAX_SIZE:
            out.close()
            parte += 1

            caminho_saida = os.path.join(output_dir, f"{nome_base}_part{parte}.csv")
            out = open(caminho_saida, 'w', encoding='latin-1')
            out.write(header)
            tamanho_atual = len(header.encode('latin-1'))

        out.write(linha)
        tamanho_atual += tamanho_linha

    out.close()

print("Arquivo dividido com sucesso.")