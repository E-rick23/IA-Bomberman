import random

import pygame
import sys
import config
import mapgenerator
import visual
import bombas
import efeitos
from player import Player
from menu import Menu
from inimigo import Inimigo


def main():
    # Inicializa o Pygame uma única vez no início
    pygame.init()
    pygame.display.set_caption("Bomberman")

    # Loop Principal
    while True:
        bombas.bombas_ativas = []
        efeitos.efeitos_ativos = []

        menu = Menu()
        # Executa o menu para coletar as configurações iniciais do mapa e quantidade de jogadores
        config_escolhida = menu.rodar()

        # Injetar as configurações escolhidas no config global antes do jogo iniciar
        config.LINHAS = config_escolhida["tamanho"]
        config.COLUNAS = config_escolhida["tamanho"]
        qtd_jogadores = config_escolhida["players"]
        qtd_inimigos = config_escolhida["inimigos"]
        algoritmo_inimigos = config_escolhida["algoritmo_inimigos"]

        print(
            f"Iniciando mapa {config.LINHAS}x{config.COLUNAS} com {qtd_jogadores} players com {qtd_inimigos} inimigos com os motores de {algoritmo_inimigos}"
        )

        # Carrega as animações e sprites antes da seleção para que a UI possa exibir o preview dos heróis
        visual.carregar_recursos()

        # Abre a tela de seleção de personagens
        sprites_escolhidos = menu.selecionar_personagens(qtd_jogadores)

        # Configurar a janela da partida baseada no tamanho do mapa escolhido
        largura = config.COLUNAS * config.TILE_SIZE
        HUD_H = 24
        altura = config.LINHAS * config.TILE_SIZE + HUD_H

        tela = pygame.display.set_mode((largura, altura))
        clock = pygame.time.Clock()

        # Gerar mapa
        tabuleiro = mapgenerator.criar_matriz_vazia()
        mapgenerator.gerar_pilares(tabuleiro)
        mapgenerator.espalhar_blocos(tabuleiro, densidade=0.60)
        mapgenerator.posicionar_jogadores(tabuleiro, qtd_jogadores)
        dados_inimigos = mapgenerator.posicionar_inimigos(tabuleiro, qtd_inimigos)

        L, C = config.LINHAS - 1, config.COLUNAS - 1

        # Cria o pool de jogadores injetando o sprite_id correspondente
        pool_jogadores = [
            Player(
                0,
                0,
                config.P1,
                sprite_id=sprites_escolhidos[0] if qtd_jogadores > 0 else 0,
            ),
            Player(
                0,
                C,
                config.P2,
                sprite_id=sprites_escolhidos[1] if qtd_jogadores > 1 else 1,
            ),
            Player(
                L,
                0,
                config.P3,
                sprite_id=sprites_escolhidos[2] if qtd_jogadores > 2 else 2,
            ),
            Player(
                L,
                C,
                config.P4,
                sprite_id=sprites_escolhidos[3] if qtd_jogadores > 3 else 3,
            ),
        ]

        # print(posicoes_inimigos, algoritmo_inimigos)
        inimigos = [
            Inimigo(dados["y"], dados["x"], dados["id"], algoritmo_inimigos)
            for dados in dados_inimigos
        ]
        jogadores = pool_jogadores[:qtd_jogadores]

        rodando = True
        acao_pos_jogo = (
            "menu"  # Define se ao sair do loop vamos voltar ao menu ou fechar tudo
        )

        # Loop da Partida
        while rodando:
            dt = clock.tick(60)

            bombas.atualizar_bombas(tabuleiro, dt)
            efeitos.atualizar_efeitos(dt)

            for jogador in jogadores:
                jogador.atualizar(dt, tabuleiro, visual.animacoes_por_sprite)

            alvo_atual = None
            for j in jogadores:
                if j.vivo:
                    alvo_atual = j
                    break

            if alvo_atual:
                for inimigo in inimigos:
                    inimigo.atualizar(dt, tabuleiro, alvo_atual)

            tela.fill((0, 0, 0))

            mapa_surface = tela.subsurface(
                pygame.Rect(0, HUD_H, largura, config.LINHAS * config.TILE_SIZE)
            )
            visual.desenhar_mapa(mapa_surface, tabuleiro)
            efeitos.desenhar_efeitos(mapa_surface, visual.sprites_animados)

            algum_vivo = False
            for jogador in jogadores:
                if jogador.vivo:
                    pos_x = jogador.visual_x
                    pos_y = jogador.visual_y + HUD_H
                    frame = jogador.frame_atual if jogador.status == "andando" else 0

                    lista = visual.animacoes_por_sprite[jogador.sprite_id][
                        jogador.direcao
                    ][jogador.status]
                    sprite = lista[frame % len(lista)]
                    tela.blit(sprite, (pos_x, pos_y))
                    algum_vivo = True

            # Se ninguém estiver vivo o jogo acaba
            if not algum_vivo:
                pygame.time.delay(1000)
                rodando = False

            # 'any' verifica se existe pelo menos um inimigo vivo. 
            # 'not any' significa que todos estão mortos.
            if inimigos and not any(inimigo.vivo for inimigo in inimigos):
                # Cria as fontes
                fonte_vitoria = pygame.font.SysFont("Arial", 55, bold=True)
                fonte_instrucao = pygame.font.SysFont("Arial", 20, bold=False)
                            
                # Renderiza o texto (Texto, Antialiasing, Cor RGB)
                texto_vit = fonte_vitoria.render("VITÓRIA!", True, (0, 255, 0)) # Verde
                texto_btn = fonte_instrucao.render("Pressione qualquer botão para voltar ao menu", True, (255, 255, 255)) # Branco
                            
                aguardando_input = True
                while aguardando_input:
                    #Calcula as coordenadas para centralizar o texto                    pos_x_vit = (largura - texto_vit.get_width()) // 2
                    pos_x_vit = (largura - texto_vit.get_width()) // 2
                    pos_y_vit = (altura - texto_vit.get_height()) // 2 - 20
                    
                    pos_x_btn = (largura - texto_btn.get_width()) // 2
                    pos_y_btn = pos_y_vit + 65
                    
                    # Desenha as mensagens por cima do estado atual do mapa
                    tela.blit(texto_vit, (pos_x_vit, pos_y_vit))
                    tela.blit(texto_btn, (pos_x_btn, pos_y_btn))
                    pygame.display.flip()
                    
                    # Captura os eventos dentro deste loop de espera
                    for evento in pygame.event.get():
                        # Se fechar a janela no 'X', encerra o jogo por completo
                        if evento.type == pygame.QUIT:
                            aguardando_input = False
                            rodando = False
                            acao_pos_jogo = "fechar"
                        
                        # Se pressionar uma tecla ou botão do mouse, sai do loop e vai para o menu
                        elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                            aguardando_input = False
                            rodando = False # Termina a partida (volta ao menu principal)

            for inimigo in inimigos:
                if inimigo.vivo and inimigo.caminho_atual:
                    # Cria uma superfície com canal Alpha (transparência)
                    superficie_trilha = pygame.Surface((config.TILE_SIZE, config.TILE_SIZE), pygame.SRCALPHA)
                    
                    # Define a cor baseada no algoritmo (R, G, B, Alpha). Alpha = 80 para ficar translúcido
                    if inimigo.algoritmo == "DFS":
                        superficie_trilha.fill((255, 0, 0, 80))    # Vermelho
                    elif inimigo.algoritmo == "BFS":
                        superficie_trilha.fill((0, 0, 255, 80))    # Azul
                    elif inimigo.algoritmo == "Busca Gulosa":
                        superficie_trilha.fill((255, 255, 0, 80))  # Amarelo
                    else: # A*
                        superficie_trilha.fill((0, 255, 0, 80))    # Verde
                    
                    # Pinta cada bloco da rota calculada
                    for (cy, cx) in inimigo.caminho_atual:
                        pos_x = cx * config.TILE_SIZE
                        pos_y = cy * config.TILE_SIZE + HUD_H
                        tela.blit(superficie_trilha, (pos_x, pos_y))

            for inimigo in inimigos:
                if inimigo.vivo:
                    pos_x = inimigo.visual_x
                    pos_y = inimigo.visual_y + HUD_H

                    lista = visual.animacoes_por_sprite["inimigos"][inimigo.algoritmo]
                    # Usa o tempo do Pygame para trocar o frame (ex: a cada 150 milissegundos)
                    tempo_atual = pygame.time.get_ticks()
                    indice_frame = (tempo_atual // 150) % len(lista)
                                        
                    sprite = lista[indice_frame]
                    tela.blit(sprite, (pos_x, pos_y))

            for b in bombas.bombas_ativas:
                if not b.explodiu:
                    pos_x = b.x * config.TILE_SIZE
                    pos_y = b.y * config.TILE_SIZE + HUD_H
                    frame_idx = b.sequencia_animacao[b.indice_animacao]
                    sprite_atual = visual.sprites_animados["bomba"][frame_idx]
                    tela.blit(sprite_atual, (pos_x, pos_y))

            for evento in pygame.event.get():
                # Fechar o jogo no X da janela
                if evento.type == pygame.QUIT:
                    rodando = False
                    acao_pos_jogo = "fechar"

                # Voltar ao menu pressionando ESC
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando = False
                    acao_pos_jogo = "menu"

                for jogador in jogadores:
                    jogador.processar_input(evento, tabuleiro)

            visual.desenhar_hud(tela, jogadores)
            pygame.display.flip()

        if acao_pos_jogo == "fechar":
            break

    # Desligamento do jogo
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
