import numpy as np
import random
from config import *

def criar_matriz_vazia():
    return np.zeros((LINHAS,COLUNAS), dtype=int) # Criando o mapa preenchido com zeros

#Cria as paredes fixas no mapa, estilo xadrez.
def gerar_pilares(matriz):
    for y in range(LINHAS):
        for x in range(COLUNAS):
            if x % 2 != 0 and y % 2 != 0:
                matriz[y][x] = PAREDE

#Função que espalha blocos destrutíveis aleatóriamente pelo mapa, evitando cantos.
#A densidade é um valor entre 0.0 e 1.0 que define a chance de um bloco aparecer.
def espalhar_blocos(matriz, densidade=0.6):
    #Últimas posições do grid
    L = LINHAS -1
    C = COLUNAS -1
    #Coordenadas que devem permanecer vazias
    areas_seguras = [
            (0,0),(0,1),(1,0), #Superior Esquerdo (P1)
            (0, C), (0, C-1), (1, C), #Superior Direito (P2)
            (L, 0), (L-1, 0), (L,1), #Inferior Esquerdo (P3)
            (L, C), (L, C-1), (L-1, C) #Inferior Direito (P4)
    ]
    for y in range(LINHAS):
        for x in range(COLUNAS):
            if matriz[y][x] == VAZIO and (y, x) not in areas_seguras:
                if random.random() < densidade:
                    matriz[y][x] = BLOCO_DESTRUTIVEL

def posicionar_jogadores(matriz):
    L = LINHAS - 1
    C = COLUNAS - 1
    matriz[0][0] = P1 #Superior Esquerdo
    matriz[0][C] = P2 #Superior Direito
    matriz[L][0] = P3 #Inferior Esquerdo
    matriz[L][C] = P4 #Inferior Direito

