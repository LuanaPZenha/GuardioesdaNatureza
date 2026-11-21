"""Guardiões da Natureza em pygame.

Rode com: python main.py
"""
import math
import os
import struct

import pygame

from gn.content import SAVE_PATH, TIERS, VW, VH, ZONES, load_all, load_save
from gn import sim, view


def make_beep(freq, duration, kind, volume):
    rate = 22050
    count = max(1, int(rate * duration))
    buf = bytearray()
    for i in range(count):
        t = i / rate
        fade = 1 - i / count
        if kind == "square":
            wave = 1.0 if int(t * freq * 2) % 2 == 0 else -1.0
        elif kind == "sawtooth":
            wave = 2 * ((t * freq) % 1) - 1
        else:
            wave = math.sin(2 * math.pi * freq * t)
        sample = int(max(-32767, min(32767, wave * fade * volume * 32767)))
        buf += struct.pack("<h", sample)
    return pygame.mixer.Sound(buffer=bytes(buf))


def load_sounds():
    spec = {
        "jump": (560, 0.07, "square", 0.35),
        "swing": (190, 0.06, "square", 0.3),
        "hit": (140, 0.05, "square", 0.4),
        "kill": (220, 0.09, "square", 0.4),
        "hurt": (80, 0.16, "sawtooth", 0.45),
        "dash": (360, 0.09, "square", 0.35),
        "shot": (680, 0.08, "square", 0.35),
        "boom": (70, 0.14, "sawtooth", 0.45),
        "heal": (620, 0.12, "triangle", 0.4),
        "coin": (880, 0.07, "square", 0.35),
        "buy": (520, 0.1, "triangle", 0.4),
        "roar": (55, 0.28, "sawtooth", 0.5),
    }
    sounds = {}
    for name, (freq, dur, kind, vol) in spec.items():
        try:
            sounds[name] = make_beep(freq, dur, kind, vol)
        except pygame.error:
            return {}
    return sounds


def code_of(key):
    table = {
        pygame.K_a: "KeyA", pygame.K_d: "KeyD", pygame.K_w: "KeyW", pygame.K_s: "KeyS",
        pygame.K_SPACE: "Space", pygame.K_UP: "ArrowUp", pygame.K_DOWN: "ArrowDown",
        pygame.K_LEFT: "ArrowLeft", pygame.K_RIGHT: "ArrowRight",
        pygame.K_j: "KeyJ", pygame.K_k: "KeyK", pygame.K_q: "KeyQ", pygame.K_e: "KeyE",
        pygame.K_LSHIFT: "ShiftLeft", pygame.K_RSHIFT: "ShiftRight",
        pygame.K_ESCAPE: "Escape",
    }
    return table.get(key)


def title_actions():
    actions = [sim.start_hub, sim.open_how, sim.open_credits]
    if sim.G.has_save:
        actions.append(sim.confirm_new)
    return actions


def on_keydown(event):
    if sim.G.ui_open:
        if event.key in (pygame.K_UP, pygame.K_w):
            sim.move_sel(-1)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            sim.move_sel(1)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            sim.activate_sel()
        elif event.key == pygame.K_ESCAPE:
            sim.escape_panel()
        return
    if sim.G.mode == "title":
        actions = title_actions()
        if event.key in (pygame.K_UP, pygame.K_w):
            sim.G.title_sel = (sim.G.title_sel - 1) % len(actions)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            sim.G.title_sel = (sim.G.title_sel + 1) % len(actions)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            actions[sim.G.title_sel]()
        return
    code = code_of(event.key)
    if not code:
        return
    if not sim.G.down.get(code):
        sim.G.pressed[code] = True
    sim.G.down[code] = True


def on_keyup(event):
    code = code_of(event.key)
    if code:
        sim.G.down[code] = False


def on_click(pos):
    for rect, fn in sim.G.hits:
        if rect.collidepoint(pos):
            fn()
            return


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pygame.init()
    try:
        pygame.mixer.init(22050, -16, 1, 512)
        sim.G.sounds = load_sounds()
    except pygame.error:
        sim.G.sounds = {}
    screen = pygame.display.set_mode((VW, VH), pygame.SCALED)
    pygame.display.set_caption("Guardiões da Natureza")
    sim.G.screen = screen
    sim.G.sprites = load_all(lambda i, total, name: view.loading(screen, i, total, name))
    sim.G.has_save = os.path.exists(SAVE_PATH)
    sim.G.save = load_save()
    clock = pygame.time.Clock()
    smoke = os.environ.get("GUARDIOES_SMOKE")
    frames = 0
    running = True
    while running:
        dt = min(0.033, clock.tick(60) / 1000)
        sim.G.time += dt
        if sim.G.shake > 0:
            sim.G.shake *= 0.04 ** dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                on_keydown(event)
            elif event.type == pygame.KEYUP:
                on_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                on_click(event.pos)
        if smoke:
            frames += 1
            if frames == 3:
                sim.start_hub()
            elif frames == 12:
                sim.start_level(ZONES[0], TIERS[0], False)
            elif frames > 30:
                running = False
        sim.step(dt)
        view.render()
        pygame.display.flip()
        sim.G.pressed.clear()
    pygame.quit()


if __name__ == "__main__":
    main()
