import matplotlib.pyplot as plt

modelos = ['Ridge', 'K-Neighbors', 'Decision Tree', 'MLP', 'Random Forest']
r2 = [0.4160, 0.4909, 0.6413, 0.6452, 0.7443]

plt.figure(figsize=(8, 5))
cores = ['#e74c3c', '#f39c12', '#3498db', '#9b59b6', '#2ecc71']

barras = plt.bar(modelos, r2, color=cores, edgecolor='black')

for barra in barras:
	yval = barra.get_height()
	plt.text(barra.get_x() + barra.get_width()/2, yval + 0.01, 
			f'{yval:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.ylabel('Coeficiente de Determinação (R²)', fontsize=12, fontweight='bold')
plt.title('Desempenho dos Modelos de Regressão', fontsize=14, fontweight='bold', pad=15)
plt.ylim(0, 0.85)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.xticks(fontsize=11)
plt.tight_layout()

plt.show()