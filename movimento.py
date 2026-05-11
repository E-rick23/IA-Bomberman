# movimento.py

from config import *
import bombas 

def tentar_mover(matriz, y_atual, x_atual, delta_y, delta_x, id_entidade):
    """
    Tenta mover uma entidade pelo mapa.
    delta_y e delta_x devem ser -1, 0 ou 1 (representando Cima, Baixo, Esquerda, Direita).
    Retorna a nova tupla de coordenadas (y, x). Se falhar, retorna a original.
    """
    novo_y = y_atual + delta_y
    novo_x = x_atual + delta_x

    # Verifica se a nova posição está dentro dos limites do mapa
    if 0 <= novo_y < LINHAS and 0 <= novo_x < COLUNAS:
    
        # Verifica se o jogador estava em cima de uma bomba que acabou de plantar
            deixou_bomba_para_tras = False
            for b in bombas.bombas_ativas:
                if b['y'] == y_atual and b['x'] == x_atual:
                    deixou_bomba_para_tras = True
                    break
                    
                if deixou_bomba_para_tras:
                    matriz[y_atual][x_atual] = BOMBA # Restaura a imagem da bomba na matriz!
                else:
                    matriz[y_atual][x_atual] = VAZIO # Apaga normalmente
                        
            matriz[novo_y][novo_x] = id_entidade     # Adiciona o jogador na posição nova
            
            return novo_y, novo_x
            
    # Se bateu em algo ou tentou sair do mapa, o movimento é ignorado
    return y_atual, x_atual

