import numpy as np
import random

class Labirinto:
	def __init__(self, n=10):
		self.mapa = None
		self.initial_position = (0, 0)
		self.posicao_atual = self.initial_position
		self.final_position = (random.randint(0, n - 1), random.randint(0, n - 1))
		self.generate_map(n, n)

	def generate_map(self, width, height):
		self.mapa = np.zeros((width, height))
		for i in range(width):
			for j in range(height):
				if (i, j) == self.initial_position:
					self.mapa[i][j] = 2
				elif (i, j) == self.final_position:
					self.mapa[i][j] = 3
				elif np.random.rand() < 0.3:
					self.mapa[i][j] = 0
				else:
					self.mapa[i][j] = 1

	def show_map(self):
		for i in range(len(self.mapa)):
			for j in range(len(self.mapa[0])):
				if (i, j) == self.initial_position:
					print('2', end=' ')
				elif self.mapa[i][j] == 0:
					print('0', end=' ')
				elif (i, j) == self.final_position:
					print('3', end=' ')
				else:
					print('1', end=' ')
			print()

	def move(self, direcao):
		x, y = self.posicao_atual
		if direcao == 'N':
			nova_posicao = (x - 1, y)
		elif direcao == 'S':
			nova_posicao = (x + 1, y)
		elif direcao == 'L':
			nova_posicao = (x, y + 1)
		elif direcao == 'O':
			nova_posicao = (x, y - 1)
		else:
			raise ValueError("Direção inválida. Use 'N', 'S', 'L' ou 'O'.")

		if self.can_move(nova_posicao):
			self.posicao_atual = nova_posicao
			return True
		return False
	
	def show_path(self, caminho):
		for i in range(len(self.mapa)):
			for j in range(len(self.mapa[0])):
				if (i, j) == self.initial_position:
					print('2', end=' ')
				elif (i, j) == self.final_position:
					print('3', end=' ')
				elif (i, j) in caminho:
					print('*', end=' ')
				elif self.mapa[i][j] == 0:
					print('0', end=' ')
				else:
					print('1', end=' ')
			print()

	def can_move(self, posicao):
		x, y = posicao
		if 0 <= x < len(self.mapa) and 0 <= y < len(self.mapa[0]):
			return self.mapa[x][y] == 1 or self.mapa[x][y] == 3
		return False

	def get_current_position(self):
		return self.posicao_atual