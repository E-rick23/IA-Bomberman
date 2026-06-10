import pygame
import sys
import config
import mapgenerator
import visual
import bombas
import efeitos
from player import Player
from menu import Menu


def main():
    menu = Menu()
    # Executa o menu para coletar as configurações iniciais do mapa e quantidade de jogadores
    config_escolhida = menu.rodar()

    # Injetar as configurações escolhidas no config global antes do jogo iniciar
    config.LINHAS = config_escolhida["tamanho"]
    config.COLUNAS = config_escolhida["tamanho"]
    qtd_jogadores = config_escolhida["players"]
    dificuldade = config_escolhida["dificuldade"]

    print(
        f"Iniciando mapa {config.LINHAS}x{config.COLUNAS} com {qtd_jogadores} players na dificuldade '{dificuldade}'"
    )

    # Carrega as animações e sprites antes da seleção para que a UI possa exibir o preview dos heróis
    visual.carregar_recursos()

    # Abre a tela de seleção de personagens sequencial para obter os IDs visuais escolhidos
    sprites_escolhidos = menu.selecionar_personagens(qtd_jogadores)

    # Inicializar a janela do jogo real com o tamanho do mapa adaptado
    pygame.init()
    pygame.display.set_caption("Bomberman")

    largura = config.COLUNAS * config.TILE_SIZE
    HUD_H = 24
    altura = config.LINHAS * config.TILE_SIZE + HUD_H

    tela = pygame.display.set_mode((largura, altura))
    clock = pygame.time.Clock()

    # Gerar mapa
    tabuleiro = mapgenerator.criar_matriz_vazia()
    mapgenerator.gerar_pilares(tabuleiro)
    mapgenerator.espalhar_blocos(tabuleiro, densidade=0.60)
    mapgenerator.posicionar_jogadores(tabuleiro)

    L, C = config.LINHAS - 1, config.COLUNAS - 1

    # Cria o pool de jogadores injetando o sprite_id correspondente à escolha de cada um no menu
    pool_jogadores = [
        Player(0, 0, config.P1, sprite_id=sprites_escolhidos[0] if qtd_jogadores > 0 else 0),
        Player(0, C, config.P2, sprite_id=sprites_escolhidos[1] if qtd_jogadores > 1 else 1),
        Player(L, 0, config.P3, sprite_id=sprites_escolhidos[2] if qtd_jogadores > 2 else 2),
        Player(L, C, config.P4, sprite_id=sprites_escolhidos[3] if qtd_jogadores > 3 else 3),
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
        efeitos.atualizar_efeitos(dt) # Atualiza timers do fogo e dos tijolos quebrando

        # Atualiza o estado lógico e passa o novo dicionário compartilhado de sprites
        for jogador in jogadores:
            jogador.atualizar(dt, tabuleiro, visual.animacoes_por_sprite)

        tela.fill((0, 0, 0))

        mapa_surface = tela.subsurface(
            pygame.Rect(0, HUD_H, largura, config.LINHAS * config.TILE_SIZE)
        )
        visual.desenhar_mapa(mapa_surface, tabuleiro)

        # Desenhar efeitos (fogo, tijolos quebrando)
        efeitos.desenhar_efeitos(mapa_surface, visual.sprites_animados)

        rodando = False
        for jogador in jogadores:
            if jogador.vivo:
                pos_x = jogador.x * config.TILE_SIZE
                pos_y = jogador.y * config.TILE_SIZE + HUD_H
                frame = jogador.frame_atual if jogador.status == "andando" else 0
                
                # 6. Renderiza o sprite correto buscando na lista estruturada por sprite_id
                lista = visual.animacoes_por_sprite[jogador.sprite_id][jogador.direcao][jogador.status]
                sprite = lista[frame % len(lista)]
                tela.blit(sprite, (pos_x, pos_y))
                rodando = True  # Continua rodando enquanto houver pelo menos um jogador vivo

        for b in bombas.bombas_ativas:
            if not b.explodiu:
                pos_x = b.x * config.TILE_SIZE
                pos_y = b.y * config.TILE_SIZE + HUD_H
                frame_idx = b.sequencia_animacao[b.indice_animacao]
                sprite_atual = visual.sprites_animados["bomba"][frame_idx]
                tela.blit(sprite_atual, (pos_x, pos_y))

        visual.desenhar_hud(tela, jogadores)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
