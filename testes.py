import movimento
import bombas
from config import *
import config
from player import Player
from inimigo import Inimigo

def testar_movimentacao(tabuleiro):
    #Função para teste da mecânica de movimento

    # Rastreando a posição do Jogador 1 (ele nasce em 0, 0)
    j1_y, j1_x = 0, 0
        
    # Simulando um movimento para a DIREITA (Y não muda, X aumenta 1)
    print("\nSimulando: Jogador 1 tenta andar para a DIREITA...")
    j1_y, j1_x = movimento.tentar_mover(tabuleiro, j1_y, j1_x, 0, 1, P1)
        
    print("\n--- Estado Após Movimento ---")
    print(tabuleiro)
        
    # Simulando um movimento para BAIXO (Y aumenta 1, X não muda)
    print("\nSimulando: Jogador 1 tenta andar para BAIXO...")
    j1_y, j1_x = movimento.tentar_mover(tabuleiro, j1_y, j1_x, 1, 0, P1)
        
    print("\n--- Estado Após Segundo Movimento ---")
    print(tabuleiro)

# ... (sua função testar_movimentacao continua aqui em cima, se quiser mantê-la) ...

def testar_bombas(tabuleiro):
    """Testa a tática de plantar a bomba e fugir para um local seguro."""
    
    print("\n--- Estado Inicial ---")
    print(tabuleiro)
    
    # Rastreando a posição do Jogador 1 (ele nasce em 0, 0)
    j1_y, j1_x = 0, 0
    
    # Move para a direita (0, 1)
    print("\nAção 1: Jogador anda para a DIREITA.")
    j1_y, j1_x = movimento.tentar_mover(tabuleiro, j1_y, j1_x, 0, 1, P1)
    
    # Planta a bomba em (0, 1)
    print("Ação 2: Jogador planta a BOMBA.")
    bombas.plantar_bomba(tabuleiro, j1_y, j1_x, raio=2, tempo_explosao=3)
    
    # Retorna para a esquerda (0, 0)
    print("Ação 3: Jogador foge para a ESQUERDA.")
    j1_y, j1_x = movimento.tentar_mover(tabuleiro, j1_y, j1_x, 0, -1, P1)
    
    #  Foge para baixo (1, 0) - Zona segura!
    print("Ação 4: Jogador desce para BAIXO.")
    j1_y, j1_x = movimento.tentar_mover(tabuleiro, j1_y, j1_x, 1, 0, P1)
    
    print("\n--- Estado Antes da Explosão ---")
    # O valor '4' (Jogador 1) estará na linha 1, coluna 0.
    # O valor '3' (Bomba) estará na linha 0, coluna 1.
    print(tabuleiro)
    
    # Simulando os turnos (Ticks do jogo)
    print("\nPassando o tempo (3 turnos)...")
    bombas.atualizar_bombas(tabuleiro) # Turno 1 (Timer cai para 2)
    bombas.atualizar_bombas(tabuleiro) # Turno 2 (Timer cai para 1)
    bombas.atualizar_bombas(tabuleiro) # Turno 3 (Timer chega a 0 e explode!)
    
    print("\n--- Estado Após a Explosão ---")
    # A bomba sumiu. O fogo consumiu a célula (0,0) que estava livre, 
    # destruiu os blocos em (0,2) ou (0,3), mas poupou o jogador em (1,0)!
    print(tabuleiro)

def mapa_teste(sprites_escolhidos, algoritmo_inimigos):
    """
    Configura um cenário completo de teste 15x15:
    - Redimensiona o mapa global.
    - Cria o tabuleiro apenas com pilares (sem blocos destrutíveis).
    - Instancia 1 Player e 1 Inimigo nas posições corretas.
    Retorna o tabuleiro e as listas de entidades prontas para a main.
    """
    #Força as configurações de tamanho para o ambiente de teste
    config.LINHAS = 15
    config.COLUNAS = 15
    
    #Cria a matriz vazia e espalha os pilares fixos
    tabuleiro = [[config.VAZIO for _ in range(config.COLUNAS)] for _ in range(config.LINHAS)]
    for y in range(1, config.LINHAS, 2):
        for x in range(1, config.COLUNAS, 2):
            tabuleiro[y][x] = config.PAREDE
            
    #Registra os IDs das entidades na matriz de posições
    tabuleiro[0][0] = config.P1
    tabuleiro[config.LINHAS - 1][config.COLUNAS - 1] = config.INIMIGO
    
    #Instancia o objeto do Jogador 1
    sprite_p1 = sprites_escolhidos[0] if sprites_escolhidos else 0
    jogadores = [Player(0, 0, config.P1, sprite_id=sprite_p1)]
    
    #Instancia o objeto do inimigo com o algoritmo selecionado
    inimigos = [Inimigo(config.LINHAS - 1, config.COLUNAS - 1, config.INIMIGO, algoritmo_inimigos)]
    
    print(f" Arena de Teste 15x15 inicializada com sucesso ({algoritmo_inimigos})")
    
    return tabuleiro, jogadores, inimigos
    return tabuleiro, dados_inimigos
