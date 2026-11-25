"""Dados, fases e carregamento dos sprites."""
import json
import os
import sys

import numpy as np
import pygame


def _install_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _bundle_dir():
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", _install_dir())
    return _install_dir()


ROOT = _install_dir()
ASSET = os.path.join(_bundle_dir(), "assets")
SAVE_PATH = os.path.join(ROOT, "save.json")

VW, VH = 960, 540
GROUND = 448

TIERS = [
    {"id": 0, "name": "Fácil", "hp": 1, "dmg": 1, "spd": 1, "reward": 1},
    {"id": 1, "name": "Médio", "hp": 1.32, "dmg": 1.22, "spd": 1.05, "reward": 1.25},
    {"id": 2, "name": "Difícil", "hp": 1.68, "dmg": 1.45, "spd": 1.1, "reward": 1.5},
    {"id": 3, "name": "Brutal", "hp": 2.1, "dmg": 1.7, "spd": 1.14, "reward": 1.8},
    {"id": 4, "name": "Extremo", "hp": 2.55, "dmg": 1.95, "spd": 1.18, "reward": 2.15},
]
TIER_FINAL = {"id": 5, "name": "Final", "hp": 3.15, "dmg": 2.2, "spd": 1.2, "reward": 3}

ABILITIES = {
    "double": {"name": "Raiz Ascendente", "desc": "O segundo pulo, no mesmo botão, sobe ainda mais alto e alcança as copas."},
    "dash": {"name": "Correnteza", "desc": "Shift. Um impulso com um instante de invulnerabilidade. Cruza vãos que o pulo não alcança."},
    "spores": {"name": "Esporos", "desc": "No ar, seta para baixo + J. Você despenca e solta uma nuvem. Quebra bulbos do pântano."},
    "wall": {"name": "Garra Glacial", "desc": "Encoste numa parede no ar e pule de novo. Sirva-se dos poços verticais."},
    "shot": {"name": "Luz do Cristal", "desc": "K. Um tiro mágico que fere de longe e desfaz barreiras de cristal."},
    "pulse": {"name": "Pulso do Planeta", "desc": "O vale silenciou. O santuário ficou inteiro."},
}

TALKS = {
    "floresta": [
        ("boss", "Essa mata inteira vira tábua. Árvore em pé é desperdício."),
        ("kai", "Elas não são tábua. Eu vou deixar esta floresta de pé."),
        ("boss", "Um garoto e um cajado contra a serra?"),
        ("kai", "Contra a serra. E contra você."),
    ],
    "mares": [
        ("boss", "O mar aguenta. Mais um carregamento de lixo não muda nada."),
        ("kai", "Muda para quem vive aí embaixo. A água vai ficar limpa."),
        ("boss", "Então nada até cansar, guardião."),
        ("kai", "Eu atravesso. A costa respira de novo."),
    ],
    "pantano": [
        ("boss", "O veneno já desceu. O pântano gosta de mim agora."),
        ("kai", "Ele não gosta. Ele está doente. Eu corto a podridão."),
        ("boss", "Chegue perto. O ar também morde."),
        ("kai", "Então eu prendo a respiração e sigo."),
    ],
    "montanhas": [
        ("boss", "O santuário rachou. O inverno fica com o que sobrou."),
        ("kai", "Rachado ainda é casa. Eu devolvo as pedras ao lugar."),
        ("boss", "O frio não devolve nada."),
        ("kai", "Eu devolvo."),
    ],
    "coracao": [
        ("boss", "O cristal apagou. Sem luz, ninguém acha o caminho."),
        ("kai", "A luz não acabou. Está presa em você. Eu solto."),
        ("boss", "Então quebre junto com ela."),
        ("kai", "Eu quebro a lança. O coração fica."),
    ],
}

RESTORE = {
    "floresta": "As árvores queimadas e os troncos cortados voltaram a ser uma floresta frondosa.",
    "mares": "A água poluída clareou. O lixo sumiu e os peixes voltaram às marés.",
    "pantano": "O lodo morto floresceu: samambaias, flores e vida no pântano.",
    "montanhas": "O santuário quebrado da montanha foi reconstruído.",
    "coracao": "O cristal do planeta voltou a brilhar no centro da base.",
    "industrial": "A fumaça do vale se apagou. Cada canto do santuário está vivo.",
}

ZONES = [
    {
        "id": "floresta", "name": "Floresta Esquecida", "tile": 0, "ability": "double",
        "bossName": "Deforestor Gamma", "bossSub": "O Triturador",
        "bossHp": 420, "bossHw": 78, "bossH": 118, "drawH": 250,
        "p1": ["saws", "charge", "slam"], "p2": ["saws", "charge", "slam", "saws"], "orbit": True,
        "enemies": [
            {"name": "Espinhento", "ai": "patrol", "hp": 34, "dmg": 8, "speed": 72, "hw": 18, "h": 44},
            {"name": "Serrídeo", "ai": "charge", "hp": 28, "dmg": 11, "speed": 86, "hw": 20, "h": 36},
            {"name": "Tronco", "ai": "hopper", "hp": 54, "dmg": 13, "speed": 42, "hw": 22, "h": 50},
        ],
    },
    {
        "id": "mares", "name": "Costa das Marés", "tile": 1, "ability": "dash",
        "bossName": "Polluto", "bossSub": "O Fardo do Oceano",
        "bossHp": 460, "bossHw": 70, "bossH": 130, "drawH": 270,
        "p1": ["spit", "slam", "tire"], "p2": ["spit", "suction", "slam"],
        "enemies": [
            {"name": "Borra", "ai": "patrol", "hp": 36, "dmg": 8, "speed": 58, "hw": 20, "h": 42},
            {"name": "Caranguejo-Lata", "ai": "shooter", "hp": 32, "dmg": 9, "speed": 48, "hw": 24, "h": 40, "shot": 2},
            {"name": "Arpão", "ai": "flyer", "hp": 24, "dmg": 10, "speed": 90, "hw": 22, "h": 32},
        ],
    },
    {
        "id": "pantano", "name": "Pântano Tóxico", "tile": 2, "ability": "spores",
        "bossName": "Miasma", "bossSub": "A Podridão",
        "bossHp": 500, "bossHw": 74, "bossH": 140, "drawH": 280,
        "p1": ["clouds", "hop", "rain"], "p2": ["rain", "hop", "clouds"],
        "enemies": [
            {"name": "Gosma", "ai": "hopper", "hp": 40, "dmg": 9, "speed": 50, "hw": 18, "h": 36},
            {"name": "Moscovórtice", "ai": "flyer", "hp": 26, "dmg": 10, "speed": 100, "hw": 22, "h": 34},
            {"name": "Barril Vivo", "ai": "shooter", "hp": 48, "dmg": 11, "speed": 40, "hw": 20, "h": 44, "shot": 3},
        ],
    },
    {
        "id": "montanhas", "name": "Montanhas Eternas", "tile": 3, "ability": "wall",
        "bossName": "Avalanche Prime", "bossSub": "O Inverno de Ferro",
        "bossHp": 540, "bossHw": 76, "bossH": 140, "drawH": 280,
        "p1": ["shards", "roll", "wind"], "p2": ["shards", "roll", "icicles"],
        "enemies": [
            {"name": "Morcego-Gelo", "ai": "flyer", "hp": 26, "dmg": 9, "speed": 110, "hw": 20, "h": 32},
            {"name": "Rolador", "ai": "charge", "hp": 46, "dmg": 13, "speed": 70, "hw": 22, "h": 40},
            {"name": "Drone-Geada", "ai": "shooter", "hp": 30, "dmg": 10, "speed": 54, "hw": 20, "h": 36, "shot": 4},
        ],
    },
    {
        "id": "coracao", "name": "Coração do Planeta", "tile": 4, "ability": "shot",
        "bossName": "Corrupto Cristalino", "bossSub": "A Lança Partida",
        "bossHp": 580, "bossHw": 72, "bossH": 145, "drawH": 290,
        "p1": ["beam", "ring", "blink"], "p2": ["beam", "ring", "blink", "ring"],
        "enemies": [
            {"name": "Lasca", "ai": "flyer", "hp": 28, "dmg": 10, "speed": 95, "hw": 18, "h": 36},
            {"name": "Ígneo", "ai": "charge", "hp": 36, "dmg": 12, "speed": 100, "hw": 20, "h": 46},
            {"name": "Marionete", "ai": "shooter", "hp": 40, "dmg": 11, "speed": 46, "hw": 20, "h": 50, "shot": 5},
        ],
    },
    {
        "id": "industrial", "name": "Vale Industrial", "tile": 5, "ability": "pulse",
        "bossName": "Fornalha-Mãe", "bossSub": "Coração da Fábrica",
        "bossHp": 760, "bossHw": 90, "bossH": 130, "drawH": 270,
        "p1": ["missile", "laser", "pound"], "p2": ["missile", "pound", "summon", "laser"],
        "p3": ["missile", "laser", "pound", "summon"],
        "enemies": [
            {"name": "Engrenado", "ai": "patrol", "hp": 48, "dmg": 12, "speed": 62, "hw": 20, "h": 48},
            {"name": "Fumaça", "ai": "flyer", "hp": 32, "dmg": 11, "speed": 80, "hw": 22, "h": 46},
            {"name": "Motosserra", "ai": "charge", "hp": 44, "dmg": 14, "speed": 78, "hw": 24, "h": 40},
        ],
    },
]

PORTAL_X = [860, 1220, 1580, 1940, 2300, 2660]
SHOP_ITEMS = [
    {"id": "hp", "name": "Vitalidade", "desc": "+22 de vida máxima", "prices": [32, 58, 96, 150], "max": 4, "rank": "hpRank"},
    {"id": "dmg", "name": "Força da Raiz", "desc": "+22% de dano", "prices": [36, 64, 110, 160], "max": 4, "rank": "dmgRank"},
    {"id": "spd", "name": "Passo Leve", "desc": "+8% de velocidade", "prices": [28, 52, 90], "max": 3, "rank": "spdRank"},
    {"id": "pot", "name": "Poção verde", "desc": "Cura 45% da vida. Você carrega até 3.", "price": 16},
]

SHEETS = [
    ("kai", "kai_sheet.jpg", 5, True),
    ("lumi", "lumi_sheet.jpg", 3, True),
    ("efloresta", "enemies_floresta.jpg", 3, True),
    ("emares", "enemies_mares.jpg", 3, True),
    ("epantano", "enemies_pantano.jpg", 3, True),
    ("emontanhas", "enemies_montanhas.jpg", 3, True),
    ("ecoracao", "enemies_coracao.jpg", 3, True),
    ("eindustrial", "enemies_industrial.jpg", 3, True),
    ("boss_floresta", "boss_floresta.jpg", 1, True),
    ("boss_mares", "boss_mares.jpg", 1, True),
    ("boss_pantano", "boss_pantano.jpg", 1, True),
    ("boss_montanhas", "boss_montanhas.jpg", 1, True),
    ("boss_coracao", "boss_coracao.jpg", 1, True),
    ("boss_industrial", "boss_industrial.jpg", 1, True),
    ("tiles", "tiles_biomes.jpg", 6, True),
    ("fx", "fx_sheet.jpg", 8, True),
    ("items", "items_sheet.jpg", 6, True),
    ("ruined", "sanctuary_ruined.jpg", 5, True),
    ("restored", "sanctuary_restored.jpg", 5, True),
    ("hub", "hub_props.jpg", 3, True),
    ("logo", "logo.jpg", 1, True),
    ("bg_floresta", "bg_floresta.jpg", 1, False),
    ("bg_mares", "bg_mares.jpg", 1, False),
    ("bg_pantano", "bg_pantano.jpg", 1, False),
    ("bg_montanhas", "bg_montanhas.jpg", 1, False),
    ("bg_coracao", "bg_coracao.jpg", 1, False),
    ("bg_industrial", "bg_industrial.jpg", 1, False),
    ("bg_santuario", "bg_santuario.jpg", 1, False),
    ("bg_title", "bg_title.jpg", 1, False),
]


def clamp(v, a, b):
    return max(a, min(b, v))


def zone_by_id(zid):
    for z in ZONES:
        if z["id"] == zid:
            return z
    return None


def plat(x, y, w, h, tile, extra=None):
    p = {"x": x, "y": y, "w": w, "h": h, "tile": tile, "dead": False}
    if extra:
        p.update(extra)
    return p


def blank_world():
    return {
        "platforms": [], "enemies": [], "hazards": [], "drops": [], "particles": [], "texts": [],
        "chests": [], "w": 960, "banner": "", "bannerT": 0, "arena": None, "boss": None,
        "zone": None, "tier": None, "replay": False, "checkpoint": {"x": 100, "y": GROUND},
        "spawn": 100, "mode": "", "bg": None, "leftWall": None,
    }


def push_arena(level, arena_x, tile):
    level["platforms"].append(plat(arena_x, GROUND, 1040, 110, tile))
    level["platforms"].append(plat(arena_x + 1000, GROUND - 300, 48, 300, tile))
    level["arena"] = {"x": arena_x, "w": 1040, "lock": arena_x + 130, "floor": GROUND, "locked": False}
    level["leftWall"] = plat(arena_x - 8, GROUND - 320, 40, 320, tile)
    level["bossPos"] = {"x": arena_x + 760, "y": GROUND}
    level["w"] = arena_x + 1120


def build_level(zone, sprites):
    t = zone["tile"]
    g = GROUND
    level = blank_world()
    level["mode"] = "level"
    level["zone"] = zone
    level["bg"] = sprites["bg_" + zone["id"]][0]
    zid = zone["id"]
    if zid == "floresta":
        level["platforms"] = [
            plat(0, g, 500, 110, t), plat(600, g, 340, 110, t),
            plat(1040, g - 64, 220, 110, t), plat(1048, g - 236, 150, 40, t),
            plat(1435, g - 64, 160, 70, t), plat(1370, g, 530, 110, t),
            plat(2010, g, 350, 110, t), plat(2470, g, 390, 110, t),
        ]
        level["enemiesSpec"] = [[0, 260, g], [1, 740, g], [2, 1120, g - 64], [0, 1600, g], [1, 2140, g], [2, 2620, g]]
        level["extras"] = [[0, 420, g, 1], [1, 1760, g, 2], [2, 2280, g, 3], [0, 2700, g, 4]]
        level["dropsSpec"] = [[820, g, 8], [1680, g, 8], [2580, g, 8]]
        level["chests"] = [
            {"id": "floresta-copa", "x": 1120, "y": g - 236, "value": 30},
            {"id": "floresta-vao", "x": 1510, "y": g - 64, "value": 24},
        ]
        push_arena(level, 2960, t)
    elif zid == "mares":
        level["platforms"] = [
            plat(0, g, 460, 110, t), plat(560, g, 280, 110, t),
            plat(930, g - 70, 200, 90, t), plat(1160, g - 70, 110, 70, t),
            plat(1310, g - 70, 150, 70, t), plat(1540, g, 420, 110, t),
            plat(2060, g - 50, 240, 80, t), plat(2060, g - 220, 140, 36, t),
            plat(2400, g, 460, 110, t),
        ]
        level["enemiesSpec"] = [[0, 240, g], [1, 680, g], [2, 1000, g - 150], [0, 1700, g], [1, 2140, g - 50], [2, 2550, g - 140]]
        level["extras"] = [[1, 400, g, 1], [2, 1400, g - 160, 2], [0, 1900, g, 3], [1, 2650, g, 4]]
        level["dropsSpec"] = [[760, g, 8], [1700, g, 8], [2550, g, 8]]
        level["chests"] = [{"id": "mares-alto", "x": 2120, "y": g - 220, "value": 32}]
        push_arena(level, 2960, t)
    elif zid == "pantano":
        level["platforms"] = [
            plat(0, g, 480, 110, t), plat(580, g, 300, 110, t),
            plat(980, g - 90, 200, 36, t), plat(1180, g - 230, 222, 28, t),
            plat(1180, g - 202, 42, 132, t, {"gate": "spores"}),
            plat(1360, g - 202, 42, 132, t), plat(1180, g - 90, 222, 36, t),
            plat(1000, g, 620, 110, t), plat(1740, g, 340, 110, t),
            plat(2180, g - 40, 250, 80, t), plat(2540, g, 400, 110, t),
        ]
        level["enemiesSpec"] = [[0, 250, g], [2, 700, g], [1, 1100, g - 170], [0, 1400, g], [2, 1880, g], [1, 2300, g - 130]]
        level["extras"] = [[1, 400, g, 1], [0, 1600, g, 2], [2, 2000, g, 3], [0, 2700, g, 4]]
        level["dropsSpec"] = [[800, g, 8], [1500, g, 8], [2680, g, 8]]
        level["chests"] = [{"id": "pantano-bulbo", "x": 1300, "y": g - 90, "value": 34}]
        push_arena(level, 3040, t)
    elif zid == "montanhas":
        level["platforms"] = [
            plat(0, g, 520, 110, t), plat(630, g - 50, 260, 90, t),
            plat(990, g, 420, 110, t), plat(1410, g, 270, 110, t),
            plat(1470, g - 270, 34, 200, t), plat(1588, g - 270, 34, 200, t),
            plat(1504, g - 246, 84, 28, t), plat(1680, g, 380, 110, t),
            plat(2160, g - 60, 220, 80, t), plat(2480, g, 430, 110, t),
        ]
        level["enemiesSpec"] = [[0, 280, g - 120], [1, 740, g - 50], [2, 1160, g], [1, 1860, g], [0, 2260, g - 140], [2, 2660, g]]
        level["extras"] = [[2, 400, g, 1], [0, 1300, g - 130, 2], [1, 2000, g, 3], [2, 2740, g, 4]]
        level["dropsSpec"] = [[860, g - 50, 8], [1900, g, 8], [2700, g, 8]]
        level["chests"] = [{"id": "montanhas-poco", "x": 1546, "y": g - 246, "value": 36}]
        push_arena(level, 3010, t)
    elif zid == "coracao":
        level["platforms"] = [
            plat(0, g, 400, 110, t), plat(400, g - 58, 42, 58, t, {"gate": "shot"}),
            plat(442, g, 200, 110, t), plat(642, g - 58, 40, 80, t),
            plat(160, g - 84, 760, 26, t), plat(1020, g - 40, 240, 80, t),
            plat(1360, g, 460, 110, t), plat(1920, g - 60, 260, 80, t),
            plat(2280, g, 420, 110, t),
        ]
        level["enemiesSpec"] = [[0, 280, g - 84], [1, 560, g - 84], [2, 1120, g - 40], [0, 1540, g], [1, 2040, g - 60], [2, 2460, g]]
        level["extras"] = [[2, 180, g, 1], [0, 1700, g, 2], [1, 2200, g, 3], [0, 2480, g, 4]]
        level["dropsSpec"] = [[700, g - 84, 8], [1600, g, 8], [2400, g, 8]]
        level["chests"] = [{"id": "coracao-selo", "x": 540, "y": g, "value": 38}]
        push_arena(level, 2800, t)
    else:
        level["platforms"] = [
            plat(0, g, 420, 110, t), plat(520, g, 360, 110, t),
            plat(640, g - 30, 130, 30, t), plat(980, g - 50, 240, 90, t),
            plat(1320, g, 420, 110, t), plat(1460, g - 30, 150, 30, t),
            plat(1840, g - 46, 220, 80, t), plat(2160, g, 460, 110, t),
            plat(2300, g - 30, 160, 30, t), plat(2720, g, 420, 110, t),
        ]
        level["hazards"] = [
            zone_hazard(640, 130, 14), zone_hazard(1460, 150, 14), zone_hazard(2300, 160, 16),
        ]
        level["enemiesSpec"] = [
            [0, 220, g], [2, 660, g], [1, 1080, g - 140], [0, 1500, g],
            [2, 1960, g - 46], [1, 2360, g - 120], [0, 2900, g],
        ]
        level["extras"] = [[2, 400, g, 0], [1, 1200, g, 0], [0, 2000, g, 0], [2, 2600, g, 0]]
        level["dropsSpec"] = [[860, g, 10], [1700, g, 10], [2500, g, 10], [3000, g, 10]]
        level["chests"] = []
        push_arena(level, 3240, t)
    return level


def zone_hazard(x, w, dmg):
    return {
        "kind": "zone", "x": x, "y": GROUND - 32, "w": w, "h": 32, "dmg": dmg,
        "life": 99999, "warn": 0, "spr": 6, "permanent": True, "next": 0, "friendly": False,
    }


def default_save():
    return {
        "crystals": 0, "hpRank": 0, "dmgRank": 0, "spdRank": 0, "potions": 0,
        "cleared": {}, "tierCleared": {}, "abilities": {}, "chests": {},
        "intro": False, "pendingZone": "", "pendingMsg": "",
    }


def load_save():
    save = default_save()
    if os.path.exists(SAVE_PATH):
        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
            if isinstance(raw, dict):
                save.update(raw)
        except (OSError, json.JSONDecodeError):
            pass
    for key in ("cleared", "tierCleared", "abilities", "chests"):
        if not isinstance(save.get(key), dict):
            save[key] = {}
    return save


def persist(save):
    with open(SAVE_PATH, "w", encoding="utf-8") as fh:
        json.dump(save, fh, ensure_ascii=False)


def key_out(img):
    img = img.convert_alpha()
    w, h = img.get_size()
    pts = [(4, 4), (w - 5, 4), (4, h - 5), (w - 5, h - 5)]
    cols = [img.get_at(p) for p in pts]
    br = sum(c.r for c in cols) / 4
    bg = sum(c.g for c in cols) / 4
    bb = sum(c.b for c in cols) / 4
    rgb = pygame.surfarray.pixels3d(img)
    alpha = pygame.surfarray.pixels_alpha(img)
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    dist = np.sqrt((r - br) ** 2 + (g - bg) ** 2 + (b - bb) ** 2)
    alpha[dist < 92] = 0
    fringe = (dist < 128) & (rgb[:, :, 0] > 170) & (rgb[:, :, 2] > 140) & (rgb[:, :, 1] < 150)
    alpha[fringe] = 0
    del rgb, alpha
    return img


def crop_slice(sheet, index, count):
    w, h = sheet.get_size()
    x0 = int(index * w / count)
    x1 = int((index + 1) * w / count)
    sub = sheet.subsurface((x0, 0, max(1, x1 - x0), h)).copy()
    mask = pygame.mask.from_surface(sub, 24)
    rects = mask.get_bounding_rects()
    if not rects:
        return pygame.Surface((8, 8), pygame.SRCALPHA)
    box = rects[0].copy()
    for rect in rects[1:]:
        box.union_ip(rect)
    pad = 2
    left = max(0, box.left - pad)
    top = max(0, box.top - pad)
    right = min(sub.get_width(), box.right + pad)
    bottom = min(sub.get_height(), box.bottom + pad)
    box = pygame.Rect(left, top, max(1, right - left), max(1, bottom - top))
    return sub.subsurface(box).copy()


def load_sheet(name, count, keyed):
    img = pygame.image.load(os.path.join(ASSET, name)).convert_alpha()
    if not keyed:
        return [img]
    sheet = key_out(img)
    return [crop_slice(sheet, i, count) for i in range(count)]


def load_all(progress=None):
    sprites = {}
    total = len(SHEETS)
    for i, (sid, name, count, keyed) in enumerate(SHEETS, start=1):
        if progress:
            progress(i, total, name)
        sprites[sid] = load_sheet(name, count, keyed)
    return sprites


def cleared_count(save):
    return sum(1 for z in ZONES if z["id"] != "industrial" and save["cleared"].get(z["id"]))


def preview_tier(save, zid):
    if zid == "industrial":
        return TIER_FINAL
    if save["cleared"].get(zid) and save["tierCleared"].get(zid) is not None:
        idx = save["tierCleared"][zid]
        if isinstance(idx, int) and 0 <= idx < len(TIERS):
            return TIERS[idx]
        return TIERS[0]
    return TIERS[min(4, cleared_count(save))]
