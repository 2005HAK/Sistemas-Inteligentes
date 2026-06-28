import spade
import numpy as np
import random
import asyncio
from spade.template import Template

class LabirintoAgent(spade.agent.Agent):
	'''
	Classe do agente labirinto
	'''

	async def setup(self, n=10):
		'''
		Inicializa o objeto labirinto.

		:param n: Tamanho do labirinto (n x n)

		:return: none
		'''

		print("Labirinto Agent {} logado com sucesso.".format(str(self.jid)))
		self.mapa = None
		self.n = n

		print("Gerando labirinto...")

		while True:
			self.initial_position = (random.randint(0, n - 1), random.randint(0, n - 1))						# Posicao inicial aleatória dentro do labirinto
			self.final_position = (random.randint(0, n - 1), random.randint(0, n - 1))							# Posicao final aleatória dentro do labirinto

			if self.initial_position == self.final_position: continue											# Gera um novo labirinto se a posicao inicial e final cairem no mesmo lugar

			self.generate_map(n, n, 0.3)																		# Gera o mapa

			if self.tem_solucao(): break																		# Se nao tem solução gera um novo labirinto

		self.posicao_atual = self.initial_position
		self.show_map()																							# Exibe o mapa no terminal

		t_req = Template()
		t_req.set_metadata("performative", "request")
		self.add_behaviour(self.TratarRequest(), t_req)

		t_sub = Template()
		t_sub.set_metadata("performative", "subscribe")
		self.add_behaviour(self.TratarSubscribe(), t_sub)

		t_qif = Template()
		t_qif.set_metadata("performative", "queryif")
		self.add_behaviour(self.TratarQueryIf(), t_qif)

		t_prop = Template()
		t_prop.set_metadata("performative", "propose")
		self.add_behaviour(self.TratarPropose(), t_prop)

	def generate_map(self, width, height, k):
		'''
		Gera o labirinto com um valor de k% de uma posicao ser uma parede.\n
		Valores:

		- 0 - Parede\n
		- 1 - Caminho\n
		- 2 - Posição inicial\n
		- 3 - Posição final\n

		:param width: Largura do mapa
		:type width: int

		:param height: Altura do mapa
		:type height: int

		:param k: Chance de uma posição do mapa ser uma parede
		:type k: float [0 à 1]

		:return: none
		'''

		self.mapa = np.zeros((width, height))
		for i in range(width):
			for j in range(height):
				if (i, j) == self.initial_position:	self.mapa[i][j] = 2
				elif (i, j) == self.final_position:	self.mapa[i][j] = 3
				elif np.random.rand() < k:			self.mapa[i][j] = 0
				else:								self.mapa[i][j] = 1

	def tem_solucao(self):
		'''
		Implementacao de uma busca em profundidade para verificar se e possivel encontrar um caminho para o labirinto

		:return: Booleano que diz se tem solucao ou nao
		'''

		fronteira = [self.initial_position]
		visitados = set()
		visitados.add(self.initial_position)

		while fronteira:
			estado_atual = fronteira.pop(0)

			if estado_atual == self.final_position:	return True

			for vizinho in self.can_move(estado_atual, is_test=True):
				if vizinho not in visitados:
					visitados.add(vizinho)
					fronteira.append(vizinho)
		return False

	def can_move(self, current_position, is_test=False):
		'''
		Funcao para verificar se pode se mover para algum lugar.

		:param current_position: Posicao atual do resolvedor
		:type current_position: tuple
		:param is_test: Flag para retornar ou nao a direcao do movimento
		:type is_test: bool

		:return can_move_positions: Lista de posicoes que pode se mover. Pode ser com ou sem o identificador de direcao com base no valor de is_test
		'''

		x, y = current_position
		new_positions = {"C": (x - 1, y), "B": (x + 1, y), "D": (x, y + 1), "E": (x, y - 1)}

		can_move_positions = []
		for key, pos in new_positions.items():
			nx, ny = pos
			if 0 <= nx < len(self.mapa) and 0 <= ny < len(self.mapa[0]):
				if self.mapa[nx][ny] in [1, 2, 3]:	can_move_positions.append(pos if is_test else key)
		return can_move_positions

	def show_map(self):
		'''
		Exibe o mapa do labirinto no terminal.

		Valores:

		- 0 - Parede\n
		- 1 - Caminho\n
		- 2 - Posição inicial\n
		- 3 - Posição final\n

		:return: none
		'''

		print("\nMAPA INICIAL")
		for i in range(len(self.mapa)):
			for j in range(len(self.mapa[0])):
				if (i, j) == self.initial_position:	print('2', end=' ')
				elif self.mapa[i][j] == 0:			print('0', end=' ')
				elif (i, j) == self.final_position:	print('3', end=' ')
				else:								print('1', end=' ')
			print()

	def move(self, direcao):
		'''
		Move para a nova posição se esta for valida

		:param direcao: Direção para onde se moverá [C, B, D ou E]
		:type direcao: str

		:return: True se moveu para a nova posição e False caso contrário
		'''

		x, y = self.posicao_atual
		if direcao == 'C':		nova_posicao = (x - 1, y)
		elif direcao == 'B':	nova_posicao = (x + 1, y)
		elif direcao == 'D':	nova_posicao = (x, y + 1)
		elif direcao == 'E':	nova_posicao = (x, y - 1)
		else:					return False

		if direcao in self.can_move(self.posicao_atual):
			self.posicao_atual = nova_posicao
			return True
		return False

	def show_path(self, caminho_string, titulo="CAMINHO FINAL NO MAPA"):
		'''
		Mostra o caminho proposto
		'''

		caminho_coords = [self.initial_position]
		x, y = self.initial_position
		for passo in caminho_string:
			if passo == 'C':	x -= 1
			elif passo == 'B':	x += 1
			elif passo == 'D':	y += 1
			elif passo == 'E':	y -= 1
			caminho_coords.append((x, y))

		print(f"\n{titulo}")

		for i in range(len(self.mapa)):
			for j in range(len(self.mapa[0])):
				if (i, j) == self.initial_position:	print('2', end=' ')
				elif (i, j) == self.final_position:	print('3', end=' ')
				elif (i, j) in caminho_coords:		print('*', end=' ')
				elif self.mapa[i][j] == 0:			print('0', end=' ')
				else:								print('1', end=' ')
			print()

	class TratarRequest(spade.behaviour.CyclicBehaviour):
		'''
		Trata as requisições de movimentação, respondendo para onde pode se mover com base na posição atual
		'''

		async def run(self):
			msg = await self.receive(timeout=1)
			if msg:
				resp = msg.make_reply()
				direcoes_possiveis = self.agent.can_move(self.agent.posicao_atual)
				print(f"Recebeu request. Enviando direções válidas: {direcoes_possiveis}")
				resp.set_metadata("performative", "inform")
				resp.body = str(direcoes_possiveis)
				await self.send(resp)

	class TratarSubscribe(spade.behaviour.CyclicBehaviour):
		'''
		Trata a proposta de movimentação.

		Responde com ok caso consiga se mover para a direção requisitada e nok caso contrário
		'''

		async def run(self):
			msg = await self.receive(timeout=1)
			if msg:
				resp = msg.make_reply()
				direcao_desejada = msg.body.strip() 
				print(f"Recebeu pedido para mover: '{direcao_desejada}'")
				if self.agent.move(direcao_desejada):
					print(f"   -> OK! Nova posição: {self.agent.posicao_atual}")

					resp.set_metadata("performative", "inform")
					resp.body = "ok"
				else:
					print(f"   -> Parede fora do mapa.")
					resp.set_metadata("performative", "inform")
					resp.body = "nok"
				await self.send(resp)

	class TratarQueryIf(spade.behaviour.CyclicBehaviour):
		'''
		Verifica se o resolvedor chegou na posição final.

		Responde com done se chegou e failure caso contrário
		'''

		async def run(self):
			msg = await self.receive(timeout=1)
			if msg:
				resp = msg.make_reply()
				resp.set_metadata("performative", "inform")

				print(f"Verificando objetivo para a posição: {self.agent.posicao_atual}")
				if self.agent.posicao_atual == self.agent.final_position:	resp.body = "done"
				else: 														resp.body = "failure"
				await self.send(resp)

	class TratarPropose(spade.behaviour.CyclicBehaviour):
		'''
		Trata as propostas enviadas pelo resolvedor.

		Responde com acept_propose caso a proposta esteja correta ou failure caso contrario
		'''

		async def run(self):
			msg = await self.receive(timeout=1)
			if msg:
				resp = msg.make_reply()
				resp.set_metadata("performative", "inform")
				resp.body = "accept_propose"												# Ta so aceitando ? e se não for uma solução?

				partes = str(msg.body).split(',')
				caminho_dfs = partes[0] if len(partes) > 0 else ""
				caminho_bfs = partes[1] if len(partes) > 1 else msg.body					# tem algo estranho aqui

				print("O Resolvedor enviou os resultados:")
				print(f"Caminho DFS: {caminho_dfs} (Tam: {len(caminho_dfs)})")
				print(f"Caminho BFS: {caminho_bfs} (Tam: {len(caminho_bfs)})")

				self.agent.show_path(caminho_dfs, "Traçado da DFS")
				self.agent.show_path(caminho_bfs, "Traçado do BFS")

				print("\nEnviando accept_propose...")
				await self.send(resp)
				await asyncio.sleep(2)
				print("Encerrando agente.")	
				await self.agent.stop()

async def main():
	#labirinto = LabirintoAgent("mashima_lab_v5@yax.im", "senha123", verify_security=False)
	labirinto = LabirintoAgent("lab@192.168.1.74", "senha123", verify_security=False)
	await labirinto.start()
	while labirinto.is_alive():
		try:
			await asyncio.sleep(1)
		except KeyboardInterrupt:
			await labirinto.stop()
			break

if __name__ == "__main__":
	asyncio.run(main())