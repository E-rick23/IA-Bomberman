import pygame
import sys
import visual
import config

pygame.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (150, 150, 150)
AZUL_SELECIONADO = (50, 150, 255)


class Menu:
    def __init__(self, largura=600, altura=500):
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Bomberman - Menu")
        self.fonte_titulo = pygame.font.SysFont("Arial", 40, bold=True)
        self.fonte_opcoes = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()

        # Opções dos seletores
        self.tamanhos_mapa = [9, 11, 13, 15]
        self.tamanho = 0

        self.qtd_players = [2, 3, 4]
        self.players = 0

        self.dificuldades = [
            "Fácil",
            "Médio",
            "Difícil",
        ]  # Felipe menionou algo de dificuldade no pitch depois vejo sobre
        self.dificuldade = 0

        # Índice do botão (0=Tamanho, 1=Players, 2=Dificuldade, 3=Jogar)
        self.opcao_focada = 0

    def desenhar_texto(self, texto, fonte, cor, x, y, centralizado=True):
        superficie = fonte.render(texto, True, cor)
        retangulo = superficie.get_rect()
        if centralizado:
            retangulo.center = (x, y)
        else:
            retangulo.topleft = (x, y)
        self.tela.blit(superficie, retangulo)
        return retangulo

    def rodar(self):
        while True:
            self.tela.fill(PRETO)

            self.desenhar_texto(
                "BOMBERMAN", self.fonte_titulo, BRANCO, self.largura // 2, 60
            )

            # Cores de destaque baseadas no foco do teclado/mouse
            cor_tamanho = AZUL_SELECIONADO if self.opcao_focada == 0 else BRANCO
            cor_players = AZUL_SELECIONADO if self.opcao_focada == 1 else BRANCO
            cor_dificuldade = AZUL_SELECIONADO if self.opcao_focada == 2 else BRANCO
            cor_jogar = AZUL_SELECIONADO if self.opcao_focada == 3 else CINZA

            # Renderizar Seletores
            txt_tamanho = f"Tamanho do Mapa:  <  {self.tamanhos_mapa[self.tamanho]}x{self.tamanhos_mapa[self.tamanho]}  >"
            rect_tamanho = self.desenhar_texto(
                txt_tamanho, self.fonte_opcoes, cor_tamanho, self.largura // 2, 160
            )

            txt_players = (
                f"Quantidade de Players:  <  {self.qtd_players[self.players]}  >"
            )
            rect_players = self.desenhar_texto(
                txt_players, self.fonte_opcoes, cor_players, self.largura // 2, 220
            )

            txt_dificuldade = (
                f"Dificuldade (IA futuro):  <  {self.dificuldades[self.dificuldade]}  >"
            )
            rect_dificuldade = self.desenhar_texto(
                txt_dificuldade,
                self.fonte_opcoes,
                cor_dificuldade,
                self.largura // 2,
                280,
            )

            # Botão Jogar
            rect_jogar = self.desenhar_texto(
                "[ INICIAR JOGO ]", self.fonte_titulo, cor_jogar, self.largura // 2, 380
            )

            pygame.display.flip()
            self.clock.tick(30)

            # Tratar Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_DOWN:
                        self.opcao_focada = (self.opcao_focada + 1) % 4
                    elif evento.key == pygame.K_UP:
                        self.opcao_focada = (self.opcao_focada - 1) % 4

                    # Interagir com as setas do teclado nas opções laterais
                    elif evento.key == pygame.K_LEFT:
                        if self.opcao_focada == 0:
                            self.tamanho = (self.tamanho - 1) % len(self.tamanhos_mapa)
                        elif self.opcao_focada == 1:
                            self.players = (self.players - 1) % len(self.qtd_players)
                        elif self.opcao_focada == 2:
                            self.dificuldade = (self.dificuldade - 1) % len(
                                self.dificuldades
                            )

                    elif evento.key == pygame.K_RIGHT:
                        if self.opcao_focada == 0:
                            self.tamanho = (self.tamanho + 1) % len(self.tamanhos_mapa)
                        elif self.opcao_focada == 1:
                            self.players = (self.players + 1) % len(self.qtd_players)
                        elif self.opcao_focada == 2:
                            self.dificuldade = (self.dificuldade + 1) % len(
                                self.dificuldades
                            )

                    elif evento.key == pygame.K_RETURN:
                        if self.opcao_focada == 3:
                            return self.coletar_configuracoes()

                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    pos = pygame.mouse.get_pos()
                    # Clique no Iniciar Jogo
                    if rect_jogar.collidepoint(pos):
                        return self.coletar_configuracoes()

                    # Permite alternar clicando
                    if rect_tamanho.collidepoint(pos):
                        self.tamanho = (self.tamanho + 1) % len(self.tamanhos_mapa)
                    if rect_players.collidepoint(pos):
                        self.players = (self.players + 1) % len(self.qtd_players)
                    if rect_dificuldade.collidepoint(pos):
                        self.dificuldade = (self.dificuldade + 1) % len(
                            self.dificuldades
                        )

    def coletar_configuracoes(self):
        return {
            "tamanho": self.tamanhos_mapa[self.tamanho],
            "players": self.qtd_players[self.players],
            "dificuldade": self.dificuldades[self.dificuldade],
        }

    def selecionar_personagens(self, qtd_players):
        escolhas = []
        for p in range(qtd_players):
            selecionado = 0
            confirmado = False
            while not confirmado:
                self.tela.fill(PRETO)
                self.desenhar_texto(f"JOGADOR {p+1}: ESCOLHA SEU HEROI", self.fonte_titulo, BRANCO, self.largura // 2, 80)
                
                # Desenhar os 4 personagens lado a lado
                for i in range(4):
                    sprite = visual.obter_sprite_menu(i)
                    x = (self.largura // 5) * (i + 1)
                    y = self.altura // 2
                    
                    # Destaque para o que está focado
                    if i == selecionado:
                        pygame.draw.rect(self.tela, AZUL_SELECIONADO, (x - 40, y - 40, 80, 80), 3)
                    
                    self.tela.blit(sprite, (x - config.TILE_SIZE//2, y - config.TILE_SIZE//2))
                
                self.desenhar_texto("< SETAS PARA MOVER | ENTER PARA CONFIRMAR >", self.fonte_opcoes, CINZA, self.largura // 2, 400)
                pygame.display.flip()

                for evento in pygame.event.get():
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_LEFT:
                            selecionado = (selecionado - 1) % 4
                        elif evento.key == pygame.K_RIGHT:
                            selecionado = (selecionado + 1) % 4
                        elif evento.key == pygame.K_RETURN:
                            escolhas.append(selecionado)
                            confirmado = True
        return escolhas
    
