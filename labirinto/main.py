import labirinto as lb
import bfs as bf
import visualizator as vz

if __name__ == "__main__":
	labirinto = lb.Labirinto(20, 40)
	labirinto.show_map()

	bfs = bf.bfs(labirinto)
	finded = bfs.find_path()
	#print("Visitados:", bfs.get_visitados())
	print("Caminho encontrado:", finded)

	#labirinto.show_path(bfs.caminho)
	visualizador = vz.VisualizadorLabirinto(labirinto)
	visualizador.wait_loop(caminho=bfs.caminho, visitados=bfs.get_visitados())