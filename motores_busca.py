import config
from collections import deque
import heapq

def obter_vizinhos(matriz, y, x):
    vizinhos = []
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    
    for dy, dx in direcoes:
        ny, nx = y + dy, x + dx
        
        # Verifica se está dentro do mapa
        if 0 <= ny < config.LINHAS and 0 <= nx < config.COLUNAS:
            alvo = matriz[ny][nx]
            # O inimigo pode andar se estiver VAZIO ou se for a posição de um Player 
            if alvo == config.VAZIO or alvo in (config.P1, config.P2, config.P3, config.P4):
                vizinhos.append((ny, nx))
    return vizinhos

def busca_bfs(matriz, inicio, objetivo):
    # Busca em largura utilizando a estrutura Fila
    fila = deque([[inicio]])
    visitados = set([inicio])

    while fila:
        caminho = fila.popleft()
        y, x = caminho[-1]

        if (y, x) == objetivo:
            return caminho  # Retorna a lista de tuplas com o caminho completo

        for vizinho in obter_vizinhos(matriz, y, x):
            if vizinho not in visitados:
                visitados.add(vizinho)
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                fila.append(novo_caminho)
    return [] 

def busca_dfs(matriz, inicio, objetivo): 
    # Busca profundidade utilizando a estrutura pilha
    pilha = deque([[inicio]])
    visitados = set([inicio])

    while pilha:
        caminho = pilha.pop()
        y, x = caminho[-1]

        if (y, x) == objetivo:
            return caminho  

        for vizinho in obter_vizinhos(matriz, y, x):
            if vizinho not in visitados:
                visitados.add(vizinho)
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                pilha.append(novo_caminho)
    return []

def busca_gulosa(matriz, inicio, objetivo):
    fila = []
    heapq.heappush(fila, (heuristica(inicio, objetivo), inicio, [inicio]))
    
    visitados = set([inicio])

    while fila:
        _, (y, x), caminho = heapq.heappop(fila)

        if (y, x) == objetivo:
            return caminho

        for vizinho in obter_vizinhos(matriz, y, x):
            if vizinho not in visitados:
                visitados.add(vizinho)
                novo_caminho = caminho + [vizinho]
                prioridade = heuristica(vizinho, objetivo)
                heapq.heappush(fila, (prioridade, vizinho, novo_caminho))
                
    return []

def heuristica(a, b): # Distância de Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def busca_a_estrela(matriz, inicio, objetivo):
    # Busca A* utilizando fila de prioridade
    fila = []
    heapq.heappush(fila, (0, inicio, [inicio]))
    visitados = {inicio: 0}

    while fila:
        custo_estimado, (y, x), caminho = heapq.heappop(fila)

        if (y, x) == objetivo:
            return caminho

        custo_real = len(caminho) - 1

        for vizinho in obter_vizinhos(matriz, y, x):
            novo_custo_real = custo_real + 1
            if vizinho not in visitados or novo_custo_real < visitados[vizinho]:
                visitados[vizinho] = novo_custo_real
                novo_caminho = caminho + [vizinho]
                # F(n) = G(n) [custo real] + H(n) [heurística]
                prioridade = novo_custo_real + heuristica(vizinho, objetivo)
                heapq.heappush(fila, (prioridade, vizinho, novo_caminho))
    return []