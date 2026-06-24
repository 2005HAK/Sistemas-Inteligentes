import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV

data = pd.read_csv("data/train_mod_tratado.csv")
test = pd.read_csv("data/test_tratado.csv")

x_columns = data.drop(columns=["Preco"]).columns
x = data.drop(columns=["Preco"])
y = data["Preco"]

y_expected = test["Preco"]
x_predict = test.drop(columns=["Preco"])

x_predict = x_predict.reindex(columns=x.columns, fill_value=0)

scaler = StandardScaler()
x = scaler.fit_transform(x)
x_predict = scaler.transform(x_predict)

def kneigbors_test():
	'''
	params = {
		'n_neighbors': np.arange(1, 100, 1),
		'weights': ['uniform', 'distance'],
		'p': [1, 2]
	}
	'''
	params = {
		'n_neighbors': [10],
		'weights': ['distance'],
		'p': [1]
	}
	grid = GridSearchCV(KNeighborsRegressor(), params, cv=3, scoring='r2', n_jobs=-1)
	grid.fit(x, y)
	previsions = grid.predict(x_predict)
	calc_metrics(grid, previsions, "K-Neighbors")

def ridge_test():
	'''
	params = {
		'alpha': np.arange(0, 10000, 10),
	}
	'''
	params = {
		'alpha': [110],
	}
	grid = GridSearchCV(Ridge(), params, cv=3, scoring='r2', n_jobs=-1)
	grid.fit(x, y)
	previsions = grid.predict(x_predict)
	calc_metrics(grid, previsions, "Ridge")

def tree_test():
	'''
	params = {
		'max_depth': [None] + list(np.arange(10, 100, 5)),
		'min_samples_split': np.arange(2, 50, 2), 
		'min_samples_leaf': np.arange(1, 100, 5)
	}
	'''
	params = {
		'max_depth': [15],
		'min_samples_split': [32], 
		'min_samples_leaf': [6]
	}
	grid = GridSearchCV(DecisionTreeRegressor(), params, cv=3, scoring='r2', n_jobs=-1) 
	grid.fit(x, y)
	previsions = grid.predict(x_predict)
	calc_metrics(grid, previsions, "Decision Tree")

def forest_test():
	'''
	params = {
		'n_estimators': np.arange(10, 1000, 10),
		'max_depth': [None] + list(np.arange(1, 21, 5)),
		'min_samples_split': np.arange(2, 36, 10)
	}
	'''
	params = {
		'n_estimators': [180],
		'max_depth': [None],
		'min_samples_split': [2]
	}
	grid = GridSearchCV(RandomForestRegressor(random_state=42), params, cv=3, scoring='r2', n_jobs=-1) 
	grid.fit(x, y)
	previsions = grid.predict(x_predict)
	calc_metrics(grid, previsions, "Random Forest")

def mlp_test():
	'''
	params = {
		'hidden_layer_sizes': [(50,), (100,), (128, 64), (100, 50, 25), (256, 128, 64)],
		'learning_rate': ['constant', 'invscaling', 'adaptive'],
		'activation': ['relu', 'identity', 'logistic', 'tanh']
	}
	'''
	params = {
		'hidden_layer_sizes': [(100,)],
		'learning_rate': ['constant'],
		'activation': ['relu']
	}
	grid = GridSearchCV(MLPRegressor(random_state=42, max_iter=2000, early_stopping=True), params, cv=3, scoring='r2', n_jobs=-1) 
	grid.fit(x, y)
	previsions = grid.predict(x_predict)
	calc_metrics(grid, previsions, "MLP")

def gerar_graficos(model, previsions, name):
	sns.set_theme(style="whitegrid")
	
	plt.figure(figsize=(8, 6))
	plt.scatter(y_expected, previsions, alpha=0.4, color='#2ecc71', edgecolor='black')
	max_val = max(max(y_expected), max(previsions))
	plt.plot([0, max_val], [0, max_val], color='#e74c3c', linestyle='--', linewidth=2, label='Previsão correta')
	
	plt.title(f'{name}: Preço Real vs. Preço Previsto', fontsize=14, fontweight='bold', pad=15)
	plt.xlabel('Preço Real (U$)', fontsize=12)
	plt.ylabel('Preço Previsto (U$)', fontsize=12)
	plt.legend()
	plt.tight_layout()
	plt.savefig(f'grafico_real_vs_previsto_{name.replace(" ", "_")}.png', dpi=300)
	plt.close()

	if hasattr(model.best_estimator_, 'feature_importances_'):
		plt.figure(figsize=(10, 6))
		importancias = model.best_estimator_.feature_importances_
		indices = np.argsort(importancias)[-10:]
		top_features = [x_columns[i] for i in indices]
		top_importancias = importancias[indices]

		sns.barplot(x=top_importancias, y=top_features, palette='viridis')
		plt.title(f'{name}: Características mais importantes', fontsize=14, fontweight='bold', pad=15)
		plt.xlabel('Grau de Importância', fontsize=12)
		plt.ylabel('Características', fontsize=12)
		plt.tight_layout()
		plt.savefig(f'grafico_importancia_{name.replace(" ", "_")}.png', dpi=300)
		plt.close()

def calc_metrics(model, previsions, name="None"):
	print(f"Metrics for {name}")
	print(f"Melhores parâmetros encontrados: {model.best_params_}")
	print(f"MAE (Erro Médio): $ {mean_absolute_error(y_expected, previsions):.2f}")
	print(f"RMSE (Penalidade): $ {np.sqrt(mean_squared_error(y_expected, previsions)):.2f}")
	print(f"R²: {r2_score(y_expected, previsions):.4f}\n")
	
	gerar_graficos(model, previsions, name)

#kneigbors_test()
#ridge_test()
tree_test()
#forest_test()
#mlp_test()