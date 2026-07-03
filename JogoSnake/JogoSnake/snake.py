##############################################################################
###                         P Y T H O N   C R A S H                        ###
##############################################################################
### Versao visual melhorada do jogo da cobrinha                             ###
##############################################################################
import math
import os
import random
import sys
from array import array

import pygame


pygame.init()
pygame.font.init()

try:
    pygame.mixer.init()
    AUDIO_OK = True
except pygame.error:
    AUDIO_OK = False


LARGURA_TELA = 800
ALTURA_TELA = 650
ALTURA_PLACAR = 120
TAMANHO = 40
AREA_JOGO_ALTURA = ALTURA_TELA - ALTURA_PLACAR
TITULO = "Python Crash - Cobrinha Neon"

COLUNAS = LARGURA_TELA // TAMANHO
LINHAS = AREA_JOGO_ALTURA // TAMANHO

COR_FUNDO_TOPO = (9, 15, 28)
COR_FUNDO_BAIXO = (20, 35, 58)
COR_GRADE = (45, 67, 95)
COR_TEXTO = (241, 245, 249)
COR_TEXTO_FRACO = (148, 163, 184)
COR_PAINEL = (15, 23, 42)
COR_PAINEL_CLARO = (30, 41, 59)
COR_PAINEL_ESCURO = (2, 6, 23)
COR_BORDA_SUAVE = (71, 85, 105)
COR_VERDE = (52, 211, 153)
COR_VERDE_ESCURO = (16, 185, 129)
COR_CAB_SOL = (236, 253, 245)
COR_MACA = (248, 113, 113)
COR_MACA_LUZ = (254, 202, 202)
COR_BOMBA = (244, 63, 94)
COR_BOMBA_LUZ = (251, 191, 36)
COR_ALERTA = (251, 191, 36)
COR_PERIGO = (248, 113, 113)
COR_AZUL = (56, 189, 248)
COR_ROXO = (168, 85, 247)

SKINS = [
    {
        "nome": "Neon",
        "arquivos": {},
        "cores": {
            "principal": (52, 211, 153),
            "secundaria": (16, 185, 129),
            "miolo": (236, 253, 245),
            "fruta": (248, 113, 113),
            "fruta_luz": (254, 202, 202),
            "bomba": (244, 63, 94),
            "bomba_luz": (251, 191, 36),
        },
    },
    {
        "nome": "Fogo",
        "arquivos": {},
        "cores": {
            "principal": (251, 146, 60),
            "secundaria": (194, 65, 12),
            "miolo": (255, 237, 213),
            "fruta": (239, 68, 68),
            "fruta_luz": (254, 215, 170),
            "bomba": (127, 29, 29),
            "bomba_luz": (253, 224, 71),
        },
    },
    {
        "nome": "Classica",
        "arquivos": {},
        "cores": {
            "principal": (132, 204, 22),
            "secundaria": (77, 124, 15),
            "miolo": (236, 252, 203),
            "fruta": (220, 38, 38),
            "fruta_luz": (254, 202, 202),
            "bomba": (51, 65, 85),
            "bomba_luz": (250, 204, 21),
        },
    },
    {
        "nome": "Gelo",
        "arquivos": {},
        "cores": {
            "principal": (56, 189, 248),
            "secundaria": (14, 116, 144),
            "miolo": (224, 242, 254),
            "fruta": (217, 70, 239),
            "fruta_luz": (245, 208, 254),
            "bomba": (99, 102, 241),
            "bomba_luz": (165, 243, 252),
        },
    },
]

skin_indice = 0

CONFIG_FASES = {
    1: {"fps": 7, "chance_bomba": 0.10, "tempo_item": 6500, "meta_score": 50},
    2: {"fps": 8, "chance_bomba": 0.18, "tempo_item": 5800, "meta_score": 90},
    3: {"fps": 9, "chance_bomba": 0.28, "tempo_item": 5200, "meta_score": 140},
    4: {"fps": 11, "chance_bomba": 0.40, "tempo_item": 4700, "meta_score": 210},
    5: {"fps": 13, "chance_bomba": 0.55, "tempo_item": 4300, "meta_score": None},
}

FASE_MAXIMA = max(CONFIG_FASES)

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption(TITULO)
relogio = pygame.time.Clock()

fonte_titulo = pygame.font.SysFont("Segoe UI", 28, bold=True)
fonte_hud = pygame.font.SysFont("Segoe UI", 22, bold=True)
fonte_pequena = pygame.font.SysFont("Segoe UI", 16, bold=True)
fonte_micro = pygame.font.SysFont("Segoe UI", 13, bold=True)
fonte_msg = pygame.font.SysFont("Segoe UI", 42, bold=True)
fonte_menu = pygame.font.SysFont("Segoe UI", 24, bold=True)

ARQUIVO_RECORDE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recorde.txt")

FRUTAS = {
    "vermelha": {"pontos": 10, "nome": "Maca", "cor": (248, 113, 113)},
    "verde": {"pontos": 15, "nome": "Kiwi", "cor": (52, 211, 153)},
    "dourada": {"pontos": 30, "nome": "Dourada", "cor": (250, 204, 21)},
    "azul": {"pontos": 10, "nome": "Tempo lento", "cor": (56, 189, 248)},
    "roxa": {"pontos": 10, "nome": "Escudo", "cor": (168, 85, 247)},
    "coracao": {"pontos": 0, "nome": "Vida extra", "cor": (244, 63, 94)},
}


def caminho_asset(pasta, arquivo):
    base = os.path.dirname(os.path.abspath(__file__))
    candidatos = [
        os.path.join(base, pasta, arquivo),
        os.path.join(os.getcwd(), pasta, arquivo),
    ]
    for caminho in candidatos:
        if os.path.exists(caminho):
            return caminho
    return candidatos[0]


def carregar_imagem(pasta, arquivo, tamanho):
    if not arquivo:
        return None
    try:
        imagem = pygame.image.load(caminho_asset(pasta, arquivo)).convert_alpha()
        return pygame.transform.smoothscale(imagem, tamanho)
    except (FileNotFoundError, pygame.error):
        return None


def carregar_som(arquivo):
    if not AUDIO_OK:
        return None
    try:
        return pygame.mixer.Sound(caminho_asset("Sons", arquivo))
    except (FileNotFoundError, pygame.error):
        return None


def gerar_som_notas(notas, volume=0.35):
    if not AUDIO_OK:
        return None

    taxa, formato, canais = pygame.mixer.get_init()
    bits = abs(formato)
    if bits != 16:
        return None

    amostras = array("h")
    for frequencia, duracao_ms in notas:
        total = max(1, int(taxa * duracao_ms / 1000))
        fade = max(1, int(taxa * 0.012))
        for i in range(total):
            if frequencia <= 0:
                onda = 0
            else:
                onda = math.sin(math.tau * frequencia * i / taxa)
                onda += 0.35 * math.sin(math.tau * frequencia * 2 * i / taxa)
            envelope = min(1, i / fade, (total - i) / fade)
            valor = int(max(-1, min(1, onda * envelope * volume)) * 32767)
            for _ in range(canais):
                amostras.append(valor)

    try:
        return pygame.mixer.Sound(buffer=amostras.tobytes())
    except pygame.error:
        return None


def montar_sons():
    mordida_arquivo = carregar_som("crunchybite.ogg")
    morte_arquivo = carregar_som("morreu.mp3")
    return {
        "inicio": gerar_som_notas([(392, 70), (523, 80), (659, 110)], 0.32),
        "virar": gerar_som_notas([(440, 35)], 0.16),
        "pausa": gerar_som_notas([(330, 60), (0, 20), (330, 60)], 0.22),
        "skin": gerar_som_notas([(587, 55), (740, 75)], 0.25),
        "mordida": mordida_arquivo or gerar_som_notas([(780, 45), (980, 55)], 0.28),
        "dourada": gerar_som_notas([(740, 45), (988, 60), (1318, 90)], 0.30),
        "poder": gerar_som_notas([(523, 60), (784, 60), (1046, 100)], 0.28),
        "vida": gerar_som_notas([(659, 60), (880, 60), (1174, 120)], 0.30),
        "fase": gerar_som_notas([(523, 70), (659, 70), (784, 70), (1046, 140)], 0.32),
        "escudo": gerar_som_notas([(220, 70), (440, 110)], 0.27),
        "bomba": gerar_som_notas([(120, 120), (80, 180)], 0.42),
        "dano": morte_arquivo or gerar_som_notas([(260, 90), (180, 130)], 0.35),
        "game_over": gerar_som_notas([(330, 150), (247, 150), (165, 240)], 0.34),
    }


def tocar_som(nome):
    som = SONS.get(nome)
    if som:
        som.play()


def skin_atual():
    return SKINS[skin_indice]


def cor_skin(chave, padrao):
    return skin_atual()["cores"].get(chave, padrao)


def carregar_sprites_da_skin():
    arquivos = skin_atual()["arquivos"]
    return {
        "cabeca": carregar_imagem("Imagens", arquivos.get("cabeca"), (TAMANHO + 22, TAMANHO + 22)),
        "corpo": carregar_imagem("Imagens", arquivos.get("corpo"), (TAMANHO, TAMANHO)),
        "maca_vermelha": carregar_imagem("Imagens", arquivos.get("maca_vermelha"), (TAMANHO, TAMANHO)),
        "maca_verde": carregar_imagem("Imagens", arquivos.get("maca_verde"), (TAMANHO, TAMANHO)),
        "bomba": carregar_imagem("Imagens", arquivos.get("bomba"), (TAMANHO, TAMANHO)),
    }


def trocar_skin(indice=None):
    global skin_indice, sprites
    if indice is None:
        skin_indice = (skin_indice + 1) % len(SKINS)
    else:
        skin_indice = indice % len(SKINS)
    sprites = carregar_sprites_da_skin()
    tocar_som("skin")


sprites = carregar_sprites_da_skin()
SONS = montar_sons()


def carregar_recorde():
    try:
        with open(ARQUIVO_RECORDE, "r", encoding="utf-8") as arquivo:
            return int(arquivo.read().strip() or "0")
    except (FileNotFoundError, ValueError, OSError):
        return 0


def salvar_recorde(valor):
    try:
        with open(ARQUIVO_RECORDE, "w", encoding="utf-8") as arquivo:
            arquivo.write(str(valor))
    except OSError:
        pass


def criar_fundo():
    rng = random.Random(42)
    fundo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))

    centro_x = LARGURA_TELA * 0.55
    centro_y = ALTURA_TELA * 0.42
    raio_maximo = math.hypot(LARGURA_TELA, ALTURA_TELA)

    for y in range(ALTURA_TELA):
        t = y / ALTURA_TELA
        brilho = max(0, 1 - abs(y - centro_y) / raio_maximo)
        cor = (
            min(255, int(COR_FUNDO_TOPO[0] * (1 - t) + COR_FUNDO_BAIXO[0] * t + brilho * 8)),
            min(255, int(COR_FUNDO_TOPO[1] * (1 - t) + COR_FUNDO_BAIXO[1] * t + brilho * 12)),
            min(255, int(COR_FUNDO_TOPO[2] * (1 - t) + COR_FUNDO_BAIXO[2] * t + brilho * 22)),
        )
        pygame.draw.line(fundo, cor, (0, y), (LARGURA_TELA, y))

    brilho_central = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    for raio in range(260, 20, -18):
        alpha = max(0, int(34 * (1 - raio / 280)))
        pygame.draw.circle(brilho_central, (45, 212, 191, alpha), (int(centro_x), int(centro_y)), raio)
    pygame.draw.circle(brilho_central, (244, 114, 182, 18), (150, 540), 190)
    pygame.draw.circle(brilho_central, (96, 165, 250, 16), (720, 160), 160)
    fundo.blit(brilho_central, (0, 0))

    for x in range(0, LARGURA_TELA, TAMANHO):
        pygame.draw.line(fundo, (34, 54, 82), (x, ALTURA_PLACAR), (x, ALTURA_TELA), 1)
    for y in range(ALTURA_PLACAR, ALTURA_TELA, TAMANHO):
        pygame.draw.line(fundo, (34, 54, 82), (0, y), (LARGURA_TELA, y), 1)

    for _ in range(90):
        x = rng.randint(0, LARGURA_TELA - 1)
        y = rng.randint(ALTURA_PLACAR + 8, ALTURA_TELA - 1)
        raio = rng.choice([1, 1, 1, 2])
        alpha = rng.randint(45, 115)
        cor = rng.choice([
            (125, 211, 252, alpha),
            (167, 243, 208, alpha),
            (248, 250, 252, alpha),
        ])
        pygame.draw.circle(fundo, cor, (x, y), raio)

    for y in range(ALTURA_PLACAR, ALTURA_TELA, TAMANHO * 2):
        pygame.draw.line(fundo, (52, 211, 153), (0, y), (LARGURA_TELA, y), 1)
        linha = pygame.Surface((LARGURA_TELA, 1), pygame.SRCALPHA)
        linha.fill((52, 211, 153, 22))
        fundo.blit(linha, (0, y))

    return fundo


FUNDO = criar_fundo()


def posicao_aleatoria(ocupadas):
    livres = []
    for coluna in range(COLUNAS):
        for linha in range(LINHAS):
            pos = (coluna * TAMANHO, ALTURA_PLACAR + linha * TAMANHO)
            if pos not in ocupadas:
                livres.append(pos)
    return random.choice(livres) if livres else (0, ALTURA_PLACAR)


def desenhar_texto_central(texto, fonte, cor, y):
    render = fonte.render(texto, True, cor)
    tela.blit(render, render.get_rect(center=(LARGURA_TELA // 2, y)))


def desenhar_retangulo_alpha(cor, rect, raio=0):
    camada = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(camada, cor, camada.get_rect(), border_radius=raio)
    tela.blit(camada, rect.topleft)


def abreviar_numero(valor):
    if valor >= 1000000:
        return f"{valor / 1000000:.1f}M"
    if valor >= 10000:
        return f"{valor / 1000:.1f}K"
    return str(valor)


def texto_cortado(texto, fonte, largura_maxima):
    if fonte.size(texto)[0] <= largura_maxima:
        return texto
    sufixo = "..."
    while texto and fonte.size(texto + sufixo)[0] > largura_maxima:
        texto = texto[:-1]
    return texto + sufixo if texto else sufixo


def desenhar_icone_hud(tipo, centro, cor):
    x, y = centro
    if tipo == "score":
        pygame.draw.circle(tela, cor, (x, y), 11)
        pygame.draw.circle(tela, (255, 255, 255), (x - 4, y - 4), 3)
    elif tipo == "vidas":
        pygame.draw.rect(tela, cor, (x - 11, y - 4, 22, 8), border_radius=3)
        pygame.draw.rect(tela, cor, (x - 4, y - 11, 8, 22), border_radius=3)
        pygame.draw.circle(tela, (255, 255, 255), (x + 6, y - 6), 2)
    elif tipo == "fase":
        pygame.draw.polygon(tela, cor, [(x, y - 13), (x + 12, y + 10), (x - 12, y + 10)])
        pygame.draw.circle(tela, (255, 255, 255), (x, y + 2), 3)
    elif tipo == "recorde":
        pygame.draw.rect(tela, cor, (x - 9, y - 8, 18, 17), border_radius=4)
        pygame.draw.rect(tela, (255, 255, 255), (x - 4, y - 13, 8, 7), border_radius=2)


def desenhar_cartao_hud(x, y, largura, altura, rotulo, valor, cor, icone):
    sombra = pygame.Rect(x + 3, y + 4, largura, altura)
    caixa = pygame.Rect(x, y, largura, altura)
    desenhar_retangulo_alpha((0, 0, 0, 70), sombra, 12)
    pygame.draw.rect(tela, (17, 24, 39), caixa, border_radius=12)
    pygame.draw.rect(tela, COR_BORDA_SUAVE, caixa, 1, border_radius=12)
    desenhar_retangulo_alpha((*cor, 38), pygame.Rect(x + 1, y + 1, largura - 2, altura - 2), 12)
    pygame.draw.rect(tela, cor, (x, y, 4, altura), border_radius=12)

    desenhar_icone_hud(icone, (x + 24, y + altura // 2 + 1), cor)
    tela.blit(fonte_micro.render(rotulo, True, COR_TEXTO_FRACO), (x + 45, y + 8))
    valor_render = fonte_hud.render(abreviar_numero(int(valor)), True, COR_TEXTO)
    tela.blit(valor_render, (x + 45, y + 25))


def desenhar_vidas(vidas, x, y):
    for i in range(6):
        cor = COR_PERIGO if i < vidas else (51, 65, 85)
        marcador = pygame.Rect(x + i * 17, y, 12, 8)
        pygame.draw.rect(tela, cor, marcador, border_radius=4)
        if i < vidas:
            pygame.draw.rect(tela, (255, 255, 255), (marcador.x + 2, marcador.y + 2, 3, 2), border_radius=1)


def desenhar_barra_fase(score, fase, x, y, largura):
    meta_atual = CONFIG_FASES[fase]["meta_score"]
    if fase == FASE_MAXIMA or meta_atual is None:
        progresso = 1
        texto = "Fase final"
    else:
        meta_anterior = CONFIG_FASES[fase - 1]["meta_score"] if fase > 1 else 0
        intervalo = max(1, meta_atual - meta_anterior)
        progresso = max(0, min(1, (score - meta_anterior) / intervalo))
        texto = f"Proxima fase: {max(0, meta_atual - score)} pts"

    trilho = pygame.Rect(x, y, largura, 8)
    pygame.draw.rect(tela, (30, 41, 59), trilho, border_radius=8)
    preenchido = pygame.Rect(x, y, max(8, int(largura * progresso)), 8)
    pygame.draw.rect(tela, cor_skin("principal", COR_VERDE), preenchido, border_radius=8)
    tela.blit(fonte_micro.render(texto, True, COR_TEXTO_FRACO), (x, y + 14))


def desenhar_hud(score, vidas, fase, pausa, recorde=0, poder=""):
    cor_principal = cor_skin("principal", COR_VERDE)
    pygame.draw.rect(tela, COR_PAINEL_ESCURO, (0, 0, LARGURA_TELA, ALTURA_PLACAR))
    desenhar_retangulo_alpha((*cor_principal, 28), pygame.Rect(0, 0, LARGURA_TELA, ALTURA_PLACAR), 0)
    pygame.draw.line(tela, cor_principal, (0, ALTURA_PLACAR - 2), (LARGURA_TELA, ALTURA_PLACAR - 2), 3)

    tela.blit(fonte_titulo.render("Python Crash", True, COR_TEXTO), (20, 10))
    skin_texto = texto_cortado(f"Skin: {skin_atual()['nome']}", fonte_pequena, 170)
    tela.blit(fonte_pequena.render(skin_texto, True, COR_TEXTO_FRACO), (23, 43))
    tela.blit(fonte_micro.render("VIDAS", True, COR_TEXTO_FRACO), (23, 70))
    desenhar_vidas(vidas, 74, 72)
    desenhar_barra_fase(score, fase, 20, 90, 305)

    desenhar_cartao_hud(345, 12, 128, 56, "SCORE", score, cor_principal, "score")
    cor_vidas = COR_PERIGO if vidas <= 1 else cor_principal
    desenhar_cartao_hud(484, 12, 98, 56, "VIDAS", vidas, cor_vidas, "vidas")
    cor_fase = COR_ALERTA if fase == FASE_MAXIMA else COR_AZUL
    desenhar_cartao_hud(593, 12, 82, 56, "FASE", fase, cor_fase, "fase")
    desenhar_cartao_hud(684, 12, 96, 56, "TOP", recorde, COR_ALERTA, "recorde")

    if poder:
        texto_poder = texto_cortado(poder, fonte_micro, 130)
        poder_rect = pygame.Rect(185, 63, 140, 21)
        pygame.draw.rect(tela, (30, 41, 59), poder_rect, border_radius=8)
        pygame.draw.rect(tela, COR_ROXO, poder_rect, 1, border_radius=8)
        tela.blit(fonte_micro.render(texto_poder, True, COR_TEXTO), (poder_rect.x + 10, poder_rect.y + 4))
    if pausa:
        pausa_rect = pygame.Rect(220, 14, 106, 24)
        pygame.draw.rect(tela, COR_ALERTA, pausa_rect, border_radius=8)
        tela.blit(fonte_micro.render("PAUSADO", True, COR_PAINEL_ESCURO), (pausa_rect.x + 24, pausa_rect.y + 5))


def desenhar_maca(pos, tipo, pulso):
    if sprites["maca_vermelha"] and tipo == "vermelha":
        tela.blit(sprites["maca_vermelha"], pos)
        return
    if sprites["maca_verde"] and tipo == "verde":
        tela.blit(sprites["maca_verde"], pos)
        return

    cx, cy = pos[0] + TAMANHO // 2, pos[1] + TAMANHO // 2
    raio = 14 + int(math.sin(pulso) * 2)
    dados = FRUTAS.get(tipo, FRUTAS["vermelha"])
    cor = dados["cor"]
    if tipo == "vermelha":
        cor = cor_skin("fruta", COR_MACA)
    elif tipo == "verde":
        cor = cor_skin("principal", COR_VERDE)

    pygame.draw.circle(tela, (0, 0, 0), (cx + 3, cy + 4), raio)
    pygame.draw.circle(tela, cor, (cx, cy), raio)
    pygame.draw.circle(tela, cor_skin("fruta_luz", COR_MACA_LUZ), (cx - 6, cy - 7), 5)
    if tipo == "dourada":
        pygame.draw.circle(tela, (255, 255, 255), (cx, cy), raio + 6, 2)
        pygame.draw.polygon(tela, (255, 255, 255), [(cx, cy - 11), (cx + 4, cy - 2), (cx + 13, cy), (cx + 4, cy + 3), (cx, cy + 12), (cx - 4, cy + 3), (cx - 13, cy), (cx - 4, cy - 2)])
    elif tipo == "azul":
        pygame.draw.circle(tela, (224, 242, 254), (cx, cy), 7, 2)
        pygame.draw.line(tela, (224, 242, 254), (cx, cy - 12), (cx, cy + 12), 2)
    elif tipo == "roxa":
        pygame.draw.circle(tela, (245, 208, 254), (cx, cy), raio + 5, 2)
        pygame.draw.circle(tela, (245, 208, 254), (cx, cy), 6)
    elif tipo == "coracao":
        pygame.draw.circle(tela, (255, 255, 255), (cx - 5, cy - 3), 5)
        pygame.draw.circle(tela, (255, 255, 255), (cx + 5, cy - 3), 5)
        pygame.draw.polygon(tela, (255, 255, 255), [(cx - 11, cy), (cx + 11, cy), (cx, cy + 12)])
    else:
        pygame.draw.rect(tela, (120, 72, 38), (cx - 2, cy - 20, 5, 11), border_radius=3)
        pygame.draw.ellipse(tela, cor_skin("principal", COR_VERDE), (cx + 3, cy - 22, 13, 8))


def desenhar_bomba(pos, pulso):
    if sprites["bomba"]:
        tela.blit(sprites["bomba"], pos)
        return

    cx, cy = pos[0] + TAMANHO // 2, pos[1] + TAMANHO // 2
    brilho = 18 + int(math.sin(pulso * 2) * 4)
    pygame.draw.circle(tela, (0, 0, 0), (cx + 3, cy + 4), 16)
    pygame.draw.circle(tela, cor_skin("bomba", COR_BOMBA), (cx, cy), 16)
    pygame.draw.circle(tela, (255, 255, 255), (cx - 6, cy - 6), 4)
    pygame.draw.line(tela, cor_skin("bomba_luz", COR_BOMBA_LUZ), (cx + 10, cy - 12), (cx + 19, cy - 24), 3)
    pygame.draw.circle(tela, cor_skin("bomba_luz", COR_BOMBA_LUZ), (cx + 22, cy - 27), max(3, brilho // 5))


def interpolar_posicao(atual, anterior, progresso):
    if anterior is None:
        return atual
    ax, ay = atual
    bx, by = anterior
    suavizado = progresso * progresso * (3 - 2 * progresso)
    return (
        int(bx + (ax - bx) * suavizado),
        int(by + (ay - by) * suavizado),
    )


def desenhar_cobra(cobra, direcao, viva, cobra_anterior=None, progresso=1.0):
    posicoes = []
    for indice, parte in enumerate(cobra):
        anterior = cobra_anterior[indice] if cobra_anterior and indice < len(cobra_anterior) else None
        posicoes.append(interpolar_posicao(parte, anterior, progresso))

    for indice, parte in enumerate(reversed(posicoes)):
        x, y = parte
        if indice == len(posicoes) - 1:
            continue
        rect = pygame.Rect(x + 3, y + 3, TAMANHO - 6, TAMANHO - 6)
        pygame.draw.rect(tela, (0, 0, 0), rect.move(3, 4), border_radius=12)
        if sprites["corpo"]:
            tela.blit(sprites["corpo"], (x, y))
        else:
            pygame.draw.rect(tela, cor_skin("secundaria", COR_VERDE_ESCURO), rect, border_radius=12)
            pygame.draw.rect(tela, cor_skin("principal", COR_VERDE), rect.inflate(-10, -10), border_radius=8)

    cabeca = posicoes[0]
    x, y = cabeca
    if sprites["cabeca"] and viva:
        tela.blit(sprites["cabeca"], (x - 11, y - 11))
        return

    rect = pygame.Rect(x + 2, y + 2, TAMANHO - 4, TAMANHO - 4)
    pygame.draw.rect(tela, (0, 0, 0), rect.move(3, 4), border_radius=14)
    pygame.draw.rect(tela, cor_skin("principal", COR_VERDE) if viva else COR_TEXTO_FRACO, rect, border_radius=14)
    pygame.draw.rect(tela, cor_skin("miolo", COR_CAB_SOL), rect.inflate(-16, -16), border_radius=8)

    dx, dy = direcao
    olho_a = (x + 13, y + 13)
    olho_b = (x + 27, y + 13)
    if dx < 0:
        olho_a, olho_b = (x + 13, y + 13), (x + 13, y + 27)
    elif dx > 0:
        olho_a, olho_b = (x + 27, y + 13), (x + 27, y + 27)
    elif dy > 0:
        olho_a, olho_b = (x + 13, y + 27), (x + 27, y + 27)
    pygame.draw.circle(tela, COR_PAINEL, olho_a, 4)
    pygame.draw.circle(tela, COR_PAINEL, olho_b, 4)


def desenhar_particulas(particulas):
    for p in particulas:
        pygame.draw.circle(tela, p["cor"], (int(p["x"]), int(p["y"])), max(1, int(p["vida"] / 6)))


def desenhar_painel_central(titulo, linhas, y=185):
    camada = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    camada.fill((2, 6, 23, 155))
    tela.blit(camada, (0, 0))

    painel = pygame.Rect(150, y, 500, 285)
    pygame.draw.rect(tela, (15, 23, 42), painel, border_radius=16)
    pygame.draw.rect(tela, cor_skin("principal", COR_VERDE), painel, 3, border_radius=16)

    titulo_render = fonte_msg.render(titulo, True, COR_TEXTO)
    tela.blit(titulo_render, titulo_render.get_rect(center=(LARGURA_TELA // 2, y + 55)))

    for indice, linha in enumerate(linhas):
        cor = COR_ALERTA if indice == 0 else COR_TEXTO_FRACO
        render = fonte_menu.render(linha, True, cor)
        tela.blit(render, render.get_rect(center=(LARGURA_TELA // 2, y + 115 + indice * 34)))


def criar_particulas(pos, cor):
    cx, cy = pos[0] + TAMANHO // 2, pos[1] + TAMANHO // 2
    novas = []
    for _ in range(16):
        angulo = random.uniform(0, math.tau)
        velocidade = random.uniform(1.5, 4)
        novas.append({
            "x": cx,
            "y": cy,
            "vx": math.cos(angulo) * velocidade,
            "vy": math.sin(angulo) * velocidade,
            "vida": random.randint(14, 28),
            "cor": cor,
        })
    return novas


def atualizar_particulas(particulas):
    vivas = []
    for p in particulas:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.08
        p["vida"] -= 1
        if p["vida"] > 0:
            vivas.append(p)
    return vivas


class Jogo:
    def __init__(self):
        self.estado = "menu"
        self.recorde = carregar_recorde()
        self.score = 0
        self.vidas = 3
        self.fase = 1
        self.pontos_vida = 0
        self.pausado = False
        self.particulas = []
        self.momento_item = 0
        self.fruta = None
        self.tipo_fruta = "vermelha"
        self.bomba = None
        self.tempo_lento_ate = 0
        self.escudo_ate = 0
        self.recorde_salvo = False
        self.cobra_anterior = []
        self.progresso_movimento = 1.0
        self.ultimo_passo = pygame.time.get_ticks()
        self.reiniciar_cobra()
        self.spawnar_itens()

    def iniciar_partida(self):
        self.reiniciar_tudo()
        self.estado = "jogando"
        self.pausado = False
        tocar_som("inicio")

    def reiniciar_cobra(self):
        centro_x = (COLUNAS // 2) * TAMANHO
        centro_y = ALTURA_PLACAR + (LINHAS // 2) * TAMANHO
        self.direcao = (TAMANHO, 0)
        self.proxima_direcao = self.direcao
        self.cobra = [
            (centro_x, centro_y),
            (centro_x - TAMANHO, centro_y),
            (centro_x - TAMANHO * 2, centro_y),
        ]
        self.cobra_anterior = list(self.cobra)
        self.progresso_movimento = 1.0
        self.ultimo_passo = pygame.time.get_ticks()

    def reiniciar_tudo(self):
        self.score = 0
        self.vidas = 3
        self.fase = 1
        self.pontos_vida = 0
        self.particulas = []
        self.tempo_lento_ate = 0
        self.escudo_ate = 0
        self.recorde_salvo = False
        self.reiniciar_cobra()
        self.spawnar_itens()

    def spawnar_itens(self):
        ocupadas = set(self.cobra)
        self.momento_item = pygame.time.get_ticks()
        self.fruta = None
        self.bomba = None
        if random.random() < CONFIG_FASES[self.fase]["chance_bomba"]:
            self.bomba = posicao_aleatoria(ocupadas)
            ocupadas.add(self.bomba)
            if random.random() < 0.55:
                self.fruta = posicao_aleatoria(ocupadas)
        else:
            self.fruta = posicao_aleatoria(ocupadas)
        self.tipo_fruta = random.choices(
            ["vermelha", "verde", "dourada", "azul", "roxa", "coracao"],
            weights=[48, 24, 8, 8, 7, 5],
            k=1,
        )[0]

    def finalizar_partida(self):
        self.estado = "game_over"
        if self.score > self.recorde:
            self.recorde = self.score
            salvar_recorde(self.recorde)
        self.recorde_salvo = True

    def escudo_ativo(self):
        return pygame.time.get_ticks() < self.escudo_ate

    def lento_ativo(self):
        return pygame.time.get_ticks() < self.tempo_lento_ate

    def poder_texto(self):
        agora = pygame.time.get_ticks()
        poderes = []
        if agora < self.escudo_ate:
            poderes.append(f"Escudo {math.ceil((self.escudo_ate - agora) / 1000)}s")
        if agora < self.tempo_lento_ate:
            poderes.append(f"Lento {math.ceil((self.tempo_lento_ate - agora) / 1000)}s")
        return " + ".join(poderes)

    def fps_atual(self):
        fps = CONFIG_FASES[self.fase]["fps"]
        if self.lento_ativo():
            fps = max(5, fps - 4)
        return fps

    def proteger_ou_morrer(self, bomba=False):
        if self.escudo_ativo():
            self.escudo_ate = 0
            tocar_som("escudo")
            self.particulas.extend(criar_particulas(self.cobra[0], (168, 85, 247)))
            self.reiniciar_cobra()
            self.spawnar_itens()
        else:
            self.perder_vida(bomba=bomba)

    def perder_vida(self, bomba=False):
        self.vidas -= 1
        self.pontos_vida = 0
        if bomba:
            tocar_som("bomba")
            self.score = max(0, self.score - 50)
            self.particulas.extend(criar_particulas(self.cobra[0], cor_skin("bomba", COR_BOMBA)))
        else:
            tocar_som("dano")
        if self.vidas > 0:
            self.reiniciar_cobra()
            self.spawnar_itens()
        else:
            tocar_som("game_over")
            self.finalizar_partida()

    def virar(self, nova):
        if self.vidas <= 0:
            return
        dx, dy = self.direcao
        ndx, ndy = nova
        if dx + ndx != 0 or dy + ndy != 0:
            if self.proxima_direcao != nova:
                tocar_som("virar")
                self.proxima_direcao = nova

    def avancar_fase_se_precisar(self):
        meta = CONFIG_FASES[self.fase]["meta_score"]
        if self.fase < FASE_MAXIMA and meta is not None and self.score >= meta:
            self.fase += 1
            tocar_som("fase")
            self.particulas.extend(criar_particulas(self.cobra[0], COR_ALERTA))

    def dar_passo(self):
        self.cobra_anterior = list(self.cobra)
        self.direcao = self.proxima_direcao
        cabeca_x, cabeca_y = self.cobra[0]
        dx, dy = self.direcao
        nova_cabeca = (cabeca_x + dx, cabeca_y + dy)

        bateu_parede = (
                nova_cabeca[0] < 0
                or nova_cabeca[0] >= LARGURA_TELA
                or nova_cabeca[1] < ALTURA_PLACAR
                or nova_cabeca[1] >= ALTURA_TELA
        )
        if bateu_parede or nova_cabeca in self.cobra:
            self.proteger_ou_morrer()
            return

        self.cobra.insert(0, nova_cabeca)

        if self.bomba and nova_cabeca == self.bomba:
            self.proteger_ou_morrer(bomba=True)
            return

        if self.fruta and nova_cabeca == self.fruta:
            pontos = FRUTAS.get(self.tipo_fruta, FRUTAS["vermelha"])["pontos"]
            self.score += pontos
            self.pontos_vida += pontos
            self.particulas.extend(criar_particulas(self.fruta, cor_skin("principal", COR_VERDE)))
            ganhou_vida = False
            if self.tipo_fruta == "dourada":
                tocar_som("dourada")
            elif self.tipo_fruta in ("azul", "roxa"):
                tocar_som("poder")
            elif self.tipo_fruta == "coracao":
                tocar_som("vida")
            else:
                tocar_som("mordida")
            if self.tipo_fruta == "azul":
                self.tempo_lento_ate = pygame.time.get_ticks() + 5000
            elif self.tipo_fruta == "roxa":
                self.escudo_ate = pygame.time.get_ticks() + 6000
            elif self.tipo_fruta == "coracao" and self.vidas < 6:
                self.vidas += 1
                ganhou_vida = True
            if self.pontos_vida >= 100 and self.vidas < 6:
                self.vidas += 1
                self.pontos_vida = 0
                ganhou_vida = True
            if ganhou_vida and self.tipo_fruta != "coracao":
                tocar_som("vida")
            self.avancar_fase_se_precisar()
            self.spawnar_itens()
        else:
            self.cobra.pop()

    def atualizar(self):
        self.particulas = atualizar_particulas(self.particulas)
        agora = pygame.time.get_ticks()

        if self.estado != "jogando" or self.pausado or self.vidas <= 0:
            self.ultimo_passo = agora
            self.progresso_movimento = 1.0
            self.cobra_anterior = list(self.cobra)
            return

        if agora - self.momento_item > CONFIG_FASES[self.fase]["tempo_item"]:
            self.spawnar_itens()

        intervalo = max(60, int(1000 / self.fps_atual()))
        tempo_desde_passo = agora - self.ultimo_passo

        if tempo_desde_passo >= intervalo:
            self.ultimo_passo = agora
            self.progresso_movimento = 0.0
            self.dar_passo()
        else:
            self.progresso_movimento = min(1.0, tempo_desde_passo / intervalo)

    def desenhar(self):
        tela.blit(FUNDO, (0, 0))
        pulso = pygame.time.get_ticks() / 260
        if self.fase == FASE_MAXIMA and self.vidas > 0:
            overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
            alpha = 22 + int(math.sin(pulso) * 10)
            overlay.fill((244, 63, 94, alpha))
            tela.blit(overlay, (0, 0))

        if self.fruta:
            desenhar_maca(self.fruta, self.tipo_fruta, pulso)
        if self.bomba:
            desenhar_bomba(self.bomba, pulso)
        desenhar_cobra(self.cobra, self.direcao, self.vidas > 0, self.cobra_anterior, self.progresso_movimento)
        desenhar_particulas(self.particulas)
        desenhar_hud(self.score, self.vidas, self.fase, self.pausado, self.recorde, self.poder_texto())

        if self.estado == "menu":
            desenhar_painel_central(
                "PYTHON CRASH",
                [
                    "ENTER para iniciar",
                    "TAB troca skin",
                    "1 Neon  2 Fogo  3 Classica  4 Gelo",
                    f"Recorde atual: {self.recorde}",
                ],
                180,
            )
        elif self.estado == "game_over":
            desenhar_painel_central(
                "FIM DE JOGO",
                [
                    f"Score final: {self.score}",
                    f"Recorde: {self.recorde}",
                    "ENTER para jogar de novo",
                    "TAB troca skin",
                ],
                190,
            )
        elif self.pausado:
            desenhar_painel_central(
                "PAUSA",
                [
                    "ESPAÇO para continuar",
                    "TAB troca skin",
                    "ENTER reinicia",
                    "ESC sai do jogo",
                ],
                190,
            )

def main():
    jogo = Jogo()
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key == pygame.K_RETURN:
                    if jogo.estado in ("menu", "game_over"):
                        jogo.iniciar_partida()
                    elif jogo.pausado:
                        jogo.iniciar_partida()
                elif evento.key == pygame.K_SPACE:
                    if jogo.estado == "jogando":
                        jogo.pausado = not jogo.pausado
                        tocar_som("pausa")
                elif evento.key == pygame.K_TAB:
                    trocar_skin()
                elif pygame.K_1 <= evento.key < pygame.K_1 + len(SKINS):
                    trocar_skin(evento.key - pygame.K_1)
                elif evento.key in (pygame.K_LEFT, pygame.K_a):
                    jogo.virar((-TAMANHO, 0))
                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    jogo.virar((TAMANHO, 0))
                elif evento.key in (pygame.K_UP, pygame.K_w):
                    jogo.virar((0, -TAMANHO))
                elif evento.key in (pygame.K_DOWN, pygame.K_s):
                    jogo.virar((0, TAMANHO))

        jogo.atualizar()
        jogo.desenhar()
        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
