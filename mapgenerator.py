import numpy as np
import random
import config


def criar_matriz_vazia():
    """Cria uma matriz preenchida com zeros"""
    return np.zeros((config.LINHAS, config.COLUNAS), dtype=int)

def gerar_pilares(matriz):
    """Cria as paredes fixas no mapa, estilo xadrez"""
    for y in range(config.LINHAS):
        for x in range(config.COLUNAS):
            if x % 2 != 0 and y % 2 != 0:
                matriz[y][x] = config.PAREDE


def espalhar_blocos(matriz, densidade=0.6):
    """Espalha blocos destrutíveis aleatoriamente pelo mapa, evitando as áreas de início dos jogadores"""

    L = config.LINHAS - 1
    C = config.COLUNAS - 1

    areas_seguras = [  # Coordenadas que devem permanecer vazias
        (0, 0),
        (0, 1),
        (1, 0),  # Superior Esquerdo (P1)
        (0, C),
        (0, C - 1),
        (1, C),  # Superior Direito (P2)
        (L, 0),
        (L - 1, 0),
        (L, 1),  # Inferior Esquerdo (P3)
        (L, C),
        (L, C - 1),
        (L - 1, C),  # Inferior Direito (P4)
    ]

    for y in range(config.LINHAS):
        for x in range(config.COLUNAS):
            if matriz[y][x] == config.VAZIO and (y, x) not in areas_seguras:
                if random.random() < densidade:
                    matriz[y][x] = config.BLOCO_DESTRUTIVEL


def posicionar_jogadores(matriz, qtd_jogadores):
    """Posiciona os jogadores nos cantos do mapa"""

    L = config.LINHAS - 1
    C = config.COLUNAS - 1
    matriz[0][0] = config.P1  # Superior Esquerdo
    if qtd_jogadores > 1:
        matriz[0][C] = config.P2  # Superior Direito
    if qtd_jogadores > 2:
        matriz[L][0] = config.P3  # Inferior Esquerdo
    if qtd_jogadores > 3:
        matriz[L][C] = config.P4  # Inferior Direito

def posicionar_inimigos(matriz, qtd_inimigos):
    inimigos_gerados = []
    metade_y = config.LINHAS // 2
    metade_x = config.COLUNAS // 2
    posicoes_vazias = []
    
    for y in range(config.LINHAS):
        for x in range(config.COLUNAS):
            fora_do_quadrante_player = (y > metade_y) or (x > metade_x)
            
            if matriz[y][x] == config.VAZIO and fora_do_quadrante_player:
                posicoes_vazias.append((y, x))
                
    random.shuffle(posicoes_vazias)
    
    for i in range(qtd_inimigos):
        if not posicoes_vazias:
            break
            
        y, x = posicoes_vazias.pop()
        
        id_inimigo = config.INIMIGO + i 
        matriz[y][x] = id_inimigo
        
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in direcoes:
            ny, nx = y + dy, x + dx
            if 0 <= ny < config.LINHAS and 0 <= nx < config.COLUNAS:
                if matriz[ny][nx] == config.BLOCO_DESTRUTIVEL:
                    matriz[ny][nx] = config.VAZIO 
                    
        inimigos_gerados.append({"y": y, "x": x, "id": id_inimigo})
        
    return inimigos_gerados
