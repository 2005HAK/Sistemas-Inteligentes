import matplotlib.pyplot as plt						# Library for plotting graphs
from matplotlib.animation import FuncAnimation		# Library for animating the decision boundary
import numpy as np
import glob
import os
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, classification_report

arquivo_dataset = 'data/iris.data'
accuracy_history = []

pasta_epochs = 'epochs'
arquivos = glob.glob(os.path.join(pasta_epochs, 'epoch_*.txt'))
arquivos = sorted(arquivos, key=lambda x: int(os.path.basename(x).replace('epoch_', '').replace('.txt', '')))

# Read the weights, bias and accuracy from each epoch file
historico_pesos = []
for arq in arquivos:
	with open(arq, 'r') as file:
		pesos = file.readline().split()
		if len(pesos) >= 2:
			w1, w2, w3, w4 = float(pesos[0]), float(pesos[1]), float(pesos[2]), float(pesos[3])
			bias = float(pesos[4]) if len(pesos) >= 5 else 0.0
			historico_pesos.append((w1, w2, w3, w4, bias))
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
w1_final, w2_final, w3_final, w4_final, bias_final = historico_pesos[-1]

# Save the true and predict classes for the test database
y_true, y_pred = [], []

with open('data/test_data.txt', 'r') as file:
	for linha in file:
		linha = linha.strip()
		if not linha: continue
		partes = linha.split(',')
		x, y, z, w, classe = float(partes[0]), float(partes[1]), float(partes[2]), float(partes[3]), int(partes[4])

		z = w1_final * x + w2_final * y + w3_final * z + w4_final * w + bias_final
		predicted_class = 1 if z >= 0 else 0
		y_true.append(classe)
		y_pred.append(predicted_class)

print(classification_report(y_true, y_pred))

cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1])
disp.plot(cmap=plt.cm.Blues)
plt.title('Matriz de Confusão', fontsize=14)

plt.show()