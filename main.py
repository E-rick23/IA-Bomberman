import mapgenerator

def main():
    tabuleiro = mapgenerator.criar_matriz_vazia() # Gerando o mapa
    
    # Gerando o cenário
    mapgenerator.gerar_pilares(tabuleiro)
    mapgenerator.espalhar_blocos(tabuleiro, densidade=0.60)  #60% de chance de um espaço livre virar um bloco destrutível

    mapgenerator.posicionar_jogadores(tabuleiro) # Posiciona os jogadores

    # Printa o mapa
    print("\n Mapa gerado:")
    print(tabuleiro) 

if __name__ == "__main__":
    main()
