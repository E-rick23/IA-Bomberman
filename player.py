import pygame
from config import *
import movimento
import efeitos
import bombas


class Player:
    CONTROLES = {
        P1: {
            "cima": pygame.K_UP,
            "baixo": pygame.K_DOWN,
            "esquerda": pygame.K_LEFT,
            "direita": pygame.K_RIGHT,
            "bomba": pygame.K_SPACE,
        },
        P2: {
            "cima": pygame.K_w,
            "baixo": pygame.K_s,
            "esquerda": pygame.K_a,
            "direita": pygame.K_d,
            "bomba": pygame.K_LSHIFT,
        },
        P3: {
            "cima": pygame.K_1,
            "baixo": pygame.K_2,
            "esquerda": pygame.K_3,
            "direita": pygame.K_4,
            "bomba": pygame.K_5,
        },
        P4: {
            "cima": pygame.K_i,
            "baixo": pygame.K_k,
            "esquerda": pygame.K_j,
            "direita": pygame.K_l,
            "bomba": pygame.K_RSHIFT,
        },
    }

    def __init__(self, y, x, player_id=P1, sprite_id=0):
        self.y = y
        self.x = x
        self.id = player_id
        self.sprite_id = sprite_id
        self.direcao = "baixo"
        self.status = "parado"
        self.frame_atual = 0
        self.timer_animacao = 0
        self.vivo = True
        self.raio_bomba = 2
        self.tempo_bomba = 3000  # ms
        self.teclas = self.CONTROLES.get(player_id, self.CONTROLES[P1])

    def processar_input(self, evento, matriz):
        if not self.vivo:
            return

        if evento.type == pygame.KEYDOWN:
            delta_y, delta_x = 0, 0

            if evento.key == self.teclas["direita"]:
                self.direcao, self.status, delta_x = "direita", "andando", 1
            elif evento.key == self.teclas["esquerda"]:
                self.direcao, self.status, delta_x = "esquerda", "andando", -1
            elif evento.key == self.teclas["baixo"]:
                self.direcao, self.status, delta_y = "baixo", "andando", 1
            elif evento.key == self.teclas["cima"]:
                self.direcao, self.status, delta_y = "cima", "andando", -1
            elif evento.key == self.teclas["bomba"]:
                self._plantar_bomba(matriz)

            if delta_x != 0 or delta_y != 0:
                self.y, self.x = movimento.tentar_mover(
                    matriz, self.y, self.x, delta_y, delta_x, self.id
                )

        elif evento.type == pygame.KEYUP:
            teclas_movimento = {
                self.teclas["cima"],
                self.teclas["baixo"],
                self.teclas["esquerda"],
                self.teclas["direita"],
            }
            if evento.key in teclas_movimento:
                self.status = "parado"

    def _plantar_bomba(self, matriz):
        """Planta uma bomba na posição atual do jogador"""
        # Não planta se já houver uma bomba no mesmo lugar
        bomba_posicionada = any(
            bomba.y == self.y and bomba.x == self.x
            for bomba in bombas.bombas_ativas
        )
        if not bomba_posicionada:
            bombas.plantar_bomba(
                matriz, self.y, self.x,
                raio=self.raio_bomba,
                tempo_explosao=self.tempo_bomba,
            )
            
    def atualizar(self, dt, matriz, animacoes):
        """Atualiza animação e verifica se o jogador foi atingido"""
        self._atualizar_animacao(dt, animacoes)
        self._verificar_morte(matriz)

    def _atualizar_animacao(self, dt, animacoes):
        if self.status == "andando":
            self.timer_animacao += dt
            if self.timer_animacao > 150:
                self.timer_animacao = 0
                lista = animacoes[self.sprite_id][self.direcao]["andando"]
                if lista:
                    self.frame_atual = (self.frame_atual + 1) % len(lista)

    def _verificar_morte(self, matriz):
        """Marca o jogador como morto se sua célula virou FOGO ou VAZIO"""
        # Se a célula foi tomada pelo fogo (8) ou limpa sem o jogador se mover (0)
        if matriz[self.y][self.x] in (VAZIO, FOGO):
            self.vivo = False
            return
        # Se ele andou para dentro de um tile com fogo ativo
        for efeito in efeitos.efeitos_ativos:
            if efeito.y == self.y and efeito.x == self.x and "fogo" in efeito.tipo:
                self.vivo = False
                matriz[self.y][self.x] = VAZIO # Limpa o "corpo" do inimigo da matriz
                break

    def desenhar(self, tela, animacoes):
        if not self.vivo:
            return
        pos_x = self.x * TILE_SIZE
        pos_y = self.y * TILE_SIZE
        frame = self.frame_atual if self.status == "andando" else 0
        lista = animacoes[self.direcao][self.status]
        sprite = lista[frame % len(lista)]
        tela.blit(sprite, (pos_x, pos_y))
