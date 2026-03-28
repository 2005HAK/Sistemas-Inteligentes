from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

iris = datasets.load_iris()
X = iris.data[:, 2:4]
y = iris.target

k = 5

neigh = KNeighborsClassifier(n_neighbors = 3)
neigh.fit(X, y)

h = .01
x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

Z = neigh.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.figure(figsize=(8, 6))
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ['#FF0000', '#00FF00', '#0000FF']

plt.pcolormesh(xx, yy, Z, cmap=cmap_light, shading='auto')

for i, color in zip(range(3), cmap_bold):
	idx = np.where(y == i)
	plt.scatter(X[idx, 0], X[idx, 1], c=color, label=iris.target_names[i], edgecolor='k', s=20)

plt.xlabel(iris.feature_names[2])
plt.ylabel(iris.feature_names[3])
plt.title(f"Fronteiras de Decisão KNN (k={k})")
plt.legend()
plt.show()