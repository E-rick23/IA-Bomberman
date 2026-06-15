import config
import movimento
import random
from motores_busca import busca_bfs, busca_a_estrela, busca_dfs, busca_gulosa 

def tem_linha_de_visao(matriz, y1, x1, y2, x2): # Verifica se o player está na linha de visão do inimigo

    if y1 == y2: # Mesma linha
        passo = 1 if x2 > x1 else -1
        for x in range(x1 + passo, x2, passo):
            if matriz[y1][x] in (config.PAREDE, config.BLOCO_DESTRUTIVEL): 
                return False
        return True
        
    elif x1 == x2: # Mesma coluna
        passo = 1 if y2 > y1 else -1
        for y in range(y1 + passo, y2, passo):
            if matriz[y][x1] in (config.PAREDE, config.BLOCO_DESTRUTIVEL): 
                return False
        return True
        
    return False


class Inimigo:
    def __init__(self, y, x, id_inimigo, algoritmo="a_estrela"):
        self.y = y
        self.x = x
        self.id = id_inimigo
        self.vivo = True
        self.algoritmo = algoritmo
        
        # Controle de velocidade
        self.timer_movimento = 0
        self.tempo_por_passo = 500  
        
        self.estado = "VAGANDO"
        self.ultimo_local_visto = None

    def atualizar(self, dt, matriz, jogador_alvo):
        if not self.vivo:
            return

        # Verifica se o inimigo está morto
        self._verificar_morte(matriz)
        if not self.vivo:
            return

        self.timer_movimento += dt
        if self.timer_movimento >= self.tempo_por_passo:
            self.timer_movimento = 0
            self._tomar_decisao(matriz, jogador_alvo)

    def _verificar_morte(self, matriz):
        if matriz[self.y][self.x] in (config.VAZIO, config.FOGO):
            self.vivo = False

    # Toma decisão se deve perseguir ou vagar
    def _tomar_decisao(self, matriz, jogador_alvo):
        if jogador_alvo and jogador_alvo.vivo:
            if tem_linha_de_visao(matriz, self.y, self.x, jogador_alvo.y, jogador_alvo.x):
                self.estado = "PERSEGUINDO"
                self.ultimo_local_visto = (jogador_alvo.y, jogador_alvo.x)

        if self.estado == "PERSEGUINDO":
            if self.ultimo_local_visto:
                if self.algoritmo == "bfs":
                    caminho = busca_bfs(matriz, (self.y, self.x), self.ultimo_local_visto)
                elif self.algoritmo == "dfs":
                    caminho = busca_dfs(matriz, (self.y, self.x), self.ultimo_local_visto)
                elif self.algoritmo == "busca_gulosa":
                    caminho = busca_gulosa(matriz, (self.y, self.x), self.ultimo_local_visto)
                else:
                    caminho = busca_a_estrela(matriz, (self.y, self.x), self.ultimo_local_visto)

                if caminho and len(caminho) > 1:
                    alvo_y, alvo_x = caminho[1]
                    self._mover_para(matriz, alvo_y, alvo_x, jogador_alvo)
                    
                    if self.y == self.ultimo_local_visto[0] and self.x == self.ultimo_local_visto[1]:
                        self.estado = "VAGANDO"
                        self.ultimo_local_visto = None
                else:
                    self.estado = "VAGANDO"
                    self.ultimo_local_visto = None
                    self._vagar(matriz, jogador_alvo)
                    
        elif self.estado == "VAGANDO":
            self._vagar(matriz, jogador_alvo)

    def _mover_para(self, matriz, alvo_y, alvo_x, jogador_alvo):
        if matriz[alvo_y][alvo_x] in (config.P1, config.P2, config.P3, config.P4):
            if jogador_alvo and jogador_alvo.y == alvo_y and jogador_alvo.x == alvo_x:
                jogador_alvo.vivo = False
                matriz[alvo_y][alvo_x] = config.VAZIO 

        delta_y = alvo_y - self.y
        delta_x = alvo_x - self.x
        self.y, self.x = movimento.tentar_mover(matriz, self.y, self.x, delta_y, delta_x, self.id)

    def _vagar(self, matriz, jogador_alvo):
        vizinhos = []
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dy, dx in direcoes:
            ny, nx = self.y + dy, self.x + dx
            if 0 <= ny < config.LINHAS and 0 <= nx < config.COLUNAS:
                alvo = matriz[ny][nx]
                if alvo == config.VAZIO or alvo in (config.P1, config.P2, config.P3, config.P4):
                    vizinhos.append((ny, nx))
        
        if vizinhos:
            escolhido = random.choice(vizinhos)
            self._mover_para(matriz, escolhido[0], escolhido[1], jogador_alvo)