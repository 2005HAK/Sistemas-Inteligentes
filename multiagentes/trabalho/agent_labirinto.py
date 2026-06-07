import spade
import numpy as np
import random

class LabirintoAgent(spade.agent.Agent):
	async def setup(self, n=10):
		print("Labirinto Agent {} is ready.".format(str(self.jid)))
		self.mapa = None
		self.initial_position = (random.randint(0, n - 1), random.randint(0, n - 1)) # acho que tem que mudar isso
		self.posicao_atual = self.initial_position
		self.final_position = (random.randint(0, n - 1), random.randint(0, n - 1))
		self.generate_map(n, n)
		self.show_map()
		self.add_behaviour(self.RecvMessage())

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

	#não sera mais usada
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
	
	#sera usada, mas precisa ser adaptada (ta recebendo um vetor de posiçoes)
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

	def can_move(self, current_position):
		'''
			This function checks to which directions the agent can move from its current position.

			:param current_position: a tuple (x, y) representing the current position of the agent in the maze.
			:type current_position: tuple
			
			:returns: A list of directions (D, E, C, B) that the agent can move
			:rtype: list

		'''

		x, y = current_position
		new_positions = {"D": [x + 1, y], "E": [x - 1, y], "C": [x, y + 1], "B": [x, y - 1]}
		can_move_positions = []
		for key, pos in new_positions.items():
			x, y = pos
			if 0 <= x < len(self.mapa) and 0 <= y < len(self.mapa[0]):
				if self.mapa[x][y] == 1 or self.mapa[x][y] == 3:
					can_move_positions.append(key)
		return can_move_positions

	#não sera mais usada, eu acho
	def get_current_position(self):
		return self.posicao_atual
	
	class RecvMessage(spade.behaviour.CyclicBehaviour):
		async def run(self):
			print("Waiting for messages...")
			while True:
				msg = await self.receive(timeout=10)
				if msg:
					print("Received message: {}".format(msg.body))

					#preciso das definições de mensagens do professor

async def main():
	labirinto = LabirintoAgent("labirinto@192.168.1.74", "labirinto", verify_security=False)
	await labirinto.start()

if __name__ == "__main__":
	spade.run(main())