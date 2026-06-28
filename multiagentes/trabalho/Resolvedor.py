import spade																								# Biblioteca para agentes
from spade.agent import Agent																				# Classe base para criar agentes
from spade.behaviour import CyclicBehaviour																	# Comportamento cíclico para execução contínua
from spade.message import Message																			# Classe para criar mensagens entre agentes
import asyncio																								# Biblioteca para operações assíncronas, permitindo que o agente espere por mensagens sem bloquear a execução

agentResolver = "resolver@192.168.1.74" 
# agentResolver = "mashima_res_v5@yax.im"
agentLab = "lab@192.168.1.74"
# agentLab = "mashima_lab_v5@yax.im"
password = "senha123"

class ExploracaoBehaviour(CyclicBehaviour):
	'''
	Agente Resolvedor de Labirinto usando DFS (Depth-First Search) e BFS (Breadth-First Search)
	'''

	async def on_start(self):
		'''
		Inicialização do comportamento, definindo variáveis e estruturas de dados necessárias para a exploração do labirinto
		'''

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
	
	async def limpar_caixa(self):
		while await self.receive(timeout=0.01):
			pass
	
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

	async def run(self):
		'''
		Método principal do comportamento, executado continuamente enquanto o agente estiver ativo.
		
		Ele é responsável por solicitar os caminhos possíveis, escolher uma direção para se mover, enviar a tentativa de movimento e processar a resposta do labirinto, atualizando a posição virtual e os caminhos percorridos.
		'''

		if self.exploracao_concluida:	return

		print(f"\nPosição Virtual: {self.posicao_virtual}")
		print("Perguntando caminhos possíveis...")

		await self.limpar_caixa()

		msg_req = Message(to=self.labirinto_jid)
		msg_req.set_metadata("performative", "request")
		msg_req.body = "precisa direção"
		await self.send(msg_req)

		resp_caminhos = None
		while True:
			msg = await self.receive(timeout=10)
			if not msg:
				print("Servidor lagou. Aguardando resposta sem spam...")
				await self.send(msg_req)
				continue
			if msg and msg.get_metadata("performative") == "inform" and "[" in msg.body:
				resp_caminhos = msg
				break

		body = str(resp_caminhos.body).replace('[', '').replace(']', '').replace("'", "").replace(" ", "")
		direcoes_recebidas = body.split(',') if body else []
		print(f"[RESOLVEDOR] <- Labirinto respondeu: {direcoes_recebidas}")

		if self.posicao_virtual not in self.grafo:	self.grafo[self.posicao_virtual] = direcoes_recebidas

		direcao_escolhida = None
		is_backtrack = False

		nao_visitadas = []
		for d in direcoes_recebidas:
			if d in self.deltas:
				dx, dy = self.deltas[d]
				nova_pos = (self.posicao_virtual[0] + dx, self.posicao_virtual[1] + dy)
				if nova_pos not in self.visitados:	nao_visitadas.append(d)

		if nao_visitadas:
			direcao_escolhida = nao_visitadas[0]
			print(f"Decisão: Novo caminho. Movendo para '{direcao_escolhida}'")
		else:
			if len(self.caminho_inverso) > 0:
				direcao_escolhida = self.caminho_inverso[-1]
				is_backtrack = True
				print(f"Beco sem saída! Fazendo backtrack para '{direcao_escolhida}'")
			else:
				print("DFS CONCLUÍDO!")
				self.exploracao_concluida = True

				if self.posicao_objetivo:
					print(f"Iniciando BFS até {self.posicao_objetivo}...")
					caminho_otimo = self.calcular_bfs()

					print("=COMPARAÇÃO DE DFS vs BFS:")
					print(f"Caminho inicial (DFS): {self.caminho_dfs_bruto} (Tamanho: {len(self.caminho_dfs_bruto)} passos)")
					print(f"Caminho otimizado (BFS): {caminho_otimo} (Tamanho: {len(caminho_otimo)} passos)")

					await self.limpar_caixa()
					msg_prop = Message(to=self.labirinto_jid)
					msg_prop.set_metadata("performative", "propose")

					payload = f"{self.caminho_dfs_bruto},{caminho_otimo}"
					msg_prop.body = payload

					print(f"\nEnviando Caminhos para o Labirinto...")
					await self.send(msg_prop)

					while True:
						msg = await self.receive(timeout=10)
						if not msg:
							print("Servidor lagou. Aguardando resposta sem spam...")
							await self.send(msg_prop)
							continue
						if str(msg.body).strip() == "accept_propose":
							print("Labirinto aceitou o caminho. Desligando...")
							self.kill()
							await self.agent.stop()
							break
				else:
					print("Labirinto totalmente explorado, mas não tem saída.")
					self.kill()
					await self.agent.stop()
				return

		print(f"Enviando tentativa de movimento: {direcao_escolhida}")

		await self.limpar_caixa()

		msg_mov = Message(to=self.labirinto_jid)
		msg_mov.set_metadata("performative", "subscribe")
		msg_mov.body = direcao_escolhida
		await self.send(msg_mov)

		resp_mov = None
		while True:
			msg = await self.receive(timeout=1)
			if not msg:
				print("O servidor lagou. Aguardando movimento sem fazer spam...")
				await self.send(msg_mov)
				continue
			if msg and msg.get_metadata("performative") == "inform":
				if msg.body.strip() in ["ok", "nok"]:
					resp_mov = msg
					break

		conteudo_mov = str(resp_mov.body).strip()

		if conteudo_mov == "ok":
			print("Labirinto confirmou movimento.")
			dx, dy = self.deltas[direcao_escolhida]
			self.posicao_virtual = (self.posicao_virtual[0] + dx, self.posicao_virtual[1] + dy)
			self.visitados.add(self.posicao_virtual)

			if not is_backtrack:
				self.caminho_atual.append(direcao_escolhida)
				self.caminho_inverso.append(self.opostos[direcao_escolhida])
			else:
				self.caminho_inverso.pop()
				self.caminho_atual.pop()

			print("Perguntando se chegou no objetivo...")
			msg_qif = Message(to=self.labirinto_jid)
			msg_qif.set_metadata("performative", "queryif")
			msg_qif.body = "Chegou?"
			await self.send(msg_qif)

			resp_qif = None
			while True:
				msg = await self.receive(timeout=1)
				if not msg:
					print("O servidor lagou. Aguardando resposta sem fazer spam...")
					await self.send(msg_qif)
					continue
				if msg and msg.get_metadata("performative") == "inform":
					if msg.body.strip() in ["done", "failure"]:
						resp_qif = msg
						break

			conteudo_qif = str(resp_qif.body).strip()

			if conteudo_qif == "done":
				if not self.posicao_objetivo:
					self.posicao_objetivo = self.posicao_virtual
					self.caminho_dfs_bruto = "".join(self.caminho_atual) 
					print(f"\nOBJETIVO ENCONTRADO em {self.posicao_virtual}!")
					print("Memorizando a posição e continuando a explorar o resto do mapa...")
		else:	print(f"[ERRO] Movimento recusado. PosVirtual={self.posicao_virtual} Resposta={conteudo_mov}")

		await asyncio.sleep(.1)

class ResolvedorAgent(Agent):
	'''
	Classe do agente Resolvedor de Labirinto, responsável por iniciar o comportamento de exploração e gerenciar a comunicação com o labirinto.
	'''

	async def setup(self):
		print(f"Resolvedor de Labirínto {self.jid} online.")
		self.add_behaviour(ExploracaoBehaviour())

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