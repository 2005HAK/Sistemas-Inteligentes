import pandas as pd
import numpy as np

data = pd.read_csv("data/train_mod.csv", delimiter=",")

len_init = len(data)
# ------------ Modificações preço --------------- #

data = data.dropna(subset=["Preco"])
print(len(data))

print(f"{((len_init - len(data)) / len_init) * 100} % da base excluido por falta do preço")

# ------------ Fim modificação preço ------------- #

print(data["Classificacao_Veiculo"].unique())

data["Classificacao_Veiculo"] = data["Classificacao_Veiculo"].astype(str).str.strip().str.lower()
data["Classificacao_Veiculo"] = (data["Classificacao_Veiculo"] == "semi-novo").astype(int)

print(data["Couro"].unique())

data["Couro"] = data["Couro"].astype(str).str.strip().str.lower()
data["Couro"] = (data["Couro"] == "sim").astype(int)

print(data["Adesivos_personalizados"].unique())

data["Adesivos_personalizados"] = data["Adesivos_personalizados"].astype(str).str.strip().str.lower()
data["Adesivos_personalizados"] = (data["Adesivos_personalizados"] == "sim").astype(int)

# ---------- Modificação dos dados dos combustiveis ----------- #

print(data["Combustivel"].unique())

data["Combustivel"] = data["Combustivel"].astype(str).str.strip().str.lower()
data["Combustivel"] = data["Combustivel"].replace({"gasol.": "gasolina", "dies.": "diesel"})

print(data["Combustivel"].unique())
data = pd.get_dummies(data, columns=["Combustivel"], drop_first=True, dtype=int)

# -------- Fim modificação dos dados dos combustiveis --------- #

# ---------- Remoção da coluna Faixa de preço ------------ #

data= data.drop(columns=["Faixa_Preco"])

# -------- Fim remoção da coluna Faixa de preço ---------- #

# -------- Modificação nas categorias ------------- #

print(data["Categoria"].unique())

data["Categoria"] = data["Categoria"].astype(str).str.strip().str.lower()
data = pd.get_dummies(data, columns=["Categoria"], drop_first=True, dtype=int)

# -------- Fim modificação nas categorias ------------- #

# -------- Modificação no volume do motor ------------- #

volume_turbo = data["Volume_motor"].astype(str).str.lower()

data["Turbo"] = volume_turbo.str.contains("turbo").astype(int)
data["Volume_motor"] = volume_turbo.str.replace("turbo", "").str.strip()
data["Volume_motor"] = data["Volume_motor"].astype(float)

print(data["Volume_motor"].unique())

quantidade_zeros = len(data[data["Volume_motor"] == 0])
total_linhas = len(data)
porcentagem = (quantidade_zeros / total_linhas) * 100

print(porcentagem)

data = data[data["Volume_motor"] > 0]

# -------- Fim modificação no volume do motor ------------- #

# -------- Modificação no tipo de cambio ------------- #

print(data["Tipo_cambio"].unique())

data["Tipo_cambio"] = data["Tipo_cambio"].astype(str).str.strip().str.lower()
data = pd.get_dummies(data, columns=["Tipo_cambio"], drop_first=True, dtype=int)

# -------- Fim modificação no tipo de cambio ------------- #

# -------- Modificações tração ----------------- #

print(data["Tração"].unique())
data["Tração"] = data["Tração"].astype(str).str.strip().str.lower()
data = pd.get_dummies(data, columns=["Tração"], drop_first=True, dtype=int)

# -------- Fim modificação tração --------------- #

# -------- Modificações portas -------------- #

print(data["Portas"].unique())
data["Portas"] = data["Portas"].astype(str).str.strip().str.lower()
dicionario_portas = {
	"2-3": 0,
	"4-5": 1,
	">5": 2
}

data["Portas"] = data["Portas"].map(dicionario_portas)

# -------- Fim modificação portas ------------- #

# -------- Modificação modelo ---------------- #

print(data["Modelo"].nunique())

data = data.drop(columns=["Modelo"])

# -------- Fim modificação modelo ------------- #

# --------- Modificação radio --------------- #

data["Radio_AM_FM"] = data["Radio_AM_FM"].astype(str).str.strip().str.lower()

data["AM"] = data["Radio_AM_FM"].str.contains("am").astype(int)

data["FM"] = data["Radio_AM_FM"].str.contains("fm").astype(int)

data = data.drop(columns=["Radio_AM_FM"])

# ------------- Fim modificação radio ---------------- #

# ------------ Modificacções cor ----------------- #

print(data["Cor"].unique())

data["Cor"] = data["Cor"].astype(str).str.strip().str.lower()
data = pd.get_dummies(data, columns=["Cor"], drop_first=True, dtype=int)

# ------------ Fim modificações cor ---------------- #

# ------------ Modificações Km ------------------ #

km_temp = data["Km"].astype(str).str.lower()
data["Km"] = km_temp.str.replace("km", "").str.strip()
data["Km"] = pd.to_numeric(data["Km"], errors='coerce')
data["Km"] = data["Km"].replace(0, np.nan)
data["Km"] = data["Km"].fillna(data.groupby("Ano")["Km"].transform("median"))

data = data.dropna(subset=["Km"])

# --------------- Fim modificações Km ------------------ #

# --------------- Modificação marcas ------------------ #

print(data["Fabricante"].unique())

data["Fabricante"] = data["Fabricante"].astype(str).str.strip().str.lower()
data = pd.get_dummies(data, columns=["Fabricante"], drop_first=True, dtype=int)

# --------------- Fim modificação marcas -------------------- #

# --------------- Modificação data da lavagem ----------------- #

data["Data_ultima_lavagem"] = pd.to_datetime(data["Data_ultima_lavagem"], errors="coerce")
data_mais_recente = data["Data_ultima_lavagem"].max()
data["Dias_desde_lavagem"] = (data_mais_recente - data["Data_ultima_lavagem"]).dt.days

data = data.drop(columns=["Data_ultima_lavagem"])

# -------------- Fim modificação data da lavagem ----------------- #

# --------------- Modificação debitos ----------------- #

data["Débitos"] = data["Débitos"].replace("-", "0")
data["Débitos"] = pd.to_numeric(data["Débitos"], errors='coerce')
data["Débitos"] = data["Débitos"].fillna(0).astype(int)

# -------------- Fim modificação debitos ------------------ #

# -------------- Modificação id e concessionaria -------------- # 

data = data.drop(columns=["ID", "Codigo_concessionaria"])

# ----------------- Fim modificação id e concessionaria ------------- #

print(f"{((len_init - len(data)) / len_init) * 100} % da base excluida")
data.to_csv("data/train_mod_tratado.csv", index=False)
