import pandas as pd
import numpy as np
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

x = data.drop(columns=["Preco"])
y = data["Preco"]

y_expected = test["Preco"]
x_predict = test.drop(columns=["Preco"])

x_predict = x_predict.reindex(columns=x.columns, fill_value=0)

scaler = StandardScaler()
x = scaler.fit_transform(x)
x_predict = scaler.transform(x_predict)

def kneigbors_test():
	params = {
		'n_neighbors': np.arange(1, 100, 1),
		'weights': ['uniform', 'distance'],
		'p': [1, 2]
	}

	grid = GridSearchCV(KNeighborsRegressor(), params, cv=3, scoring='r2', n_jobs=-1)
	grid.fit(x, y)

	previsions = grid.predict(x_predict)

	calc_metrics(grid, previsions, "K-Neigbors Regressor")

def ridge_test():
	params = {
		'alpha': np.arange(0, 10000, 10),
	}

	grid = GridSearchCV(Ridge(), params, cv=3, scoring='r2', n_jobs=-1)
	grid.fit(x, y)

	previsions = grid.predict(x_predict)

	calc_metrics(grid, previsions, "Ridge")

def tree_test():
	params = {
		'max_depth': [None] + list(np.arange(10, 100, 5)),
		'min_samples_split': np.arange(2, 50, 2), 
		'min_samples_leaf': np.arange(1, 100, 5)
	}

	grid = GridSearchCV(DecisionTreeRegressor(), params, cv=3, scoring='r2', n_jobs=-1) 
	grid.fit(x, y)

	previsions = grid.predict(x_predict)

	calc_metrics(grid, previsions, "Decision Tree Regressor")

def forest_test():
	params = {
		'n_estimators': np.arange(10, 1000, 10),
		'max_depth': [None] + list(np.arange(1, 21, 5)),
		'min_samples_split': np.arange(2, 36, 10)
	}

	grid = GridSearchCV(RandomForestRegressor(random_state=42), params, cv=3, scoring='r2', n_jobs=-1) 
	grid.fit(x, y)

	previsions = grid.predict(x_predict)

	calc_metrics(grid, previsions, "Random Forest")

def mlp_test():
	params = {
		'hidden_layer_sizes': [(50,), (100,), (128, 64), (100, 50, 25), (256, 128, 64)],
		'learning_rate': ['constant', 'invscaling', 'adaptive'],
		'activation': ['relu', 'identity', 'logistic', 'tanh']
	}
	grid = GridSearchCV(MLPRegressor(random_state=42, max_iter=2000, early_stopping=True), params, cv=3, scoring='r2', n_jobs=-1) 
	grid.fit(x, y)

	previsions = grid.predict(x_predict)

	calc_metrics(grid, previsions, "Multilayer Perceptron Regressor")

def calc_metrics(model, previsions, name="None"):
	print(f"Metrics for {name}")

	print(f"Melhores parâmetros encontrados: {model.best_params_}")
	print(f"MAE (Erro Médio): $ {mean_absolute_error(y_expected, previsions):.2f}")
	print(f"RMSE (Penalidade): $ {np.sqrt(mean_squared_error(y_expected, previsions)):.2f}")
	print(f"R²: {r2_score(y_expected, previsions):.4f}")

#kneigbors_test()
#ridge_test()
#tree_test()
#forest_test()
mlp_test()