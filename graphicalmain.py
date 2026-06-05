import pygame
import sys
import mapgenerator
import visual
import bombas
from config import *
from player import Player


def main():
    pygame.init()
    pygame.display.set_caption("Bomberman")

    largura = COLUNAS * TILE_SIZE
    # Altura extra no topo para o HUD
    HUD_H = 24
    altura = LINHAS * TILE_SIZE + HUD_H

    tela = pygame.display.set_mode((largura, altura))
    visual.carregar_recursos()
    clock = pygame.time.Clock()

    # --- Mapa ---
    tabuleiro = mapgenerator.criar_matriz_vazia()
    mapgenerator.gerar_pilares(tabuleiro)
    mapgenerator.espalhar_blocos(tabuleiro, densidade=0.60)
    mapgenerator.posicionar_jogadores(tabuleiro)

    # --- Jogadores ---
    L, C = LINHAS - 1, COLUNAS - 1
    jogadores = [
        Player(0, 0, P1),   # canto superior esquerdo
        Player(0, C, P2),   # canto superior direito
    ]

    rodando = True
    while rodando:
        dt = clock.tick(60)  # 4K 60 FPS

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False

            for jogador in jogadores:
                jogador.processar_input(evento, tabuleiro)

        bombas.atualizar_bombas(tabuleiro, dt)

        for jogador in jogadores:
            jogador.atualizar(dt, tabuleiro, visual.animacoes_player)

        tela.fill((0, 0, 0))

        # Offset vertical para o HUD
        mapa_surface = tela.subsurface(pygame.Rect(0, HUD_H, largura, LINHAS * TILE_SIZE))
        visual.desenhar_mapa(mapa_surface, tabuleiro)

        for jogador in jogadores:
            # Ajusta posição para o offset do HUD
            if jogador.vivo:
                pos_x = jogador.x * TILE_SIZE
                pos_y = jogador.y * TILE_SIZE + HUD_H
                frame = jogador.frame_atual if jogador.status == "andando" else 0
                lista = visual.animacoes_player[jogador.direcao][jogador.status]
                sprite = lista[frame % len(lista)]
                tela.blit(sprite, (pos_x, pos_y))

        # Bombas (desenhadas sobre o mapa)
        for b in bombas.bombas_ativas:
            if not b.explodiu:
                pos_x = b.x * TILE_SIZE
                pos_y = b.y * TILE_SIZE + HUD_H
                tela.blit(visual.sprites[BOMBA], (pos_x, pos_y))

        visual.desenhar_hud(tela, jogadores)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
