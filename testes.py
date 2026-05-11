import movimento
from config import *

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
