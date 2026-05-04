import numpy as np

# Constantes do mapa

VAZIO = 0
PAREDE = 1
BLOCO_DESTRUTIVEL = 2
BOMBA = 3
JOGADOR = 4
INIMIGO = 5

linhas, colunas = 9, 9 # Variáveis da matriz do mapa
mapa = np.zeros((linhas,colunas), dtype=int) # Criando o mapa preenchido com zeros

#Cria as paredes fixas no mapa, estilo xadrez.
def gerar_pilares(matriz):
    for y in range(linhas):
        for x in range(colunas):
            if x % 2 != 0 and y % 2 != 0:
                matriz[y][x] = PAREDE

gerar_pilares(mapa)
print(mapa)
