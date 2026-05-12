import pygame
import sys

COR_FUNDO = (30, 30, 30)
COR_PAREDE = (0, 0, 0) 
COR_CAMINHO = (255, 255, 255)
COR_INICIO = (0, 255, 0)
COR_FIM = (255, 0, 0)
COR_ROTA = (255, 255, 0)
COR_VISITADOS = (50, 50, 150)

class VisualizadorLabirinto:
	def __init__(self, labirinto, tile_size=20):
		pygame.init()

		self.lab = labirinto
		self.tile_size = tile_size

		self.width = len(labirinto.mapa[0]) * tile_size
		self.height = len(labirinto.mapa) * tile_size
		self.screen = pygame.display.set_mode((self.width, self.height), pygame.SHOWN)
		pygame.display.set_caption("Labirinto")

	def draw(self, caminho=[], visitados=[]):
		self.screen.fill(COR_FUNDO)

		for i in range(len(self.lab.mapa)):
			for j in range(len(self.lab.mapa[0])):
				rect = pygame.Rect(j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size)
				
				if self.lab.mapa[i][j] == 0:
					pygame.draw.rect(self.screen, COR_PAREDE, rect)
				else:
					pygame.draw.rect(self.screen, COR_CAMINHO, rect)

				if (i, j) in visitados and (i, j) != self.lab.initial_position:
					pygame.draw.rect(self.screen, COR_VISITADOS, rect)

				if (i, j) in caminho:
					pygame.draw.rect(self.screen, COR_ROTA, rect)

				if (i, j) == self.lab.initial_position:
					pygame.draw.rect(self.screen, COR_INICIO, rect)
				elif (i, j) == self.lab.final_position:
					pygame.draw.rect(self.screen, COR_FIM, rect)

				pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

		pygame.display.flip()

	def wait_loop(self, caminho=[], visitados=[]):
		run = True
		while run:
			for evento in pygame.event.get():
				if evento.type == pygame.QUIT:
					run = False
			self.draw(caminho, visitados)
		pygame.quit()