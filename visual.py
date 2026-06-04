# visual.py
import pygame
from config import *

# Definição de Cores (RGB)
COR_VAZIO = (34, 139, 34)         # Verde (Grama)
COR_PAREDE = (128, 128, 128)      # Cinza (Pilar indestrutível)
COR_BLOCO = (139, 69, 19)         # Marrom (Bloco destrutível)
COR_BOMBA = (0, 0, 0)             # Preto
COR_PLAYER = (0, 0, 255)          # Azul (Representando o P1)
COR_INIMIGO = (255, 0, 0)         # Vermelho (Outros players)

def desenhar_mapa(tela, matriz):
    """Varre a matriz e desenha cada elemento na tela baseado no TILE_SIZE."""
    for y in range(LINHAS):
        for x in range(COLUNAS):
            # Calcula a posição do topo esquerdo do bloco em pixels
            pos_x = x * TILE_SIZE
            pos_y = y * TILE_SIZE
            
            # Cria o retângulo que define a área do bloco
            retangulo = pygame.Rect(pos_x, pos_y, TILE_SIZE, TILE_SIZE)
            
            # Identifica o que está na célula atual e define a cor
            celula = matriz[y][x]
            
            if celula == VAZIO:
                pygame.draw.rect(tela, COR_VAZIO, retangulo)
            elif celula == PAREDE:
                pygame.draw.rect(tela, COR_PAREDE, retangulo)
            elif celula == BLOCO_DESTRUTIVEL:
                pygame.draw.rect(tela, COR_BLOCO, retangulo)
            elif celula == BOMBA:
                pygame.draw.rect(tela, COR_BOMBA, retangulo)
            elif celula == P1:
                # Desenha o chão verde por baixo e o jogador (um círculo) por cima
                pygame.draw.rect(tela, COR_VAZIO, retangulo)
                pygame.draw.circle(tela, COR_PLAYER, (pos_x + TILE_SIZE//2, pos_y + TILE_SIZE//2), TILE_SIZE//3)
            elif celula in [P2, P3, P4]:
                # Outros jogadores
                pygame.draw.rect(tela, COR_VAZIO, retangulo)
                pygame.draw.circle(tela, COR_INIMIGO, (pos_x + TILE_SIZE//2, pos_y + TILE_SIZE//2), TILE_SIZE//3)
                
            # Opcional: Desenha uma linha fina ao redor de cada tile para ajudar a enxergar o grid
            pygame.draw.rect(tela, (0, 100, 0), retangulo, 1)
