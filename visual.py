import pygame
import config

sprites = {}
sprites_animados = {}
animacoes_por_sprite = {}


def recortar_sprite(
    sheet, col, linha, largura=config.SPRITE_SIZE, altura=config.SPRITE_SIZE
):
    rect = pygame.Rect(col * largura, linha * altura, largura, altura)
    sub = sheet.subsurface(rect)
    return pygame.transform.scale(sub, (config.TILE_SIZE, config.TILE_SIZE))


def _fazer_sprite_solido(cor):
    s = pygame.Surface((config.SPRITE_SIZE, config.SPRITE_SIZE))
    s.fill(cor)
    return pygame.transform.scale(s, (config.TILE_SIZE, config.TILE_SIZE))


def obter_sprite_menu(sprite_id):
    return animacoes_por_sprite[sprite_id]["baixo"]["parado"][0]


def _carregar_sprites_bomba():
    sheet_bomba = pygame.image.load("Assets/Bomba.png").convert_alpha()
    bomba = []
    for i in range(3):
        bomba.append(recortar_sprite(sheet_bomba, i, 0))

    sprites_animados["bomba"] = bomba


def _carregar_sprites_tijolo():
    sheet_tijolo = pygame.image.load("Assets/Tijolo.png").convert_alpha()

    sprites[config.PAREDE] = recortar_sprite(sheet_tijolo, 0, 0)
    sprites[config.BLOCO_DESTRUTIVEL] = recortar_sprite(sheet_tijolo, 1, 0)

    bloco_destruindo = []

    for i in range(7):
        bloco_destruindo.append(recortar_sprite(sheet_tijolo, i, 0))

    sprites_animados["bloco_destruindo"] = bloco_destruindo


def _carregar_sprites_fogo():
    sheet_fogo = pygame.image.load("Assets/Fogo.png").convert_alpha()

    partes_fogo = [
        "fogo_centro",
        "fogo_horizontal",
        "fogo_vertical",
        "fogo_cima",
        "fogo_baixo",
        "fogo_esq",
        "fogo_dir",
    ]
    for p in partes_fogo:
        sprites_animados[p] = []

    for linha in range(2):
        for col in range(2):
            base_x, base_y = col * 80, linha * 80

            def extrair(px, py):
                rect = pygame.Rect(base_x + px, base_y + py, 16, 16)
                sub = sheet_fogo.subsurface(rect)
                return pygame.transform.scale(sub, (config.TILE_SIZE, config.TILE_SIZE))

            # Centro da cruz (x=32, y=32)
            sprites_animados["fogo_centro"].append(extrair(32, 32))

            # Corpos (meios da cruz)
            sprites_animados["fogo_horizontal"].append(extrair(16, 32))
            sprites_animados["fogo_vertical"].append(extrair(32, 16))

            # Pontas extremas da cruz
            sprites_animados["fogo_cima"].append(extrair(32, 0))
            sprites_animados["fogo_baixo"].append(extrair(32, 64))
            sprites_animados["fogo_esq"].append(extrair(0, 32))
            sprites_animados["fogo_dir"].append(extrair(64, 32))


def _carregar_sprites_jogadores():
    arquivos_players = [f"Assets/Player{i}.png" for i in range(1, 5)]

    for sprite_id, arquivo in enumerate(arquivos_players):
        # Dicionário base para este jogador
        anim = {
            "direita": {"parado": [], "andando": [], "plantando": []},
            "esquerda": {"parado": [], "andando": [], "plantando": []},
            "baixo": {"parado": [], "andando": [], "plantando": []},
            "cima": {"parado": [], "andando": [], "plantando": []},
        }

        try:
            sheet = pygame.image.load(arquivo).convert_alpha()

            # Direita
            anim["direita"]["parado"].append(recortar_sprite(sheet, 0, 0))
            anim["direita"]["andando"].append(recortar_sprite(sheet, 1, 0))
            anim["direita"]["plantando"].append(recortar_sprite(sheet, 2, 0))
            # Esquerda
            anim["esquerda"]["parado"].append(recortar_sprite(sheet, 0, 1))
            anim["esquerda"]["andando"].append(recortar_sprite(sheet, 1, 1))
            anim["esquerda"]["plantando"].append(recortar_sprite(sheet, 2, 1))
            # Baixo
            anim["baixo"]["parado"].append(recortar_sprite(sheet, 5, 0))
            anim["baixo"]["andando"].extend(
                [recortar_sprite(sheet, 6, 0), recortar_sprite(sheet, 6, 1)]
            )
            # Cima
            anim["cima"]["parado"].append(recortar_sprite(sheet, 7, 0))
            anim["cima"]["andando"].extend(
                [recortar_sprite(sheet, 8, 0), recortar_sprite(sheet, 8, 1)]
            )

        except (pygame.error, FileNotFoundError):
            placeholder = _fazer_sprite_solido((0, 0, 255))
            for direcao in anim:
                for acao in anim[direcao]:
                    anim[direcao][acao].append(placeholder)

        animacoes_por_sprite[sprite_id] = anim


def _carregar_sprites_inimigos():
    sheet_inimigos = pygame.image.load("Assets/Inimigos.png").convert_alpha()

    linhas = [1, 4, 5, 6]
    algoritmos = ["BFS", "DFS", "A*", "Busca Gulosa"]
    
    dicionario_sprites = {} 
    
    for linha, algoritmo in zip(linhas, algoritmos):
        dicionario_sprites[algoritmo] = []
        for i in range(6):
            sprite_recortado = recortar_sprite(sheet_inimigos, i, linha)
            dicionario_sprites[algoritmo].append(sprite_recortado)

    animacoes_por_sprite["inimigos"] = dicionario_sprites

def carregar_recursos():
    """Função principal que chama todos os sprites"""
    _carregar_sprites_bomba()
    _carregar_sprites_tijolo()
    _carregar_sprites_fogo()
    _carregar_sprites_jogadores()
    _carregar_sprites_inimigos()

    # Sprites do mapa base
    sprites[config.VAZIO] = _fazer_sprite_solido((34, 139, 34))


def desenhar_mapa(tela, matriz):
    for y in range(config.LINHAS):
        for x in range(config.COLUNAS):
            pos = (x * config.TILE_SIZE, y * config.TILE_SIZE)
            celula = matriz[y][x]

            # Sempre desenha o chão primeiro
            tela.blit(sprites[config.VAZIO], pos)

            # Desenha os obstáculos
            if celula in (config.PAREDE, config.BLOCO_DESTRUTIVEL, config.FOGO):
                tela.blit(sprites[celula], pos)

                # Se for fogo, podemos limpar da matriz para sumir no próximo frame
                # (depende de como está controlando a lógica no seu gameloop)
                if celula == config.FOGO:
                    matriz[y][x] = config.VAZIO


def desenhar_hud(tela, jogadores):
    """Exibe status básico dos jogadores no topo da tela."""
    fonte = pygame.font.SysFont("Arial", 16, bold=True)
    cores_id = {config.P1: (100, 180, 255), config.P2: (255, 120, 120)}
    nomes_id = {config.P1: "P1 ↑↓←→ [Space]", config.P2: "P2 WASD [Shift]"}

    for i, jogador in enumerate(jogadores):
        cor = cores_id.get(jogador.id, (255, 255, 255))
        status = "VIVO" if jogador.vivo else "MORTO"
        texto = fonte.render(
            f"{nomes_id.get(jogador.id, f'P{i+1}')}  {status}", True, cor
        )
        tela.blit(texto, (10 + i * 300, 4))
