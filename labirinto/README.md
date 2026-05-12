# Solucionador de Labirintos - Busca Cega (BFS & DFS)

Este projeto implementa e visualiza algoritmos de busca não informada (Largura e Profundidade) para resolver labirintos gerados aleatoriamente. O objetivo é comparar a eficiência e o comportamento de cada método em um ambiente de grade 2D.

# Tecnologias e Dependências

O projeto foi desenvolvido em Python 3.10+ e utiliza as seguintes bibliotecas:

NumPy: Para manipulação da matriz do labirinto.

Pygame: Para a interface gráfica e visualização em tempo real da busca.

Para instalar as dependências, execute:

```bash
pip install numpy pygame
```


# Como Executar

Certifique-se de que todos os arquivos (main.py, bfs.py, dfs.py, labirinto.py e visualizator.py) estão na mesma pasta.

Abra o terminal e execute:

```Bash
python main.py
```

A janela do Pygame será aberta e o algoritmo selecionado (configurado na variavel escolha no main.py) iniciará a busca automaticamente.

# Estrutura do Projeto

main.py: Ponto de entrada do programa. Configura o tamanho do labirinto e alterna entre os algoritmos.

bfs.py: Implementação da Busca em Largura..

dfs.py: Implementação da Busca em Profundidade.

labirinto.py: Lógica do ambiente, incluindo a função sucessor (can_move) e geração de obstáculos.

visualizator.py: Gerenciador da interface gráfica em Pygame.

### Legenda Visual

🟩 Verde: Ponto de Início.

🟥 Vermelho: Objetivo Final.

⬛ Preto: Paredes/Obstáculos (Valor 0).

⬜ Branco: Caminho livre (Valor 1).

🟦 Azul: Células visitadas/exploradas pelo algoritmo.

🟨 Amarelo: Caminho final encontrado da origem ao destino.

# Notas de Implementação

Função Sucessor: Implementada no método can_move da classe Labirinto, respeitando os limites da matriz e os obstáculos.

Teste de Objetivo: Verificado a cada iteração comparando a posição atual com o valor 3 (destino) na matriz.

Visualização em Tempo Real: O código está configurado para atualizar a interface a cada nó explorado, permitindo observar a diferença de comportamento entre a expansão radial do BFS e a expansão linear do DFS.