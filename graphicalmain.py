import pygame
import sys
import mapgenerator
from config import *
import visual

def main():
    # Inicializa o Pygame
    pygame.init()
    pygame.display.set_caption("Bomberman - Protótipo Grid")
    
    # Define o tamanho da janela dinamicamente com base nas linhas/colunas do grid
    largura_tela = COLUNAS * TILE_SIZE
    altura_tela = LINHAS * TILE_SIZE
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    
    clock = pygame.time.Clock()

    # Gerando o cenário inicial com a sua lógica existente
    tabuleiro = mapgenerator.criar_matriz_vazia()
    mapgenerator.gerar_pilares(tabuleiro)
    mapgenerator.espalhar_blocos(tabuleiro, densidade=0.60)
    mapgenerator.posicionar_jogadores(tabuleiro)

    # Loop principal do jogo
    rodando = True
    while rodando:
        # 1. Tratamento de Eventos (Inputs)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # 2. Atualização de Lógica (Vazio por enquanto)

        # 3. Renderização
        tela.fill((0, 0, 0)) # Limpa a tela com fundo preto
        
        # Chama a função que criamos para desenhar o tabuleiro
        visual.desenhar_mapa(tela, tabuleiro)
        
        pygame.display.flip() # Atualiza a tela com o que foi desenhado
        
        clock.tick(60) # Limita o loop a 60 frames por segundo

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
