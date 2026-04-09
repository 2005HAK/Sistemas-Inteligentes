import labirinto as lb
import bfs as bf
import dfs as df
import visualizator as vz

if __name__ == "__main__":
	labirinto = lb.Labirinto(40)
	labirinto.show_map()
	
	escolha = "bfs"

	visualizador = vz.VisualizadorLabirinto(labirinto)

	if escolha == "dfs":
		dfs = df.dfs(labirinto, visualizador)
		finded = dfs.find_path()
		visualizador.wait_loop(caminho=dfs.caminho, visitados=dfs.get_visitados())
	elif escolha == "bfs":
		bfs = bf.bfs(labirinto, visualizador)
		finded = bfs.find_path()
		visualizador.wait_loop(caminho=bfs.caminho, visitados=bfs.get_visitados())