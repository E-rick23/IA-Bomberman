from time import sleep

import pygame
import config

sprites = {}

animacoes_player = {
    "direita": {"parado": [], "andando": [], "plantando": []},
    "esquerda": {"parado": [], "andando": [], "plantando": []},
    "baixo": {"parado": [], "andando": [], "plantando": []},
    "cima": {"parado": [], "andando": [], "plantando": []},
}


def recortar_sprite(sheet, col, linha):
    rect = pygame.Rect(
        col * config.SPRITE_SIZE,
        linha * config.SPRITE_SIZE,
        config.SPRITE_SIZE,
        config.SPRITE_SIZE,
    )
    sub = sheet.subsurface(rect)
    return pygame.transform.scale(sub, (config.TILE_SIZE, config.TILE_SIZE))


def _fazer_sprite_solido(cor):
    s = pygame.Surface((config.SPRITE_SIZE, config.SPRITE_SIZE))
    s.fill(cor)
    return pygame.transform.scale(s, (config.TILE_SIZE, config.TILE_SIZE))


def _fazer_sprite_bomba():
    s = pygame.Surface((config.TILE_SIZE, config.TILE_SIZE), pygame.SRCALPHA)
    cx, cy, r = config.TILE_SIZE // 2, config.TILE_SIZE // 2, config.TILE_SIZE // 2 - 4
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
    sprites[config.VAZIO] = _fazer_sprite_solido((34, 139, 34))
    sprites[config.PAREDE] = _fazer_sprite_solido((128, 128, 128))
    sprites[config.FOGO] = _fazer_sprite_solido((255, 69, 0))
    sprites[config.BLOCO_DESTRUTIVEL] = _fazer_sprite_solido((139, 69, 19))
    sprites[config.BOMBA] = _fazer_sprite_bomba()


def desenhar_mapa(tela, matriz):
    for y in range(config.LINHAS):
        for x in range(config.COLUNAS):
            pos = (x * config.TILE_SIZE, y * config.TILE_SIZE)
            celula = matriz[y][x]

            # Sempre desenha o chão primeiro
            tela.blit(sprites[config.VAZIO], pos)

            if celula == config.PAREDE:
                tela.blit(sprites[config.PAREDE], pos)
            elif celula == config.BLOCO_DESTRUTIVEL:
                tela.blit(sprites[config.BLOCO_DESTRUTIVEL], pos)
            elif celula == config.BOMBA:
                tela.blit(sprites[config.BOMBA], pos)
            elif celula == config.FOGO:
                tela.blit(sprites[config.FOGO], pos)
                sleep(0.1)  # Pequena pausa para destacar o fogo
                matriz[y][x] = config.VAZIO
            # Players são desenhados pelos próprios objetos Player


def desenhar_hud(tela, jogadores):
    """Exibe status básico dos jogadores no topo da tela."""
    fonte = pygame.font.SysFont("Arial", 16, bold=True)
    cores_id = {config.P1: (100, 180, 255), config.P2: (255, 120, 120)}
    nomes_id = {config.P1: "P1 ↑↓←→ [Space]", config.P2: "P2 WASD [Shift]"}

    for i, jogador in enumerate(jogadores):
        cor = cores_id.get(jogador.id, (255, 255, 255))
        status = "VIVO" if jogador.vivo else "MORTO"
        texto = fonte.render(
            f"{nomes_id.get(jogador.id, f'P{i+1}')}  {status}", True, cor
        )
        tela.blit(texto, (10 + i * 300, 4))
