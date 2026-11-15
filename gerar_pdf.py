"""Gera o Documento de Visão da Sprint 1 (Projeto ATALAIA) em PDF."""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                PageBreak, Table, TableStyle, Flowable, KeepTogether,
                                NextPageTemplate)
from reportlab.platypus.tableofcontents import TableOfContents

OUT = sys.argv[1]

F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("Arial", F + "arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-B", F + "arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-I", F + "ariali.ttf"))
pdfmetrics.registerFont(TTFont("Arial-BI", F + "arialbi.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Arial", normal="Arial", bold="Arial-B", italic="Arial-I", boldItalic="Arial-BI")

NAVY = colors.HexColor("#12355B")
ACCENT = colors.HexColor("#1F7A8C")
LIGHT = colors.HexColor("#E8F1F5")
GREY = colors.HexColor("#5F6B76")
LINE = colors.HexColor("#B8C4CC")
RED = colors.HexColor("#B3261E")
AMBER = colors.HexColor("#C77700")
GREEN = colors.HexColor("#2E7D32")

st = {}
st["body"] = ParagraphStyle("body", fontName="Arial", fontSize=10.5, leading=15, alignment=TA_JUSTIFY, spaceAfter=6)
st["bullet"] = ParagraphStyle("bullet", parent=st["body"], leftIndent=14, bulletIndent=4, spaceAfter=3)
st["h1"] = ParagraphStyle("h1", fontName="Arial-B", fontSize=16, leading=20, textColor=NAVY, spaceBefore=4, spaceAfter=10)
st["h2"] = ParagraphStyle("h2", fontName="Arial-B", fontSize=12.5, leading=16, textColor=ACCENT, spaceBefore=10, spaceAfter=6)
st["h2c"] = ParagraphStyle("h2c", parent=st["h2"])
st["cell"] = ParagraphStyle("cell", fontName="Arial", fontSize=9, leading=12, alignment=TA_LEFT)
st["cellb"] = ParagraphStyle("cellb", parent=st["cell"], fontName="Arial-B")
st["cellh"] = ParagraphStyle("cellh", parent=st["cell"], fontName="Arial-B", textColor=colors.white)
st["caption"] = ParagraphStyle("caption", fontName="Arial-I", fontSize=9, leading=12, textColor=GREY, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)
st["quote"] = ParagraphStyle("quote", parent=st["body"], fontName="Arial-I", leftIndent=16, rightIndent=16, textColor=NAVY,
                             borderColor=ACCENT, borderWidth=0, backColor=LIGHT, borderPadding=8, spaceBefore=6, spaceAfter=12)
st["toc1"] = ParagraphStyle("toc1", fontName="Arial", fontSize=10.5, leading=13.5, leftIndent=0)
st["toc2"] = ParagraphStyle("toc2", fontName="Arial", fontSize=9.5, leading=11.5, leftIndent=16, textColor=GREY)


class Doc(BaseDocTemplate):
    """Documento A4 com capa, cabeçalho/rodapé e sumário automático."""
    def __init__(self, fn, **kw):
        super().__init__(fn, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                         topMargin=22 * mm, bottomMargin=20 * mm,
                         title="Documento de Visão – Projeto ATALAIA",
                         author="Equipe do Projeto ATALAIA",
                         subject="Sprint 1 – Desafio Amazul", **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate("cover", [frame], onPage=self.cover),
                               PageTemplate("normal", [frame], onPage=self.decor)])

    def cover(self, c, d):
        w, h = A4
        c.saveState()
        c.setFillColor(NAVY)
        c.rect(0, h - 95 * mm, w, 95 * mm, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.rect(0, h - 98 * mm, w, 3 * mm, fill=1, stroke=0)
        c.restoreState()

    def decor(self, c, d):
        w, h = A4
        c.saveState()
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(20 * mm, h - 14 * mm, w - 20 * mm, h - 14 * mm)
        c.setFont("Arial", 8)
        c.setFillColor(GREY)
        c.drawString(20 * mm, h - 12 * mm, "Projeto ATALAIA – Documento de Visão")
        c.drawRightString(w - 20 * mm, h - 12 * mm, "Sprint 1 · Desafio Amazul")
        c.line(20 * mm, 14 * mm, w - 20 * mm, 14 * mm)
        c.drawRightString(w - 20 * mm, 9 * mm, "Página %d" % d.page)
        c.restoreState()

    def afterFlowable(self, f):
        if isinstance(f, Paragraph):
            s = f.style.name
            if s == "h1":
                self.notify("TOCEntry", (0, f.getPlainText(), self.page))
            elif s == "h2":
                self.notify("TOCEntry", (1, f.getPlainText(), self.page))


def P(t, s="body"):
    return Paragraph(t, st[s])


def bullets(items):
    return [Paragraph(i, st["bullet"], bulletText="•") for i in items]


def table(data, widths, header=True, zebra=True):
    """Cria uma tabela formatada; strings viram parágrafos com quebra de linha."""
    rows = []
    for r, row in enumerate(data):
        out = []
        for cidx, cell in enumerate(row):
            if isinstance(cell, str):
                style = "cellh" if (header and r == 0) else ("cellb" if cidx == 0 else "cell")
                out.append(Paragraph(cell, st[style]))
            else:
                out.append(cell)
        rows.append(out)
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    cmds = [("GRID", (0, 0), (-1, -1), 0.4, LINE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if header:
        cmds.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    if zebra:
        for i in range(1 if header else 0, len(rows)):
            if i % 2 == 0:
                cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(cmds))
    return t


class Drawing(Flowable):
    def __init__(self, w, h, fn):
        super().__init__()
        self.width, self.height, self.fn = w, h, fn

    def draw(self):
        self.fn(self.canv, self.width, self.height)


def box(c, x, y, w, h, text=None, fill=colors.white, stroke=GREY, size=7.5, bold=False,
        tcolor=colors.black, dash=False, align="center", radius=3):
    c.saveState()
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.8)
    if dash:
        c.setDash(3, 2)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    c.restoreState()
    if text:
        lines = text.split("\n")
        c.saveState()
        c.setFillColor(tcolor)
        c.setFont("Arial-B" if bold else "Arial", size)
        total = len(lines) * (size + 2)
        ty = y + h / 2 + total / 2 - size
        for ln in lines:
            if align == "center":
                c.drawCentredString(x + w / 2, ty, ln)
            else:
                c.drawString(x + 4, ty, ln)
            ty -= size + 2
        c.restoreState()


def arrow(c, x1, y1, x2, y2, color=GREY, label=None):
    import math
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(1)
    c.line(x1, y1, x2, y2)
    a = math.atan2(y2 - y1, x2 - x1)
    L = 5
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - L * math.cos(a - 0.4), y2 - L * math.sin(a - 0.4))
    p.lineTo(x2 - L * math.cos(a + 0.4), y2 - L * math.sin(a + 0.4))
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    if label:
        c.setFont("Arial-I", 6.5)
        c.drawString((x1 + x2) / 2 + 4, (y1 + y2) / 2 - 2, label)
    c.restoreState()


def txt(c, x, y, s, size=7, font="Arial", color=colors.black):
    c.saveState()
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, s)
    c.restoreState()


def tela_principal(c, W, H):
    """Wireframe de baixa fidelidade – Painel Operacional."""
    box(c, 0, 0, W, H, fill=colors.white, stroke=colors.black, radius=4)
    box(c, 0, H - 22, W, 22, fill=colors.HexColor("#DDDDDD"), stroke=colors.black, radius=0)
    txt(c, 8, H - 15, "ATALAIA  |  Painel Operacional", 8.5, "Arial-B")
    txt(c, W - 205, H - 15, "Turno: B   Operador: [nome]   14:32:05   Status: ONLINE", 7)
    box(c, 0, 0, 62, H - 22, fill=colors.HexColor("#EEEEEE"), stroke=colors.black, radius=0)
    for i, item in enumerate(["Painel", "Mapa", "Ocorrências", "Drones", "Sensores", "Missões", "Relatórios", "Admin"]):
        txt(c, 8, H - 40 - i * 16, ("> " if i == 0 else "  ") + item, 7, "Arial-B" if i == 0 else "Arial")
    kx, ky = 70, H - 56
    kw = (W - 70 - 8 - 3 * 6) / 4
    for i, (k, v) in enumerate([("Alertas ativos", "3"), ("Drones disponíveis", "2/3"),
                                ("Sensores online", "46/48"), ("Tempo médio verif.", "02:10")]):
        box(c, kx + i * (kw + 6), ky, kw, 28, fill=colors.white, stroke=GREY)
        txt(c, kx + i * (kw + 6) + 5, ky + 18, k, 6.5, color=GREY)
        txt(c, kx + i * (kw + 6) + 5, ky + 5, v, 10, "Arial-B")
    mx, my, mw, mh = 70, 92, W - 70 - 8 - 150, H - 22 - 92 - 42
    box(c, mx, my, mw, mh, fill=colors.HexColor("#F7F7F7"), stroke=colors.black)
    txt(c, mx + 5, my + mh - 11, "MAPA GEORREFERENCIADO DO SÍTIO", 7, "Arial-B")
    c.saveState()
    c.setStrokeColor(colors.black); c.setDash(4, 3); c.setLineWidth(1)
    c.rect(mx + 15, my + 15, mw - 30, mh - 38)
    c.setDash(2, 2); c.setStrokeColor(GREY)
    c.rect(mx + mw * 0.32, my + mh * 0.25, mw * 0.36, mh * 0.40)
    c.restoreState()
    txt(c, mx + mw * 0.34, my + mh * 0.25 + 4, "Área Vital (Zona 3)", 6.5, color=GREY)
    txt(c, mx + 19, my + 19, "Perímetro externo (Zona 1)", 6.5, color=GREY)
    import random
    random.seed(4)
    for i in range(14):
        sx = mx + 15 + (mw - 30) * i / 13
        c.circle(sx, my + mh - 23, 1.8, fill=1)
    for i in range(6):
        c.circle(mx + 15, my + 15 + (mh - 38) * i / 5, 1.8, fill=1)
    for (dx, dy, lab) in [(0.20, 0.55, "D1"), (0.75, 0.70, "D2")]:
        px, py = mx + mw * dx, my + mh * dy
        c.saveState(); c.setStrokeColor(colors.black)
        c.line(px - 6, py - 6, px + 6, py + 6); c.line(px - 6, py + 6, px + 6, py - 6)
        for ox, oy in [(-6, -6), (6, 6), (-6, 6), (6, -6)]:
            c.circle(px + ox, py + oy, 2.5)
        c.restoreState()
        txt(c, px + 9, py - 2, lab, 7, "Arial-B")
    ax, ay = mx + mw * 0.82, my + mh * 0.30
    c.saveState(); c.setStrokeColor(GREY); c.setDash(1, 2)
    c.line(mx + mw * 0.20, my + mh * 0.55, ax, ay); c.restoreState()
    c.saveState(); c.setStrokeColor(RED); c.setFillColor(RED); c.setLineWidth(1.4)
    c.circle(ax, ay, 9, fill=0); c.circle(ax, ay, 3, fill=1); c.restoreState()
    txt(c, ax - 75, ay - 21, "ALERTA #0142 – Zona 1 Leste", 6.5, "Arial-B", RED)
    txt(c, mx + 5, my + 4, "•  sensor     X  drone     O  alerta (vermelho)     - - -  limite de zona", 6.5, color=GREY)
    rx, rw = W - 8 - 144, 144
    box(c, rx, my, rw, mh, fill=colors.white, stroke=colors.black)
    txt(c, rx + 5, my + mh - 11, "FILA DE ALERTAS (por risco)", 7, "Arial-B")
    alerts = [("ALTO", RED, "#0142 Pessoa detectada", "Zona 1 Leste · 14:31", "Cerca + Câmera + IA 0,91"),
              ("MÉDIO", AMBER, "#0141 Veículo parado", "Acesso Norte · 14:20", "Câmera + IA 0,74"),
              ("BAIXO", GREEN, "#0140 Sensor offline", "S-17 · 13:58", "Falha técnica")]
    for i, (lvl, colr, t1, t2, t3) in enumerate(alerts):
        by = my + mh - 24 - (i + 1) * 46
        box(c, rx + 5, by, rw - 10, 42, fill=colors.white, stroke=GREY)
        c.saveState(); c.setFillColor(colr); c.rect(rx + 5, by, 4, 42, fill=1, stroke=0); c.restoreState()
        txt(c, rx + 13, by + 31, lvl + "  " + t1, 6.8, "Arial-B")
        txt(c, rx + 13, by + 20, t2, 6.5, color=GREY)
        txt(c, rx + 13, by + 9, t3, 6.5, color=GREY)
    txt(c, rx + 5, my + 6, "[ ver todas as ocorrências ]", 6.5, color=GREY)
    fx, fy, fw, fh = 70, 8, (W - 70 - 8) * 0.55, 78
    box(c, fx, fy, fw, fh, fill=colors.HexColor("#F0F0F0"), stroke=colors.black)
    c.saveState(); c.setStrokeColor(LINE); c.line(fx, fy, fx + fw, fy + fh); c.line(fx, fy + fh, fx + fw, fy); c.restoreState()
    txt(c, fx + 5, fy + fh - 10, "VÍDEO AO VIVO – Câmera C-08 / Drone D1 (RGB | Térmica)", 6.8, "Arial-B")
    c.saveState(); c.setStrokeColor(RED); c.setLineWidth(1.2)
    c.rect(fx + fw * 0.55, fy + 18, 22, 32); c.restoreState()
    txt(c, fx + fw * 0.55, fy + 52, "pessoa 0,91", 6.3, "Arial-B", RED)
    ax2 = fx + fw + 6
    aw = W - 8 - ax2
    box(c, ax2, fy, aw, fh, fill=colors.white, stroke=colors.black)
    txt(c, ax2 + 5, fy + fh - 10, "AÇÕES SOBRE O ALERTA #0142", 6.8, "Arial-B")
    bw = (aw - 15) / 2
    for i, b in enumerate(["Enviar drone p/ verificar", "Confirmar ameaça", "Marcar falso alarme", "Acionar equipe de resposta"]):
        bx = ax2 + 5 + (i % 2) * (bw + 5)
        byy = fy + fh - 34 - (i // 2) * 24
        box(c, bx, byy, bw, 19, b, fill=colors.HexColor("#EEEEEE"), stroke=colors.black, size=6.5)
    txt(c, ax2 + 5, fy + 5, "Toda ação exige justificativa e fica no registro de auditoria.", 6, "Arial-I", GREY)


def tela_ocorrencia(c, W, H):
    """Wireframe de baixa fidelidade – Detalhe da ocorrência."""
    box(c, 0, 0, W, H, fill=colors.white, stroke=colors.black, radius=4)
    box(c, 0, H - 22, W, 22, fill=colors.HexColor("#DDDDDD"), stroke=colors.black, radius=0)
    txt(c, 8, H - 15, "ATALAIA  |  Ocorrência #0142 – Intrusão no perímetro (Zona 1 Leste)", 8.5, "Arial-B")
    txt(c, W - 110, H - 15, "Status: EM VERIFICAÇÃO", 7, "Arial-B", AMBER)
    lw = W * 0.48
    box(c, 8, 8, lw, H - 38, fill=colors.white, stroke=GREY)
    txt(c, 14, H - 42, "EVIDÊNCIAS", 7, "Arial-B")
    for i, lab in enumerate(["C-08 · 14:31:02", "D1 térmica · 14:32:40", "D1 RGB · 14:32:55"]):
        bx = 14 + i * ((lw - 12) / 3)
        bwid = (lw - 12) / 3 - 6
        box(c, bx, H - 120, bwid, 70, fill=colors.HexColor("#F0F0F0"), stroke=GREY)
        c.saveState(); c.setStrokeColor(LINE); c.line(bx, H - 120, bx + bwid, H - 50); c.line(bx, H - 50, bx + bwid, H - 120); c.restoreState()
        txt(c, bx + 2, H - 130, lab, 6)
    txt(c, 14, H - 150, "LEITURAS DOS SENSORES", 7, "Arial-B")
    rows = [("14:30:58", "Sensor de vibração da cerca S-21", "disparo"),
            ("14:31:01", "Barreira infravermelha B-04", "interrompida"),
            ("14:31:02", "IA – câmera C-08", "pessoa (0,91)"),
            ("14:32:40", "IA – drone D1 térmica", "1 pessoa (0,95)")]
    for i, r in enumerate(rows):
        y = H - 166 - i * 13
        txt(c, 14, y, r[0], 6.5, color=GREY); txt(c, 58, y, r[1], 6.5); txt(c, lw - 52, y, r[2], 6.5, "Arial-B")
    txt(c, 14, H - 230, "ÍNDICE DE RISCO (fusão de sensores): 0,93 – ALTO", 7, "Arial-B", RED)
    c.saveState(); c.setFillColor(LINE); c.rect(14, H - 244, lw - 12, 7, fill=1, stroke=0)
    c.setFillColor(RED); c.rect(14, H - 244, (lw - 12) * 0.93, 7, fill=1, stroke=0); c.restoreState()
    txt(c, 14, 16, "Mini-mapa: posição do evento, rota do drone e zona afetada  [ abrir no mapa ]", 6.5, color=GREY)
    rx = lw + 16
    rw = W - rx - 8
    box(c, rx, 8, rw, H - 38, fill=colors.white, stroke=GREY)
    txt(c, rx + 6, H - 42, "LINHA DO TEMPO (registro de auditoria)", 7, "Arial-B")
    ev = ["14:30:58  Alarme da cerca S-21 recebido", "14:31:02  IA confirma pessoa na câmera C-08",
          "14:31:03  Alerta ALTO criado e exibido", "14:31:20  Operador assume o alerta",
          "14:31:25  Drone D1 enviado (missão automática)", "14:32:40  D1 sobre o ponto – vídeo ao vivo",
          "--:--:--  Aguardando decisão do operador"]
    for i, e in enumerate(ev):
        y = H - 60 - i * 15
        c.circle(rx + 10, y + 2.5, 2, fill=1 if i < 6 else 0)
        txt(c, rx + 17, y, e, 6.6, "Arial-I" if i == 6 else "Arial", GREY if i == 6 else colors.black)
    c.saveState(); c.setStrokeColor(GREY); c.line(rx + 10, H - 60 - 6 * 15 + 4, rx + 10, H - 58); c.restoreState()
    txt(c, rx + 6, H - 180, "DECISÃO DO OPERADOR", 7, "Arial-B")
    box(c, rx + 6, H - 215, rw - 12, 26, "Justificativa / observações (obrigatório)", fill=colors.white, stroke=GREY, size=6.5,
        tcolor=GREY, align="left")
    bw = (rw - 12 - 10) / 3
    for i, b in enumerate(["Confirmar ameaça", "Falso alarme", "Escalar ao gestor"]):
        box(c, rx + 6 + i * (bw + 5), H - 243, bw, 20, b, fill=colors.HexColor("#EEEEEE"), stroke=colors.black, size=6.5)
    txt(c, rx + 6, 34, "Classificação do falso alarme (animal, vegetação, clima, manutenção)", 6.3, color=GREY)
    txt(c, rx + 6, 22, "realimenta o modelo de IA e as regras de fusão.", 6.3, color=GREY)


def fluxo(c, W, H):
    """Fluxo geral de utilização (raias)."""
    lanes = [("Campo\n(sensores/drones)", colors.HexColor("#F3F6F8")),
             ("Sistema\nATALAIA (IA)", colors.HexColor("#E8F1F5")),
             ("Operador de\nmonitoramento", colors.HexColor("#F3F6F8")),
             ("Equipe de\nsegurança / gestor", colors.HexColor("#E8F1F5"))]
    lh = H / len(lanes)
    for i, (n, colr) in enumerate(lanes):
        y = H - (i + 1) * lh
        c.saveState(); c.setFillColor(colr); c.setStrokeColor(LINE); c.rect(0, y, W, lh, fill=1, stroke=1)
        c.setFillColor(NAVY); c.rect(0, y, 70, lh, fill=1, stroke=0); c.restoreState()
        lines = n.split("\n")
        for j, ln in enumerate(lines):
            txt(c, 5, y + lh / 2 + 3 - j * 9, ln, 6.8, "Arial-B", colors.white)

    def lane_y(i):
        return H - (i + 1) * lh + (lh - 34) / 2

    bw, bh = 50, 34
    step = (W - 76) / 7
    xs = [76 + k * step + (step - bw) / 2 for k in range(7)]
    n = {}
    n["A"] = (xs[0], lane_y(0), "1. Sensor ou\ncâmera detecta\no evento")
    n["B"] = (xs[1], lane_y(1), "2. IA classifica\ne funde os\nsinais")
    n["C"] = (xs[2], lane_y(1), "3. Gera alerta\ncom nível\nde risco")
    n["D"] = (xs[3], lane_y(2), "4. Operador\nanalisa as\nevidências")
    n["E"] = (xs[4], lane_y(0), "5. Drone faz\nvoo de\nverificação")
    n["F"] = (xs[5], lane_y(2), "6. Operador\nconfirma ou\ndescarta")
    n["G"] = (xs[6], lane_y(3), "7. Equipe\nresponde\nno local")
    n["H"] = (xs[6], lane_y(1), "8. Registro,\nrelatório e\naprendizado")
    for k, (x, y, t) in n.items():
        box(c, x, y, bw, bh, t, fill=colors.white, stroke=NAVY, size=6.2)

    def mid_r(k): x, y, _ = n[k]; return x + bw, y + bh / 2
    def mid_l(k): x, y, _ = n[k]; return x, y + bh / 2
    def mid_t(k): x, y, _ = n[k]; return x + bw / 2, y + bh
    def mid_b(k): x, y, _ = n[k]; return x + bw / 2, y

    arrow(c, *mid_r("A"), *mid_l("B"))
    arrow(c, *mid_r("B"), *mid_l("C"))
    arrow(c, *mid_r("C"), *mid_l("D"))
    arrow(c, *mid_r("D"), *mid_l("E"), label="solicita drone")
    arrow(c, *mid_r("E"), *mid_l("F"), label="vídeo ao vivo")
    arrow(c, *mid_r("F"), *mid_l("G"), label="confirma")
    arrow(c, *mid_r("F"), *mid_l("H"), label="descarta")
    arrow(c, *mid_t("G"), *mid_b("H"))


def arquitetura(c, W, H):
    """Diagrama das quatro camadas da solução."""
    cols = [("CAMPO", ["Drones com câmera\nRGB + térmica", "Câmeras fixas\n(CFTV)", "Sensores IoT de\nperímetro"]),
            ("BORDA (EDGE)", ["Gateway de borda\n(ex.: NVIDIA Jetson)", "Inferência de visão\ncomputacional", "Buffer local\n(operação offline)"]),
            ("CENTRAL", ["Motor de fusão e\níndice de risco", "API + regras de\nalerta + missões", "Banco de dados\ngeoespacial + auditoria"]),
            ("APRESENTAÇÃO", ["Painel operacional\n(web)", "Gestão de\nocorrências", "Relatórios e\nindicadores"])]
    cw = (W - 3 * 18) / 4
    for i, (title, items) in enumerate(cols):
        x = i * (cw + 18)
        box(c, x, 0, cw, H, fill=LIGHT, stroke=LINE)
        txt(c, x + 6, H - 13, title, 7, "Arial-B", NAVY)
        for j, it in enumerate(items):
            box(c, x + 8, H - 58 - j * 44, cw - 16, 34, it, fill=colors.white, stroke=ACCENT, size=6.8)
        if i < 3:
            arrow(c, x + cw + 2, H / 2, x + cw + 16, H / 2, color=NAVY)
    txt(c, 0, -12, "Rede privada e segmentada, sem dependência de internet; dados criptografados em trânsito (MQTT/TLS) e em repouso.", 6.8, "Arial-I", GREY)


def matriz(c, W, H):
    """Matriz de poder × interesse dos stakeholders."""
    box(c, 30, 20, W - 30, H - 20, fill=colors.white, stroke=GREY, radius=0)
    mx, my, mw, mh = 30, 20, W - 30, H - 20
    c.saveState(); c.setStrokeColor(LINE); c.line(mx + mw / 2, my, mx + mw / 2, my + mh); c.line(mx, my + mh / 2, mx + mw, my + mh / 2); c.restoreState()
    labels = [("Manter satisfeito", mx + 5, my + mh - 12), ("Gerenciar de perto", mx + mw / 2 + 5, my + mh - 12),
              ("Monitorar", mx + 5, my + 5), ("Manter informado", mx + mw / 2 + 5, my + 5)]
    for t, x, y in labels:
        txt(c, x, y, t, 7, "Arial-B", GREY)
    pts = [("Órgão regulador (ANSN/CNEN)", 0.30, 0.88), ("Gestores da instalação", 0.82, 0.90),
           ("Equipes de segurança", 0.80, 0.68), ("Operadores de monitoramento", 0.90, 0.60),
           ("Equipes de inspeção", 0.66, 0.36), ("Administradores do sistema", 0.60, 0.20),
           ("Autoridade aeronáutica (DECEA/ANAC)", 0.18, 0.66), ("Comunidade do entorno", 0.30, 0.22),
           ("Equipe de desenvolvimento", 0.72, 0.10)]
    for t, px, py in pts:
        x, y = mx + mw * px, my + mh * py
        c.saveState(); c.setFillColor(NAVY); c.circle(x, y, 3, fill=1, stroke=0); c.restoreState()
        txt(c, x + 5, y - 2, t, 6.6) if px < 0.7 else txt(c, x - 5 - pdfmetrics.stringWidth(t, "Arial", 6.6), y - 2, t, 6.6)
    txt(c, mx + mw / 2 - 25, 6, "INTERESSE  →", 7, "Arial-B", NAVY)
    c.saveState(); c.translate(18, my + mh / 2 - 25); c.rotate(90); c.setFont("Arial-B", 7); c.setFillColor(NAVY)
    c.drawString(0, 0, "PODER / INFLUÊNCIA  →"); c.restoreState()


def build():
    """Monta todas as seções do documento e gera o PDF (duas passagens para o sumário)."""
    doc = Doc(OUT)
    S = []
    W = doc.width

    S.append(Spacer(1, 18 * mm))
    S.append(Paragraph("SPRINT 1 · DESAFIO AMAZUL", ParagraphStyle("k", fontName="Arial-B", fontSize=10, textColor=colors.HexColor("#9CC9D6"), leading=14)))
    S.append(Spacer(1, 4))
    S.append(Paragraph("Documento de Visão e<br/>Definição da Solução", ParagraphStyle("t", fontName="Arial-B", fontSize=26, leading=31, textColor=colors.white)))
    S.append(Spacer(1, 8))
    S.append(Paragraph("<b>ATALAIA</b> – Plataforma de monitoramento inteligente e inspeção autônoma para a segurança física de instalações nucleares",
                       ParagraphStyle("s", fontName="Arial", fontSize=12, leading=16, textColor=colors.white)))
    S.append(Spacer(1, 38 * mm))
    S.append(P("Integrantes do grupo", "h2c"))
    membros = [["Nome completo", "RM", "Papel na Sprint"],
               ["Igor Mota Marran", "567823", "<b>Elaboração do Documento de Visão (responsável principal)</b>"],
               ["Kaue Souza Rodrigues", "567716", "Contexto do problema e pesquisa"],
               ["Dante Daher Garçon", "567727", "Análise de stakeholders"],
               ["Pedro Henrique Camacho de Alencar", "568071", "Definição da solução e arquitetura"],
               ["Gabriel Kenishi Furuzawa", "568245", "Definição do escopo"],
               ["Murylo Silva Amaral", "568241", "Protótipo conceitual"]]
    S.append(table(membros, [W * 0.40, W * 0.14, W * 0.46]))
    S.append(Spacer(1, 10))
    S.append(P("Repositório do projeto", "h2c"))
    S.append(P('<link href="https://github.com/IgorMarran/atalaia" color="#1F7A8C"><u>https://github.com/IgorMarran/atalaia</u></link>'))
    S.append(Spacer(1, 6))
    info = [["Disciplina", "Software Engineering"], ["Professor", "Leandro Ramos da Silva"],
            ["Empresa parceira", "Amazul – Amazônia Azul Tecnologias de Defesa S.A."],
            ["Versão do documento", "1.0 – novembro de 2026"]]
    S.append(table(info, [W * 0.35, W * 0.65], header=False))
    S.append(NextPageTemplate("normal"))
    S.append(PageBreak())

    S.append(Paragraph("Sumário", ParagraphStyle("hs", parent=st["h1"])))
    toc = TableOfContents()
    toc.levelStyles = [st["toc1"], st["toc2"]]
    toc.dotsMinLevel = 0
    S.append(toc)
    S.append(PageBreak())

    S.append(P("1. Introdução", "h1"))
    S.append(P("Este Documento de Visão apresenta a compreensão da equipe sobre o desafio proposto pela "
               "<b>Amazul – Amazônia Azul Tecnologias de Defesa S.A.</b> e define a visão inicial da solução que será "
               "desenvolvida ao longo do projeto. O desafio foi formulado da seguinte maneira:"))
    S.append(P("“Como utilizar drones, sensores, visão computacional e Inteligência Artificial para monitorar, inspecionar "
               "e identificar situações anômalas em ambientes críticos relacionados à segurança física de instalações nucleares?”", "quote"))
    S.append(P("Nesta primeira Sprint o foco não é a implementação técnica, mas sim o entendimento do problema: quem são os "
               "envolvidos, quais são suas necessidades, qual valor a solução precisa entregar e quais são os limites do que será "
               "construído. As decisões registradas aqui servirão de base para as próximas etapas de especificação de requisitos, "
               "modelagem e desenvolvimento."))
    S.append(P("1.1 Propósito do documento", "h2"))
    S.append(P("Alinhar equipe, professores e empresa parceira sobre <b>o que</b> será construído e <b>por quê</b>, antes de "
               "decidir <b>como</b>. O documento também funciona como referência de escopo: qualquer nova funcionalidade "
               "proposta nas Sprints seguintes deve ser comparada com a visão e o escopo aqui definidos."))
    S.append(P("1.2 Glossário", "h2"))
    gl = [["Termo", "Significado neste documento"],
          ["Segurança física (<i>security</i>)", "Proteção contra ações intencionais: intrusão, sabotagem, furto de material, vigilância hostil. É o foco do projeto."],
          ["Segurança nuclear (<i>safety</i>)", "Prevenção de acidentes de operação (radiação, reator). <b>Não</b> é o foco do projeto."],
          ["Situação anômala", "Qualquer evento que foge do padrão esperado para o local e horário: pessoa ou veículo em área proibida, cerca danificada, objeto abandonado, drone não autorizado etc."],
          ["Fusão de sensores", "Combinação de sinais de várias fontes (cerca, câmera, drone) para concluir se um evento é real com maior confiança do que uma fonte isolada."],
          ["Edge computing", "Processamento feito perto da fonte do dado (no próprio drone ou em um gateway local), sem depender de nuvem."],
          ["Human-in-the-loop", "Princípio em que a IA sugere, mas a decisão final sobre a resposta é sempre de uma pessoa."],
          ["Falso alarme", "Alerta gerado sem ameaça real (animal, vegetação, chuva, manutenção programada)."]]
    S.append(table(gl, [W * 0.28, W * 0.72]))

    S.append(PageBreak())
    S.append(P("2. Contexto do Problema", "h1"))
    S.append(P("2.1 A empresa parceira e o ambiente", "h2"))
    S.append(P("A Amazul é uma empresa pública vinculada ao Ministério da Defesa, por meio do Comando da Marinha, que atua no "
               "desenvolvimento de tecnologias para o Programa Nuclear da Marinha (PNM), o Programa de Desenvolvimento de Submarinos "
               "(PROSUB) e o Programa Nuclear Brasileiro. Seu trabalho envolve instalações e áreas consideradas <b>críticas</b>: "
               "locais que abrigam material nuclear, equipamentos sensíveis e conhecimento estratégico para o país."))
    S.append(P("Instalações desse tipo costumam ocupar grandes áreas, com perímetros extensos, vegetação, vias internas, edifícios de "
               "diferentes níveis de sensibilidade e operação 24 horas por dia, 7 dias por semana. A proteção física desses sítios "
               "segue o modelo de <b>zonas concêntricas</b> recomendado pela Agência Internacional de Energia Atômica (AIEA): "
               "área controlada, área protegida e área vital, cada uma com controles progressivamente mais rígidos."))
    S.append(P("2.2 Qual problema de segurança está sendo tratado", "h2"))
    S.append(P("A doutrina de proteção física se baseia em três funções: <b>detectar</b> uma ação hostil, <b>retardar</b> o agressor "
               "(barreiras) e <b>responder</b> com a força de segurança antes que o objetivo seja alcançado. A eficácia do sistema depende "
               "de a detecção e a avaliação acontecerem rápido o suficiente para que a resposta chegue a tempo."))
    S.append(P("O problema central identificado pela equipe é que <b>a etapa de detecção e avaliação ainda depende fortemente "
               "da atenção humana sobre muitas fontes ao mesmo tempo</b>. Na prática, isso gera quatro dificuldades:"))
    S.extend(bullets([
        "<b>Sobrecarga de informação:</b> operadores precisam acompanhar dezenas de câmeras e sensores; a atenção humana cai depois de "
        "pouco tempo de observação contínua de monitores, o que aumenta a chance de um evento real passar despercebido.",
        "<b>Excesso de falsos alarmes:</b> sensores de perímetro disparam com animais, vento, chuva e vegetação. Muitos alarmes falsos "
        "levam à “fadiga de alarme”, e o operador passa a desconfiar do sistema.",
        "<b>Pontos cegos e demora na verificação:</b> câmeras fixas não cobrem todo o perímetro; quando um alarme dispara em uma área "
        "sem visão, é preciso deslocar uma equipe até o local só para confirmar o que aconteceu.",
        "<b>Rondas e inspeções manuais:</b> inspeções de cercas, portões e áreas remotas são feitas a pé ou de viatura, consomem tempo, "
        "são pouco frequentes e geram registros em papel ou planilhas difíceis de auditar."]))
    S.append(P("2.3 Riscos e situações anômalas que podem ocorrer", "h2"))
    S.append(P("A tabela a seguir resume as situações anômalas que a equipe considera relevantes para o contexto, com a forma "
               "como poderiam ser percebidas por tecnologia."))
    riscos = [["Situação anômala", "Exemplo", "Como pode ser percebida", "Gravidade"],
              ["Intrusão no perímetro", "Pessoa pula ou corta a cerca à noite", "Sensor de vibração na cerca + câmera térmica + IA", "Alta"],
              ["Presença em área restrita", "Pessoa sem autorização perto de um prédio sensível", "Visão computacional com regra de zona (geofence) e horário", "Alta"],
              ["Veículo suspeito", "Carro parado por muito tempo junto ao perímetro externo", "Detecção de veículo + tempo de permanência", "Média"],
              ["Objeto abandonado", "Mochila ou pacote deixado perto de portão", "Comparação de imagens ao longo do tempo", "Alta"],
              ["Drone não autorizado", "Drone de terceiros sobrevoando o sítio", "Câmeras / sensores de RF (evolução futura)", "Alta"],
              ["Dano à barreira física", "Cerca rompida, portão aberto, iluminação apagada", "Inspeção autônoma por drone + comparação com voo anterior", "Média"],
              ["Vigilância hostil", "Mesma pessoa ou veículo observando o local em dias diferentes", "Padrões de recorrência (sem identificação pessoal)", "Média"],
              ["Falha do próprio sistema", "Sensor offline, câmera obstruída", "Monitoramento de saúde dos dispositivos", "Média"]]
    S.append(table(riscos, [W * 0.20, W * 0.28, W * 0.38, W * 0.14]))
    S.append(P("2.4 Como tecnologias emergentes podem ajudar", "h2"))
    tec = [["Tecnologia", "Contribuição para o problema"],
           ["Drones autônomos", "Cobrem pontos cegos, chegam ao local de um alarme em poucos minutos e fazem rondas e inspeções programadas com registro georreferenciado."],
           ["Sensores IoT", "Dão cobertura contínua e de baixo custo ao perímetro (vibração, infravermelho, abertura de portão) e informam a própria saúde."],
           ["Visão computacional", "Identifica automaticamente pessoas, veículos e objetos em vídeo RGB e térmico, inclusive à noite, reduzindo a carga sobre o operador."],
           ["Inteligência Artificial", "Funde os sinais de várias fontes, calcula um índice de risco, prioriza alertas e aprende com falsos alarmes classificados pelos operadores."],
           ["Edge computing", "Processa vídeo no local, com baixa latência e sem enviar imagens sensíveis para fora da instalação."],
           ["Geolocalização", "Posiciona cada evento, sensor e drone em um mapa do sítio e permite regras por zona (geofencing)."],
           ["Dashboards operacionais", "Concentram em uma única tela o que importa agora, com evidências e ações, em vez de dezenas de monitores."]]
    S.append(table(tec, [W * 0.24, W * 0.76]))
    S.append(P("2.5 Impacto esperado para a operação", "h2"))
    S.append(P("Com a solução, a equipe de segurança deixa de “olhar tudo o tempo todo” e passa a <b>atuar sobre alertas já "
               "filtrados, priorizados e acompanhados de evidências</b>. O tempo entre o disparo de um alarme e a confirmação visual "
               "do que está acontecendo cai de dezenas de minutos (deslocamento de uma equipe) para poucos minutos (voo do drone). "
               "Além disso, toda ocorrência passa a ter um registro completo e auditável, o que facilita a prestação de contas aos "
               "órgãos reguladores e a melhoria contínua dos procedimentos."))

    S.append(PageBreak())
    S.append(P("3. Objetivos da Solução", "h1"))
    S.append(P("3.1 Objetivo geral", "h2"))
    S.append(P("Desenvolver uma plataforma que integre drones, sensores IoT, visão computacional e Inteligência Artificial para "
               "<b>detectar, verificar, priorizar e registrar situações anômalas</b> no perímetro e nas áreas restritas de instalações "
               "nucleares, apoiando a decisão dos operadores de segurança sem substituí-los."))
    S.append(P("3.2 Objetivos específicos", "h2"))
    S.extend(bullets([
        "<b>OE1</b> – Detectar automaticamente pessoas e veículos em zonas restritas a partir de vídeo RGB e térmico.",
        "<b>OE2</b> – Combinar sinais de sensores de perímetro e câmeras para reduzir falsos alarmes.",
        "<b>OE3</b> – Enviar automaticamente um drone para verificar visualmente o local de um alarme.",
        "<b>OE4</b> – Executar rondas e inspeções programadas do perímetro com drones, comparando o estado atual com o anterior.",
        "<b>OE5</b> – Apresentar alertas priorizados por risco em um painel operacional com mapa georreferenciado.",
        "<b>OE6</b> – Registrar cada ocorrência de ponta a ponta (evidências, decisões e justificativas) em trilha de auditoria.",
        "<b>OE7</b> – Gerar relatórios e indicadores para gestores e para prestação de contas a órgãos reguladores."]))
    S.append(P("3.3 Metas mensuráveis (a validar no protótipo)", "h2"))
    S.append(P("As metas abaixo são hipóteses iniciais da equipe e serão validadas com a Amazul e testadas em ambiente simulado."))
    metas = [["Indicador", "Meta inicial", "Como medir"],
             ["Tempo entre alarme e confirmação visual", "≤ 3 minutos", "Diferença entre o horário do alarme e o primeiro vídeo do drone no local"],
             ["Taxa de detecção de pessoas (IA)", "≥ 90% em cenário de teste", "Conjunto de vídeos de teste com eventos rotulados"],
             ["Redução de falsos alarmes", "≥ 50% em relação a um sensor isolado", "Comparação entre alertas com e sem fusão de sensores"],
             ["Ocorrências com registro completo", "100%", "Ocorrências com evidência, decisão e justificativa preenchidas"],
             ["Tempo para o operador entender um alerta", "≤ 30 segundos", "Teste de usabilidade com o protótipo"]]
    S.append(table(metas, [W * 0.34, W * 0.24, W * 0.42]))

    S.append(PageBreak())
    S.append(P("4. Stakeholders", "h1"))
    S.append(P("Foram mapeados os principais envolvidos no projeto, com seu papel, suas necessidades e a forma como a solução os atende."))
    sh = [["Stakeholder", "Papel", "Principais necessidades", "Como a solução atende"],
          ["Operadores de monitoramento", "Acompanham câmeras e alarmes na central de segurança e fazem a primeira avaliação de cada evento.",
           "Menos falsos alarmes; ver rapidamente o que está acontecendo; tela clara; registrar ações sem burocracia.",
           "Alertas priorizados com evidências, vídeo do drone sob demanda, ações em um clique e registro automático."],
          ["Equipes de segurança (resposta)", "Força que se desloca ao local para conter uma ameaça.",
           "Saber exatamente onde e o que é a ameaça antes de chegar; acionamento rápido.",
           "Localização no mapa, imagens atualizadas pelo drone e acionamento direto pelo painel."],
          ["Gestores da instalação", "Responsáveis pela segurança do sítio, pelos recursos e pelo cumprimento das normas.",
           "Visão consolidada; indicadores de desempenho; justificar investimentos; evidências para auditorias.",
           "Relatórios por período, indicadores (tempo de resposta, falsos alarmes) e histórico completo."],
          ["Equipes de inspeção", "Verificam periodicamente cercas, portões, iluminação e barreiras.",
           "Inspeções mais frequentes e seguras em áreas remotas; registro padronizado.",
           "Missões de inspeção programadas por drone, com fotos georreferenciadas e comparação com a inspeção anterior."],
          ["Órgãos reguladores (ANSN / CNEN)", "Fiscalizam e licenciam as instalações e exigem um sistema de proteção física adequado.",
           "Rastreabilidade; registros íntegros; conformidade com normas de proteção física.",
           "Trilha de auditoria inviolável e relatórios exportáveis por ocorrência e por período."],
          ["Administradores do sistema", "Configuram usuários, permissões, zonas, sensores, drones e regras de alerta.",
           "Configuração simples; controle de acesso; monitorar a saúde do sistema.",
           "Módulo de administração com perfis de acesso, cadastro de dispositivos e painel de saúde."],
          ["Autoridade aeronáutica (DECEA / ANAC)", "Regula o uso do espaço aéreo e a operação de drones.",
           "Voos registrados e dentro das regras.",
           "Rotas e limites de voo configuráveis; registro de todas as missões."],
          ["Amazul (empresa parceira)", "Propõe o desafio e valida a aderência da solução à realidade das instalações.",
           "Solução viável, segura e alinhada às práticas do setor.",
           "Documentação, protótipo e validações a cada Sprint."]]
    S.append(table(sh, [W * 0.18, W * 0.25, W * 0.29, W * 0.28]))
    S.append(Spacer(1, 6))
    S.append(P("4.1 Matriz de poder × interesse", "h2"))
    S.append(P("A matriz orienta como a equipe vai se relacionar com cada grupo: operadores, equipes de segurança e gestores serão "
               "envolvidos de perto (validação do protótipo); reguladores e autoridade aeronáutica impõem restrições que precisam ser "
               "respeitadas desde o início."))
    S.append(KeepTogether([Drawing(W, 200, matriz), P("Figura 1 – Matriz de poder × interesse dos stakeholders.", "caption")]))
    S.append(P("4.2 Personas principais", "h2"))
    per = [["Persona", "Perfil", "Frase que resume a dor"],
           ["Carla, operadora de monitoramento", "12 horas de turno, 30 câmeras e 48 sensores para acompanhar; recebe dezenas de alarmes por noite.",
            "“A maioria dos alarmes é bicho ou vento. Quando aparece um de verdade, tenho medo de não perceber.”"],
           ["Roberto, gestor de segurança", "Responde pela proteção física do sítio e presta contas a auditorias e à direção.",
            "“Preciso provar que reagimos rápido e bem, mas os registros estão espalhados em papel e planilhas.”"]]
    S.append(table(per, [W * 0.24, W * 0.38, W * 0.38]))

    S.append(PageBreak())
    S.append(P("5. Descrição da Solução Proposta", "h1"))
    S.append(P("5.1 Nome da solução", "h2"))
    S.append(P("<b>ATALAIA</b> – Plataforma de monitoramento inteligente e inspeção autônoma. “Atalaia” é a torre de vigia ou a "
               "sentinela que observa do alto: representa exatamente o papel dos drones e da IA na proposta, ampliar o alcance da "
               "visão da equipe de segurança."))
    S.append(P("5.2 Problema que será resolvido", "h2"))
    S.append(P("A ATALAIA resolve a dificuldade de <b>detectar e avaliar rapidamente, com confiança, situações anômalas em grandes "
               "perímetros</b>, reduzindo a dependência de observação humana contínua, os falsos alarmes e o tempo para confirmar "
               "visualmente um evento, além de garantir o registro auditável de todas as ocorrências."))
    S.append(P("5.3 Declaração de visão", "h2"))
    S.append(P("<b>Para</b> operadores e gestores de segurança de instalações nucleares, <b>que</b> precisam detectar e avaliar ameaças "
               "em perímetros extensos com muitas fontes de informação, <b>a ATALAIA é</b> uma plataforma de monitoramento inteligente "
               "<b>que</b> combina sensores, câmeras, drones e IA para entregar alertas confiáveis, verificados e registrados. "
               "<b>Diferente</b> de sistemas de CFTV e alarmes isolados, <b>nossa solução</b> funde os sinais, envia um drone para "
               "confirmar o evento automaticamente e mantém o operador no controle de todas as decisões.", "quote"))
    S.append(P("5.4 Principais funcionalidades", "h2"))
    func = [["#", "Funcionalidade", "Descrição"],
            ["F1", "Detecção por visão computacional", "Identifica pessoas, veículos e objetos em vídeo de câmeras fixas e de drones (RGB e térmico)."],
            ["F2", "Integração de sensores IoT", "Recebe eventos de sensores de perímetro (vibração de cerca, barreira infravermelha, abertura de portão) e o estado de cada dispositivo."],
            ["F3", "Fusão de sinais e índice de risco", "Combina as fontes, considera zona e horário e calcula um nível de risco (baixo, médio, alto) para cada evento."],
            ["F4", "Alertas automáticos priorizados", "Gera alertas com evidências e os ordena por risco no painel; alertas altos têm destaque visual e sonoro."],
            ["F5", "Drone de verificação", "Ao surgir um alerta, propõe ou dispara uma missão para o drone mais próximo ir ao local e transmitir vídeo ao vivo."],
            ["F6", "Rondas e inspeções programadas", "Missões periódicas no perímetro; compara imagens com a ronda anterior para apontar mudanças (cerca rompida, portão aberto)."],
            ["F7", "Painel operacional georreferenciado", "Mapa do sítio com zonas, sensores, drones e alertas em tempo real, indicadores e vídeo."],
            ["F8", "Gestão e registro de ocorrências", "Linha do tempo de cada ocorrência, decisão do operador com justificativa obrigatória e trilha de auditoria."],
            ["F9", "Relatórios e indicadores", "Relatórios por período e por ocorrência; tempo de resposta, falsos alarmes, disponibilidade dos dispositivos."],
            ["F10", "Administração", "Cadastro de usuários e perfis, zonas, sensores, drones, rotas e regras de alerta."]]
    S.append(table(func, [W * 0.07, W * 0.30, W * 0.63]))
    S.append(P("5.5 Visão geral da arquitetura", "h2"))
    S.append(P("A arquitetura é organizada em quatro camadas. O processamento pesado de vídeo acontece na borda, perto das câmeras e "
               "drones; a camada central faz a fusão, as regras e o armazenamento; e a camada de apresentação entrega o painel aos usuários."))
    S.append(KeepTogether([Spacer(1, 4), Drawing(W, 165, arquitetura), Spacer(1, 14),
                           P("Figura 2 – Visão conceitual das camadas da solução.", "caption")]))
    S.append(P("5.6 Tecnologias que poderão ser utilizadas", "h2"))
    tecs = [["Área", "Opções consideradas (a confirmar nas próximas Sprints)"],
            ["Drones", "Multirrotores com câmera RGB + térmica e estação de pouso e recarga automática (<i>drone-in-a-box</i>); PX4/ArduPilot com protocolo MAVLink; simulação em Gazebo para o protótipo."],
            ["Sensores IoT", "Sensores de vibração para cerca, barreiras infravermelhas, sensores de abertura, sensores de presença; comunicação por MQTT (e LoRaWAN para áreas remotas)."],
            ["Visão computacional", "Modelos de detecção de objetos da família YOLO, rastreamento de múltiplos objetos (ex.: ByteTrack), OpenCV; treinamento com conjuntos de dados públicos RGB e térmicos."],
            ["Inteligência Artificial", "Fusão de sinais por regras ponderadas evoluindo para modelo de aprendizado de máquina; detecção de anomalias em padrões de tempo e local; aprendizado com falsos alarmes rotulados."],
            ["Edge computing", "Gateways embarcados com GPU (ex.: NVIDIA Jetson) executando inferência com baixa latência e operação offline."],
            ["Geolocalização", "GNSS nos drones, mapa do sítio em coordenadas, PostGIS para consultas espaciais e geofencing; Leaflet ou OpenLayers no painel."],
            ["Back-end e dados", "Python (FastAPI), PostgreSQL + PostGIS, broker MQTT, WebSocket para atualizações em tempo real, armazenamento de evidências com hash para garantir integridade."],
            ["Front-end", "Aplicação web (React) com mapa, fila de alertas, vídeo e relatórios."],
            ["Segurança da solução", "Rede isolada, autenticação com perfis de acesso, criptografia em trânsito e em repouso, registro de todas as ações."]]
    S.append(table(tecs, [W * 0.22, W * 0.78]))
    S.append(P("5.7 Diferenciais da proposta", "h2"))
    S.extend(bullets([
        "<b>Verificação automática por drone:</b> o alarme não fica apenas na tela; um drone vai até o local e mostra o que está acontecendo, "
        "reduzindo o tempo de avaliação sem expor pessoas.",
        "<b>Fusão de sensores contra falsos alarmes:</b> um evento só vira alerta alto quando fontes diferentes concordam, o que aumenta a confiança do operador.",
        "<b>Humano no controle (<i>human-in-the-loop</i>):</b> a IA sugere e prioriza, mas toda decisão de resposta é tomada e justificada por uma pessoa.",
        "<b>IA que aprende com a operação:</b> cada falso alarme classificado pelo operador (animal, vegetação, clima) realimenta o modelo.",
        "<b>Processamento local e privacidade:</b> o vídeo é analisado na própria instalação, sem nuvem, e o sistema não faz reconhecimento facial.",
        "<b>Trilha de auditoria pronta para o regulador:</b> evidências com hash de integridade e linha do tempo completa de cada ocorrência.",
        "<b>Inspeção com comparação temporal:</b> as rondas por drone não apenas filmam, mas apontam o que mudou desde a última inspeção."]))

    S.append(Spacer(1, 8))
    S.append(P("6. Benefícios Esperados", "h1"))
    ben = [["Dimensão", "Benefício", "Principal beneficiado"],
           ["Segurança", "Detecção mais rápida e confiável de intrusões; menos eventos reais despercebidos.", "Instalação, equipes de segurança"],
           ["Eficiência operacional", "Menos falsos alarmes e menos deslocamentos desnecessários; operador concentra a atenção no que importa.", "Operadores, equipes de resposta"],
           ["Tempo de resposta", "Confirmação visual em minutos com o drone, antes de enviar uma equipe.", "Equipes de segurança"],
           ["Segurança das pessoas", "O drone é o primeiro a chegar em áreas remotas ou de risco, e não um vigilante.", "Equipes de segurança e inspeção"],
           ["Cobertura", "Eliminação de pontos cegos e inspeções mais frequentes do perímetro.", "Equipes de inspeção"],
           ["Conformidade", "Registros completos, íntegros e exportáveis para auditorias e fiscalizações.", "Gestores, órgãos reguladores"],
           ["Gestão", "Indicadores objetivos para avaliar o desempenho e planejar melhorias e investimentos.", "Gestores"],
           ["Melhoria contínua", "Base histórica de ocorrências que permite ajustar regras, rotas e o próprio modelo de IA.", "Gestores, administradores"]]
    S.append(table(ben, [W * 0.2, W * 0.52, W * 0.28]))

    S.append(Spacer(1, 6))
    S.append(P("7. Escopo", "h1"))
    S.append(P("Para manter a proposta viável dentro do projeto, o escopo foi delimitado ao <b>perímetro e às áreas externas</b> de uma "
               "instalação, usando <b>dados e ambientes simulados</b> no protótipo."))
    S.append(P("7.1 Dentro do escopo – o que o sistema fará", "h2"))
    dentro = [["#", "O sistema fará", "Funcionalidade"],
              ["D1", "Detectar invasões em áreas restritas e no perímetro, a partir de câmeras e sensores.", "F1, F2"],
              ["D2", "Monitorar o perímetro de forma contínua e com rondas programadas por drone.", "F2, F6"],
              ["D3", "Gerar alertas automáticos classificados por nível de risco.", "F3, F4"],
              ["D4", "Enviar um drone para verificação visual do local de um alerta.", "F5"],
              ["D5", "Exibir informações em painel operacional com mapa, alertas, vídeo e indicadores.", "F7"],
              ["D6", "Registrar ocorrências com evidências, decisões e justificativas (trilha de auditoria).", "F8"],
              ["D7", "Emitir relatórios e indicadores para gestores e reguladores.", "F9"],
              ["D8", "Permitir configuração de usuários, perfis, zonas, dispositivos e regras.", "F10"],
              ["D9", "Monitorar a saúde dos dispositivos (sensor offline, bateria do drone, câmera obstruída).", "F2, F7"]]
    S.append(table(dentro, [W * 0.07, W * 0.75, W * 0.18]))
    S.append(P("7.2 Fora do escopo – o que o sistema não fará", "h2"))
    fora = [["#", "O sistema não fará", "Motivo"],
            ["N1", "Neutralizar ameaças ou realizar qualquer ação de contenção física (incluindo derrubar drones invasores).", "Responsabilidade exclusiva da força de segurança; envolve riscos legais e operacionais."],
            ["N2", "Tomar decisões de resposta de forma autônoma.", "Princípio <i>human-in-the-loop</i>: a IA apenas recomenda."],
            ["N3", "Reconhecimento facial ou identificação nominal de pessoas.", "Privacidade (LGPD) e complexidade; o foco é detectar a presença, não identificar quem é."],
            ["N4", "Monitorar radiação ou parâmetros de segurança nuclear operacional (<i>safety</i>).", "O desafio trata de segurança física (<i>security</i>)."],
            ["N5", "Substituir o controle de acesso (catracas, crachás, biometria) da instalação.", "Já existe nas instalações; integração pode ser avaliada no futuro."],
            ["N6", "Monitorar o interior de edifícios e da área do reator.", "O escopo inicial é o perímetro e as áreas externas."],
            ["N7", "Proteger a rede industrial da planta (cibersegurança de sistemas de controle).", "Tema distinto e altamente especializado."],
            ["N8", "Projetar ou fabricar drones e sensores.", "Serão usados equipamentos e simuladores existentes no mercado."],
            ["N9", "Integrar-se a sistemas reais ou classificados da Amazul durante o projeto.", "O protótipo usará dados simulados e conjuntos de dados públicos."]]
    S.append(table(fora, [W * 0.07, W * 0.50, W * 0.43]))
    S.append(P("7.3 Premissas e restrições", "h2"))
    S.extend(bullets([
        "<b>Premissa:</b> o protótipo será validado em ambiente simulado (drone em simulador e vídeos de teste), pois não haverá acesso a uma instalação real.",
        "<b>Premissa:</b> a instalação dispõe de rede local e energia para câmeras, sensores, gateways e estações de pouso dos drones.",
        "<b>Restrição:</b> a operação real de drones depende de autorização do DECEA/ANAC e das regras de voo da instalação.",
        "<b>Restrição:</b> dados e imagens sensíveis não podem sair da instalação; a solução deve funcionar sem internet.",
        "<b>Restrição:</b> o tratamento de imagens de pessoas deve respeitar a LGPD e as políticas internas de segurança da informação."]))
    S.append(P("7.4 Principais riscos do projeto", "h2"))
    rp = [["Risco", "Impacto", "Mitigação"],
          ["Falta de dados reais de instalações nucleares para treinar a IA", "Alto", "Usar conjuntos de dados públicos (RGB e térmicos) e vídeos gravados pela equipe em cenário semelhante."],
          ["Escopo crescer além da capacidade da equipe", "Alto", "Seguir a lista de “fora do escopo” e priorizar D1–D6 como MVP."],
          ["Dificuldade em operar drones reais", "Médio", "Usar simulação (PX4 + Gazebo) e, se possível, drone pequeno em área aberta autorizada."],
          ["Desempenho da IA abaixo da meta", "Médio", "Combinar IA com sensores (fusão) e manter decisão humana."]]
    S.append(table(rp, [W * 0.38, W * 0.12, W * 0.50]))

    S.append(PageBreak())
    S.append(P("8. Protótipo Conceitual (Baixa Fidelidade)", "h1"))
    S.append(P("O protótipo a seguir é um esboço de baixa fidelidade, com o objetivo de mostrar a organização das informações e o fluxo de "
               "uso, não o acabamento visual. Os dados exibidos são fictícios."))
    S.append(P("8.1 Tela principal – Painel Operacional", "h2"))
    S.append(Drawing(W, 330, tela_principal))
    S.append(P("Figura 3 – Wireframe da tela principal (Painel Operacional).", "caption"))
    S.append(P("<b>Elementos da tela:</b> (1) barra superior com turno, operador e status do sistema; (2) menu lateral com os módulos; "
               "(3) indicadores do momento; (4) mapa georreferenciado com zonas, sensores, drones e alertas; (5) fila de alertas ordenada "
               "por risco, mostrando quais fontes confirmaram cada evento; (6) vídeo ao vivo com a detecção da IA destacada; "
               "(7) ações sobre o alerta selecionado."))
    S.append(PageBreak())
    S.append(P("8.2 Tela de detalhe da ocorrência", "h2"))
    S.append(P("Ao abrir um alerta, o operador vê todas as evidências reunidas, a linha do tempo e registra a decisão com justificativa."))
    S.append(Drawing(W, 290, tela_ocorrencia))
    S.append(P("Figura 4 – Wireframe da tela de detalhe da ocorrência.", "caption"))
    S.append(P("8.3 Fluxo geral de utilização", "h2"))
    S.append(P("O fluxo mostra o caminho de um evento desde a detecção até o registro final, destacando a participação de cada ator."))
    S.append(KeepTogether([Drawing(W, 230, fluxo), P("Figura 5 – Fluxo geral de utilização da ATALAIA.", "caption")]))
    S.append(P("<b>Fluxo alternativo – ronda programada:</b> o administrador cadastra a rota → o drone executa a missão no horário definido → "
               "a IA compara as imagens com a ronda anterior → mudanças relevantes (cerca rompida, portão aberto) geram alertas que seguem "
               "o mesmo fluxo a partir do passo 3."))
    S.append(P("8.4 Mapa das funcionalidades por perfil", "h2"))
    mapa = [["Perfil", "Telas e funcionalidades acessadas"],
            ["Operador de monitoramento", "Painel operacional, detalhe da ocorrência, envio de drone, registro de decisão."],
            ["Equipe de segurança", "Notificação de acionamento com localização e imagens; registro do resultado no local."],
            ["Equipe de inspeção", "Agenda de rondas, resultados das inspeções e comparação de imagens."],
            ["Gestor", "Relatórios, indicadores, histórico de ocorrências e aprovação de escalonamentos."],
            ["Administrador", "Usuários e perfis, zonas e mapa, dispositivos, rotas e regras de alerta, saúde do sistema."],
            ["Regulador (via gestor)", "Relatórios exportados e trilha de auditoria das ocorrências."]]
    S.append(table(mapa, [W * 0.3, W * 0.7]))

    S.append(Spacer(1, 6))
    S.append(P("9. Conclusão", "h1"))
    S.append(P("Nesta Sprint, a equipe analisou o desafio da Amazul e concluiu que o principal problema de segurança física em instalações "
               "nucleares não está na falta de sensores ou câmeras, mas na <b>dificuldade de transformar muitos sinais em decisões rápidas e "
               "confiáveis</b>. Excesso de falsos alarmes, pontos cegos, verificação lenta e registros fragmentados comprometem a etapa de "
               "detecção e avaliação, que é a base de toda a resposta."))
    S.append(P("A proposta <b>ATALAIA</b> responde a esse problema integrando sensores IoT, visão computacional, IA e drones autônomos em uma "
               "plataforma que filtra, prioriza, verifica e registra os eventos, mantendo sempre o operador no controle. O escopo foi delimitado "
               "ao perímetro e às áreas externas, com protótipo em ambiente simulado, e deixa claro o que não será feito, como neutralização de "
               "ameaças e reconhecimento facial."))
    S.append(P("<b>Próximos passos:</b> validar a visão e as metas com a Amazul; detalhar requisitos funcionais e não funcionais; modelar casos "
               "de uso, arquitetura e dados; definir o MVP (itens D1 a D6 do escopo); selecionar conjuntos de dados e montar o ambiente de "
               "simulação; e evoluir o protótipo para média fidelidade."))
    S.append(P("Referências", "h2"))
    refs = ["AGÊNCIA INTERNACIONAL DE ENERGIA ATÔMICA (IAEA). <i>Nuclear Security Recommendations on Physical Protection of Nuclear Material "
            "and Nuclear Facilities (INFCIRC/225/Revision 5)</i>. IAEA Nuclear Security Series No. 13. Viena: IAEA, 2011.",
            "AMAZUL – Amazônia Azul Tecnologias de Defesa S.A. Site institucional. Disponível em: https://www.amazul.mar.mil.br.",
            "BRASIL. Lei nº 14.222, de 15 de outubro de 2021. Cria a Autoridade Nacional de Segurança Nuclear (ANSN).",
            "BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD).",
            "ANAC. RBAC-E nº 94 – Requisitos gerais para aeronaves não tripuladas de uso civil.",
            "DECEA. ICA 100-40 – Aeronaves não tripuladas e o acesso ao espaço aéreo brasileiro.",
            "GARCIA, M. L. <i>The Design and Evaluation of Physical Protection Systems</i>. 2. ed. Butterworth-Heinemann, 2007."]
    for r in refs:
        S.append(Paragraph(r, ParagraphStyle("ref", parent=st["body"], fontSize=9, leading=12, alignment=TA_LEFT, spaceAfter=4)))

    doc.multiBuild(S)


build()
print("ok", OUT)
