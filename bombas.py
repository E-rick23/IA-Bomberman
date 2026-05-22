from config import *

# Lista para rastrear as bombas ativas.
# Dicionário {'y': int, 'x': int, 'timer': 'int, 'raio': int}

bombas_ativas = []

def plantar_bomba(matriz, y, x, raio=2, tempo_explosao=3):
    # Planta uma bomba na posição atual do jogador se a célula estiver livre.
    if matriz[y][x] != BOMBA:
        matriz[y][x] = BOMBA
        nova_bomba = {
            'y': y,
            'x': x,
            'timer': tempo_explosao,
            'raio': raio
        }
        bombas_ativas.append(nova_bomba)
        return True
    return False

def calcular_explosao(matriz, centro_y, centro_x, raio):
    #Propaga o fogo nas 4 direções, destruindo blocos ou parando em paredes.
    #O centro da explosão sempre fica vazio
    matriz[centro_y][centro_x] = VAZIO

    #Vetores de direção: (delta_y, delta_x)
    direcoes = [
        (-1, 0), # Cima
        (1, 0), # Baixo
        (0, -1), # Esquerda
        (0, 1) # Direita
    ]

    for dy, dx in direcoes:
        for passo in range(1, raio + 1):
            alvo_y = centro_y + (dy * passo)
            alvo_x = centro_x + (dx * passo)

            #Verificando se saiu do mapa
            if not (0 <= alvo_y < LINHAS and 0 <= alvo_x < COLUNAS):
                break #impede que o fogo se espalhe
            alvo = matriz[alvo_y][alvo_x]

            #Verificando se bateu em uma parede fixa
            if alvo == PAREDE:
                break #Impede que o fogo se espalhe

            #Verificando se bateu em um bloco destrutível
            elif alvo == BLOCO_DESTRUTIVEL:
                matriz[alvo_y][alvo_x] = VAZIO # Destrói o bloco
                break # O fogo para após destruir o bloco (não atravessa)

            # Caso o caminho esteja livre
            else:
                matriz[alvo_y][alvo_x] = VAZIO # Destroi o que estiver no caminho
                #implementar morte do player aqui
                 
def atualizar_bombas(matriz):
    # Diminui o timer de todas as bombas e verifica quais devem explodir
    #Retorna uma lista das coordenadas que explodiram nesse turno
    bombas_para_remover = []

    for bomba in bombas_ativas:
        bomba['timer'] -= 1

        #Função que faz a bomba explodir
        if bomba['timer'] <= 0:
            calcular_explosao(matriz, bomba['y'], bomba['x'], bomba['raio'])
            bombas_para_remover.append(bomba)

    #Limpa as bombas que já explodiram da lista ativa
    for bomba in bombas_para_remover:
        bombas_ativas.remove(bomba)
