import spade																								# Biblioteca para agentes
from spade.agent import Agent																				# Classe base para criar agentes
from spade.behaviour import FSMBehaviour, State																# Comportamento FSM para execução em estados
from spade.message import Message																			# Classe para criar mensagens entre agentes
import asyncio																								# Biblioteca para operações assíncronas, permitindo que o agente espere por mensagens sem bloquear a execução

agentResolver = "resolver@192.168.1.74" 
#agentResolver = "mashima_res_v5@yax.im"
agentLab = "lab@192.168.1.74"
#agentLab = "mashima_lab_v5@yax.im"
password = "senha123"

class PedirState(State):
	async def run(self):
		if self.agent.exploracao_concluida:	return

		if not hasattr(self.agent, 'esperando_pedir') or not self.agent.esperando_pedir:
			while await self.receive(timeout=0.01): pass

			print(f"\nPosição Virtual: {self.agent.posicao_virtual}")
			print("Perguntando caminhos possíveis...")

			await asyncio.sleep(0.5)
			msg_req = Message(to=self.agent.labirinto_jid)
			msg_req.set_metadata("performative", "request")
			msg_req.body = "precisa direção"
			await self.send(msg_req)
			self.agent.msg_req = msg_req
			self.agent.esperando_pedir = True

		msg = await self.receive(timeout=10)
		if not msg:
			self.agent.esperando_pedir = False
			self.set_next_state("PEDIR")
			return

		if msg and msg.get_metadata("performative") == "inform" and "[" in msg.body:
			self.agent.esperando_pedir = False
			body = str(msg.body).replace('[', '').replace(']', '').replace("'", "").replace(" ", "")
			direcoes_recebidas = body.split(',') if body else []
			print(f"Labirinto respondeu: {direcoes_recebidas}")

			if self.agent.posicao_virtual not in self.agent.grafo:	self.agent.grafo[self.agent.posicao_virtual] = direcoes_recebidas

			self.agent.direcao_escolhida = None
			self.agent.is_backtrack = False

			nao_visitadas = []
			for d in direcoes_recebidas:
				if d in self.agent.deltas:
					dx, dy = self.agent.deltas[d]
					nova_pos = (self.agent.posicao_virtual[0] + dx, self.agent.posicao_virtual[1] + dy)
					if nova_pos not in self.agent.visitados:	nao_visitadas.append(d)

			if nao_visitadas:
				self.agent.direcao_escolhida = nao_visitadas[0]
				print(f"Decisão: Novo caminho. Movendo para '{self.agent.direcao_escolhida}'")
				self.set_next_state("MOVER")
			else:
				if len(self.agent.caminho_inverso) > 0:
					self.agent.direcao_escolhida = self.agent.caminho_inverso[-1]
					self.agent.is_backtrack = True
					print(f"Beco sem saída! Fazendo backtrack para '{self.agent.direcao_escolhida}'")
					self.set_next_state("MOVER")
				else:
					print("DFS CONCLUÍDO!")
					self.agent.exploracao_concluida = True
					self.set_next_state("FINALIZAR")
		else:	self.set_next_state("PEDIR")

class MoverState(State):
	async def run(self):
		if not hasattr(self.agent, 'esperando_mover') or not self.agent.esperando_mover:
			while await self.receive(timeout=0.01): pass

			print(f"Enviando tentativa de movimento: {self.agent.direcao_escolhida}")

			await asyncio.sleep(1.5)
			msg_mov = Message(to=self.agent.labirinto_jid)
			msg_mov.set_metadata("performative", "subscribe")
			msg_mov.body = self.agent.direcao_escolhida
			await self.send(msg_mov)
			self.agent.msg_mov = msg_mov
			self.agent.esperando_mover = True

		msg = await self.receive(timeout=15)
		if not msg:
			self.agent.esperando_mover = False
			self.set_next_state("MOVER")
			return

		if msg and msg.get_metadata("performative") == "inform":
			if msg.body.strip() in ["ok", "nok"]:
				self.agent.esperando_mover = False
				conteudo_mov = str(msg.body).strip()

				if conteudo_mov == "ok":
					print("Labirinto confirmou movimento.")
					dx, dy = self.agent.deltas[self.agent.direcao_escolhida]
					self.agent.posicao_virtual = (self.agent.posicao_virtual[0] + dx, self.agent.posicao_virtual[1] + dy)
					self.agent.visitados.add(self.agent.posicao_virtual)

					if not self.agent.is_backtrack:
						self.agent.caminho_atual.append(self.agent.direcao_escolhida)
						self.agent.caminho_inverso.append(self.agent.opostos[self.agent.direcao_escolhida])
					else:
						self.agent.caminho_inverso.pop()
						self.agent.caminho_atual.pop()

					self.set_next_state("VERIFICAR")
				else:	self.set_next_state("PEDIR")
			else:	self.set_next_state("MOVER")
		else:	self.set_next_state("MOVER")

class VerificarState(State):
	async def run(self):
		if not hasattr(self.agent, 'esperando_verificar') or not self.agent.esperando_verificar:
			while await self.receive(timeout=0.01): pass
			
			print("Perguntando se chegou no objetivo...")

			await asyncio.sleep(0.5)
			msg_qif = Message(to=self.agent.labirinto_jid)
			msg_qif.set_metadata("performative", "queryif")
			msg_qif.body = "Chegou?"
			await self.send(msg_qif)
			self.agent.msg_qif = msg_qif
			self.agent.esperando_verificar = True

		msg = await self.receive(timeout=10)
		if not msg:
			self.agent.esperando_verificar = False
			self.set_next_state("VERIFICAR")
			return

		if msg and msg.get_metadata("performative") == "inform":
			if msg.body.strip() in ["done", "failure"]:
				self.agent.esperando_verificar = False
				conteudo_qif = str(msg.body).strip()

				if conteudo_qif == "done":
					if not self.agent.posicao_objetivo:
						self.agent.posicao_objetivo = self.agent.posicao_virtual
						self.agent.caminho_dfs_bruto = "".join(self.agent.caminho_atual) 
						print(f"\nOBJETIVO ENCONTRADO em {self.agent.posicao_virtual}!")
						print("Memorizando a posição e continuando a explorar o resto do mapa...")
				
				await asyncio.sleep(.1)
				self.set_next_state("PEDIR")
			else:	self.set_next_state("VERIFICAR")
		else:	self.set_next_state("VERIFICAR")

class FinalizarState(State):
	async def run(self):
		if self.agent.posicao_objetivo:
			if not hasattr(self.agent, 'esperando_finalizar') or not self.agent.esperando_finalizar:
				print(f"Iniciando BFS até {self.agent.posicao_objetivo}...")
				caminho_otimo = self.agent.calcular_bfs()

				print("=COMPARAÇÃO DE DFS vs BFS:")
				print(f"Caminho inicial (DFS): {self.agent.caminho_dfs_bruto} (Tamanho: {len(self.agent.caminho_dfs_bruto)} passos)")
				print(f"Caminho otimizado (BFS): {caminho_otimo} (Tamanho: {len(caminho_otimo)} passos)")

				while await self.receive(timeout=0.01): pass

				await asyncio.sleep(0.5)
				msg_prop = Message(to=self.agent.labirinto_jid)
				msg_prop.set_metadata("performative", "propose")
				payload = f"{self.agent.caminho_dfs_bruto},{caminho_otimo}"
				msg_prop.body = payload

				print(f"\nEnviando Caminhos para o Labirinto...")
				await self.send(msg_prop)
				self.agent.msg_prop = msg_prop
				self.agent.esperando_finalizar = True

			msg = await self.receive(timeout=10)
			if not msg:
				self.agent.esperando_finalizar = False
				self.set_next_state("FINALIZAR")
				return

			if str(msg.body).strip() == "accept_propose":
				print("Labirinto aceitou o caminho. Desligando...")
				self.kill()
				await self.agent.stop()
			else:	self.set_next_state("FINALIZAR")
		else:
			print("Labirinto totalmente explorado, mas não tem saída.")
			self.kill()
			await self.agent.stop()

class ExploracaoFSM(FSMBehaviour):
	'''
	Agente Resolvedor de Labirinto usando DFS (Depth-First Search) e BFS (Breadth-First Search)
	'''

	pass

class ResolvedorAgent(Agent):
	'''
	Classe do agente Resolvedor de Labirinto, responsável por iniciar o comportamento de exploração e gerenciar a comunicação com o labirinto.
	'''

	async def setup(self):
		'''
		Inicialização do comportamento, definindo variáveis e estruturas de dados necessárias para a exploração do labirinto
		'''

		print(f"Resolvedor de Labirínto {self.jid} online.")

		self.labirinto_jid = agentLab
		self.posicao_virtual = (0, 0)
		self.visitados = set([self.posicao_virtual])
		self.caminho_atual = []
		self.caminho_inverso = []
		self.opostos = {'D': 'E', 'E': 'D', 'C': 'B', 'B': 'C'}
		self.deltas = {'C': (-1, 0), 'B': (1, 0), 'D': (0, 1), 'E': (0, -1)}
		self.grafo = {}
		self.posicao_objetivo = None
		self.exploracao_concluida = False
		self.caminho_dfs_bruto = ""
		self.direcao_escolhida = None
		self.is_backtrack = False

		fsm = ExploracaoFSM()

		fsm.add_state(name="PEDIR", state=PedirState(), initial=True)
		fsm.add_state(name="MOVER", state=MoverState())
		fsm.add_state(name="VERIFICAR", state=VerificarState())
		fsm.add_state(name="FINALIZAR", state=FinalizarState())

		fsm.add_transition(source="PEDIR", dest="MOVER")
		fsm.add_transition(source="PEDIR", dest="FINALIZAR")
		fsm.add_transition(source="PEDIR", dest="PEDIR")
		fsm.add_transition(source="MOVER", dest="VERIFICAR")
		fsm.add_transition(source="MOVER", dest="PEDIR")
		fsm.add_transition(source="MOVER", dest="MOVER")
		fsm.add_transition(source="VERIFICAR", dest="PEDIR")
		fsm.add_transition(source="VERIFICAR", dest="VERIFICAR")
		fsm.add_transition(source="FINALIZAR", dest="FINALIZAR")

		self.add_behaviour(fsm)

	def calcular_bfs(self):
		'''
		Calcula o caminho para o objetico usando BFS
		'''

		fila = [((0, 0), "")]
		visitados_bfs = set([(0, 0)])

		while fila:
			atual, caminho = fila.pop(0)

			if atual == self.posicao_objetivo:	return caminho

			direcoes = self.grafo.get(atual, [])
			for d in direcoes:
				if d in self.deltas:
					dx, dy = self.deltas[d]
					vizinho = (atual[0] + dx, atual[1] + dy)
					if vizinho not in visitados_bfs:
						visitados_bfs.add(vizinho)
						fila.append((vizinho, caminho + d))
		return ""

async def main():
	'''
	Função principal para iniciar o agente Resolvedor.
	'''

	resolvedor = ResolvedorAgent(agentResolver, password, verify_security=False)
	await resolvedor.start()
	while resolvedor.is_alive():
		try:
			await asyncio.sleep(1)
		except KeyboardInterrupt:
			print("Encerrando...")
			await resolvedor.stop()
			break

if __name__ == "__main__":	asyncio.run(main())