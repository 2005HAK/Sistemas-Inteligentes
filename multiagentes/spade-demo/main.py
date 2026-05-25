import spade

class DummyAgent(spade.agent.Agent):
	async def setup(self):
		print("Hello World! I'm agent {}".format(str(self.jid)))

async def main():
	dummy = DummyAgent("ti@150.162.216.218", "teste", verify_security=False)
	await dummy.start(auto_register=False)

if __name__ == "__main__":
	spade.run(main())
