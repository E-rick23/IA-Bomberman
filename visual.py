# visual.py
import pygame
from config import *

# Dicionário para guardar as imagens carregadas e escalonadas
sprites = {}

# Definição de Cores (RGB)
COR_VAZIO = (34, 139, 34)         # Verde (Grama)
COR_PAREDE = (128, 128, 128)      # Cinza (Pilar indestrutível)
COR_BLOCO = (139, 69, 19)         # Marrom (Bloco destrutível)
COR_BOMBA = (0, 0, 0)             # Preto
COR_PLAYER = (0, 0, 255)          # Azul (Representando o P1)
COR_INIMIGO = (255, 0, 0)         # Vermelho (Outros players)

# Dicionário estruturado para as animações do jogador
animacoes_player = {
    "direita":  {"parado": [], "andando": [], "plantando": []},
    "esquerda": {"parado": [], "andando": [], "plantando": []},
    "baixo":    {"parado": [], "andando": [], "plantando": []},
    "cima":     {"parado": [], "andando": [], "plantando": []}
}

def recortar_sprite(sheet, col, linha):
    """Corta um quadrado 16x16 da spritesheet e amplia para o TILE_SIZE."""
    # Define o retângulo de corte na imagem original (16x16)
    rect = pygame.Rect(col * SPRITE_SIZE, linha * SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE)
    sub_surface = sheet.subsurface(rect)
    
    # Amplia preservando os pixels nítidos (Filtro NEAREST)
    return pygame.transform.scale(sub_surface, (TILE_SIZE, TILE_SIZE))

def desenhar_player(tela, player_estado):
    pos_x = player_estado["x"] * TILE_SIZE
    pos_y = player_estado["y"] * TILE_SIZE
    
    direcao = player_estado["direcao"]
    status = player_estado["status"]
    frame = player_estado["frame_atual"]
    
    # Se o status for parado ou plantando, geralmente só temos 1 frame (índice 0)
    if status != "andando":
        frame = 0
        
    sprite_final = animacoes_player[direcao][status][frame]
    tela.blit(sprite_final, (pos_x, pos_y))
    
def carregar_recursos():
    """Carrega as imagens 16x16 e redimensiona para o tamanho de exibição."""
    global animacoes_player
    # Carrega a spritesheet (lembre de salvar sua imagem na pasta do script)
    sheet = pygame.image.load("Assets/Players.png").convert_alpha()
    
    # --- DIREITA ---
    animacoes_player["direita"]["parado"].append(recortar_sprite(sheet, 0, 0))
    animacoes_player["direita"]["andando"].append(recortar_sprite(sheet, 1, 0))
    animacoes_player["direita"]["plantando"].append(recortar_sprite(sheet, 2, 0))
    
    # --- ESQUERDA ---
    animacoes_player["esquerda"]["parado"].append(recortar_sprite(sheet, 0, 1))
    animacoes_player["esquerda"]["andando"].append(recortar_sprite(sheet, 1, 1))
    animacoes_player["esquerda"]["plantando"].append(recortar_sprite(sheet, 2, 1))
    
    # --- BAIXO --- (Tem 2 frames de caminhada alternando braços)
    animacoes_player["baixo"]["parado"].append(recortar_sprite(sheet, 5, 0))
    animacoes_player["baixo"]["andando"].append(recortar_sprite(sheet, 6, 0)) # Braço R
    animacoes_player["baixo"]["andando"].append(recortar_sprite(sheet, 6, 1)) # Braço L
    
    # --- CIMA --- (Tem 2 frames de caminhada alternando braços)
    animacoes_player["cima"]["parado"].append(recortar_sprite(sheet, 7, 0))
    animacoes_player["cima"]["andando"].append(recortar_sprite(sheet, 8, 0)) # Braço R
    animacoes_player["cima"]["andando"].append(recortar_sprite(sheet, 8, 1)) # Braço L
    
    # Por enquanto, vamos criar superfícies genéricas de 16x16 para simular os seus sprites
    img_vazio = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
    img_vazio.fill((34, 139, 34)) # Verde
    
    img_parede = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
    img_parede.fill((128, 128, 128)) # Cinza
    
    img_bloco = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
    img_bloco.fill((139, 69, 19)) # Marrom
    
    img_p1 = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(img_p1, (0, 0, 255), (SPRITE_SIZE//2, SPRITE_SIZE//2), SPRITE_SIZE//2 - 1) # Círculo Azul interno
    
    # ESCALONAMENTO: Aqui o Pygame pega a imagem 16x16 e transforma no TILE_SIZE (ex: 64x64)
    # O filtro 'NEAREST' impede que a pixel art fique borrada ao crescer
    sprites[VAZIO] = pygame.transform.scale(img_vazio, (TILE_SIZE, TILE_SIZE))
    sprites[PAREDE] = pygame.transform.scale(img_parede, (TILE_SIZE, TILE_SIZE))
    sprites[BLOCO_DESTRUTIVEL] = pygame.transform.scale(img_bloco, (TILE_SIZE, TILE_SIZE))
    sprites[P1] = pygame.transform.scale(img_p1, (TILE_SIZE, TILE_SIZE))
    
def desenhar_mapa(tela, matriz):
    """Desenha o mapa utilizando os sprites escalonados."""
    for y in range(LINHAS):
        for x in range(COLUNAS):
            pos_x = x * TILE_SIZE
            pos_y = y * TILE_SIZE
            
            celula = matriz[y][x]
            
            # Como os players se movem por cima do chão, desenha o VAZIO (grama) primeiro
            if celula in [P1, P2, P3, P4, BOMBA]:
                tela.blit(sprites[VAZIO], (pos_x, pos_y))
                
            # Desenha o sprite correspondente se ele existir no nosso dicionário
            if celula in sprites:
                tela.blit(sprites[celula], (pos_x, pos_y))
            else:
                # Caso seja P2, P3 ou P4 e ainda não tenhamos o sprite deles
                if celula != VAZIO:
                    # Desenha o fundo padrão para segurança
                    tela.blit(sprites[VAZIO], (pos_x, pos_y))
