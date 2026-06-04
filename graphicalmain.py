import pygame
import sys
import mapgenerator
import visual
import movimento
from config import *

def main():
    # Inicializa o Pygame
    pygame.init()
    pygame.display.set_caption("Bomberman - Protótipo Grid")
    
    # Define o tamanho da janela dinamicamente com base nas linhas/colunas do grid
    largura_tela = COLUNAS * TILE_SIZE
    altura_tela = LINHAS * TILE_SIZE
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    visual.carregar_recursos()
    clock = pygame.time.Clock()
    # Estado inicial do Player 1
    player_estado = {
        "y": 0,
        "x": 0,
        "direcao": "baixo",       # "cima", "baixo", "esquerda", "direita"
        "status": "parado",       # "parado", "andando", "plantando"
        "frame_atual": 0,         # Controla qual perna/braço está usando
        "timer_animacao": 0       # Tempo para alternar os frames da caminhada
    }

    # Gerando o cenário inicial com a sua lógica existente
    tabuleiro = mapgenerator.criar_matriz_vazia()
    mapgenerator.gerar_pilares(tabuleiro)
    mapgenerator.espalhar_blocos(tabuleiro, densidade=0.60)
    mapgenerator.posicionar_jogadores(tabuleiro)

    # Loop principal do jogo
    rodando = True
    while rodando:
        # Pega o tempo decorrido desde o último frame (em milissegundos)
        dt = clock.tick(60) 

        # PARTE 1: CAPTURA DE INPUTS (Eventos do Teclado)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            elif evento.type == pygame.KEYDOWN:
                # Variáveis temporárias para calcular o passo
                delta_y = 0
                delta_x = 0
                
                if evento.key == pygame.K_RIGHT:
                    player_estado["direcao"] = "direita"
                    player_estado["status"] = "andando"
                    delta_x = 1
                    
                elif evento.key == pygame.K_LEFT:
                    player_estado["direcao"] = "esquerda"
                    player_estado["status"] = "andando"
                    delta_x = -1
                    
                elif evento.key == pygame.K_DOWN:
                    player_estado["direcao"] = "baixo"
                    player_estado["status"] = "andando"
                    delta_y = 1
                    
                elif evento.key == pygame.K_UP:
                    player_estado["direcao"] = "cima"
                    player_estado["status"] = "andando"
                    delta_y = -1

                # Se houve intenção de movimento, aplica a sua lógica
                if delta_x != 0 or delta_y != 0:
                    # Envia a matriz e a posição atual para o seu script de movimento
                    novo_y, novo_x = movimento.tentar_mover(
                        tabuleiro, 
                        player_estado["y"], 
                        player_estado["x"], 
                        delta_y, 
                        delta_x, 
                        P1
                    )
                    
                    # Atualiza a posição do jogador no dicionário de estado
                    player_estado["y"] = novo_y
                    # Se bater em uma parede, novo_x/y voltam iguais ao que eram,
                    player_estado["x"] = novo_x
                    # impedindo o jogador de sair do lugar na tela!

            elif evento.type == pygame.KEYUP:
                # Quando soltar qualquer tecla de seta, o jogador para a animação
                if evento.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP]:
                    player_estado["status"] = "parado"       

        # PARTE 2: ATUALIZAÇÃO DA LÓGICA 

        if player_estado["status"] == "andando":
            # Acumula o tempo que passou (dt) no timer de animação
            player_estado["timer_animacao"] += dt
            
            # Se passou mais de 150 milissegundos, alterna o frame
            if player_estado["timer_animacao"] > 150:
                player_estado["timer_animacao"] = 0
              
                # Pega a lista correta para a direção atual
                lista_frames = visual.animacoes_player[player_estado["direcao"]]["andando"]
                                
                # Evita divisão por zero se a lista estiver vazia por acidente
                if len(lista_frames) > 0:
                    player_estado["frame_atual"] = (player_estado["frame_atual"] + 1) % len(lista_frames)
                else:
                    player_estado["frame_atual"] = 0
               
        # PARTE 3: RENDERIZAÇÃO 
        tela.fill((0, 0, 0)) 
        
        # Desenha o mapa (cenário estático)
        visual.desenhar_mapa(tela, tabuleiro)
        
        # Desenha o jogador dinâmico baseado no estado dele
        visual.desenhar_player(tela, player_estado)
        
        pygame.display.flip() 

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
