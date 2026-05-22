import matplotlib.pyplot as plt						# Library for plotting graphs
from matplotlib.animation import FuncAnimation		# Library for animating the decision boundary
import numpy as np
import glob
import os
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, classification_report

arquivo_dataset = 'data/2ddatabase.txt'
x_class_0, y_class_0, x_class_1, y_class_1 = [], [], [], []
accuracy_history = []

# Read the dataset and separate the points by class
with open(arquivo_dataset, 'r') as file:
	for linha in file:
		linha = linha.strip()
		if not linha: continue
		partes = linha.split(',')

		x, y, classe = float(partes[0]), float(partes[1]), int(partes[2])

		if classe == 0: x_class_0.append(x); y_class_0.append(y)
		else: x_class_1.append(x); y_class_1.append(y)

pasta_epochs = 'epochs'
arquivos = glob.glob(os.path.join(pasta_epochs, 'epoch_*.txt'))
arquivos = sorted(arquivos, key=lambda x: int(os.path.basename(x).replace('epoch_', '').replace('.txt', '')))

# Read the weights, bias and accuracy from each epoch file
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

if not historico_pesos:
	print("No epoch data found!")
	exit()

accuracy_figure, accuracy_ax = plt.subplots(figsize=(8, 6))

accuracy_ax.scatter(range(1, len(accuracy_history) + 1), accuracy_history, color='purple', label='Acurácia', marker='o', s=100, edgecolors='black')
accuracy_ax.set_title('Acurácia por Época', fontsize=14)
accuracy_ax.set_xlabel('Época', fontsize=12)
accuracy_ax.set_ylabel('Acurácia', fontsize=12)
accuracy_ax.set_xlim(0, len(accuracy_history) + 1)
accuracy_ax.set_ylim(0, 1.05)
accuracy_ax.grid(True, linestyle=':', alpha=0.7)
accuracy_ax.legend(loc='lower right')

# Get the final wights and bias from the last epoch
w1_final, w2_final, bias_final = historico_pesos[-1]

# Save the true and predict classes for the test database
y_true, y_pred = [], []

with open('data/test_data.txt', 'r') as file:
	for linha in file:
		linha = linha.strip()
		if not linha: continue
		partes = linha.split(',')
		x, y, classe = float(partes[0]), float(partes[1]), int(partes[2])

		z = w1_final * x + w2_final * y + bias_final
		predicted_class = 1 if z >= 0 else 0
		y_true.append(classe)
		y_pred.append(predicted_class)

print(classification_report(y_true, y_pred))

cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1])
disp.plot(cmap=plt.cm.Blues)
plt.title('Matriz de Confusão', fontsize=14)

data_figure, data_figure_ax = plt.subplots(figsize=(8, 6))

data_figure_ax.scatter(x_class_0, y_class_0, color='blue', label='Classe 0', marker='o', s=100, edgecolors='black')
data_figure_ax.scatter(x_class_1, y_class_1, color='red', label='Classe 1', marker='s', s=100, edgecolors='black')

linha_decisao, = data_figure_ax.plot([], [], color='green', linewidth=3, linestyle='--', label='Fronteira')
texto_epoch = data_figure_ax.text(0.05, 0.95, '', transform=data_figure_ax.transAxes, fontsize=14, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

data_figure_ax.set_xlim(-1, 11)
data_figure_ax.set_ylim(-1, 11)
data_figure_ax.set_title('Treinamento do Perceptron', fontsize=14)
data_figure_ax.legend(loc='lower right')
data_figure_ax.grid(True, linestyle=':', alpha=0.7)

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

anim = FuncAnimation(data_figure, atualizar, frames=len(historico_pesos), interval=200, blit=True, repeat=False)

plt.show()