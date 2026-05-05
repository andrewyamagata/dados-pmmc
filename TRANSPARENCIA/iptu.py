import os

input_dir = r"C:\Users\Positivo\Downloads\SIC"
output_dir = r"C:\Users\Positivo\Downloads\SIC\iptu_dividido"

os.makedirs(output_dir, exist_ok=True)

MAX_SIZE = 10 * 1024 * 1024  # 10 MB

for nome_arquivo in os.listdir(input_dir):
    if nome_arquivo.startswith("pmmc_iptu_") and nome_arquivo.endswith(".csv"):
        caminho_entrada = os.path.join(input_dir, nome_arquivo)

        with open(caminho_entrada, 'r', encoding='latin-1') as f:
            header = f.readline()

            parte = 1
            tamanho_atual = 0

            caminho_saida = os.path.join(
                output_dir,
                nome_arquivo.replace(".csv", f"_part{parte}.csv")
            )
            out = open(caminho_saida, 'w', encoding='latin-1')
            out.write(header)
            tamanho_atual += len(header.encode('latin-1'))

            for linha in f:
                tamanho_linha = len(linha.encode('latin-1'))

                if tamanho_atual + tamanho_linha > MAX_SIZE:
                    out.close()
                    parte += 1

                    caminho_saida = os.path.join(
                        output_dir,
                        nome_arquivo.replace(".csv", f"_part{parte}.csv")
                    )
                    out = open(caminho_saida, 'w', encoding='latin-1')
                    out.write(header)
                    tamanho_atual = len(header.encode('latin-1'))

                out.write(linha)
                tamanho_atual += tamanho_linha

            out.close()

        print(f"Dividido: {nome_arquivo}")