"""Desenho da tela, do mundo e dos painéis."""
import math
import random

import pygame

from gn.content import GROUND, PORTAL_X, VW, VH, ZONES, cleared_count, preview_tier
from gn import sim

_cache = {}
_fonts = {}
OX = OY = 0


def font(size):
    size = max(13, int(size * 1.55))
    if size not in _fonts:
        _fonts[size] = pygame.font.SysFont("segoe ui", size)
    return _fonts[size]


def color(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def scaled(spr, height, flip):
    height = max(1, int(height))
    key = (id(spr), height, bool(flip))
    img = _cache.get(key)
    if img is None:
        w = max(1, int(height * spr.get_width() / max(1, spr.get_height())))
        img = pygame.transform.scale(spr, (w, height))
        if flip:
            img = pygame.transform.flip(img, True, False)
        _cache[key] = img
    return img


def blit(spr, x, y, height, flip=False, screen=False):
    if spr is None or spr.get_width() < 1:
        return
    img = scaled(spr, height, flip)
    if screen:
        sx, sy = int(x), int(y)
    else:
        sx, sy = int(x - sim.G.camx + OX), int(y + OY)
    sim.G.screen.blit(img, (sx - img.get_width() // 2, sy - img.get_height()))


def screen_text(text, x, y, size, fill="#f6edd4", align="center"):
    face = font(size)
    img = face.render(str(text), True, color(fill))
    shadow = face.render(str(text), True, (16, 32, 24))
    if align == "left":
        pos = (int(x), int(y))
    elif align == "right":
        pos = (int(x - img.get_width()), int(y))
    else:
        pos = (int(x - img.get_width() / 2), int(y))
    sim.G.screen.blit(shadow, (pos[0] + 2, pos[1] + 2))
    sim.G.screen.blit(img, pos)


def draw_bar(x, y, w, h, ratio, fill, back):
    screen = sim.G.screen
    pygame.draw.rect(screen, color(back), (x, y, w, h))
    pygame.draw.rect(screen, color(fill), (x, y, max(0, w * max(0, min(1, ratio))), h))
    pygame.draw.rect(screen, (12, 18, 28), (x, y, w, h), 1)


def draw_cover(img):
    scale = max(VW / img.get_width(), VH / img.get_height())
    dw, dh = int(img.get_width() * scale), int(img.get_height() * scale)
    sim.G.screen.blit(pygame.transform.scale(img, (dw, dh)), ((VW - dw) // 2, (VH - dh) // 2))


def draw_parallax(img):
    screen = sim.G.screen
    screen.fill((142, 200, 234))
    if img is None:
        return
    dh = int(VH * 0.7)
    scale = dh / img.get_height()
    dw = max(1, int(img.get_width() * scale))
    frame = pygame.transform.scale(img, (dw, dh))
    shift = (sim.G.camx * 0.28) % dw
    x = -shift
    while x < VW:
        screen.blit(frame, (int(x), 0))
        x += dw - 1
    shade = pygame.Surface((VW, 80), pygame.SRCALPHA)
    for i in range(80):
        alpha = int(255 * (i / 80))
        pygame.draw.line(shade, (142, 200, 234, alpha), (0, i), (VW, i))
    screen.blit(shade, (0, dh - 70))


def draw_platform(p):
    sprites = sim.G.sprites
    if p.get("gate"):
        spr = sprites["tiles"][4] if p["gate"] == "shot" else sprites["fx"][3]
        sim.G.screen.blit(
            pygame.transform.scale(spr, (max(1, int(p["w"])), max(1, int(p["h"])))),
            (int(p["x"] - sim.G.camx + OX), int(p["y"] + OY)),
        )
        return
    tile = sprites["tiles"][p["tile"] % len(sprites["tiles"])]
    size = 64
    screen = sim.G.screen
    clip = screen.get_clip()
    area = pygame.Rect(int(p["x"] - sim.G.camx + OX), int(p["y"] - 16 + OY), int(p["w"]), int(p["h"] + 16))
    screen.set_clip(area)
    top = scaled(tile, size, False)
    x = p["x"]
    while x < p["x"] + p["w"]:
        screen.blit(top, (int(x - sim.G.camx + OX), int(p["y"] - 14 + OY)))
        x += size - 1
    dirt_top = p["y"] - 14 + size - 10
    dirt_h = p["y"] + p["h"] - dirt_top
    if dirt_h > 4:
        src = pygame.Rect(0, int(tile.get_height() * 0.58), tile.get_width(), max(1, int(tile.get_height() * 0.42)))
        dirt = pygame.transform.scale(tile.subsurface(src), (size, max(1, int(dirt_h))))
        x = p["x"]
        while x < p["x"] + p["w"]:
            screen.blit(dirt, (int(x - sim.G.camx + OX), int(dirt_top + OY)))
            x += size - 1
    screen.set_clip(clip)


def draw_player():
    player = sim.G.player
    sprites = sim.G.sprites
    if player["hurt"] > 0.4:
        frame = 4
    elif player["atk"] > 0:
        frame = 3
    elif not player["onGround"]:
        frame = 2
    elif abs(player["vx"]) > 20:
        frame = 1 if int(sim.G.time * 8) % 2 == 0 else 0
    else:
        frame = 0
    spr = sprites["kai"][min(frame, len(sprites["kai"]) - 1)]
    shadow = pygame.Surface((36, 12), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (4, 16, 24, 90), shadow.get_rect())
    sim.G.screen.blit(shadow, (int(player["x"] - sim.G.camx + OX - 18), int(player["y"] + OY - 4)))
    if player["hurt"] > 0 and int(sim.G.time * 16) % 2 == 0:
        spr = spr.copy()
        spr.set_alpha(115)
    blit(spr, player["x"], player["y"], 86, player["dir"] == -1)
    if player["atk"] > 0.05:
        blit(sprites["fx"][0], player["x"] + player["dir"] * 34, player["y"] - 16, 36, player["dir"] == -1)
    if player["dash"] > 0:
        blit(sprites["fx"][7], player["x"] - player["dir"] * 20, player["y"] - 20, 40, False)


def draw_lumi():
    player = sim.G.player
    frame = 2 if int(sim.G.time * 3) % 3 == 2 else 0
    frames = sim.G.sprites["lumi"]
    blit(frames[min(frame, len(frames) - 1)], player["x"] - player["dir"] * 28, player["y"] - 62 + math.sin(sim.G.time * 4) * 4, 42, False)


def draw_enemy(enemy):
    sheet = sim.G.sprites["e" + sim.G.world["zone"]["id"]]
    spr = sheet[enemy["type"] % len(sheet)]
    bob = 0 if enemy["fly"] else math.sin(sim.G.time * 2 + enemy["x"])
    blit(spr, enemy["x"], enemy["y"] + bob, enemy["h"] + 16, enemy["dir"] == 1)
    if enemy["hp"] < enemy["max"]:
        draw_bar(enemy["x"] - sim.G.camx + OX - 16, enemy["y"] + OY - enemy["h"] - 12, 32, 4, enemy["hp"] / enemy["max"], "#e23d4a", "#2a1218")


def draw_boss(boss):
    spr = sim.G.sprites["boss_" + boss["def"]["id"]][0]
    if boss["flash"] > 0:
        spr = spr.copy()
        spr.set_alpha(165)
    blit(spr, boss["x"], boss["y"], boss["def"]["drawH"], boss["dir"] == 1)
    arena = sim.G.world["arena"]
    if boss["def"].get("orbit") and boss["phase"] >= 2 and arena["locked"]:
        ang = sim.G.time * 3.2
        for i in range(2):
            blit(
                sim.G.sprites["fx"][1],
                boss["x"] + math.cos(ang + i * math.pi) * 92,
                boss["y"] - 70 + math.sin(ang + i * math.pi) * 26,
                28, False,
            )
    if not arena["locked"]:
        return
    screen_text(boss["def"]["bossName"], VW / 2, 22, 11)
    screen_text(boss["def"]["bossSub"] + "  ·  fase " + str(boss["phase"]), VW / 2, 40, 8, "#d5e6cf")
    col = "#ffb020" if boss["phase"] >= 3 else "#ff7a3c" if boss["phase"] == 2 else "#e23d4a"
    draw_bar(VW / 2 - 220, 50, 440, 14, boss["hp"] / max(1, boss["max"]), col, "#2a1218")
    if boss["state"] == "tell":
        label = "PULO!" if boss["pattern"] == "pound" else "!"
        screen_text(label, boss["x"] - sim.G.camx + OX, boss["y"] - boss["h"] - 16, 12, "#ffd0a1")


def draw_hazard(h):
    sprites = sim.G.sprites
    if h["kind"] == "proj":
        spr = sprites["fx"][h.get("spr", 5) % len(sprites["fx"])]
        img = scaled(spr, 28, False)
        if h.get("spin"):
            img = pygame.transform.rotate(img, -sim.G.time * 12 * 57)
        sim.G.screen.blit(img, (int(h["x"] - sim.G.camx + OX - img.get_width() / 2), int(h["y"] + OY - img.get_height() / 2)))
    elif h["kind"] == "zone":
        alpha = 0.35 + math.sin(sim.G.time * 24) * 0.15 if h.get("warn", 0) > 0 else 0.8
        if h.get("beam"):
            spr = pygame.transform.scale(sprites["fx"][5], (max(1, int(h["w"])), max(1, int(h["h"]))))
            spr.set_alpha(int(alpha * 255))
            sim.G.screen.blit(spr, (int(h["x"] - sim.G.camx + OX), int(h["y"] + OY)))
        elif h.get("permanent"):
            x = h["x"]
            while x < h["x"] + h["w"]:
                blit(sprites["fx"][6], x, h["y"] + h["h"], 26, False)
                x += 28
        else:
            blit(sprites["fx"][h.get("spr", 7) % len(sprites["fx"])], h["x"] + h["w"] / 2, h["y"] + h["h"], 30 if h.get("warn", 0) > 0 else 48, False)


def draw_hub():
    sprites = sim.G.sprites
    save = sim.G.save
    blit(sprites["hub"][0], 220, GROUND, 150, False)
    blit(sprites["hub"][1], 430, GROUND, 110, False)
    blit(sprites["hub"][2], 620, GROUND, 120, False)
    for i, zone in enumerate(ZONES):
        x = PORTAL_X[i]
        if i < 5:
            sheet = sprites["restored"] if save["cleared"].get(zone["id"]) else sprites["ruined"]
            blit(sheet[i], x, GROUND + 6, 168, False)
        open_gate = cleared_count(save) >= 5 if zone["id"] == "industrial" else True
        door = sprites["items"][5] if save["cleared"].get(zone["id"]) or (zone["id"] == "industrial" and open_gate) else sprites["items"][4]
        blit(door, x, GROUND, 132, False)
        tier = preview_tier(save, zone["id"])
        label = "Restaurada" if save["cleared"].get(zone["id"]) else tier["name"]
        if zone["id"] == "industrial" and cleared_count(save) < 5:
            label = "Selado"
        if zone["id"] == "industrial" and save["cleared"].get(zone["id"]):
            label = "Em paz"
        tint = "#b6ffb0" if save["cleared"].get(zone["id"]) else "#ffe08a"
        screen_text(zone["name"], x - sim.G.camx + OX, GROUND - 168, 8)
        screen_text(label, x - sim.G.camx + OX, GROUND - 150, 8, tint)
    screen_text("Loja", 220 - sim.G.camx + OX, GROUND - 160, 8)
    player = sim.G.player
    near = ""
    if abs(player["x"] - 220) < 70:
        near = "E  Loja"
    for i, zone in enumerate(ZONES):
        if abs(player["x"] - PORTAL_X[i]) < 54:
            near = "Selado" if zone["id"] == "industrial" and cleared_count(save) < 5 else "E  Entrar"
    if near:
        screen_text(near, player["x"] - sim.G.camx + OX, player["y"] - 86, 8)


def draw_hud():
    player = sim.G.player
    save = sim.G.save
    sprites = sim.G.sprites
    blit(sprites["kai"][0], 58, 86, 70, False, True)
    screen_text("KAI", 100, 18, 10, "#fff6df", "left")
    screen_text("Nv." + str(1 + cleared_count(save)), 100, 38, 8, "#d5e6cf", "left")
    draw_bar(100, 58, 170, 12, player["hp"] / sim.max_hp(), "#e23d4a", "#3a141c")
    screen_text(str(math.ceil(player["hp"])) + "/" + str(sim.max_hp()), 278, 56, 8, "#fff6df", "left")
    blit(sprites["items"][0], 118, 96, 18, False, True)
    screen_text(str(save["crystals"]), 132, 84, 8, "#9fd8ff", "left")
    blit(sprites["items"][2], 210, 96, 20, False, True)
    screen_text(str(save["potions"]), 224, 84, 8, "#b6ffb0", "left")
    icons = [("pulo", True), ("double", False), ("dash", False), ("spores", False), ("wall", False), ("shot", False)]
    labels = {"pulo": "pulo", "double": "raiz", "dash": "dash", "spores": "esporo", "wall": "parede", "shot": "tiro"}
    ix = 100
    for ability, always in icons:
        if not always and not sim.has(ability):
            continue
        screen_text(labels[ability], ix + 16, 108, 7, "#d5e6cf")
        ix += 78
    world = sim.G.world
    if world["mode"] == "level" and world.get("tier"):
        screen_text(world["zone"]["name"], VW - 16, 16, 8, "#fff6df", "right")
        screen_text(world["tier"]["name"], VW - 16, 36, 8, "#ffe08a", "right")


def render_world():
    global OX, OY
    world = sim.G.world
    OX = OY = 0
    if sim.G.shake > 0.4:
        OX = random.uniform(-sim.G.shake, sim.G.shake)
        OY = random.uniform(-sim.G.shake, sim.G.shake)
    draw_parallax(world.get("bg"))
    band = (22, 54, 40) if world["mode"] == "hub" else (16, 24, 16)
    sim.G.screen.fill(band, (0, GROUND + 8, VW, VH - GROUND))
    if world["mode"] == "hub":
        draw_hub()
    for p in world["platforms"]:
        draw_platform(p)
    for chest in world.get("chests") or []:
        if not sim.G.save["chests"].get(chest["id"]):
            blit(sim.G.sprites["items"][3], chest["x"], chest["y"], 36, False)
    for drop in world["drops"]:
        blit(sim.G.sprites["items"][0], drop["x"], drop["y"], 22, False)
    for h in world["hazards"]:
        draw_hazard(h)
    for enemy in world["enemies"]:
        draw_enemy(enemy)
    if world.get("boss") and world.get("arena"):
        draw_boss(world["boss"])
    draw_player()
    draw_lumi()
    for p in world["particles"]:
        spr = sim.G.sprites["fx"][p["spr"] % len(sim.G.sprites["fx"])]
        img = scaled(spr, p["s"], False).copy()
        img.set_alpha(int(255 * max(0, p["life"] / p["max"])))
        sim.G.screen.blit(img, (int(p["x"] - sim.G.camx + OX - img.get_width() / 2), int(p["y"] + OY - img.get_height())))
    for t in world["texts"]:
        screen_text(t["t"], t["x"] - sim.G.camx + OX, t["y"] + OY, 8, t["color"])
    draw_hud()
    if world["bannerT"] > 0:
        screen_text(world["banner"], VW / 2, 78, 12)
    if world["mode"] == "level":
        for chest in world.get("chests") or []:
            if sim.G.save["chests"].get(chest["id"]):
                continue
            if abs(sim.G.player["x"] - chest["x"]) < 36:
                screen_text("E  Baú + vida", chest["x"] - sim.G.camx + OX, chest["y"] - 48, 8)


def wrap(text, face, width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if face.size(trial)[0] <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


def add_button(rect, fn):
    sim.G.hits.append((rect, fn))


def draw_title():
    draw_cover(sim.G.sprites["bg_title"][0])
    logo = sim.G.sprites["logo"][0]
    lh = 210
    lw = int(lh * logo.get_width() / logo.get_height())
    sim.G.screen.blit(pygame.transform.scale(logo, (lw, lh)), (24, 8))
    if sim.G.ui_open:
        return
    note = "O santuário lembra de você." if sim.G.has_save else "A natureza precisa de novos guardiões."
    screen_text(note, 48, 250, 8, "#d5e6cf", "left")
    buttons = [("Jogar", sim.start_hub), ("Controles", sim.open_how), ("Créditos", sim.open_credits)]
    if sim.G.has_save:
        buttons.append(("Novo jogo", sim.confirm_new))
    y = 278
    for i, (label, fn) in enumerate(buttons):
        rect = pygame.Rect(36, y, 280, 36)
        selected = i == sim.G.title_sel
        pygame.draw.rect(sim.G.screen, (47, 122, 63) if selected else (24, 48, 32), rect)
        pygame.draw.rect(sim.G.screen, (214, 232, 190), rect, 2)
        screen_text(label, rect.centerx, rect.y + 8, 10)
        add_button(rect, fn)
        y += 44


def draw_panel():
    panel = sim.G.panel
    if not panel:
        return
    shade = pygame.Surface((VW, VH), pygame.SRCALPHA)
    shade.fill((6, 14, 10, 150))
    sim.G.screen.blit(shade, (0, 0))
    card = pygame.Rect(120, 36, 720, 468)
    pygame.draw.rect(sim.G.screen, (18, 36, 28), card)
    pygame.draw.rect(sim.G.screen, (214, 232, 190), card, 3)
    screen_text(panel["kicker"], card.x + 28, card.y + 16, 8, "#9dcc8a", "left")
    screen_text(panel["title"], card.x + 28, card.y + 40, 14, "#fff6df", "left")
    face = font(9)
    y = card.y + 84
    for line in panel["lines"]:
        for piece in wrap(line, face, card.w - 56):
            screen_text(piece, card.x + 28, y, 9, "#d5e6cf", "left")
            y += face.get_height() + 4
        y += 8
    by = card.bottom - 24 - 40 * len(panel["buttons"])
    by = max(by, y + 8)
    for i, btn in enumerate(panel["buttons"]):
        rect = pygame.Rect(card.x + 28, by, card.w - 56, 34)
        selected = i == panel["sel"]
        fill = (47, 122, 63) if selected and btn["enabled"] else (32, 48, 36)
        if not btn["enabled"]:
            fill = (28, 32, 30)
        pygame.draw.rect(sim.G.screen, fill, rect)
        pygame.draw.rect(sim.G.screen, (214, 232, 190) if btn["enabled"] else (90, 100, 90), rect, 2)
        screen_text(btn["label"], rect.centerx, rect.y + 6, 9, "#fff6df" if btn["enabled"] else "#8a948c")
        if btn["enabled"]:
            add_button(rect, btn["fn"])
        by += 40


def render():
    sim.G.hits = []
    if sim.G.mode == "title":
        draw_title()
    elif sim.G.world:
        render_world()
    if sim.G.ui_open:
        sim.G.hits = []
        draw_panel()


def loading(screen, done, total, name):
    screen.fill((12, 28, 22))
    sim.G.screen = screen
    screen_text("Carregando sprites " + str(done) + "/" + str(total), VW / 2, VH / 2 - 20, 12)
    screen_text(name, VW / 2, VH / 2 + 16, 8, "#d5e6cf")
    pygame.display.flip()
    pygame.event.pump()
