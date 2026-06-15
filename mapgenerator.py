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
    inimigos = []

    while len(inimigos) < qtd_inimigos:
        x = random.randint(1, config.COLUNAS - 1)
        y = random.randint(1, config.LINHAS - 1)
        
        if not (x % 2 != 0 and y % 2 != 0):
            if matriz[y][x] != 9:
                matriz[y][x] = 9
                inimigos.append([x, y])
    
    return inimigos