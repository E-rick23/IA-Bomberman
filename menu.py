import pygame
import sys
import visual
import config

pygame.init()

# Cores
BRANCO      = (255, 255, 255)
PRETO       = (0,   0,   0)
CINZA       = (150, 150, 150)
CINZA_ESC   = (60,  60,  60)
AZUL        = (50,  150, 255)
LARANJA     = (255, 140,  0)
VERMELHO    = (200,  40,  40)

# Tamanho mínimo seguro para o menu
LARGURA_MIN = 640
ALTURA_MIN  = 520


def _fonte_para(tamanho_base, largura_tela):
    """Escala a fonte de acordo com a largura da tela."""
    escala = min(1.0, largura_tela / LARGURA_MIN)
    return max(10, int(tamanho_base * escala))


class Seletor:
    """Um item do menu com label, setas e valor."""

    def __init__(self, label, opcoes):
        self.label  = label
        self.opcoes = opcoes
        self.idx    = 0

    @property
    def valor(self):
        return self.opcoes[self.idx]

    def avancar(self, delta=1):
        self.idx = (self.idx + delta) % len(self.opcoes)

    def valor_str(self):
        return str(self.valor)


class Menu:
    def __init__(self, largura=720, altura=560):
        self.largura = max(largura, LARGURA_MIN)
        self.altura  = max(altura,  ALTURA_MIN)
        self.tela = pygame.display.set_mode(
            (self.largura, self.altura), pygame.RESIZABLE
        )
        pygame.display.set_caption("Bombasticos - Menu")
        self.clock = pygame.time.Clock()

        # Seletores
        self.seletores = [
            Seletor("Tamanho do Mapa",       [9, 11, 13, 15]),
            Seletor("Quantidade de Players",  [1, 2, 3, 4]),
            Seletor("Quantidade de Inimigos", [1, 2, 3, 4]),
            Seletor("Algoritmo dos Inimigos", ["BFS", "DFS", "A*", "Busca Gulosa"]),
        ]
        # índice 0-3 = seletores, 4 = botão Jogar
        self.opcao_focada = 0

        self._atualizar_fontes()

    # ------------------------------------------------------------------
    def _atualizar_fontes(self):
        lg = self.largura
        self.fonte_titulo  = pygame.font.SysFont("Arial", _fonte_para(42, lg), bold=True)
        self.fonte_label   = pygame.font.SysFont("Arial", _fonte_para(20, lg), bold=True)
        self.fonte_valor   = pygame.font.SysFont("Arial", _fonte_para(22, lg))
        self.fonte_jogar   = pygame.font.SysFont("Arial", _fonte_para(32, lg), bold=True)
        self.fonte_dica    = pygame.font.SysFont("Arial", _fonte_para(14, lg))

    def _blit_centro(self, texto, fonte, cor, cx, cy):
        surf = fonte.render(texto, True, cor)
        rect = surf.get_rect(center=(cx, cy))
        self.tela.blit(surf, rect)
        return rect

    def _blit_topo(self, texto, fonte, cor, cx, top):
        surf = fonte.render(texto, True, cor)
        rect = surf.get_rect(centerx=cx, top=top)
        self.tela.blit(surf, rect)
        return rect

    # ------------------------------------------------------------------
    def _desenhar_seletor(self, seletor, cx, cy, focado, rect_dest):
        """Desenha label + setas + valor de um seletor.

        Retorna (rect_esq, rect_dir, rect_valor) para hit-test do mouse.
        """
        pad_v  = 6
        cor_label = AZUL if focado else CINZA
        cor_val   = BRANCO if focado else CINZA

        # --- label ---
        l_surf = self.fonte_label.render(seletor.label + ":", True, cor_label)
        lh = l_surf.get_height()
        l_rect = l_surf.get_rect(centerx=cx, centery=cy - lh // 2 - pad_v)
        self.tela.blit(l_surf, l_rect)

        # --- linha do valor: seta_esq  valor  seta_dir ---
        val_str  = seletor.valor_str()
        v_surf   = self.fonte_valor.render(val_str, True, cor_val)
        aw       = self.fonte_valor.size("◄")[0]
        gap      = 14
        total_w  = aw + gap + v_surf.get_width() + gap + aw

        row_y    = cy + lh // 2 + pad_v
        left_x   = cx - total_w // 2

        # seta esquerda
        se_surf  = self.fonte_valor.render("◄", True, cor_val)
        se_rect  = se_surf.get_rect(left=left_x, centery=row_y)
        self.tela.blit(se_surf, se_rect)

        # valor
        v_rect   = v_surf.get_rect(left=se_rect.right + gap, centery=row_y)
        self.tela.blit(v_surf, v_rect)

        # seta direita
        sd_surf  = self.fonte_valor.render("►", True, cor_val)
        sd_rect  = sd_surf.get_rect(left=v_rect.right + gap, centery=row_y)
        self.tela.blit(sd_surf, sd_rect)

        # bounding box do seletor inteiro (para hit-test)
        rect_dest.update(
            l_rect.left,
            l_rect.top,
            max(l_rect.width, sd_rect.right - l_rect.left),
            sd_rect.bottom - l_rect.top,
        )

        return se_rect, sd_rect

    # ------------------------------------------------------------------
    def _desenhar_fundo(self):
        self.tela.fill((10, 10, 20))

        # grade decorativa sutil
        step = 40
        cor_grade = (20, 20, 40)
        for x in range(0, self.largura, step):
            pygame.draw.line(self.tela, cor_grade, (x, 0), (x, self.altura))
        for y in range(0, self.altura, step):
            pygame.draw.line(self.tela, cor_grade, (0, y), (self.largura, y))

        # borda
        pygame.draw.rect(self.tela, (40, 40, 80), (0, 0, self.largura, self.altura), 3)

    # ------------------------------------------------------------------
    def rodar(self):
        while True:
            # Trata resize
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif evento.type == pygame.VIDEORESIZE:
                    self.largura = max(evento.w, LARGURA_MIN)
                    self.altura  = max(evento.h, ALTURA_MIN)
                    self.tela = pygame.display.set_mode(
                        (self.largura, self.altura), pygame.RESIZABLE
                    )
                    self._atualizar_fontes()

                elif evento.type == pygame.KEYDOWN:
                    resultado = self._processar_teclado(evento.key)
                    if resultado is not None:
                        return resultado

                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    resultado = self._processar_clique(pygame.mouse.get_pos())
                    if resultado is not None:
                        return resultado

                elif evento.type == pygame.MOUSEMOTION:
                    self._processar_hover(pygame.mouse.get_pos())

            self._renderizar()
            pygame.display.flip()
            self.clock.tick(30)

    # ------------------------------------------------------------------
    def _renderizar(self):
        cx  = self.largura  // 2
        lg  = self.largura
        alt = self.altura

        self._desenhar_fundo()

        # Título
        self._blit_centro("BOMBASTICOS", self.fonte_titulo, LARANJA, cx, int(alt * 0.09))

        # Linha separadora
        sep_y = int(alt * 0.15)
        pygame.draw.line(self.tela, (60, 60, 120), (lg // 8, sep_y), (7 * lg // 8, sep_y), 2)

        # Distribui os 4 seletores verticalmente entre 20 % e 80 % da altura
        n   = len(self.seletores)
        top = int(alt * 0.20)
        bot = int(alt * 0.80)
        step = (bot - top) / n

        self.rects_seletores = []
        self.rects_setas = []     # lista de (rect_esq, rect_dir) por seletor

        for i, sel in enumerate(self.seletores):
            cy   = int(top + step * i + step / 2)
            focado = (self.opcao_focada == i)
            r    = pygame.Rect(0, 0, 0, 0)
            setas = self._desenhar_seletor(sel, cx, cy, focado, r)
            self.rects_seletores.append(r)
            self.rects_setas.append(setas)

            # Destaque de foco (caixa)
            if focado:
                pad = 8
                pygame.draw.rect(
                    self.tela, AZUL,
                    r.inflate(pad * 2, pad * 2),
                    2, border_radius=6
                )

        # Botão Jogar
        btn_y  = int(alt * 0.90)
        focado = (self.opcao_focada == 4)
        cor_btn = LARANJA if focado else CINZA
        btn_surf = self.fonte_jogar.render("[ INICIAR JOGO ]", True, cor_btn)
        self.rect_jogar = btn_surf.get_rect(center=(cx, btn_y))
        if focado:
            pygame.draw.rect(
                self.tela, VERMELHO,
                self.rect_jogar.inflate(20, 12), 2, border_radius=8
            )
        self.tela.blit(btn_surf, self.rect_jogar)

        # Dica de teclado
        dica = "↑↓ navegar   ◄► mudar   Enter confirmar"
        self._blit_centro(dica, self.fonte_dica, CINZA_ESC, cx, btn_y + 28)

    # ------------------------------------------------------------------
    def _processar_teclado(self, key):
        if key == pygame.K_DOWN:
            self.opcao_focada = (self.opcao_focada + 1) % 5
        elif key == pygame.K_UP:
            self.opcao_focada = (self.opcao_focada - 1) % 5
        elif key == pygame.K_LEFT:
            if self.opcao_focada < 4:
                self.seletores[self.opcao_focada].avancar(-1)
        elif key == pygame.K_RIGHT:
            if self.opcao_focada < 4:
                self.seletores[self.opcao_focada].avancar(+1)
        elif key == pygame.K_RETURN:
            if self.opcao_focada == 4:
                return self.coletar_configuracoes()
        return None

    def _processar_clique(self, pos):
        if hasattr(self, "rect_jogar") and self.rect_jogar.collidepoint(pos):
            return self.coletar_configuracoes()

        for i, (re, rd) in enumerate(getattr(self, "rects_setas", [])):
            if re.collidepoint(pos):
                self.seletores[i].avancar(-1)
                self.opcao_focada = i
            elif rd.collidepoint(pos):
                self.seletores[i].avancar(+1)
                self.opcao_focada = i
            elif self.rects_seletores[i].collidepoint(pos):
                self.opcao_focada = i
        return None

    def _processar_hover(self, pos):
        for i, r in enumerate(getattr(self, "rects_seletores", [])):
            if r.inflate(16, 8).collidepoint(pos):
                self.opcao_focada = i
                return
        if hasattr(self, "rect_jogar") and self.rect_jogar.inflate(20, 12).collidepoint(pos):
            self.opcao_focada = 4

    # ------------------------------------------------------------------
    def coletar_configuracoes(self):
        return {
            "tamanho":            self.seletores[0].valor,
            "players":            self.seletores[1].valor,
            "inimigos":           self.seletores[2].valor,
            "algoritmo_inimigos": self.seletores[3].valor,
        }

    # ------------------------------------------------------------------
    def selecionar_personagens(self, qtd_players):
        escolhas = []
        for p in range(qtd_players):
            selecionado = 0
            confirmado  = False

            while not confirmado:
                # Atualiza dimensões caso janela tenha sido redimensionada
                lg  = self.largura
                alt = self.altura
                cx  = lg // 2
                self._atualizar_fontes()

                self._desenhar_fundo()

                # Título — garante que nunca ultrapasse a largura
                titulo = f"JOGADOR {p+1} — ESCOLHA SEU HERÓI"
                t_surf = self.fonte_label.render(titulo, True, BRANCO)
                # Encolhe fonte se necessário
                f_tit = self.fonte_label
                while t_surf.get_width() > lg - 40:
                    f_tit = pygame.font.SysFont(
                        "Arial", max(10, f_tit.size("A")[1] - 2), bold=True
                    )
                    t_surf = f_tit.render(titulo, True, BRANCO)
                self.tela.blit(t_surf, t_surf.get_rect(centerx=cx, top=int(alt * 0.08)))

                # Instrução
                dica_surf = self.fonte_dica.render(
                    "◄► mover   Enter / clique selecionar", True, CINZA
                )
                self.tela.blit(dica_surf, dica_surf.get_rect(centerx=cx, top=int(alt * 0.18)))

                # Personagens — espaço disponível
                tile = config.TILE_SIZE
                n_chars   = 4
                espaco_x  = lg - 80
                passo_x   = espaco_x // n_chars
                y_char    = int(alt * 0.50)

                retangulos_personagens = []
                for i in range(n_chars):
                    sprite = visual.obter_sprite_menu(i)
                    x = 40 + passo_x * i + passo_x // 2

                    # Nome do personagem abaixo
                    nome = f"Player {i+1}"
                    n_surf = self.fonte_dica.render(nome, True, BRANCO)
                    self.tela.blit(n_surf, n_surf.get_rect(centerx=x, bottom=y_char - tile // 2 - 6))

                    rect_p = pygame.Rect(x - tile // 2, y_char - tile // 2, tile, tile)
                    retangulos_personagens.append(rect_p)

                    # Destaque de seleção
                    cor_borda = AZUL if i == selecionado else CINZA_ESC
                    largura_b = 3  if i == selecionado else 1
                    pygame.draw.rect(self.tela, cor_borda, rect_p.inflate(8, 8), largura_b, border_radius=5)

                    self.tela.blit(sprite, rect_p)

                # Seta indicadora acima do selecionado
                rx = retangulos_personagens[selecionado].centerx
                ry = retangulos_personagens[selecionado].top - 18
                pts = [(rx, ry + 14), (rx - 10, ry), (rx + 10, ry)]
                pygame.draw.polygon(self.tela, LARANJA, pts)

                # Botão confirmar
                btn_y  = int(alt * 0.82)
                b_surf = self.fonte_jogar.render("[ CONFIRMAR ]", True, LARANJA)
                b_rect = b_surf.get_rect(center=(cx, btn_y))
                pygame.draw.rect(self.tela, VERMELHO, b_rect.inflate(20, 12), 2, border_radius=8)
                self.tela.blit(b_surf, b_rect)

                pygame.display.flip()
                self.clock.tick(30)

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif evento.type == pygame.VIDEORESIZE:
                        self.largura = max(evento.w, LARGURA_MIN)
                        self.altura  = max(evento.h, ALTURA_MIN)
                        self.tela = pygame.display.set_mode(
                            (self.largura, self.altura), pygame.RESIZABLE
                        )

                    elif evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_LEFT:
                            selecionado = (selecionado - 1) % n_chars
                        elif evento.key == pygame.K_RIGHT:
                            selecionado = (selecionado + 1) % n_chars
                        elif evento.key == pygame.K_RETURN:
                            escolhas.append(selecionado)
                            confirmado = True

                    elif evento.type == pygame.MOUSEMOTION:
                        for i, rect in enumerate(retangulos_personagens):
                            if rect.inflate(8, 8).collidepoint(evento.pos):
                                selecionado = i

                    elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                        for i, rect in enumerate(retangulos_personagens):
                            if rect.inflate(8, 8).collidepoint(evento.pos):
                                selecionado = i
                                escolhas.append(selecionado)
                                confirmado = True
                                break
                        if not confirmado and b_rect.inflate(20, 12).collidepoint(evento.pos):
                            escolhas.append(selecionado)
                            confirmado = True

        return escolhas