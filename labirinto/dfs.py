class dfs:
	def __init__(self, labirinto, visualizator):
		self.labirinto = labirinto
		self.vz = visualizator
		self.visitados = []
		self.caminho = []

	def find_path(self):
		start = self.labirinto.initial_position
		end = None

		pilha = [start]
		parent = {start: None}
		self.visitados = [start]

		found = False

		while pilha:
			atual = pilha[-1]

			if self.labirinto.mapa[atual[0], atual[1]] == 3:
				end = atual
				found = True
				break
			
			movimento = [(-1, 0), (1, 0), (0, -1), (0, 1)]

			if self.labirinto.can_move((atual[0] + movimento[0][0], atual[1] + movimento[0][1])) and (atual[0] + movimento[0][0], atual[1] + movimento[0][1]) not in parent:
				proxima_pos = (atual[0] + movimento[0][0], atual[1] + movimento[0][1])
				pilha.append(proxima_pos)
				parent[proxima_pos] = atual
			elif self.labirinto.can_move((atual[0] + movimento[1][0], atual[1] + movimento[1][1])) and (atual[0] + movimento[1][0], atual[1] + movimento[1][1]) not in parent:
				proxima_pos = (atual[0] + movimento[1][0], atual[1] + movimento[1][1])
				pilha.append(proxima_pos)
				parent[proxima_pos] = atual
			elif self.labirinto.can_move((atual[0] + movimento[2][0], atual[1] + movimento[2][1])) and (atual[0] + movimento[2][0], atual[1] + movimento[2][1]) not in parent:
				proxima_pos = (atual[0] + movimento[2][0], atual[1] + movimento[2][1])
				pilha.append(proxima_pos)
				parent[proxima_pos] = atual
			elif self.labirinto.can_move((atual[0] + movimento[3][0], atual[1] + movimento[3][1])) and (atual[0] + movimento[3][0], atual[1] + movimento[3][1]) not in parent:
				proxima_pos = (atual[0] + movimento[3][0], atual[1] + movimento[3][1])
				pilha.append(proxima_pos)
				parent[proxima_pos] = atual
			else:
				self.visitados.append(atual)
				pilha.pop()

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