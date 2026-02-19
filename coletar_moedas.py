import requests
import pandas as pd
from datetime import datetime, timedelta


periodo_dias = 30  # pode mudar para 7, 30 ou 90

# Códigos das moedas (Banco Central)
moedas = {
    "Dolar": 10813,
    "Euro": 21619,
    "Libra": 21623,
    "Iene": 21621
}


data_final = datetime.today()
data_inicial = data_final - timedelta(days=periodo_dias)

data_inicial_str = data_inicial.strftime("%d/%m/%Y")
data_final_str = data_final.strftime("%d/%m/%Y")


def buscar_dados(codigo_serie, nome_moeda):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados"
    
    params = {
        "formato": "json",
        "dataInicial": data_inicial_str,
        "dataFinal": data_final_str
    }
    
    response = requests.get(url, params=params)
    dados = response.json()
    
    df = pd.DataFrame(dados)
    df["valor"] = df["valor"].astype(float)
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)
    df["moeda"] = nome_moeda
    
    return df


lista_dfs = []

for nome, codigo in moedas.items():
    df_moeda = buscar_dados(codigo, nome)
    lista_dfs.append(df_moeda)

df_final = pd.concat(lista_dfs)


df_final.to_csv("cotacoes_moedas.csv", index=False)

print("Arquivo CSV gerado com sucesso!")
