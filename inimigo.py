import random
import config
import movimento
import efeitos
from motores_busca import busca_bfs, busca_a_estrela, busca_dfs, busca_gulosa

def tem_linha_de_visao(matriz, y1, x1, y2, x2): # Verifica se o player está na linha de visão do inimigo

    if y1 == y2: # Mesma linha
        passo = 1 if x2 > x1 else -1
        for x in range(x1 + passo, x2, passo):
            if matriz[y1][x] in (config.PAREDE, config.BLOCO_DESTRUTIVEL): 
                return False
        return True
    elif x1 == x2: #Mesma coluna
        passo = 1 if y2 > y1 else -1
        for y in range(y1 + passo, y2, passo):
            if matriz[y][x1] in (config.PAREDE, config.BLOCO_DESTRUTIVEL): 
                return False
        return True
    
    return False

class Inimigo:
    def __init__(self, y, x, id_inimigo, algoritmo="BFS"):
        self.y = y
        self.x = x
        self.id = id_inimigo
        self.visual_x = self.x * config.TILE_SIZE 
        self.visual_y = self.y * config.TILE_SIZE
        self.vivo = True
        self.algoritmo = algoritmo
        self.timer_movimento = 0
        self.tempo_por_passo = 500  
        self.estado = "VAGANDO"
        self.caminho_atual = [] 
        self.alvo_da_rota = None

    def atualizar(self, dt, matriz, jogador_alvo):
        if not self.vivo:
            return

        # Verifica se o inimigo está morto
        self._verificar_morte(matriz)
        if not self.vivo:
            return

        # Suavização do Movimento Visual
        alvo_x = self.x * config.TILE_SIZE
        alvo_y = self.y * config.TILE_SIZE
        self.visual_x += (alvo_x - self.visual_x) * 0.2 # Inimigos podem deslizar um pouco mais lento
        self.visual_y += (alvo_y - self.visual_y) * 0.2
        
        self.timer_movimento += dt
        if self.timer_movimento >= self.tempo_por_passo:
            self.timer_movimento = 0
            self._tomar_decisao(matriz, jogador_alvo)

    def _verificar_morte(self, matriz):
        # Se a bomba explodiu exatamente onde ele já estava (a matriz virou VAZIO)
        if matriz[self.y][self.x] in (config.VAZIO, config.FOGO):
            self.vivo = False
            return
        # Se ele andou para dentro de um tile com fogo ativo    
        for efeito in efeitos.efeitos_ativos:
                    if efeito.y == self.y and efeito.x == self.x and "fogo" in efeito.tipo:
                        self.vivo = False
                        matriz[self.y][self.x] = config.VAZIO # Limpa o "corpo" do inimigo da matriz
                        break

    def _tomar_decisao(self, matriz, jogador_alvo):
        if self.estado == "VAGANDO" and jogador_alvo and jogador_alvo.vivo:
            if tem_linha_de_visao(matriz, self.y, self.x, jogador_alvo.y, jogador_alvo.x):
                self.estado = "PERSEGUINDO"

        if self.estado == "PERSEGUINDO":
            if jogador_alvo and jogador_alvo.vivo:
                alvo_atual = (jogador_alvo.y, jogador_alvo.x)

                # --- LÓGICA DE MEMÓRIA DE ROTA ---
                precisa_recalcular = True

                # Se já temos uma rota e o jogador NÃO mudou de bloco, tentamos manter a rota
                if self.caminho_atual and self.alvo_da_rota == alvo_atual:
                    proximo_y, proximo_x = self.caminho_atual[0]
                    alvo_matriz = matriz[proximo_y][proximo_x]
                    
                    # Verifica se o próximo passo da lista ainda está livre (não tem bomba)
                    if alvo_matriz == config.VAZIO or alvo_matriz in (config.P1, config.P2, config.P3, config.P4):
                        precisa_recalcular = False

                # Só aciona os motores pesados de IA se for realmente necessário
                if precisa_recalcular:
                    if self.algoritmo == "BFS":
                        caminho = busca_bfs(matriz, (self.y, self.x), alvo_atual)
                    elif self.algoritmo == "DFS":
                        caminho = busca_dfs(matriz, (self.y, self.x), alvo_atual)
                    elif self.algoritmo == "Busca Gulosa":
                        caminho = busca_gulosa(matriz, (self.y, self.x), alvo_atual)
                    elif self.algoritmo == "A*":
                        caminho = busca_a_estrela(matriz, (self.y, self.x), alvo_atual)
                    else:
                        caminho = []

                    if caminho and len(caminho) > 1:
                        self.caminho_atual = caminho[1:]
                        self.alvo_da_rota = alvo_atual # Memoriza para onde essa rota vai
                    else:
                        self.caminho_atual = []
                        self.alvo_da_rota = None

                # --- EXECUÇÃO DO MOVIMENTO ---
                if self.caminho_atual:
                    # Remove o próximo passo do começo da lista (pop) e anda para ele
                    alvo_y, alvo_x = self.caminho_atual.pop(0)
                    self._mover_para(matriz, alvo_y, alvo_x, jogador_alvo)
                else:
                    # Se o caminho sumir (ex: você se trancou com bombas), ele anda aleatório
                    self._vagar(matriz, jogador_alvo)
            else:
                self.estado = "VAGANDO"
                self.caminho_atual = []
                self.alvo_da_rota = None
                self._vagar(matriz, jogador_alvo)
                    
        elif self.estado == "VAGANDO":
            self.caminho_atual = [] 
            self.alvo_da_rota = None
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
