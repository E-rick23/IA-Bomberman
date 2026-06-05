from config import *
import bombas


def tentar_mover(matriz, y_atual, x_atual, delta_y, delta_x, id_entidade):
    """    Tenta mover uma entidade pelo mapa"""
    novo_y = y_atual + delta_y
    novo_x = x_atual + delta_x

    # Verifica limites do mapa
    if not (0 <= novo_y < LINHAS and 0 <= novo_x < COLUNAS):
        return y_atual, x_atual

    # Verifica se o destino está livre
    if matriz[novo_y][novo_x] != VAZIO:
        return y_atual, x_atual

    # Descobre o que colocar na célula de origem após o jogador sair
    origem_tem_bomba = any(
        b.y == y_atual and b.x == x_atual
        for b in bombas.bombas_ativas
    )
    matriz[y_atual][x_atual] = BOMBA if origem_tem_bomba else VAZIO

    # Coloca a entidade na nova posição
    matriz[novo_y][novo_x] = id_entidade
    return novo_y, novo_x
