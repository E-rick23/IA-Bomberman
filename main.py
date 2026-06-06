import pygame
import sys
import config
import mapgenerator
import visual
import bombas
from player import Player
from menu import Menu


def main():
    menu = Menu()
    config_escolhida = menu.rodar()

    # Injetar as configurações escolhidas no config global antes do jogo iniciar
    config.LINHAS = config_escolhida["tamanho"]
    config.COLUNAS = config_escolhida["tamanho"]
    qtd_jogadores = config_escolhida["players"]
    dificuldade = config_escolhida["dificuldade"]

    print(
        f"Iniciando mapa {config.LINHAS}x{config.COLUNAS} com {qtd_jogadores} players na dificuldade '{dificuldade}'"
    )

    # Inicializar o jogo real com o tamanho do mapa adaptado
    pygame.init()
    pygame.display.set_caption("Bomberman")

    largura = config.COLUNAS * config.TILE_SIZE
    HUD_H = 24
    altura = config.LINHAS * config.TILE_SIZE + HUD_H

    tela = pygame.display.set_mode((largura, altura))
    visual.carregar_recursos()
    clock = pygame.time.Clock()

    # Gerar mapa
    tabuleiro = mapgenerator.criar_matriz_vazia()
    mapgenerator.gerar_pilares(tabuleiro)
    mapgenerator.espalhar_blocos(tabuleiro, densidade=0.60)
    mapgenerator.posicionar_jogadores(tabuleiro)

    L, C = config.LINHAS - 1, config.COLUNAS - 1

    pool_jogadores = [
        Player(0, 0, config.P1),
        Player(0, C, config.P2),
        Player(L, 0, config.P3),
        Player(L, C, config.P4),
    ]

    # Filtra apenas a quantidade selecionada no menu
    jogadores = pool_jogadores[:qtd_jogadores]

    rodando = True
    while rodando:
        dt = clock.tick(60)

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

        mapa_surface = tela.subsurface(
            pygame.Rect(0, HUD_H, largura, config.LINHAS * config.TILE_SIZE)
        )
        visual.desenhar_mapa(mapa_surface, tabuleiro)

        rodando = False
        for jogador in jogadores:
            if jogador.vivo:
                pos_x = jogador.x * config.TILE_SIZE
                pos_y = jogador.y * config.TILE_SIZE + HUD_H
                frame = jogador.frame_atual if jogador.status == "andando" else 0
                lista = visual.animacoes_player[jogador.direcao][jogador.status]
                sprite = lista[frame % len(lista)]
                tela.blit(sprite, (pos_x, pos_y))
                rodando = True  # Continua rodando enquanto houver pelo menos um jogador vivo


        for b in bombas.bombas_ativas:
            if not b.explodiu:
                pos_x = b.x * config.TILE_SIZE
                pos_y = b.y * config.TILE_SIZE + HUD_H
                tela.blit(visual.sprites[config.BOMBA], (pos_x, pos_y))

        visual.desenhar_hud(tela, jogadores)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
