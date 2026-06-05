import pygame
from config import *

bombas_ativas: list["Bomba"] = []


class Bomba:
    def __init__(self, y, x, raio=2, tempo_explosao=3000):
        self.y = y
        self.x = x
        self.raio = raio
        self.timer = tempo_explosao
        self.explodiu = False

    def atualizar(self, dt, matriz):
        """Diminui o timer usando o delta time (dt) do Pygame"""
        if not self.explodiu:
            self.timer -= dt
            if self.timer <= 0:
                self.calcular_explosao(matriz)

    def calcular_explosao(self, matriz):
        """Propaga o fogo parando em paredes e destrindo blocos"""
        self.explodiu = True
        matriz[self.y][self.x] = VAZIO

        # Vetores de direção: (delta_y, delta_x)
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dy, dx in direcoes:
            for passo in range(1, self.raio + 1):
                alvo_y = self.y + (dy * passo)
                alvo_x = self.x + (dx * passo)

                # Verificando se esta dentro do mapa
                if not (0 <= alvo_y < LINHAS and 0 <= alvo_x < COLUNAS):
                    break

                alvo = matriz[alvo_y][alvo_x]

                # Verificando se bateu em uma parede fixa
                if alvo == PAREDE:
                    break

                # Verificando se bateu em um bloco destrutível
                elif alvo == BLOCO_DESTRUTIVEL:
                    matriz[alvo_y][alvo_x] = VAZIO  # Destrói o bloco
                    break  # O fogo para

                # Caso o caminho esteja livre
                else:
                    # Mata jogadores que estiverem no fogo
                    if alvo in (P1, P2, P3, P4):
                        matriz[alvo_y][alvo_x] = FOGO
                    else:
                        matriz[alvo_y][alvo_x] = FOGO

    def desenhar(self, tela, sprite_bomba):
        """Desenhar a bomba na tela"""
        if not self.explodiu:
            tela.blit(sprite_bomba, (self.x * TILE_SIZE, self.y * TILE_SIZE))


def plantar_bomba(matriz, y, x, raio=2, tempo_explosao=3000):
    """Cria uma bomba na posição e a registra na lista global."""
    bomba = Bomba(y, x, raio, tempo_explosao)
    bombas_ativas.append(bomba)
    matriz[y][x] = BOMBA
    return bomba


def atualizar_bombas(matriz, dt=1):
    """Atualiza todas as bombas e remove as que já explodiram."""
    for bomba in bombas_ativas:
        bomba.atualizar(dt, matriz)
    # Remove bombas que já explodiram (após a iteração, sem afetar o loop)
    bombas_ativas[:] = [b for b in bombas_ativas if not b.explodiu]
