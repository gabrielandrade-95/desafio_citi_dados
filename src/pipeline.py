import pandas as pd

lista_logs = []

def registrar_log(encontrei, fiz, afetadas, justificativa):
    dic_log = {
        "O que encontrei": encontrei,
        "O que fiz": fiz,
        "Linhas afetadas": afetadas,
        "Justificativa": justificativa
    }
    lista_logs.append(dic_log)

caminho_entrada = '../data/brutos/pedidos_metalurgica_mezzalira.xlsx'
caminho_saida = '../data/processed/planilha_final_mezzalira.xlsx'

#camada bronze, leitura dos dados

print("Iniciando a leitura dos dados da planilha de pedidos...")
df_bronze = pd.read_excel(caminho_entrada)

#criando a aba bronze no arquivo
with pd.ExcelWriter(caminho_saida, engine='openpyxl') as writer:
    df_bronze.to_excel(writer, sheet_name='bronze', index=False)
    print("Aba 'bronze' criada com sucesso no arquivo de saída.")

#criando a camada prata

df_prata = df_bronze.copy()

#removendo linhas vazias
df_prata = df_prata.dropna(how='all')
registrar_log(
    encontrei="Linhas totalmente vazias no final ou meio da planilha",
    fiz="Usei dropna(how='all') para remover a linha",
    afetadas="Todas as linhas que estavam 100% vazias",
    justificativa="Linhas vazias quebram os cálculos de faturamento."
)

#removendo pedidos duplicados
df_prata = df_prata.drop_duplicates()
registrar_log(
    encontrei="Pedidos duplicados",
    fiz="Usei drop_duplicates() para manter apenas a primeira ocorrência",
    afetadas="Linhas com todos os dados idênticos",
    justificativa="Evitar dupla contagem no faturamento final."
)

#paadronizando nomes das cidades em strings sem espaços em branco no início e no final
df_prata["Cidade"] = df_prata["Cidade"].astype(str).str.strip()

#resolvendo o problema de nomes distintos para representar a mesma cidade
df_prata["Cidade"] = df_prata["Cidade"].replace({
    "recife": "Recife",
    "REC": "Recife",
}), regex=False

registrar_log(
    encontrei="Nomes diferentes para Recife na coluna 'Cidade'.",
    fiz="Converti as células da coluna 'Cidade' para string e usei strip() para remover espaços em branco no começo e no final. Também usei replace() pra padronizar os nomes diferentes que tinham apontando para a mesma cidade, no caso Recife.",
    afetadas="Todas as linhas referentes à cidade do Recife",
    justificativa="Garantir o agrupamento correto. Evitar que a cidade do Recife seja contabilizada como duas cidades diferentes no faturamento."
)
#pegando a coluna de valores e transformando tudo em float após remover símbolos

df_prata["Valor (R$)"] = (df_prata["Valor (R$)"].astype(str)
    .str.replace("R$", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False).str.strip()
)
registrar_log(
    encontrei="Valores numéricos digitados como texto ('R$ 630,00')",
    fiz="Removi o 'R$', converti as vírgulas em pontos e transformei em float",
    afetadas="Coluna inteira de 'Valor (R$)'"
    justificativa="Garantir que os valores sejam tratados como números para cálculos de faturamento."
)

#convertendo a coluna de valores para float
df_prata["Valor (R$)"] = (pd.to_numeric(df_prata["Valor (R$)"], errors='coerce'))

#ajustando as datas, usei dayfirst para que o formato seja dia/mes/ano
df_prata["Data do Pedido"] = pd.to_datetime(df_prata["Data do Pedido"], errors='coerce', dayfirst=True)
registrar_log(
    encontrei="Datas em formatos diferente",
    fiz="Usei pd.to_datetime() para forçar o padrão de data e hora, com dayfirst=True para que o formato seja dia/mês/ano",
    afetadas="Coluna inteira de 'Data'",
    justificativa="Necessário para extrair o mês corretamente depois."
)

df_log = pd.DataFrame(lista_logs)

with pd.excel_writer(caminho_saida, engine='openpyxl') as writer:
    df_bronze.to_excel(writer, sheet_name='Bronze', index=False)
    df_prata.to_excel(writer, sheet_name='Prata', index=False)
    df_log.to_excel(writer, sheet_name='Log', index=False)



