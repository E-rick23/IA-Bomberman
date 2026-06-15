import pygame
import config
import efeitos

bombas_ativas: list["Bomba"] = []

class Bomba:
    def __init__(self, y, x, raio=2, tempo_explosao=3000):
        self.y = y
        self.x = x
        self.raio = raio
        self.timer = tempo_explosao
        self.explodiu = False
        self.sequencia_animacao = [0, 1, 2, 1]  # Vai do 1º ao 3º e volta pro 2º
        self.indice_animacao = 0
        self.timer_animacao = 0
        self.tempo_por_frame = 200 # ms por frame da bomba

    def atualizar(self, dt, matriz):
        if not self.explodiu:
            # Atualiza timer da explosão
            self.timer -= dt
            
            # Atualiza timer da animação visual
            self.timer_animacao += dt
            if self.timer_animacao >= self.tempo_por_frame:
                self.timer_animacao = 0
                self.indice_animacao = (self.indice_animacao + 1) % len(self.sequencia_animacao)
    
            if self.timer <= 0:
                self.calcular_explosao(matriz)

    def calcular_explosao(self, matriz):
            """Propaga o fogo parando em paredes e destruindo blocos"""
            self.explodiu = True
            seq_fogo = [0, 1, 2, 3, 2, 1, 0]
            
            # 1. Centro da explosão: limpa a matriz e adiciona o efeito do fogo
            matriz[self.y][self.x] = config.VAZIO
            efeitos.adicionar_efeito(self.y, self.x, "fogo_centro", seq_fogo, 80)
            
            # Mapeando os vetores para as peças visuais corretas: (dy, dx): ("Sprite Ponta", "Sprite Corpo")
            direcoes = {
                (-1, 0): ("fogo_cima", "fogo_vertical"),
                (1, 0): ("fogo_baixo", "fogo_vertical"),
                (0, -1): ("fogo_esq", "fogo_horizontal"),
                (0, 1): ("fogo_dir", "fogo_horizontal")
            }
    
            for (dy, dx), (tipo_ponta, tipo_corpo) in direcoes.items():
                for passo in range(1, self.raio + 1):
                    alvo_y = self.y + (dy * passo)
                    alvo_x = self.x + (dx * passo)
    
                    # Verificando se esta dentro do mapa
                    if not (0 <= alvo_y < config.LINHAS and 0 <= alvo_x < config.COLUNAS):
                        break
    
                    alvo = matriz[alvo_y][alvo_x]
    
                    # Verificando se bateu em uma parede fixa
                    if alvo == config.PAREDE:
                        break
    
                    # Verificando se bateu em um bloco destrutível
                    elif alvo == config.BLOCO_DESTRUTIVEL:
                        matriz[alvo_y][alvo_x] = config.VAZIO  # Destrói o bloco
                        # Dispara a animação do tijolo destruindo (frames 1 até 6)
                        efeitos.adicionar_efeito(alvo_y, alvo_x, "bloco_destruindo", [1, 2, 3, 4, 5, 6], 100)
                        break
                    
                    elif alvo == config.BOMBA:
                        for outra_bomba in bombas_ativas:
                            if outra_bomba.y == alvo_y and outra_bomba.x == alvo_x and not outra_bomba.explodiu:
                                
                                # Calcula um tempo de detonação baseado na distância (100ms por bloco)
                                atraso_cascata = passo * 100
                                
                                # Reduz o timer da bomba atingida APENAS se o novo tempo 
                                # for menor que o tempo que ela já tinha para explodir naturalmente
                                if outra_bomba.timer > atraso_cascata:
                                    outra_bomba.timer = atraso_cascata
                                    
                                break
                        
                        # O fogo desta bomba PARA aqui
                        break
                    # Caso o caminho esteja livre (inclui jogadores)
                    else:
                        # Sobrescreve com VAZIO. Isso automaticamente "mata" jogadores, 
                        # pois o método _verificar_morte deles identifica que o ID sumiu.
                        matriz[alvo_y][alvo_x] = config.VAZIO

                        # Decide qual sprite usar: se for o último passo da explosão, usa a ponta.
                        tipo_fogo = tipo_ponta if passo == self.raio else tipo_corpo
                         # Adiciona a animação visual do fogo expandindo                    
                        efeitos.adicionar_efeito(alvo_y, alvo_x, tipo_fogo, seq_fogo, 80)
                       
    def desenhar(self, tela, sprite_bomba):
        """Desenhar a bomba na tela"""
        if not self.explodiu:
            tela.blit(
                sprite_bomba, (self.x * config.TILE_SIZE, self.y * config.TILE_SIZE)
            )


def plantar_bomba(matriz, y, x, raio=2, tempo_explosao=3000):
    """Cria uma bomba na posição e a registra na lista global."""
    bomba = Bomba(y, x, raio, tempo_explosao)
    bombas_ativas.append(bomba)
    matriz[y][x] = config.BOMBA
    return bomba


def atualizar_bombas(matriz, dt=1):
    """Atualiza todas as bombas e remove as que já explodiram."""
    for bomba in bombas_ativas:
        bomba.atualizar(dt, matriz)
    # Remove bombas que já explodiram (após a iteração, sem afetar o loop)
    bombas_ativas[:] = [b for b in bombas_ativas if not b.explodiu]
