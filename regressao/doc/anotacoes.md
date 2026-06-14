**Análise exploratória dos dados**

- Exclusão de preços nulos +
- Instancias com preços abaixo de 1000 dolares foram retirados +
- Exlusão dos 1% carros mais caros +
- Não faz sentido usar a faixa de preço, ja tem o proprio preço +
- Adesivos personalizados é binario (sim - 1, não - 0) +
- Couro é binario (sim - 1, não - 0) +
- Combustivel são 4 diferentes, criar uma coluna pra cada de true/false +
- Categoria são 11 diferentes, criar uma coluna pra cada de true/false +
- Tipo de cambio são 4 diferentes, separar em colunas de True/false + 
- Tipo de tração são 4 diferentes, separar em colunas de true/false +
- Separação dos fabricantes por colunas true/false +
- Separação das cores em colunas true/false +
- Cores agrupadas: red/vermelho, azul ceu/azul +
- Separação entre volume do motor e ser turbo +
- Volume do motor de 0 sendo que a base não tem carro eletrico, descartar instancias +
- Quantidade de portas (2-3 = 0, 4-5=1, >5=2) ordem de grandeza +
- Mais de 1000 modelos, jogar fora +
- Radio am e fm separados em duas colunas
- Substituição das kilometragens faltantes pela mediana por ano +
- ~20% dos dados foram excluidos

***Dados de teste***

- Exclusão das instancias sem preço para poder tirar as metricas

**Métodos de regressão**

Preenchimento de colunas faltantes na tabela de teste
Ajuste da escala dos dados
Testes feitos sem retirar os outliers de preços altos e baixo fizeram os modelos serem piores que chutar a média 
Ao retirar os preços abaixo de 1000 e os 1% mais caros o R² foi pra perto de 0.5 em todos os modelos
Retirar a coluna de data da lavagem melhora a predição

***KNeighborsRegressor***

- 7 vizinhos mais proximos maximiza o resultado de R²

***MLP***

- Não convergiu
- 3000 iterações
- 1 camada oculta, 100 neuronios
- mais camadas piorou o modelo
- alpha maior piorou o modelo

**Resultados**

- Metrics for K-Neigbors Regressor
	- Melhores parâmetros encontrados: {'n_neighbors': 10, 'p': 1, 'weights': 'distance'}
	- MAE (Erro Médio): $ 7085.93
	- RMSE (Penalidade): $ 10591.17
	- R²: 0.4909

- Metrics for Ridge
	- Melhores parâmetros encontrados: {'alpha': np.int64(110)}
	- MAE (Erro Médio): $ 8096.72
	- RMSE (Penalidade): $ 11342.61
	- R²: 0.4160

- Metrics for Decision Tree Regressor
	- Melhores parâmetros encontrados: {'max_depth': 15, 'min_samples_leaf': 6, 'min_samples_split': 32}
	- MAE (Erro Médio): $ 5619.51
	- RMSE (Penalidade): $ 8890.14
	- R²: 0.6413

- Metrics for Random Forest
	- Melhores parâmetros encontrados: {'max_depth': None, 'min_samples_split': 2, 'n_estimators': 180}
	- MAE (Erro Médio): $ 4621.95
	- RMSE (Penalidade): $ 7506.02
	- R²: 0.7443

- Metrics for Multilayer Perceptron Regressor
	- Melhores parâmetros encontrados: {'activation': 'relu', 'hidden_layer_sizes': (100,), 'learning_rate': 'constant'}
	- MAE (Erro Médio): $ 5796.82
	- RMSE (Penalidade): $ 8840.99
	- R²: 0.6452