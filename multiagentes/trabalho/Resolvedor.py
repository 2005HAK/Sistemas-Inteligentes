import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio



class ExploracaoDFSBehaviour(CyclicBehaviour):
    async def on_start(self):
       
    

       # IP local do servidor XMPP
        self.labirinto_jid = "labirinto@192.168.1.74"

        self.posicao_virtual = (0, 0)
        self.visitados = set([self.posicao_virtual])
        self.caminho_atual = []
        self.caminho_inverso = []

        # Dicionários
        self.opostos = {'D': 'E', 'E': 'D', 'C': 'B', 'B': 'C'}
        self.deltas = {'D': (1, 0), 'E': (-1, 0), 'C': (0, 1), 'B': (0, -1)}

        self.achou_objetivo = False

    async def run(self):
        if self.achou_objetivo:
            return

        msg_req = Message(to=self.labirinto_jid)
        msg_req.set_metadata("performative", "request")
        msg_req.body = "precisa direção"
        await self.send(msg_req)

        resp_caminhos = await self.receive(timeout=10)
        if not resp_caminhos:
            print("Aguardando...")
            await asyncio.sleep(2)
            return

        body = resp_caminhos.body.replace('[', '').replace(']', '').replace("'", "").replace(" ", "")
        direcoes_recebidas = body.split(',') if body else []

        direcao_escolhida = None
        is_backtrack = False

        nao_visitadas = []
        for d in direcoes_recebidas:
            if d in self.deltas:
                dx, dy = self.deltas[d]
                nova_pos = (self.posicao_virtual[0] + dx, self.posicao_virtual[1] + dy)
                if nova_pos not in self.visitados:
                    nao_visitadas.append(d)

        if nao_visitadas:
            direcao_escolhida = nao_visitadas[0]
        else:
            if len(self.caminho_inverso) > 0:
                print("Beco sem saída, voltando...")
                direcao_escolhida = self.caminho_inverso.pop()
                self.caminho_atual.pop()
                is_backtrack = True
            else:
                print("Oxi '-' eae Hebert")
                self.kill()
                return

        msg_mov = Message(to=self.labirinto_jid)
        msg_mov.set_metadata("performative", "subscribe")
        msg_mov.body = direcao_escolhida
        await self.send(msg_mov)

        resp_mov = await self.receive(timeout=10)
        if resp_mov and resp_mov.body == "ok":
            dx, dy = self.deltas[direcao_escolhida]
            self.posicao_virtual = (self.posicao_virtual[0] + dx, self.posicao_virtual[1] + dy)
            self.visitados.add(self.posicao_virtual)

            if not is_backtrack:
                self.caminho_atual.append(direcao_escolhida)
                self.caminho_inverso.append(self.opostos[direcao_escolhida])
        else:
            print(f"Erro ao mover para {direcao_escolhida}. Labirinto não enviou 'ok'.")
            return

        msg_obj = Message(to=self.labirinto_jid)
        msg_obj.set_metadata("performative", "query_if")
        msg_obj.body = "objetivo"
        await self.send(msg_obj)

        resp_obj = await self.receive(timeout=10)
        if resp_obj and resp_obj.set_metadata("performative") == "inform-done":
            print("ONE PIECE!")
            self.achou_objetivo = True
            
            msg_prop = Message(to=self.labirinto_jid)
            msg_prop.set_metadata("performative", "propose")
            string_final = "".join(self.caminho_atual)
            msg_prop.body = string_final
            
            print(f"Caminho Final: {string_final}")
            await self.send(msg_prop)

            resp_final = await self.receive(timeout=10)
            if resp_final and resp_final.set_metadata("performative") == "accept_propose":
                self.kill()

        await asyncio.sleep(0.5)

class ResolvedorAgent(Agent):
    async def setup(self):
        print(f"Agente Resolvedor {self.jid} ligado.")
        self.add_behaviour(ExploracaoDFSBehaviour())




async def main():


    # servidor
    resolvedor = ResolvedorAgent("resolvedor_teste123@yax.im", "senha_secreta_123")
    
    
    await resolvedor.start(auto_register=True)
    while resolvedor.is_alive():
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("Encerrando...")
            await resolvedor.stop()
            break


if __name__ == "__main__":
    asyncio.run(main())