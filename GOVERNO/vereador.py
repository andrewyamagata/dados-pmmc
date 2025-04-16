import pandas as pd
import re


solicitacoes = pd.read_excel(r"C:\Users\andre\OneDrive - PRODESP\Documentos - CODATA-GIDE\UNIFICAÇÃO DE BASES\SOLICITAÇÃO VEREADOR\DADOS\solicitacoes.xlsx")
enderecos = pd.read_excel(r"C:\Users\andre\OneDrive - PRODESP\Documentos - CODATA-GIDE\UNIFICAÇÃO DE BASES\SOLICITAÇÃO VEREADOR\DADOS\enderecos.xlsx")


def extrair_rua(texto):
    padrao = r"\b(Alameda|Avenida|Estrada|Largo|Loteamento|Rodovia|Rua|Travessa|Via|Viela)\s+([^,\.]+)"
    match = re.search(padrao, str(texto), re.IGNORECASE)
    if match:
        return f"{match.group(1)} {match.group(2).strip()}"
    return None


solicitacoes["RUA_EXTRAIDA"] = solicitacoes["SOLICITAÇÃO"].apply(extrair_rua)


def normalizar(texto):
    if pd.isna(texto):
        return ""
    return texto.lower().strip()

solicitacoes["RUA_NORM"] = solicitacoes["RUA_EXTRAIDA"].apply(normalizar)
enderecos["LOGRADOURO_NORM"] = enderecos["LOGRADOURO"].apply(normalizar)


enderecos_deduplicado = enderecos.drop_duplicates(subset="LOGRADOURO_NORM", keep="first")

resultado = solicitacoes.merge(enderecos_deduplicado[["LOGRADOURO_NORM", "CEP"]], 
                                how="left", 
                                left_on="RUA_NORM", 
                                right_on="LOGRADOURO_NORM")



resultado_final = resultado.drop(columns=["RUA_NORM", "LOGRADOURO_NORM"])

resultado_final.to_excel(r"C:\Users\andre\OneDrive - PRODESP\Documentos - CODATA-GIDE\UNIFICAÇÃO DE BASES\SOLICITAÇÃO VEREADOR\DADOS\solicitacoes_com_cep.xlsx", index=False)
