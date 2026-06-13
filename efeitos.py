# efeitos.py
import pygame
import config

efeitos_ativos = []


class EfeitoVisual:
    def __init__(self, y, x, tipo, frames, tempo_por_frame=100, loop=False):
        self.y = y
        self.x = x
        self.tipo = tipo
        self.frames = frames  # Lista com a ordem dos frames
        self.frame_atual = 0
        self.timer = 0
        self.tempo_por_frame = tempo_por_frame
        self.loop = loop
        self.concluido = False

    def atualizar(self, dt):
        if self.concluido:
            return

        self.timer += dt
        if self.timer >= self.tempo_por_frame:
            self.timer = 0
            self.frame_atual += 1

            # Verifica se a animação acabou
            if self.frame_atual >= len(self.frames):
                if self.loop:
                    self.frame_atual = 0
                else:
                    self.concluido = True
                    self.frame_atual = len(self.frames) - 1  # Trava no último frame

    def desenhar(self, tela, dicionario_sprites):
        if not self.concluido:
            # Pega o frame atual com base na sequência definida
            indice_sprite = self.frames[self.frame_atual]
            sprite = dicionario_sprites[self.tipo][indice_sprite]
            pos_x = self.x * config.TILE_SIZE
            pos_y = self.y * config.TILE_SIZE
            tela.blit(sprite, (pos_x, pos_y))


def adicionar_efeito(y, x, tipo, frames, tempo_por_frame, loop=False):
    efeitos_ativos.append(EfeitoVisual(y, x, tipo, frames, tempo_por_frame, loop))


def atualizar_efeitos(dt):
    global efeitos_ativos
    for efeito in efeitos_ativos:
        efeito.atualizar(dt)
    # Remove os que já terminaram
    efeitos_ativos[:] = [e for e in efeitos_ativos if not e.concluido]


def desenhar_efeitos(tela, dicionario_sprites):
    """Percorre a lista de efeitos ativos e desenha cada um na tela."""
    global efeitos_ativos
    for efeito in efeitos_ativos:
        efeito.desenhar(tela, dicionario_sprites)
