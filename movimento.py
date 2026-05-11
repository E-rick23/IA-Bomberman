# movimento.py

from config import *

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
        
        # Verifica se a célula de destino está VAZIA (não é parede, bloco ou bomba)
        if matriz[novo_y][novo_x] == VAZIO:
            
            # Executa o movimento na matriz de dados
            matriz[y_atual][x_atual] = VAZIO         # Apaga o personagem da posição antiga
            matriz[novo_y][novo_x] = id_entidade     # Adiciona ele na posição nova
            
            return novo_y, novo_x
            
    # Se bateu em algo ou tentou sair do mapa, o movimento é ignorado
    return y_atual, x_atual

