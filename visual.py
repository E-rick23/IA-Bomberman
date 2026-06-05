from time import sleep

import pygame
from config import *

sprites = {}

animacoes_player = {
    "direita":  {"parado": [], "andando": [], "plantando": []},
    "esquerda": {"parado": [], "andando": [], "plantando": []},
    "baixo":    {"parado": [], "andando": [], "plantando": []},
    "cima":     {"parado": [], "andando": [], "plantando": []},
}


def recortar_sprite(sheet, col, linha):
    rect = pygame.Rect(col * SPRITE_SIZE, linha * SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE)
    sub = sheet.subsurface(rect)
    return pygame.transform.scale(sub, (TILE_SIZE, TILE_SIZE))


def _fazer_sprite_solido(cor):
    s = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
    s.fill(cor)
    return pygame.transform.scale(s, (TILE_SIZE, TILE_SIZE))


def _fazer_sprite_bomba():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    cx, cy, r = TILE_SIZE // 2, TILE_SIZE // 2, TILE_SIZE // 2 - 4
    pygame.draw.circle(s, (20, 20, 20), (cx, cy), r)
    # Pavio
    pygame.draw.line(s, (200, 100, 0), (cx, cy - r), (cx + 6, cy - r - 8), 3)
    return s


def carregar_recursos():
    global animacoes_player

    # Tenta carregar spritesheet real; se não existir usa placeholders
    try:
        sheet = pygame.image.load("Assets/Players.png").convert_alpha()

        animacoes_player["direita"]["parado"].append(recortar_sprite(sheet, 0, 0))
        animacoes_player["direita"]["andando"].append(recortar_sprite(sheet, 1, 0))
        animacoes_player["direita"]["plantando"].append(recortar_sprite(sheet, 2, 0))

        animacoes_player["esquerda"]["parado"].append(recortar_sprite(sheet, 0, 1))
        animacoes_player["esquerda"]["andando"].append(recortar_sprite(sheet, 1, 1))
        animacoes_player["esquerda"]["plantando"].append(recortar_sprite(sheet, 2, 1))

        animacoes_player["baixo"]["parado"].append(recortar_sprite(sheet, 5, 0))
        animacoes_player["baixo"]["andando"].append(recortar_sprite(sheet, 6, 0))
        animacoes_player["baixo"]["andando"].append(recortar_sprite(sheet, 6, 1))

        animacoes_player["cima"]["parado"].append(recortar_sprite(sheet, 7, 0))
        animacoes_player["cima"]["andando"].append(recortar_sprite(sheet, 8, 0))
        animacoes_player["cima"]["andando"].append(recortar_sprite(sheet, 8, 1))

    except (pygame.error, FileNotFoundError):
        # Placeholder: quadrado azul para o jogador
        placeholder = _fazer_sprite_solido((0, 0, 255))
        for direcao in animacoes_player:
            for acao in animacoes_player[direcao]:
                animacoes_player[direcao][acao] = [placeholder]

    # Sprites do mapa
    sprites[VAZIO]            = _fazer_sprite_solido((34, 139, 34))
    sprites[PAREDE]           = _fazer_sprite_solido((128, 128, 128))
    sprites[FOGO]             = _fazer_sprite_solido((255, 69, 0))
    sprites[BLOCO_DESTRUTIVEL]= _fazer_sprite_solido((139, 69, 19))
    sprites[BOMBA]            = _fazer_sprite_bomba()


def desenhar_mapa(tela, matriz):
    for y in range(LINHAS):
        for x in range(COLUNAS):
            pos = (x * TILE_SIZE, y * TILE_SIZE)
            celula = matriz[y][x]

            # Sempre desenha o chão primeiro
            tela.blit(sprites[VAZIO], pos)

            if celula == PAREDE:
                tela.blit(sprites[PAREDE], pos)
            elif celula == BLOCO_DESTRUTIVEL:
                tela.blit(sprites[BLOCO_DESTRUTIVEL], pos)
            elif celula == BOMBA:
                tela.blit(sprites[BOMBA], pos)
            elif celula == FOGO:
                tela.blit(sprites[FOGO], pos)
                sleep(0.1)  # Pequena pausa para destacar o fogo
                matriz[y][x] = VAZIO
            # Players são desenhados pelos próprios objetos Player


def desenhar_hud(tela, jogadores):
    """Exibe status básico dos jogadores no topo da tela."""
    fonte = pygame.font.SysFont("Arial", 16, bold=True)
    cores_id = {P1: (100, 180, 255), P2: (255, 120, 120)}
    nomes_id  = {P1: "P1 ↑↓←→ [Space]", P2: "P2 WASD [Shift]"}

    for i, jogador in enumerate(jogadores):
        cor = cores_id.get(jogador.id, (255, 255, 255))
        status = "VIVO" if jogador.vivo else "MORTO"
        texto = fonte.render(f"{nomes_id.get(jogador.id, f'P{i+1}')}  {status}", True, cor)
        tela.blit(texto, (10 + i * 300, 4))
