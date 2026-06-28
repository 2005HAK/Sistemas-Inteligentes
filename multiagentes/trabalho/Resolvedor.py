import spade # Biblioteca para agentes
from spade.agent import Agent # Classe base para criar agentes
from spade.behaviour import CyclicBehaviour # Comportamento cíclico para execução contínua
from spade.message import Message # Classe para criar mensagens entre agentes
import asyncio # Biblioteca para operações assíncronas, permitindo que o agente espere por mensagens sem bloquear a execução

agentResolver = "resolver@192.168.1.74"
# agent = "mashima_res_v5@yax.im"
agentLab = "lab@192.168.1.74"
# agentLab = "mashima_lab_v5@yax.im"
password = "senha123"

# Agente Resolvedor de Labirinto usando DFS (Depth-First Search)
class ExploracaoDFSBehaviour(CyclicBehaviour):
	# Inicialização do comportamento, definindo variáveis e estruturas de dados necessárias para a exploração do labirinto
	async def on_start(self):
		self.labirinto_jid = agentLab
		self.posicao_virtual = (0, 0)
		self.visitados = set([self.posicao_virtual])
		self.caminho_atual = []
		self.caminho_inverso = []
		self.opostos = {'D': 'E', 'E': 'D', 'C': 'B', 'B': 'C'}
		self.deltas = {'C': (-1, 0), 'B': (1, 0), 'D': (0, 1), 'E': (0, -1)}
		self.achou_objetivo = False

	# Método principal do comportamento, executado continuamente enquanto o agente estiver ativo.
	# Ele é responsável por solicitar os caminhos possíveis, escolher uma direção para se mover, 
	# enviar a tentativa de movimento e processar a resposta do labirinto, atualizando a posição 
	# virtual e os caminhos percorridos.
	async def run(self):
		if self.achou_objetivo:	return

		print(f"\nPosição Virtual: {self.posicao_virtual}")
		print("Perguntando caminhos possíveis...")
		
		msg_req = Message(to=self.labirinto_jid)
		msg_req.set_metadata("performative", "request")
		msg_req.body = "precisa direção"
		await self.send(msg_req)

		resp_caminhos = None
		for _ in range(10):
			msg = await self.receive(timeout=1)
			if msg and msg.get_metadata("performative") == "inform" and "[" in msg.body:
				resp_caminhos = msg
				break

		if not resp_caminhos:
			print("Timeout. Tentando novamente...")
			return

		body = str(resp_caminhos.body).replace('[', '').replace(']', '').replace("'", "").replace(" ", "")
		direcoes_recebidas = body.split(',') if body else []
		print(f"Labirinto respondeu: {direcoes_recebidas}")

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
			print(f"Novo caminho. Movendo para '{direcao_escolhida}'")
		else:
			if len(self.caminho_inverso) > 0:
				direcao_escolhida = self.caminho_inverso[-1]
				is_backtrack = True
				print(f"Beco sem saída! voltando '{direcao_escolhida}'")
			else:
				print("Labirinto sem saída. Eae Hebert '-'")								# -_-
				self.kill()
				await self.agent.stop()
				return

		print(f"Enviando tentativa de movimento: {direcao_escolhida}")
		msg_mov = Message(to=self.labirinto_jid)
		msg_mov.set_metadata("performative", "subscribe")
		msg_mov.body = direcao_escolhida
		await self.send(msg_mov)
		
		resp_mov = None
		for _ in range(10):
			msg = await self.receive(timeout=1)
			if msg and msg.get_metadata("performative") == "inform":
				if msg.body.strip() in ["ok", "nok"]:
					resp_mov = msg
					break

		if not resp_mov:
			print("Timeout ao mover...")
			return

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
			for _ in range(10):
				msg = await self.receive(timeout=.2)
				if msg and msg.get_metadata("performative") == "inform":
					if msg.body.strip() in ["done", "failure"]:
						resp_qif = msg
						break

			if not resp_qif:
				print("Timeout ao verificar objetivo...")
				return
			
			conteudo_qif = str(resp_qif.body).strip()

			if conteudo_qif == "done":
				print("\n THE ONE PIECE IS REAL! (Objetivo Encontrado)")
				self.achou_objetivo = True
				
				msg_prop = Message(to=self.labirinto_jid)
				msg_prop.set_metadata("performative", "propose")
				string_final = "".join(self.caminho_atual)
				msg_prop.body = string_final
				
				print(f"Enviando Caminho Final para validação: {string_final}")
				await self.send(msg_prop)
				
				resp_final = None
				for _ in range(10):
					msg = await self.receive(timeout=.2)
					if msg and str(msg.body).strip() == "accept_propose":
						resp_final = msg
						break

				if resp_final:
					print("Labirinto aceitou o caminho. Agente desligando!")
					self.kill()
					await self.agent.stop()
		else:
			print(f"[ERRO] Movimento recusado. PosVirtual={self.posicao_virtual} Resposta={conteudo_mov}")

# Classe do agente Resolvedor de Labirinto, responsável por iniciar o comportamento de exploração e gerenciar a comunicação com o labirinto.
class ResolvedorAgent(Agent):
	async def setup(self):
		print(f"Resolvedor de Labirínto {self.jid} online.")
		self.add_behaviour(ExploracaoDFSBehaviour())

# Função principal para iniciar o agente Resolvedor.
async def main():
	resolvedor = ResolvedorAgent(agentResolver, password, verify_security=False)
	await resolvedor.start()
	while resolvedor.is_alive():
		try:
			await asyncio.sleep(1)
		except KeyboardInterrupt:
			print("Encerrando...")
			await resolvedor.stop()
			break

# Ponto de entrada do script, iniciando a função principal para criar e executar o agente Resolvedor.
if __name__ == "__main__":
	asyncio.run(main())