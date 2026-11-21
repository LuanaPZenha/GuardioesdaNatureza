"""Simulação: jogador, inimigos, chefes, loja e progressão."""
import math
import random

from gn.content import (
    ABILITIES, GROUND, PORTAL_X, RESTORE, SHOP_ITEMS, TIER_FINAL, VW, ZONES,
    blank_world, build_level, cleared_count, clamp, persist, plat, preview_tier, zone_by_id,
)

class Game:
    save = None
    mode = "title"
    player = None
    world = None
    camx = 0.0
    time = 0.0
    shake = 0.0
    sprites = {}
    ui_open = False
    down = {}
    pressed = {}
    panel = None
    title_sel = 0
    has_save = False
    sounds = {}
    hits = []
    screen = None


G = Game()


def sfx(name):
    sound = G.sounds.get(name)
    if sound:
        sound.play()


def has(ability):
    return bool(G.save and G.save["abilities"].get(ability))


def max_hp():
    return 100 + 22 * (G.save["hpRank"] or 0)


def dmg_mul():
    return 1 + 0.22 * (G.save["dmgRank"] or 0)


def speed_mul():
    return 1 + 0.08 * (G.save["spdRank"] or 0)


def heal_fraction(part):
    before = G.player["hp"]
    cap = max_hp()
    G.player["hp"] = min(cap, before + round(cap * part))
    gained = G.player["hp"] - before
    if gained > 0:
        sfx("heal")
    return gained


def open_panel(pid, kicker, title, lines, buttons):
    G.panel = {
        "id": pid, "kicker": kicker, "title": title, "lines": lines,
        "buttons": buttons, "sel": 0,
    }
    G.ui_open = True


def close_panels():
    G.panel = None
    G.ui_open = False


def float_text(x, y, text, color="#fff6df"):
    G.world["texts"].append({"x": x, "y": y, "t": text, "color": color, "life": 0.7})


def burst(x, y, spr, n):
    for _ in range(n):
        G.world["particles"].append({
            "x": x, "y": y, "spr": spr,
            "vx": (random.random() - 0.5) * 180,
            "vy": -40 - random.random() * 140,
            "life": 0.35 + random.random() * 0.3,
            "max": 0.6,
            "s": 16 + random.random() * 14,
        })


def make_player(x, y):
    return {
        "x": x, "y": y, "vx": 0, "vy": 0, "dir": 1, "hw": 13, "h": 46,
        "onGround": True, "coyote": 0.12, "jumpBuf": 0, "jumpsLeft": 1, "jumpLock": 0,
        "wallDir": 0, "wallCoy": 0, "atk": 0, "atkCd": 0, "swing": 0,
        "hurt": 0, "dash": 0, "dashCd": 0, "dashDir": 1, "slam": False, "shotCd": 0,
        "hp": max_hp(), "anim": 0, "blocked": False,
    }


def build_hub():
    world = blank_world()
    world["mode"] = "hub"
    world["w"] = 3480
    world["bg"] = G.sprites["bg_santuario"][0]
    world["platforms"] = [
        plat(0, GROUND, 3480, 110, 0),
        plat(70, GROUND - 86, 130, 44, 0),
        plat(70, GROUND - 196, 110, 36, 0),
        plat(390, GROUND - 86, 130, 44, 0),
        plat(3188, GROUND - 250, 32, 180, 3),
        plat(3304, GROUND - 250, 32, 180, 3),
        plat(3220, GROUND - 230, 84, 28, 3),
    ]
    world["spawn"] = 130
    world["checkpoint"] = {"x": 130, "y": GROUND}
    return world


def spawn_enemy(kind, x, y, zone, tier):
    d = zone["enemies"][kind]
    return {
        "type": kind, "name": d["name"], "ai": d["ai"], "shot": d.get("shot"),
        "x": x, "y": y, "vx": 0, "vy": 0, "dir": -1,
        "hw": d["hw"], "h": d["h"],
        "hp": round(d["hp"] * tier["hp"]),
        "max": round(d["hp"] * tier["hp"]),
        "dmg": max(1, round(d["dmg"] * tier["dmg"])),
        "speed": d["speed"] * tier["spd"],
        "home": x, "baseY": y - (90 if d["ai"] == "flyer" else 0),
        "timer": 0.4 + random.random(),
        "state": "walk", "iframe": 0, "lastSwing": -1, "touch": 0,
        "fly": d["ai"] == "flyer", "gone": False, "blocked": False, "onGround": False,
    }


def make_boss(zone, tier, pos):
    hp = round(zone["bossHp"] * tier["hp"])
    return {
        "def": zone, "x": pos["x"], "y": pos["y"], "vx": 0, "vy": 0, "dir": -1,
        "hp": hp, "max": hp, "hw": zone["bossHw"], "h": zone["bossH"],
        "phase": 1, "state": "wait", "t": 0, "step": 0, "pattern": "",
        "aimX": pos["x"], "aimY": pos["y"] - 40, "lastSwing": -1,
        "dying": 0, "rewarded": False, "flash": 0, "hop": False, "wind": 0,
    }


def start_hub():
    G.mode = "hub"
    G.world = build_hub()
    idx = next((i for i, z in enumerate(ZONES) if z["id"] == G.save["pendingZone"]), -1)
    x = PORTAL_X[idx] if idx >= 0 else 140
    G.player = make_player(x, GROUND)
    G.player["hp"] = max_hp()
    G.camx = clamp(x - 420, 0, G.world["w"] - VW)
    if G.save["pendingMsg"]:
        G.world["banner"] = G.save["pendingMsg"]
        G.world["bannerT"] = 4
        G.save["pendingMsg"] = ""
        G.save["pendingZone"] = ""
        persist(G.save)
    close_panels()
    if not G.save["intro"]:
        open_intro()


def start_level(zone, tier, replay):
    G.mode = "level"
    world = build_level(zone, G.sprites)
    world["tier"] = tier
    world["replay"] = replay
    world["banner"] = zone["name"] + " — " + tier["name"]
    world["bannerT"] = 3.4
    world["enemies"] = [spawn_enemy(t, x, y, zone, tier) for t, x, y in world.get("enemiesSpec") or []]
    for kind, x, y, min_tier in world.get("extras") or []:
        if tier["id"] >= min_tier:
            world["enemies"].append(spawn_enemy(kind, x, y, zone, tier))
    world["drops"] = [
        {"x": x, "y": y, "vy": -40, "value": value, "life": 30}
        for x, y, value in world.get("dropsSpec") or []
    ]
    world["hazards"] = world.get("hazards") or []
    for h in world["hazards"]:
        h["dmg"] = round(h["dmg"] * tier["dmg"])
    world["boss"] = make_boss(zone, tier, world["bossPos"])
    G.world = world
    G.player = make_player(90, GROUND)
    G.player["hp"] = max_hp()
    world["checkpoint"] = {"x": 90, "y": GROUND}
    G.camx = 0
    close_panels()


def overlap_x(body, p):
    return body["x"] + body["hw"] > p["x"] + 1 and body["x"] - body["hw"] < p["x"] + p["w"] - 1


def overlap_body(body, p):
    return overlap_x(body, p) and body["y"] > p["y"] and body["y"] - body["h"] < p["y"] + p["h"]


def rects(a, b):
    return a["x"] < b["x"] + b["w"] and a["x"] + a["w"] > b["x"] and a["y"] < b["y"] + b["h"] and a["y"] + a["h"] > b["y"]


def circle_rect(cx, cy, r, p):
    x = clamp(cx, p["x"], p["x"] + p["w"])
    y = clamp(cy, p["y"], p["y"] + p["h"])
    return (cx - x) ** 2 + (cy - y) ** 2 <= r * r


def move_body(body, dt):
    body["x"] += body["vx"] * dt
    for p in G.world["platforms"]:
        if p["dead"] or p.get("oneWay"):
            continue
        if body["y"] <= p["y"] + 8:
            continue
        if not overlap_body(body, p):
            continue
        if body["x"] < p["x"] + p["w"] / 2:
            body["x"] = p["x"] - body["hw"]
        else:
            body["x"] = p["x"] + p["w"] + body["hw"]
        body["vx"] = 0
        body["blocked"] = True
    prev = body["y"]
    body["y"] += body["vy"] * dt
    body["onGround"] = False
    for p in G.world["platforms"]:
        if p["dead"] or not overlap_x(body, p):
            continue
        if body["vy"] >= 0 and prev <= p["y"] + 6 and body["y"] >= p["y"] and body["y"] - prev <= 64:
            body["y"] = p["y"]
            body["vy"] = 0
            body["onGround"] = True
        elif not p.get("oneWay") and body["vy"] < 0 and overlap_body(body, p):
            body["y"] = p["y"] + p["h"] + body["h"]
            body["vy"] = 0


def supported(x, feet):
    for p in G.world["platforms"]:
        if p["dead"] or p.get("gate"):
            continue
        if p["x"] <= x <= p["x"] + p["w"] and abs(feet - p["y"]) < 10:
            return True
    return False


def blocked_at(x, y):
    for p in G.world["platforms"]:
        if p["dead"] or p.get("oneWay"):
            continue
        if p["x"] <= x <= p["x"] + p["w"] and p["y"] + 8 <= y <= p["y"] + p["h"]:
            return True
    return False


def hurt_player(dmg, from_x):
    player = G.player
    if player["hurt"] > 0 or player["hp"] <= 0:
        return
    player["hp"] -= dmg
    player["hurt"] = 0.85
    player["vx"] = -200 if player["x"] < from_x else 200
    player["vy"] = -240
    player["slam"] = False
    G.shake = max(G.shake, 6)
    sfx("hurt")
    float_text(player["x"], player["y"] - 60, "-" + str(dmg), "#ffb0b0")
    if player["hp"] <= 0:
        player["hp"] = 0
        open_panel(
            "dead", "Kai caiu", "A natureza ainda precisa de você",
            ["Os cristais que você já pegou continuam na bolsa. O chefe desta tentativa ainda está de pé."],
            [
                {"label": "Tentar de novo", "fn": retry_level, "enabled": True},
                {"label": "Santuário", "fn": start_hub, "enabled": True},
            ],
        )


def damage_enemy(enemy, dmg, knock):
    if not enemy or enemy["hp"] <= 0:
        return
    enemy["hp"] -= dmg
    enemy["iframe"] = 0.07
    enemy["vx"] = knock or 0
    enemy["vy"] = min(enemy["vy"], -80)
    float_text(enemy["x"], enemy["y"] - enemy["h"], str(round(dmg)), "#ffe08a")
    if enemy["hp"] <= 0:
        val = round((6 + enemy["type"] * 2) * G.world["tier"]["reward"])
        G.world["drops"].append({"x": enemy["x"], "y": enemy["y"] - 16, "vy": -80, "value": val, "life": 16})
        burst(enemy["x"], enemy["y"] - 20, 7, 4)
        sfx("kill")
        enemy["gone"] = True
    else:
        sfx("hit")


def damage_boss(dmg):
    boss = G.world["boss"]
    arena = G.world["arena"]
    if not boss or boss["rewarded"] or boss["state"] == "wait" or not arena["locked"]:
        return
    boss["hp"] -= dmg
    boss["flash"] = 0.08
    G.shake = max(G.shake, 5)
    float_text(boss["x"], boss["y"] - boss["h"], str(round(dmg)), "#ffe08a")
    sfx("hit")
    if boss["hp"] <= 0:
        boss["hp"] = 0
        boss["dying"] = 0.85
        boss["state"] = "dead"
        burst(boss["x"], boss["y"] - 80, 7, 10)
        sfx("roar")
    elif boss["phase"] == 1 and boss["hp"] < boss["max"] * 0.5 and boss["def"]["id"] != "industrial":
        enter_phase(boss, 2)
    elif boss["def"]["id"] == "industrial" and boss["phase"] == 1 and boss["hp"] < boss["max"] * 0.66:
        enter_phase(boss, 2)
    elif boss["def"]["id"] == "industrial" and boss["phase"] == 2 and boss["hp"] < boss["max"] * 0.33:
        enter_phase(boss, 3)


def enter_phase(boss, phase):
    boss["phase"] = phase
    boss["state"] = "roar"
    boss["t"] = 1
    G.shake = 10
    sfx("roar")
    float_text(boss["x"], boss["y"] - boss["h"] - 20, "FASE " + str(phase), "#ffd0a1")


def land_slam():
    player = G.player
    player["slam"] = False
    G.shake = 8
    sfx("boom")
    burst(player["x"], player["y"], 3, 6)
    r = 82
    for enemy in G.world["enemies"]:
        if math.hypot(enemy["x"] - player["x"], enemy["y"] - player["y"]) < r + 20:
            damage_enemy(enemy, 18 * dmg_mul(), math.copysign(180, enemy["x"] - player["x"] or 1))
    boss = G.world.get("boss")
    if boss and math.hypot(boss["x"] - player["x"], boss["y"] - player["y"]) < r + 50:
        damage_boss(20 * dmg_mul())
    for p in G.world["platforms"]:
        if p.get("gate") == "spores" and circle_rect(player["x"], player["y"] - 10, r, p):
            p["dead"] = True


def melee_box():
    player = G.player
    w, h = 48, 36
    x = player["x"] + 6 if player["dir"] == 1 else player["x"] - 6 - w
    return {"x": x, "y": player["y"] - player["h"] + 6, "w": w, "h": h}


def update_player(dt):
    player = G.player
    player["jumpBuf"] = max(0, player["jumpBuf"] - dt)
    player["atkCd"] = max(0, player["atkCd"] - dt)
    player["dashCd"] = max(0, player["dashCd"] - dt)
    player["shotCd"] = max(0, player["shotCd"] - dt)
    player["hurt"] = max(0, player["hurt"] - dt)
    player["atk"] = max(0, player["atk"] - dt)
    if G.pressed.get("Space") or G.pressed.get("ArrowUp") or G.pressed.get("KeyW"):
        player["jumpBuf"] = 0.13

    can_ground = player["coyote"] > 0
    can_double = player["jumpsLeft"] > 0 and not player["onGround"]
    can_wall = has("wall") and player["wallCoy"] > 0 and not player["onGround"]
    if player["jumpBuf"] > 0 and player["dash"] <= 0 and (can_ground or can_double or can_wall):
        if can_wall and not can_ground:
            away = -(player["wallDir"] or 1)
            player["vy"] = -600
            player["vx"] = away * 300
            player["dir"] = away
            player["jumpsLeft"] = 1
            player["wallCoy"] = 0
        elif can_ground:
            player["vy"] = -620
            player["jumpsLeft"] = 1
            player["coyote"] = 0
        else:
            player["vy"] = -700 if has("double") else -640
            player["jumpsLeft"] -= 1
            burst(player["x"], player["y"] - 20, 3, 3)
        player["jumpLock"] = 0.14
        player["jumpBuf"] = 0
        player["onGround"] = False
        player["slam"] = False
        sfx("jump")
    player["jumpLock"] = max(0, (player["jumpLock"] or 0) - dt)
    holding = G.down.get("Space") or G.down.get("ArrowUp") or G.down.get("KeyW")
    if player["jumpLock"] <= 0 and not holding and player["vy"] < -460:
        player["vy"] = -460

    if (G.pressed.get("ShiftLeft") or G.pressed.get("ShiftRight")) and has("dash") and player["dashCd"] <= 0 and player["dash"] <= 0:
        player["dash"] = 0.18
        player["dashCd"] = 0.52
        player["dashDir"] = player["dir"] or 1
        player["hurt"] = max(player["hurt"], 0.16)
        player["slam"] = False
        sfx("dash")
    down_held = G.down.get("ArrowDown") or G.down.get("KeyS")
    if G.pressed.get("KeyJ") and down_held and has("spores") and not player["onGround"] and not player["slam"]:
        player["slam"] = True
        player["vy"] = 840
        sfx("boom")
    elif G.pressed.get("KeyJ") and player["atkCd"] <= 0 and not player["slam"]:
        player["atk"] = 0.18
        player["atkCd"] = 0.36
        player["swing"] += 1
        sfx("swing")
    if G.pressed.get("KeyK") and has("shot") and player["shotCd"] <= 0:
        player["shotCd"] = 0.42
        G.world["hazards"].append({
            "kind": "proj", "friendly": True, "x": player["x"] + player["dir"] * 24, "y": player["y"] - 30,
            "vx": player["dir"] * 480, "vy": 0, "r": 12, "dmg": 14 * dmg_mul(), "life": 0.7, "spr": 5,
        })
        sfx("shot")
    if G.pressed.get("KeyQ") and G.mode == "level" and G.save["potions"] > 0 and player["hp"] < max_hp():
        G.save["potions"] -= 1
        player["hp"] = min(max_hp(), player["hp"] + max_hp() * 0.45)
        persist(G.save)
        sfx("heal")
        float_text(player["x"], player["y"] - 70, "poção", "#b6ffb0")

    axis = (1 if G.down.get("ArrowRight") or G.down.get("KeyD") else 0) - (1 if G.down.get("ArrowLeft") or G.down.get("KeyA") else 0)
    if player["dash"] > 0:
        player["dash"] -= dt
        player["vx"] = player["dashDir"] * 1120
        player["vy"] = 0
    else:
        max_sp = 215 * speed_mul()
        if axis:
            player["dir"] = axis
            player["vx"] += axis * 2400 * speed_mul() * dt
        else:
            player["vx"] *= max(0, 1 - dt * 12)
        player["vx"] = clamp(player["vx"], -max_sp, max_sp)
        player["vy"] += (2600 if player["slam"] else 1900) * dt
        if player["wallDir"] and has("wall") and not player["onGround"] and player["vy"] > 50:
            player["vy"] = 50
        player["vy"] = min(player["vy"], 900)
    player["blocked"] = False
    was_slam = player["slam"]
    move_body(player, dt)
    if was_slam and player["onGround"]:
        land_slam()

    player["wallDir"] = 0
    if not player["onGround"]:
        if blocked_at(player["x"] + player["hw"] + 3, player["y"] - 16):
            player["wallDir"] = 1
        elif blocked_at(player["x"] - player["hw"] - 3, player["y"] - 16):
            player["wallDir"] = -1
    if player["onGround"]:
        player["coyote"] = 0.12
        player["jumpsLeft"] = 1
    else:
        player["coyote"] = max(0, player["coyote"] - dt)
    if player["wallDir"]:
        player["wallCoy"] = 0.12
    else:
        player["wallCoy"] = max(0, player["wallCoy"] - dt)

    arena = G.world.get("arena")
    if arena and arena["locked"]:
        player["x"] = clamp(player["x"], arena["x"] + 24, arena["x"] + arena["w"] - 24)
    player["x"] = clamp(player["x"], 20, G.world["w"] - 20)

    if player["onGround"] and player["y"] < 600:
        wide = None
        for p in G.world["platforms"]:
            if p["dead"] or p.get("gate") or p["w"] <= 140:
                continue
            if overlap_x(player, p) and abs(player["y"] - p["y"]) < 4:
                wide = p
                break
        if wide and wide["x"] + 40 < player["x"] < wide["x"] + wide["w"] - 40:
            G.world["checkpoint"]["x"] = player["x"]
            G.world["checkpoint"]["y"] = wide["y"]
    if player["y"] > 640:
        if G.mode == "hub":
            player["x"] = 140
            player["y"] = GROUND
        else:
            hurt_player(12, player["x"])
            player["x"] = G.world["checkpoint"]["x"]
            player["y"] = G.world["checkpoint"]["y"]
        player["vx"] = 0
        player["vy"] = 0


def update_enemies(dt):
    player = G.player
    for enemy in G.world["enemies"]:
        if enemy["gone"]:
            continue
        enemy["iframe"] = max(0, enemy["iframe"] - dt)
        enemy["touch"] = max(0, enemy["touch"] - dt)
        enemy["timer"] -= dt
        see = abs(player["x"] - enemy["x"]) < 420 and abs(player["y"] - enemy["y"]) < 160
        if enemy["fly"]:
            goal = player["x"] if see else enemy["home"]
            enemy["dir"] = -1 if goal < enemy["x"] else 1
            enemy["x"] += enemy["dir"] * enemy["speed"] * dt
            enemy["y"] = clamp(enemy["baseY"] + math.sin(G.time * 3 + enemy["home"]) * 18, 160, GROUND - 20)
        elif enemy["ai"] == "charge":
            if enemy["state"] == "walk":
                if enemy["x"] > enemy["home"] + 90:
                    enemy["dir"] = -1
                elif enemy["x"] < enemy["home"] - 90:
                    enemy["dir"] = 1
                enemy["vx"] = enemy["dir"] * enemy["speed"] * 0.45
                if see and enemy["timer"] <= 0:
                    enemy["state"] = "wind"
                    enemy["timer"] = 0.38
                    enemy["dir"] = -1 if player["x"] < enemy["x"] else 1
            elif enemy["state"] == "wind":
                enemy["vx"] = 0
                if enemy["timer"] <= 0:
                    enemy["state"] = "dash"
                    enemy["timer"] = 0.42
                    enemy["vx"] = enemy["dir"] * 320
            else:
                enemy["vx"] = enemy["dir"] * 320
                if enemy["timer"] <= 0 or enemy["blocked"]:
                    enemy["state"] = "walk"
                    enemy["timer"] = 1.1
                    enemy["vx"] = 0
            enemy["vy"] += 1900 * dt
            enemy["blocked"] = False
            move_body(enemy, dt)
            if enemy["onGround"] and enemy["state"] == "walk":
                ahead = enemy["x"] + enemy["dir"] * (enemy["hw"] + 10)
                if not supported(ahead, enemy["y"]) or blocked_at(ahead, enemy["y"] - 16):
                    enemy["dir"] *= -1
        elif enemy["ai"] == "shooter":
            want = -1 if player["x"] < enemy["x"] else 1
            ahead = enemy["x"] + want * (enemy["hw"] + 10)
            enemy["dir"] = -want if enemy["onGround"] and not supported(ahead, enemy["y"]) else want
            enemy["vx"] = enemy["dir"] * enemy["speed"] * 0.35
            if enemy["timer"] <= 0 and see:
                enemy["timer"] = 2.15
                sx, sy = enemy["x"], enemy["y"] - enemy["h"] * 0.55
                dx, dy = player["x"] - sx, (player["y"] - 28) - sy
                mag = math.hypot(dx, dy) or 1
                G.world["hazards"].append({
                    "kind": "proj", "x": sx, "y": sy, "vx": dx / mag * 230, "vy": dy / mag * 230,
                    "r": 12, "dmg": enemy["dmg"], "life": 3, "spr": enemy["shot"] or 2, "friendly": False,
                })
            enemy["vy"] += 1900 * dt
            move_body(enemy, dt)
        else:
            enemy["vx"] = enemy["dir"] * enemy["speed"]
            if enemy["ai"] == "hopper" and enemy["onGround"] and enemy["timer"] <= 0:
                enemy["vy"] = -460
                enemy["timer"] = 1.35
                enemy["dir"] = -1 if player["x"] < enemy["x"] else 1
            enemy["vy"] += 1900 * dt
            move_body(enemy, dt)
            if enemy["onGround"]:
                ahead = enemy["x"] + enemy["dir"] * (enemy["hw"] + 10)
                if not supported(ahead, enemy["y"]) or blocked_at(ahead, enemy["y"] - 12):
                    enemy["dir"] *= -1
        if not enemy["fly"] and enemy["y"] > 700:
            enemy["gone"] = True
        if enemy["gone"]:
            continue
        if (
            enemy["touch"] <= 0 and player["hurt"] <= 0
            and abs(player["x"] - enemy["x"]) < enemy["hw"] + player["hw"]
            and abs((player["y"] - player["h"] / 2) - (enemy["y"] - enemy["h"] / 2)) < (player["h"] + enemy["h"]) / 2
        ):
            enemy["touch"] = 0.6
            hurt_player(enemy["dmg"], enemy["x"])
    if 0.05 < player["atk"] < 0.18:
        box = melee_box()
        for enemy in G.world["enemies"]:
            if enemy["gone"] or enemy["lastSwing"] == player["swing"]:
                continue
            eb = {"x": enemy["x"] - enemy["hw"], "y": enemy["y"] - enemy["h"], "w": enemy["hw"] * 2, "h": enemy["h"]}
            if rects(box, eb):
                enemy["lastSwing"] = player["swing"]
                damage_enemy(enemy, (15 + enemy["type"] * 2) * dmg_mul(), player["dir"] * 160)
        boss = G.world.get("boss")
        if boss and boss["lastSwing"] != player["swing"]:
            bb = {"x": boss["x"] - boss["hw"], "y": boss["y"] - boss["h"], "w": boss["hw"] * 2, "h": boss["h"]}
            if rects(box, bb):
                boss["lastSwing"] = player["swing"]
                damage_boss(18 * dmg_mul())
    G.world["enemies"] = [e for e in G.world["enemies"] if not e["gone"]]


def spawn_pattern(boss):
    direction = math.copysign(1, player_dx(boss)) if player_dx(boss) else -1
    arena = G.world["arena"]
    floor = arena["floor"]

    def spr(n, extra):
        base = {"kind": "proj", "friendly": False, "life": 3.2, "r": 14, "boss": True, "spr": n}
        base.update(extra)
        return base

    pattern = boss["pattern"]
    if pattern == "saws":
        for i in range(3):
            G.world["hazards"].append(spr(1, {"x": boss["x"], "y": floor - 36 - i * 34, "vx": direction * 280, "vy": 0, "dmg": 12, "spin": True}))
    elif pattern in ("charge", "roll"):
        boss["vx"] = direction * (520 if pattern == "roll" else 430)
        boss["t"] = 0.7 if pattern == "roll" else 0.55
    elif pattern == "slam":
        r = 62
        G.world["hazards"].append({"kind": "zone", "x": boss["aimX"] - r, "y": floor - 36, "w": r * 2, "h": 40, "dmg": 14, "warn": 0.42, "life": 0.62, "spr": 7, "next": 0})
    elif pattern == "spit":
        for i in range(-1, 2):
            G.world["hazards"].append(spr(2, {"x": boss["x"] + direction * 20, "y": boss["y"] - 90, "vx": direction * 180 + i * 50, "vy": -300, "grav": 720, "dmg": 11}))
    elif pattern == "tire":
        G.world["hazards"].append(spr(2, {"x": boss["x"], "y": floor - 18, "vx": direction * 340, "vy": 0, "dmg": 12, "r": 16}))
    elif pattern == "suction":
        boss["t"] = 1.15
        G.world["hazards"].append({"kind": "zone", "x": boss["aimX"] - 50, "y": floor - 34, "w": 100, "h": 34, "dmg": 10, "warn": 0.35, "life": 0.9, "spr": 2, "next": 0})
    elif pattern == "clouds":
        for i in range(3):
            G.world["hazards"].append(spr(3, {"x": boss["x"], "y": boss["y"] - 80, "vx": direction * 90 + (i - 1) * 40, "vy": -30 - i * 20, "dmg": 10, "life": 4, "r": 18}))
    elif pattern == "hop":
        boss["vy"] = -560
        boss["vx"] = direction * 180
        boss["hop"] = True
        boss["t"] = 1.4
    elif pattern in ("rain", "icicles"):
        for _ in range(4):
            x = arena["x"] + 80 + random.random() * (arena["w"] - 160)
            G.world["hazards"].append({
                "kind": "zone", "x": x - 28, "y": floor - 36, "w": 56, "h": 40, "dmg": 12,
                "warn": 0.62, "life": 0.86, "spr": 3 if pattern == "rain" else 4, "next": 0,
            })
    elif pattern in ("shards", "ring"):
        n = 8 if pattern == "ring" else 5
        for i in range(n):
            ang = (i / n) * math.pi * 2 if pattern == "ring" else (-0.7 + i * 0.35)
            G.world["hazards"].append(spr(5 if pattern == "ring" else 4, {
                "x": boss["x"], "y": boss["y"] - 80, "vx": math.cos(ang) * 230, "vy": math.sin(ang) * 230, "dmg": 11,
            }))
    elif pattern == "wind":
        boss["t"] = 1.2
        boss["wind"] = direction
    elif pattern in ("beam", "laser"):
        y = clamp(boss["aimY"], 180, floor - 50)
        left = min(boss["x"], boss["x"] + direction * 640)
        G.world["hazards"].append({"kind": "zone", "x": left, "y": y - 14, "w": 640, "h": 28, "dmg": 16, "warn": 0.4, "life": 0.72, "spr": 5, "beam": True, "next": 0})
    elif pattern == "blink":
        nx = G.player["x"] + (150 if G.player["x"] < boss["x"] else -150)
        boss["x"] = clamp(nx, arena["x"] + 100, arena["x"] + arena["w"] - 100)
        G.world["hazards"].append({"kind": "zone", "x": boss["x"] - 60, "y": floor - 40, "w": 120, "h": 40, "dmg": 14, "warn": 0.28, "life": 0.5, "spr": 7, "next": 0})
    elif pattern == "missile":
        for i in range(2):
            G.world["hazards"].append(spr(6, {"x": boss["x"], "y": boss["y"] - 70 - i * 20, "vx": direction * 80, "vy": -40, "dmg": 13, "homing": True, "life": 4}))
    elif pattern == "pound":
        G.world["hazards"].append({"kind": "zone", "x": arena["x"] + 20, "y": floor - 34, "w": arena["w"] - 40, "h": 34, "dmg": 15, "warn": 0.55, "life": 0.85, "spr": 7, "next": 0})
    elif pattern == "summon" and len(G.world["enemies"]) < 3:
        G.world["enemies"].append(spawn_enemy(0, arena["x"] + 180, floor, boss["def"], G.world["tier"]))
        G.world["enemies"].append(spawn_enemy(2, arena["x"] + arena["w"] - 180, floor, boss["def"], G.world["tier"]))


def player_dx(boss):
    return G.player["x"] - boss["x"]


def update_boss(dt):
    boss = G.world.get("boss")
    if not boss or boss["rewarded"]:
        return
    boss["flash"] = max(0, boss["flash"] - dt)
    if boss["state"] == "dead":
        boss["dying"] -= dt
        boss["y"] += 30 * dt
        if boss["dying"] <= 0:
            defeat_boss()
        return
    arena = G.world["arena"]
    if not arena["locked"] or boss["state"] == "wait":
        return
    player = G.player
    boss["dir"] = -1 if player["x"] < boss["x"] else 1
    if boss["state"] != "intro":
        if player["hurt"] <= 0 and abs(player["x"] - boss["x"]) < boss["hw"] + player["hw"] - 8 and player["y"] > boss["y"] - boss["h"] and player["y"] - player["h"] < boss["y"]:
            hurt_player(round(14 * G.world["tier"]["dmg"] * (1.12 if boss["phase"] > 1 else 1)), boss["x"])
        if boss["def"].get("orbit") and boss["phase"] >= 2:
            ang = G.time * 3.2
            for i in range(2):
                ox = boss["x"] + math.cos(ang + i * math.pi) * 92
                oy = boss["y"] - 70 + math.sin(ang + i * math.pi) * 26
                if player["hurt"] <= 0 and math.hypot(player["x"] - ox, (player["y"] - 24) - oy) < 22:
                    hurt_player(round(10 * G.world["tier"]["dmg"]), ox)
    if boss["state"] == "intro":
        boss["t"] -= dt
        if boss["t"] <= 0:
            boss["state"] = "idle"
            boss["t"] = 0.45
        return
    if boss["state"] == "roar":
        boss["t"] -= dt
        if boss["t"] <= 0:
            boss["state"] = "idle"
            boss["t"] = 0.35
        return
    if boss["state"] == "idle":
        dist = player["x"] - boss["x"]
        if abs(dist) > 210:
            boss["x"] += math.copysign(55 * dt, dist)
        boss["x"] = clamp(boss["x"], arena["x"] + 90, arena["x"] + arena["w"] - 90)
        boss["t"] -= dt
        if boss["t"] <= 0:
            if boss["phase"] == 1:
                patterns = boss["def"]["p1"]
            elif boss["phase"] == 2:
                patterns = boss["def"]["p2"]
            else:
                patterns = boss["def"].get("p3") or boss["def"]["p2"]
            boss["pattern"] = patterns[boss["step"] % len(patterns)]
            boss["step"] += 1
            boss["state"] = "tell"
            boss["t"] = 0.58
            boss["aimX"] = player["x"]
            boss["aimY"] = player["y"] - 24
        return
    if boss["state"] == "tell":
        boss["t"] -= dt
        if boss["t"] <= 0:
            boss["state"] = "act"
            boss["t"] = 0.45
            boss["wind"] = 0
            boss["hop"] = False
            spawn_pattern(boss)
        return
    if boss["state"] == "act":
        if boss["pattern"] in ("charge", "roll"):
            boss["x"] += boss["vx"] * dt
            lo, hi = arena["x"] + 80, arena["x"] + arena["w"] - 80
            if boss["x"] < lo or boss["x"] > hi:
                boss["x"] = clamp(boss["x"], lo, hi)
                boss["t"] = 0
        if boss["hop"]:
            boss["vy"] += 1700 * dt
            boss["x"] += boss["vx"] * dt
            boss["y"] += boss["vy"] * dt
            boss["x"] = clamp(boss["x"], arena["x"] + 80, arena["x"] + arena["w"] - 80)
            if boss["y"] >= arena["floor"]:
                boss["y"] = arena["floor"]
                boss["hop"] = False
                boss["t"] = 0
                G.world["hazards"].append({"kind": "zone", "x": boss["x"] - 70, "y": arena["floor"] - 40, "w": 140, "h": 40, "dmg": 14, "warn": 0.05, "life": 0.28, "spr": 3, "next": 0})
                G.shake = 8
        if boss["wind"]:
            player["vx"] += boss["wind"] * 420 * dt
        if boss["pattern"] == "suction":
            player["vx"] += math.copysign(380 * dt, boss["x"] - player["x"] or 1)
        boss["t"] -= dt
        if boss["t"] <= 0:
            boss["state"] = "recover"
            boss["t"] = 0.42 if boss["phase"] > 1 else 0.58
            boss["vx"] = 0
        return
    if boss["state"] == "recover":
        boss["t"] -= dt
        if boss["t"] <= 0:
            boss["state"] = "idle"
            boss["t"] = 0.32 if boss["phase"] > 1 else 0.5


def update_hazards(dt):
    player = G.player
    for h in G.world["hazards"]:
        if not h.get("permanent"):
            h["life"] -= dt
        if h.get("warn", 0) > 0:
            h["warn"] -= dt
        if h["kind"] == "proj":
            if h.get("grav"):
                h["vy"] += h["grav"] * dt
            if h.get("homing"):
                dx = player["x"] - h["x"]
                dy = (player["y"] - 24) - h["y"]
                mag = math.hypot(dx, dy) or 1
                h["vx"] += (dx / mag) * 280 * dt
                h["vy"] += (dy / mag) * 280 * dt
            h["x"] += h["vx"] * dt
            h["y"] += h["vy"] * dt
            inside = any(
                not p["dead"] and p["x"] < h["x"] < p["x"] + p["w"] and p["y"] + 6 < h["y"] < p["y"] + p["h"]
                for p in G.world["platforms"]
            )
            if inside:
                h["life"] = 0
            if h.get("friendly"):
                for enemy in G.world["enemies"]:
                    if math.hypot(enemy["x"] - h["x"], (enemy["y"] - enemy["h"] / 2) - h["y"]) < enemy["hw"] + h["r"]:
                        damage_enemy(enemy, h["dmg"], math.copysign(80, h["vx"] or 1))
                        h["life"] = 0
                boss = G.world.get("boss")
                if boss and not boss["rewarded"] and math.hypot(boss["x"] - h["x"], (boss["y"] - boss["h"] / 2) - h["y"]) < boss["hw"]:
                    damage_boss(h["dmg"])
                    h["life"] = 0
                for p in G.world["platforms"]:
                    if p.get("gate") == "shot" and circle_rect(h["x"], h["y"], h["r"], p):
                        p["dead"] = True
                        h["life"] = 0
                        burst(h["x"], h["y"], 5, 4)
                        sfx("boom")
            elif player["hurt"] <= 0 and math.hypot(player["x"] - h["x"], (player["y"] - 24) - h["y"]) < player["hw"] + h["r"]:
                dmg = max(1, round(h["dmg"] * G.world["tier"]["dmg"])) if h.get("boss") else h["dmg"]
                hurt_player(dmg, h["x"])
                h["life"] = 0
        elif h["kind"] == "zone" and h.get("warn", 0) <= 0 and player["hurt"] <= 0:
            h["next"] = h.get("next", 0) - dt
            box = {"x": player["x"] - player["hw"], "y": player["y"] - player["h"], "w": player["hw"] * 2, "h": player["h"]}
            if h["next"] <= 0 and rects(box, h):
                scaled = h["dmg"] if h.get("permanent") or h["dmg"] > 20 else round(h["dmg"] * (G.world["tier"]["dmg"] if G.world.get("tier") else 1))
                hurt_player(scaled, h["x"] + h["w"] / 2)
                h["next"] = 0.48
                if not h.get("permanent"):
                    h["life"] = min(h["life"], 0.05)
    G.world["hazards"] = [h for h in G.world["hazards"] if h.get("permanent") or h["life"] > 0]
    G.world["platforms"] = [p for p in G.world["platforms"] if not p["dead"]]


def update_drops(dt):
    player = G.player
    for drop in G.world["drops"]:
        drop["life"] -= dt
        drop["vy"] = min(420, drop["vy"] + 900 * dt)
        drop["y"] += drop["vy"] * dt
        if drop["y"] > GROUND:
            drop["y"] = GROUND
            drop["vy"] = 0
        dist = math.hypot(player["x"] - drop["x"], (player["y"] - 20) - drop["y"])
        if dist < 70:
            drop["x"] += (player["x"] - drop["x"]) * 8 * dt
            drop["y"] += ((player["y"] - 20) - drop["y"]) * 8 * dt
        if dist < 22:
            G.save["crystals"] += drop["value"]
            persist(G.save)
            float_text(drop["x"], drop["y"] - 10, "+" + str(drop["value"]), "#9fd8ff")
            sfx("coin")
            if heal_fraction(0.5):
                float_text(drop["x"], drop["y"] - 28, "meia vida", "#b6ffb0")
            drop["life"] = 0
    G.world["drops"] = [d for d in G.world["drops"] if d["life"] > 0]
    for p in G.world["particles"]:
        p["life"] -= dt
        p["x"] += p["vx"] * dt
        p["y"] += p["vy"] * dt
    G.world["particles"] = [p for p in G.world["particles"] if p["life"] > 0]
    for t in G.world["texts"]:
        t["life"] -= dt
        t["y"] -= 24 * dt
    G.world["texts"] = [t for t in G.world["texts"] if t["life"] > 0]


def try_chests():
    if not G.pressed.get("KeyE"):
        return
    for chest in G.world.get("chests") or []:
        if G.save["chests"].get(chest["id"]):
            continue
        if abs(G.player["x"] - chest["x"]) < 36 and abs(G.player["y"] - chest["y"]) < 30:
            G.save["chests"][chest["id"]] = True
            G.save["crystals"] += chest["value"]
            persist(G.save)
            sfx("coin")
            float_text(chest["x"], chest["y"] - 40, "+" + str(chest["value"]) + " baú", "#9fd8ff")
            if heal_fraction(1):
                float_text(chest["x"], chest["y"] - 58, "vida cheia", "#b6ffb0")


def defeat_boss():
    boss = G.world["boss"]
    if not boss or boss["rewarded"]:
        return
    boss["rewarded"] = True
    zone = G.world["zone"]
    zid = zone["id"]
    first = not G.save["cleared"].get(zid)
    reward = round((58 if first else 26) * G.world["tier"]["reward"])
    G.save["crystals"] += reward
    if first:
        G.save["cleared"][zid] = True
        if zid != "industrial":
            G.save["tierCleared"][zid] = G.world["tier"]["id"]
        if zone.get("ability"):
            G.save["abilities"][zone["ability"]] = True
    G.save["pendingZone"] = zid
    G.save["pendingMsg"] = RESTORE[zid] if first else "Você cruzou esta região de novo."
    persist(G.save)
    if zid == "industrial" and first:
        open_ending(reward)
    else:
        open_unlock(first, reward)


def open_unlock(first, reward):
    zone = G.world["zone"]
    ab = ABILITIES.get(zone.get("ability"))
    kicker = "Chefe derrotado" if first else "Reviver"
    title = ab["name"] if first and ab else zone["bossName"] + " caiu"
    desc = ab["desc"] if first and ab else "Você já conhecia este lugar. +" + str(reward) + " cristais."
    restore = ((RESTORE[zone["id"]] + " ") if first else "") + "+" + str(reward) + " cristais."
    open_panel("unlock", kicker, title, [desc, restore], [
        {"label": "Voltar ao santuário", "fn": start_hub, "enabled": True},
    ])


def open_ending(reward):
    G.save["pendingMsg"] = RESTORE["industrial"] + " +" + str(reward) + " cristais."
    persist(G.save)
    open_panel(
        "ending", "Final", "O planeta respira",
        [
            "A Fornalha-Mãe apagou. O Vale Industrial ficou em silêncio e o santuário recuperou cada pedaço: floresta, marés, pântano, montanha e cristal.",
            "Kai recebeu o Pulso do Planeta. Lumi volta a brilhar por inteiro.",
        ],
        [{"label": "Caminhar pelo santuário", "fn": start_hub, "enabled": True}],
    )


def update_hub(dt):
    update_player(dt)
    if G.ui_open:
        return
    if G.pressed.get("KeyE"):
        if abs(G.player["x"] - 220) < 70 and abs(G.player["y"] - GROUND) < 20:
            open_shop()
        else:
            for i, zone in enumerate(ZONES):
                if abs(G.player["x"] - PORTAL_X[i]) < 54 and abs(G.player["y"] - GROUND) < 24:
                    open_zone(zone["id"])
    if G.pressed.get("Escape"):
        open_pause()


def update_level(dt):
    update_player(dt)
    if G.ui_open:
        return
    arena = G.world.get("arena")
    if arena and not arena["locked"] and arena["lock"] < G.player["x"] < arena["x"] + arena["w"]:
        arena["locked"] = True
        G.world["platforms"].append(G.world["leftWall"])
        G.world["boss"]["state"] = "intro"
        G.world["boss"]["t"] = 1.15
        G.world["banner"] = G.world["zone"]["bossName"]
        G.world["bannerT"] = 2.2
        sfx("roar")
    update_enemies(dt)
    update_boss(dt)
    update_hazards(dt)
    update_drops(dt)
    try_chests()
    if G.pressed.get("Escape"):
        open_pause()


def step(dt):
    if G.ui_open or G.mode == "title":
        return
    if G.mode == "hub":
        update_hub(dt)
    else:
        update_level(dt)
    if G.world["bannerT"] > 0:
        G.world["bannerT"] -= dt
    target = clamp(G.player["x"] - VW * 0.42, 0, max(0, G.world["w"] - VW))
    G.camx += (target - G.camx) * min(1, dt * 6)
    arena = G.world.get("arena")
    if arena and arena["locked"]:
        G.camx = clamp(G.camx, arena["x"], max(arena["x"], arena["x"] + arena["w"] - VW))


def retry_level():
    if G.world and G.world.get("zone"):
        start_level(G.world["zone"], G.world["tier"], G.world["replay"])
    else:
        start_hub()


def open_intro():
    open_panel(
        "intro", "Lumi", "O santuário está ferido",
        [
            "Escolha qualquer portal, menos o Vale Industrial. A primeira região entra no grau fácil. Cada chefe derrotado sobe o grau da próxima e cura um pedaço da base.",
            "Na loja você troca cristais por vida, força, velocidade e poções. Segredos nas fases pedem as habilidades dos chefes. Dá para voltar depois.",
            "Baús enchem a vida. Cristais no chão devolvem metade da vida.",
        ],
        [{"label": "Entendi", "fn": ack_intro, "enabled": True}],
    )


def ack_intro():
    G.save["intro"] = True
    persist(G.save)
    close_panels()


def open_pause():
    buttons = [
        {"label": "Continuar", "fn": close_panels, "enabled": True},
        {"label": "Controles", "fn": open_how, "enabled": True},
    ]
    if G.mode == "level":
        buttons.append({"label": "Santuário", "fn": start_hub, "enabled": True})
    open_panel("pause", "Pausa", "Guardiões", [], buttons)


def open_how():
    back = close_panels if G.mode == "title" else open_pause
    open_panel(
        "how", "Controles", "Como jogar",
        [
            "A D ou setas — andar",
            "Espaço ou W — pular. Aperte de novo no ar para o segundo pulo",
            "J — ataque. Segure baixo e aperte J no ar para os esporos",
            "Shift — Correnteza, o dash, depois do chefe das marés",
            "K — Luz do Cristal, depois do Coração",
            "Q — poção. E — loja, portais e baús",
            "O baú enche a vida. Cristais no chão devolvem metade da vida.",
            "Esc — pausa. Setas e Enter também funcionam nos menus.",
        ],
        [{"label": "Fechar", "fn": back, "enabled": True}],
    )


def open_credits():
    open_panel(
        "credits", "Créditos", "Guardiões da Natureza",
        [
            "Kai e Lumi atravessam florestas, marés, pântanos, montanhas e o coração do planeta para apagar o Vale Industrial.",
            "Cada chefe entrega uma habilidade. A primeira região escolhida é a mais fácil. A próxima fica mais dura, até o vale final.",
        ],
        [{"label": "Fechar", "fn": close_panels, "enabled": True}],
    )


def open_shop():
    lines = ["Cristais: " + str(G.save["crystals"])]
    buttons = []
    for item in SHOP_ITEMS:
        if item["id"] == "pot":
            full = G.save["potions"] >= 3
            label = "Cheia" if full else item["name"] + " — " + str(item["price"])
            enabled = not full and G.save["crystals"] >= item["price"]
            buttons.append({
                "label": label,
                "fn": (lambda price=item["price"]: buy_potion(price)),
                "enabled": enabled,
            })
            lines.append(item["desc"] + " Na bolsa: " + str(G.save["potions"]) + "/3.")
        else:
            rank = G.save[item["rank"]] or 0
            if rank >= item["max"]:
                buttons.append({"label": item["name"] + " " + str(rank) + "/" + str(item["max"]) + " — Máximo", "fn": lambda: None, "enabled": False})
            else:
                price = item["prices"][rank]
                buttons.append({
                    "label": item["name"] + " " + str(rank) + "/" + str(item["max"]) + " — " + str(price),
                    "fn": (lambda it=item, price=price, rank=rank: buy_rank(it, price, rank)),
                    "enabled": G.save["crystals"] >= price,
                })
            lines.append(item["desc"])
    buttons.append({"label": "Fechar", "fn": close_panels, "enabled": True})
    open_panel("shop", "Loja do santuário", "Troca de cristais", lines, buttons)


def buy_potion(price):
    if G.save["crystals"] < price or G.save["potions"] >= 3:
        return
    G.save["crystals"] -= price
    G.save["potions"] += 1
    persist(G.save)
    sfx("buy")
    open_shop()


def buy_rank(item, price, rank):
    if G.save["crystals"] < price:
        return
    G.save["crystals"] -= price
    G.save[item["rank"]] = rank + 1
    if G.player:
        G.player["hp"] = max_hp()
    persist(G.save)
    sfx("buy")
    open_shop()


def open_zone(zid):
    zone = zone_by_id(zid)
    tier = preview_tier(G.save, zid)
    locked = zid == "industrial" and cleared_count(G.save) < 5
    replay = bool(G.save["cleared"].get(zid))
    n = cleared_count(G.save)
    kicker = "Região restaurada" if replay else "Escolher região"
    if zid == "industrial":
        tier_text = "Grau Final. Esta fase só abre depois das outras cinco e é sempre a mais dura, não importa a ordem anterior."
    elif replay:
        tier_text = "Reviver no grau em que você a venceu: " + tier["name"] + ". A habilidade já é sua. Inimigos e o chefe voltam, com menos cristais."
    else:
        order = ["primeira", "segunda", "terceira", "quarta", "quinta"]
        word = order[n] if n < len(order) else "próxima"
        tier_text = "Esta será a sua " + word + " região, então o grau é " + tier["name"] + ". A dificuldade segue a ordem das vitórias, não o nome do mapa."
    names = ", ".join(e["name"] for e in zone["enemies"])
    enemies = "Três espécies: " + names + ". Chefe: " + zone["bossName"] + ", " + zone["bossSub"] + "."
    lines = [tier_text, enemies]
    if locked:
        lines.append("O portal ainda está selado. Restaure as outras cinco regiões.")
    open_panel("zone", kicker, zone["name"], lines, [
        {"label": "Entrar", "fn": (lambda z=zone, t=tier, r=replay and zid != "industrial": start_level(z, t, r)), "enabled": not locked},
        {"label": "Voltar", "fn": close_panels, "enabled": True},
    ])


def new_game():
    from gn.content import default_save
    G.save = default_save()
    persist(G.save)
    G.has_save = True
    start_hub()


def confirm_new():
    open_panel(
        "confirm", "Novo jogo", "Apagar o progresso?",
        ["Cristais, habilidades e regiões restauradas voltam ao começo."],
        [
            {"label": "Apagar e começar", "fn": new_game, "enabled": True},
            {"label": "Cancelar", "fn": close_panels, "enabled": True},
        ],
    )


def escape_panel():
    if not G.panel:
        return
    if G.panel["id"] in ("dead", "unlock", "ending"):
        return
    if G.mode == "title":
        close_panels()
    elif G.panel["id"] == "pause":
        close_panels()
    elif G.panel["id"] in ("how", "shop", "zone", "intro", "confirm"):
        if G.mode == "title":
            close_panels()
        elif G.panel["id"] == "how":
            open_pause()
        else:
            close_panels()


def move_sel(delta):
    panel = G.panel
    if not panel:
        return
    n = len(panel["buttons"])
    if n == 0:
        return
    i = panel["sel"]
    for _ in range(n):
        i = (i + delta) % n
        if panel["buttons"][i]["enabled"]:
            panel["sel"] = i
            return


def activate_sel():
    panel = G.panel
    if not panel or not panel["buttons"]:
        return
    btn = panel["buttons"][panel["sel"]]
    if btn["enabled"]:
        btn["fn"]()
