import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

csv_train = open("data/train_mod.csv")

reader = csv.reader(csv_train, delimiter=",")

id = []
deb = []
fabr = []
model = []
ano = []
categ = []
couro = []
comb = []
vol_motor = []
km = []
cilindros = []
t_cambio = []
trac = []
portas = []
rodas = []
cor = []
airb = []
preco = []
num_propr = []
ult_lav = []
ades_pers = []
radio = []
troca_oleo = []
cod_conss = []
class_veic = []
faixa_preco = []

first = True

for line in reader:
	if first == True: 
		first = False
		continue

	id.append(int(line[0]))
	deb.append(int(line[1]) if line[1] != "-" else 0)
	fabr.append(line[2])
	model.append(line[3])
	ano.append(int(line[4]))
	categ.append(line[5])
	couro.append(1 if line[6] == "Sim" else 0)
	comb.append(line[7])
	vol_motor.append(line[8])
	km.append(line[9])
	cilindros.append(int(line[10]))
	t_cambio.append(line[11])
	trac.append(line[12])
	portas.append(line[13])
	rodas.append(int(line[14]))
	cor.append(line[15])
	airb.append(int(line[16]))
	preco.append(int(line[17]) if line[17] != "NA" else 0)
	num_propr.append(int(line[18]))
	ult_lav.append(line[19])
	ades_pers.append(1 if line[20] == "Sim" else 0)
	radio.append(line[21])
	troca_oleo.append(int(line[22]))
	cod_conss.append(int(line[23]))
	class_veic.append(line[24])
	faixa_preco.append(line[25])

fig, ax = plt.subplots()
ax.scatter(id, deb)

plt.show()