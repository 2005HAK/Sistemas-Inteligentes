class bfs:
	def __init__(self, labirinto, visualizator):
		self.labirinto = labirinto
		self.vz = visualizator
		self.visitados = []
		self.caminho = []

	def find_path(self):
		start = self.labirinto.initial_position
		end = None

		fila = [start]
		parent = {start: None}
		self.visitados = [start]

		found = False

		while fila:
			atual = fila.pop(0)

			if self.labirinto.mapa[atual[0], atual[1]] == 3:
				end = atual
				found = True
				break

			for movimento in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
				proxima_pos = (atual[0] + movimento[0], atual[1] + movimento[1])

				if self.labirinto.can_move(proxima_pos) and proxima_pos not in parent:
					fila.append(proxima_pos)
					parent[proxima_pos] = atual
					self.visitados.append(proxima_pos)
					self.vz.draw(self.caminho, self.visitados)

		if found:
			passo = end
			while passo is not None:
				self.caminho.append(passo)
				passo = parent[passo]
			self.caminho.reverse()
			
		return found

	def get_visitados(self):
		return self.visitados