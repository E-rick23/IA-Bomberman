import mapgenerator
import pygame
import sys
import testes

pygame.init()
pygame.display.set_caption("Bomberman")

largura, altura = 600, 600
tela = pygame.display.set_mode((largura, altura))
ticks = pygame.time.Clock()
cor_fundo = (255, 255, 255)
cor_texto = (0, 0, 0)

# parametros iniciais

pixel = 20
velocidade_jogo = 10


def desenhar_texto(mensagem, x, y):
    fonte = pygame.font.SysFont("Arial", 20)
    texto = fonte.render(f"Pontos: {mensagem}", True, cor_texto)
    text_quadro = texto.get_rect(center=(largura / x, altura / y))
    tela.blit(texto, text_quadro)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    bomberman()

        tela.fill(cor_fundo)

        desenhar_texto("Menu Principal", 2, 4)
        desenhar_texto("Pressione Enter para iniciar o jogo", 2, 2)

        pygame.display.flip()


def bomberman():
    tabuleiro = mapgenerator.criar_matriz_vazia()  # Gerando o mapa

    # Gerando o cenário
    mapgenerator.gerar_pilares(tabuleiro)
    mapgenerator.espalhar_blocos(
        tabuleiro, densidade=0.60
    )  # 60% de chance de um espaço livre virar um bloco destrutível

    mapgenerator.posicionar_jogadores(tabuleiro)  # Posiciona os jogadores

    # Printa o mapa
    print("\n Estado Inicial:")
    print(tabuleiro)

    # Função de teste de movimento (Nota: Desative a função de gerar_pilares para garantir o movimento para baixo).
    # testes.testar_movimentacao(tabuleiro)
    # Função de teste de Bombas
    testes.testar_bombas(tabuleiro)


if __name__ == "__main__":
    main()
