import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import glob
import os

arquivo_dataset = 'data/2ddatabase.txt'
x_class_0, y_class_0, x_class_1, y_class_1 = [], [], [], []
accuracy_history, epochs_history = [], []

with open(arquivo_dataset, 'r') as file:
	for linha in file:
		linha = linha.strip()
		if not linha: continue
		partes = linha.split(',')
		x, y, classe = float(partes[0]), float(partes[1]), int(partes[2])
		if classe == 0:
			x_class_0.append(x); y_class_0.append(y)
		else:
			x_class_1.append(x); y_class_1.append(y)

pasta_epochs = 'epochs'
arquivos = glob.glob(os.path.join(pasta_epochs, 'epoch_*.txt'))
arquivos = sorted(arquivos, key=lambda x: int(os.path.basename(x).replace('epoch_', '').replace('.txt', '')))

historico_pesos = []
for arq in arquivos:
	with open(arq, 'r') as file:
		pesos = file.readline().split()
		if len(pesos) >= 2:
			w1, w2 = float(pesos[0]), float(pesos[1])
			bias = float(pesos[2]) if len(pesos) >= 3 else 0.0
			historico_pesos.append((w1, w2, bias))
		performance = file.readline().split()
		accuracy_history.append(float(performance[0]))
		epochs_history.append(int(performance[1]))

if not historico_pesos:
	print("Nenhum arquivo de epoch encontrado!")
	exit()

figure, ax1 = plt.subplots(figsize=(8, 6))

ax1.scatter(epochs_history, accuracy_history, color='purple', label='Acurácia', marker='o', s=100, edgecolors='black')
ax1.set_title('Acurácia por Época', fontsize=14)
ax1.set_xlabel('Época', fontsize=12)
ax1.set_ylabel('Acurácia', fontsize=12)
ax1.set_xlim(0, max(epochs_history) + 1)
ax1.set_ylim(0, 1.05)
ax1.grid(True, linestyle=':', alpha=0.7)
ax1.legend(loc='lower right')

fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(x_class_0, y_class_0, color='blue', label='Classe 0', marker='o', s=100, edgecolors='black')
ax.scatter(x_class_1, y_class_1, color='red', label='Classe 1', marker='s', s=100, edgecolors='black')

linha_decisao, = ax.plot([], [], color='green', linewidth=3, linestyle='--', label='Fronteira')
texto_epoch = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.set_xlim(-1, 11)
ax.set_ylim(-1, 11)
ax.set_title('Treinamento do Perceptron', fontsize=14)
ax.legend(loc='lower right')
ax.grid(True, linestyle=':', alpha=0.7)

def atualizar(frame):
	w1, w2, bias = historico_pesos[frame]
	x_reta = np.array([-2, 12])

	if w2 != 0:
		y_reta = -(w1 / w2) * x_reta - (bias / w2)
		linha_decisao.set_data(x_reta, y_reta)
	elif w1 != 0:
		linha_decisao.set_data([-bias/w1, -bias/w1], [-2, 12])

	texto_epoch.set_text(f'Epoch: {frame}\nw1: {w1:.2f}\nw2: {w2:.2f}\nbias: {bias:.2f}')
	return linha_decisao, texto_epoch

anim = FuncAnimation(fig, atualizar, frames=len(historico_pesos), interval=200, blit=True, repeat=False)

plt.show()