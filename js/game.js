const VW = 960;
const VH = 540;
const GROUND = 448;
const SAVE_KEY = "guardioes-natureza-1";

const TIERS = [
  { id: 0, name: "Fácil", hp: 1, dmg: 1, spd: 1, reward: 1 },
  { id: 1, name: "Médio", hp: 1.32, dmg: 1.22, spd: 1.05, reward: 1.25 },
  { id: 2, name: "Difícil", hp: 1.68, dmg: 1.45, spd: 1.1, reward: 1.5 },
  { id: 3, name: "Brutal", hp: 2.1, dmg: 1.7, spd: 1.14, reward: 1.8 },
  { id: 4, name: "Extremo", hp: 2.55, dmg: 1.95, spd: 1.18, reward: 2.15 },
];
const TIER_FINAL = { id: 5, name: "Final", hp: 3.15, dmg: 2.2, spd: 1.2, reward: 3 };

const ABILITIES = {
  double: { name: "Raiz Ascendente", desc: "O segundo pulo, no mesmo botão, sobe ainda mais alto e alcança as copas." },
  dash: { name: "Correnteza", desc: "Shift. Um impulso com um instante de invulnerabilidade. Cruza vãos que o pulo não alcança." },
  spores: { name: "Esporos", desc: "No ar, seta para baixo + J. Você despenca e solta uma nuvem. Quebra bulbos do pântano." },
  wall: { name: "Garra Glacial", desc: "Encoste numa parede no ar e pule de novo. Sirva-se dos poços verticais." },
  shot: { name: "Luz do Cristal", desc: "K. Um tiro mágico que fere de longe e desfaz barreiras de cristal." },
  pulse: { name: "Pulso do Planeta", desc: "O vale silenciou. O santuário ficou inteiro." },
};

const RESTORE = {
  floresta: "As árvores queimadas e os troncos cortados voltaram a ser uma floresta frondosa.",
  mares: "A água poluída clareou. O lixo sumiu e os peixes voltaram às marés.",
  pantano: "O lodo morto floresceu: samambaias, flores e vida no pântano.",
  montanhas: "O santuário quebrado da montanha foi reconstruído.",
  coracao: "O cristal do planeta voltou a brilhar no centro da base.",
  industrial: "A fumaça do vale se apagou. Cada canto do santuário está vivo.",
};

const ZONES = [
  {
    id: "floresta",
    name: "Floresta Esquecida",
    tile: 0,
    ability: "double",
    bossName: "Deforestor Gamma",
    bossSub: "O Triturador",
    bossHp: 420,
    bossHw: 78,
    bossH: 118,
    drawH: 250,
    p1: ["saws", "charge", "slam"],
    p2: ["saws", "charge", "slam", "saws"],
    orbit: true,
    enemies: [
      { name: "Espinhento", ai: "patrol", hp: 34, dmg: 8, speed: 72, hw: 18, h: 44 },
      { name: "Serrídeo", ai: "charge", hp: 28, dmg: 11, speed: 86, hw: 20, h: 36 },
      { name: "Tronco", ai: "hopper", hp: 54, dmg: 13, speed: 42, hw: 22, h: 50 },
    ],
  },
  {
    id: "mares",
    name: "Costa das Marés",
    tile: 1,
    ability: "dash",
    bossName: "Polluto",
    bossSub: "O Fardo do Oceano",
    bossHp: 460,
    bossHw: 70,
    bossH: 130,
    drawH: 270,
    p1: ["spit", "slam", "tire"],
    p2: ["spit", "suction", "slam"],
    enemies: [
      { name: "Borra", ai: "patrol", hp: 36, dmg: 8, speed: 58, hw: 20, h: 42 },
      { name: "Caranguejo-Lata", ai: "shooter", hp: 32, dmg: 9, speed: 48, hw: 24, h: 40, shot: 2 },
      { name: "Arpão", ai: "flyer", hp: 24, dmg: 10, speed: 90, hw: 22, h: 32 },
    ],
  },
  {
    id: "pantano",
    name: "Pântano Tóxico",
    tile: 2,
    ability: "spores",
    bossName: "Miasma",
    bossSub: "A Podridão",
    bossHp: 500,
    bossHw: 74,
    bossH: 140,
    drawH: 280,
    p1: ["clouds", "hop", "rain"],
    p2: ["rain", "hop", "clouds"],
    enemies: [
      { name: "Gosma", ai: "hopper", hp: 40, dmg: 9, speed: 50, hw: 18, h: 36 },
      { name: "Moscovórtice", ai: "flyer", hp: 26, dmg: 10, speed: 100, hw: 22, h: 34 },
      { name: "Barril Vivo", ai: "shooter", hp: 48, dmg: 11, speed: 40, hw: 20, h: 44, shot: 3 },
    ],
  },
  {
    id: "montanhas",
    name: "Montanhas Eternas",
    tile: 3,
    ability: "wall",
    bossName: "Avalanche Prime",
    bossSub: "O Inverno de Ferro",
    bossHp: 540,
    bossHw: 76,
    bossH: 140,
    drawH: 280,
    p1: ["shards", "roll", "wind"],
    p2: ["shards", "roll", "icicles"],
    enemies: [
      { name: "Morcego-Gelo", ai: "flyer", hp: 26, dmg: 9, speed: 110, hw: 20, h: 32 },
      { name: "Rolador", ai: "charge", hp: 46, dmg: 13, speed: 70, hw: 22, h: 40 },
      { name: "Drone-Geada", ai: "shooter", hp: 30, dmg: 10, speed: 54, hw: 20, h: 36, shot: 4 },
    ],
  },
  {
    id: "coracao",
    name: "Coração do Planeta",
    tile: 4,
    ability: "shot",
    bossName: "Corrupto Cristalino",
    bossSub: "A Lança Partida",
    bossHp: 580,
    bossHw: 72,
    bossH: 145,
    drawH: 290,
    p1: ["beam", "ring", "blink"],
    p2: ["beam", "ring", "blink", "ring"],
    enemies: [
      { name: "Lasca", ai: "flyer", hp: 28, dmg: 10, speed: 95, hw: 18, h: 36 },
      { name: "Ígneo", ai: "charge", hp: 36, dmg: 12, speed: 100, hw: 20, h: 46 },
      { name: "Marionete", ai: "shooter", hp: 40, dmg: 11, speed: 46, hw: 20, h: 50, shot: 5 },
    ],
  },
  {
    id: "industrial",
    name: "Vale Industrial",
    tile: 5,
    ability: "pulse",
    bossName: "Fornalha-Mãe",
    bossSub: "Coração da Fábrica",
    bossHp: 760,
    bossHw: 90,
    bossH: 130,
    drawH: 270,
    p1: ["missile", "laser", "pound"],
    p2: ["missile", "pound", "summon", "laser"],
    p3: ["missile", "laser", "pound", "summon"],
    enemies: [
      { name: "Engrenado", ai: "patrol", hp: 48, dmg: 12, speed: 62, hw: 20, h: 48 },
      { name: "Fumaça", ai: "flyer", hp: 32, dmg: 11, speed: 80, hw: 22, h: 46 },
      { name: "Motosserra", ai: "charge", hp: 44, dmg: 14, speed: 78, hw: 24, h: 40 },
    ],
  },
];

const PORTAL_X = [860, 1220, 1580, 1940, 2300, 2660];
const SHOP_ITEMS = [
  { id: "hp", name: "Vitalidade", desc: "+22 de vida máxima", prices: [32, 58, 96, 150], max: 4, rank: "hpRank" },
  { id: "dmg", name: "Força da Raiz", desc: "+22% de dano", prices: [36, 64, 110, 160], max: 4, rank: "dmgRank" },
  { id: "spd", name: "Passo Leve", desc: "+8% de velocidade", prices: [28, 52, 90], max: 3, rank: "spdRank" },
  { id: "pot", name: "Poção verde", desc: "Cura 45% da vida. Você carrega até 3.", price: 16 },
];

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
ctx.imageSmoothingEnabled = false;

const down = Object.create(null);
const pressed = Object.create(null);
let save = null;
let mode = "title";
let player = null;
let world = null;
let cam = { x: 0, y: 0 };
let time = 0;
let shake = 0;
let S = {};
let uiOpen = false;
let actx = null;

window.addEventListener("keydown", (e) => {
  const keys = ["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "KeyW", "KeyA", "KeyS", "KeyD"];
  if (keys.includes(e.code)) e.preventDefault();
  if (e.code === "Escape") e.preventDefault();
  if (!down[e.code]) pressed[e.code] = true;
  down[e.code] = true;
});
window.addEventListener("keyup", (e) => { down[e.code] = false; });

function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
function zoneById(id) { return ZONES.find((z) => z.id === id); }
function clearedCount() {
  return ZONES.filter((z) => z.id !== "industrial" && save.cleared[z.id]).length;
}
function has(id) { return !!(save && save.abilities[id]); }
function maxHp() { return 100 + 22 * (save.hpRank || 0); }
function healFraction(part) {
  const before = player.hp;
  const cap = maxHp();
  player.hp = Math.min(cap, before + Math.round(cap * part));
  if (player.hp > before) sfx("heal");
  return player.hp - before;
}
function dmgMul() { return 1 + 0.22 * (save.dmgRank || 0); }
function speedMul() { return 1 + 0.08 * (save.spdRank || 0); }

function previewTier(id) {
  if (id === "industrial") return TIER_FINAL;
  if (save.cleared[id] && save.tierCleared[id] != null) return TIERS[save.tierCleared[id]] || TIERS[0];
  return TIERS[Math.min(4, clearedCount())];
}

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error(src));
    img.src = src;
  });
}

function keyOut(img) {
  const c = document.createElement("canvas");
  c.width = img.width;
  c.height = img.height;
  const g = c.getContext("2d", { willReadFrequently: true });
  g.drawImage(img, 0, 0);
  const data = g.getImageData(0, 0, c.width, c.height);
  const d = data.data;
  const pts = [[4, 4], [c.width - 5, 4], [4, c.height - 5], [c.width - 5, c.height - 5]];
  let br = 0, bg = 0, bb = 0;
  for (const [x, y] of pts) {
    const i = (y * c.width + x) * 4;
    br += d[i]; bg += d[i + 1]; bb += d[i + 2];
  }
  br /= pts.length; bg /= pts.length; bb /= pts.length;
  for (let i = 0; i < d.length; i += 4) {
    const dr = d[i] - br, dg = d[i + 1] - bg, db = d[i + 2] - bb;
    const dist = Math.sqrt(dr * dr + dg * dg + db * db);
    if (dist < 92) d[i + 3] = 0;
    else if (dist < 128 && d[i] > 170 && d[i + 2] > 140 && d[i + 1] < 150) d[i + 3] = 0;
  }
  g.putImageData(data, 0, 0);
  return c;
}

function cropSlice(sheet, index, count) {
  const x0 = Math.floor(index * sheet.width / count);
  const x1 = Math.floor((index + 1) * sheet.width / count);
  const g = sheet.getContext("2d");
  const { data, width } = g.getImageData(0, 0, sheet.width, sheet.height);
  let minx = x1, miny = sheet.height, maxx = x0, maxy = 0, found = false;
  for (let y = 0; y < sheet.height; y++) {
    for (let x = x0; x < x1; x++) {
      if (data[(y * width + x) * 4 + 3] > 24) {
        found = true;
        if (x < minx) minx = x;
        if (x > maxx) maxx = x;
        if (y < miny) miny = y;
        if (y > maxy) maxy = y;
      }
    }
  }
  const c = document.createElement("canvas");
  if (!found) { c.width = 8; c.height = 8; return c; }
  const pad = 2;
  minx = Math.max(x0, minx - pad);
  miny = Math.max(0, miny - pad);
  maxx = Math.min(x1 - 1, maxx + pad);
  maxy = Math.min(sheet.height - 1, maxy + pad);
  c.width = maxx - minx + 1;
  c.height = maxy - miny + 1;
  c.getContext("2d").drawImage(sheet, minx, miny, c.width, c.height, 0, 0, c.width, c.height);
  return c;
}

async function loadSheet(src, count, key) {
  const img = await loadImage(src);
  if (!key) return [img];
  const sheet = keyOut(img);
  const frames = [];
  for (let i = 0; i < count; i++) frames.push(cropSlice(sheet, i, count));
  return frames;
}

async function loadAll() {
  const jobs = [
    ["kai", "assets/kai_sheet.jpg", 5, true],
    ["lumi", "assets/lumi_sheet.jpg", 3, true],
    ["efloresta", "assets/enemies_floresta.jpg", 3, true],
    ["emares", "assets/enemies_mares.jpg", 3, true],
    ["epantano", "assets/enemies_pantano.jpg", 3, true],
    ["emontanhas", "assets/enemies_montanhas.jpg", 3, true],
    ["ecoracao", "assets/enemies_coracao.jpg", 3, true],
    ["eindustrial", "assets/enemies_industrial.jpg", 3, true],
    ["boss_floresta", "assets/boss_floresta.jpg", 1, true],
    ["boss_mares", "assets/boss_mares.jpg", 1, true],
    ["boss_pantano", "assets/boss_pantano.jpg", 1, true],
    ["boss_montanhas", "assets/boss_montanhas.jpg", 1, true],
    ["boss_coracao", "assets/boss_coracao.jpg", 1, true],
    ["boss_industrial", "assets/boss_industrial.jpg", 1, true],
    ["tiles", "assets/tiles_biomes.jpg", 6, true],
    ["fx", "assets/fx_sheet.jpg", 8, true],
    ["items", "assets/items_sheet.jpg", 6, true],
    ["ruined", "assets/sanctuary_ruined.jpg", 5, true],
    ["restored", "assets/sanctuary_restored.jpg", 5, true],
    ["hub", "assets/hub_props.jpg", 3, true],
    ["logo", "assets/logo.jpg", 1, true],
    ["bg_floresta", "assets/bg_floresta.jpg", 1, false],
    ["bg_mares", "assets/bg_mares.jpg", 1, false],
    ["bg_pantano", "assets/bg_pantano.jpg", 1, false],
    ["bg_montanhas", "assets/bg_montanhas.jpg", 1, false],
    ["bg_coracao", "assets/bg_coracao.jpg", 1, false],
    ["bg_industrial", "assets/bg_industrial.jpg", 1, false],
    ["bg_santuario", "assets/bg_santuario.jpg", 1, false],
    ["bg_title", "assets/bg_title.jpg", 1, false],
  ];
  let done = 0;
  const label = document.getElementById("loadstate");
  for (const [id, src, count, key] of jobs) {
    S[id] = await loadSheet(src, count, key);
    done++;
    label.textContent = "Carregando sprites " + done + "/" + jobs.length;
  }
}

function defaultSave() {
  return {
    crystals: 0, hpRank: 0, dmgRank: 0, spdRank: 0, potions: 0,
    cleared: {}, tierCleared: {}, abilities: {}, chests: {},
    intro: false, pendingZone: "", pendingMsg: "",
  };
}
function persist() { localStorage.setItem(SAVE_KEY, JSON.stringify(save)); }
function loadSave() {
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    save = raw ? Object.assign(defaultSave(), JSON.parse(raw)) : defaultSave();
  } catch (err) {
    save = defaultSave();
  }
}

function sfx(name) {
  const map = {
    jump: [560, 0.07, "square", 0.04],
    swing: [190, 0.06, "square", 0.035],
    hit: [140, 0.05, "square", 0.05],
    kill: [220, 0.09, "square", 0.05],
    hurt: [80, 0.16, "sawtooth", 0.06],
    dash: [360, 0.09, "square", 0.04],
    shot: [680, 0.08, "square", 0.04],
    boom: [70, 0.14, "sawtooth", 0.06],
    heal: [620, 0.12, "triangle", 0.05],
    coin: [880, 0.07, "square", 0.04],
    buy: [520, 0.1, "triangle", 0.05],
    roar: [55, 0.28, "sawtooth", 0.07],
  };
  const spec = map[name];
  if (!spec) return;
  try {
    if (!actx) actx = new (window.AudioContext || window.webkitAudioContext)();
    if (actx.state === "suspended") actx.resume();
    const o = actx.createOscillator();
    const g = actx.createGain();
    o.type = spec[2];
    o.frequency.value = spec[0];
    g.gain.value = spec[3];
    g.gain.exponentialRampToValueAtTime(0.001, actx.currentTime + spec[1]);
    o.connect(g); g.connect(actx.destination);
    o.start();
    o.stop(actx.currentTime + spec[1]);
  } catch (err) { /* sem áudio */ }
}

function openPanel(id) {
  document.querySelectorAll(".panel").forEach((p) => p.classList.add("hidden"));
  const el = document.getElementById("panel-" + id);
  if (el) el.classList.remove("hidden");
  uiOpen = true;
}
function closePanels() {
  document.querySelectorAll(".panel").forEach((p) => p.classList.add("hidden"));
  uiOpen = false;
}

function plat(x, y, w, h, tile, extra) {
  return Object.assign({ x, y, w, h, tile }, extra || {});
}

function blankWorld() {
  return {
    platforms: [], enemies: [], hazards: [], drops: [], particles: [], texts: [],
    w: 960, banner: "", bannerT: 0, arena: null, boss: null, zone: null, tier: null,
    replay: false, checkpoint: { x: 100, y: GROUND }, spawn: 100,
  };
}

function buildHub() {
  world = blankWorld();
  world.mode = "hub";
  world.w = 3480;
  world.bg = S.bg_santuario[0];
  world.platforms = [
    plat(0, GROUND, 3480, 110, 0),
    plat(70, GROUND - 86, 130, 44, 0),
    plat(70, GROUND - 196, 110, 36, 0),
    plat(390, GROUND - 86, 130, 44, 0),
    plat(3188, GROUND - 250, 32, 180, 3),
    plat(3304, GROUND - 250, 32, 180, 3),
    plat(3220, GROUND - 230, 84, 28, 3),
  ];
  world.spawn = 130;
  world.checkpoint = { x: 130, y: GROUND };
}

function pushArena(level, arenaX, tile) {
  level.platforms.push(plat(arenaX, GROUND, 1040, 110, tile));
  level.platforms.push(plat(arenaX + 1000, GROUND - 300, 48, 300, tile));
  level.arena = { x: arenaX, w: 1040, lock: arenaX + 130, floor: GROUND, locked: false };
  level.leftWall = plat(arenaX - 8, GROUND - 320, 40, 320, tile);
  level.bossPos = { x: arenaX + 760, y: GROUND };
  level.w = arenaX + 1120;
}

function buildLevel(zone) {
  const t = zone.tile;
  const G = GROUND;
  const L = blankWorld();
  L.mode = "level";
  L.zone = zone;
  L.bg = S["bg_" + zone.id][0];
  if (zone.id === "floresta") {
    L.platforms = [
      plat(0, G, 500, 110, t),
      plat(600, G, 340, 110, t),
      plat(1040, G - 64, 220, 110, t),
      plat(1048, G - 236, 150, 40, t),
      plat(1435, G - 64, 160, 70, t),
      plat(1370, G, 530, 110, t),
      plat(2010, G, 350, 110, t),
      plat(2470, G, 390, 110, t),
    ];
    L.enemiesSpec = [
      [0, 260, G], [1, 740, G], [2, 1120, G - 64], [0, 1600, G], [1, 2140, G], [2, 2620, G],
    ];
    L.extras = [[0, 420, G, 1], [1, 1760, G, 2], [2, 2280, G, 3], [0, 2700, G, 4]];
    L.dropsSpec = [[820, G, 8], [1680, G, 8], [2580, G, 8]];
    L.chests = [
      { id: "floresta-copa", x: 1120, y: G - 236, value: 30 },
      { id: "floresta-vao", x: 1510, y: G - 64, value: 24 },
    ];
    pushArena(L, 2960, t);
  } else if (zone.id === "mares") {
    L.platforms = [
      plat(0, G, 460, 110, t),
      plat(560, G, 280, 110, t),
      plat(930, G - 70, 200, 90, t),
      plat(1160, G - 70, 110, 70, t),
      plat(1310, G - 70, 150, 70, t),
      plat(1540, G, 420, 110, t),
      plat(2060, G - 50, 240, 80, t),
      plat(2060, G - 220, 140, 36, t),
      plat(2400, G, 460, 110, t),
    ];
    L.enemiesSpec = [
      [0, 240, G], [1, 680, G], [2, 1000, G - 150], [0, 1700, G], [1, 2140, G - 50], [2, 2550, G - 140],
    ];
    L.extras = [[1, 400, G, 1], [2, 1400, G - 160, 2], [0, 1900, G, 3], [1, 2650, G, 4]];
    L.dropsSpec = [[760, G, 8], [1700, G, 8], [2550, G, 8]];
    L.chests = [{ id: "mares-alto", x: 2120, y: G - 220, value: 32 }];
    pushArena(L, 2960, t);
  } else if (zone.id === "pantano") {
    L.platforms = [
      plat(0, G, 480, 110, t),
      plat(580, G, 300, 110, t),
      plat(980, G - 90, 200, 36, t),
      plat(1180, G - 230, 222, 28, t),
      plat(1180, G - 202, 42, 132, t, { gate: "spores" }),
      plat(1360, G - 202, 42, 132, t),
      plat(1180, G - 90, 222, 36, t),
      plat(1000, G, 620, 110, t),
      plat(1740, G, 340, 110, t),
      plat(2180, G - 40, 250, 80, t),
      plat(2540, G, 400, 110, t),
    ];
    L.enemiesSpec = [
      [0, 250, G], [2, 700, G], [1, 1100, G - 170], [0, 1400, G], [2, 1880, G], [1, 2300, G - 130],
    ];
    L.extras = [[1, 400, G, 1], [0, 1600, G, 2], [2, 2000, G, 3], [0, 2700, G, 4]];
    L.dropsSpec = [[800, G, 8], [1500, G, 8], [2680, G, 8]];
    L.chests = [{ id: "pantano-bulbo", x: 1300, y: G - 90, value: 34 }];
    pushArena(L, 3040, t);
  } else if (zone.id === "montanhas") {
    L.platforms = [
      plat(0, G, 520, 110, t),
      plat(630, G - 50, 260, 90, t),
      plat(990, G, 420, 110, t),
      plat(1410, G, 270, 110, t),
      plat(1470, G - 270, 34, 200, t),
      plat(1588, G - 270, 34, 200, t),
      plat(1504, G - 246, 84, 28, t),
      plat(1680, G, 380, 110, t),
      plat(2160, G - 60, 220, 80, t),
      plat(2480, G, 430, 110, t),
    ];
    L.enemiesSpec = [
      [0, 280, G - 120], [1, 740, G - 50], [2, 1160, G], [1, 1860, G], [0, 2260, G - 140], [2, 2660, G],
    ];
    L.extras = [[2, 400, G, 1], [0, 1300, G - 130, 2], [1, 2000, G, 3], [2, 2740, G, 4]];
    L.dropsSpec = [[860, G - 50, 8], [1900, G, 8], [2700, G, 8]];
    L.chests = [{ id: "montanhas-poco", x: 1546, y: G - 246, value: 36 }];
    pushArena(L, 3010, t);
  } else if (zone.id === "coracao") {
    L.platforms = [
      plat(0, G, 400, 110, t),
      plat(400, G - 58, 42, 58, t, { gate: "shot" }),
      plat(442, G, 200, 110, t),
      plat(642, G - 58, 40, 80, t),
      plat(160, G - 84, 760, 26, t),
      plat(1020, G - 40, 240, 80, t),
      plat(1360, G, 460, 110, t),
      plat(1920, G - 60, 260, 80, t),
      plat(2280, G, 420, 110, t),
    ];
    L.enemiesSpec = [
      [0, 280, G - 84], [1, 560, G - 84], [2, 1120, G - 40], [0, 1540, G], [1, 2040, G - 60], [2, 2460, G],
    ];
    L.extras = [[2, 180, G, 1], [0, 1700, G, 2], [1, 2200, G, 3], [0, 2480, G, 4]];
    L.dropsSpec = [[700, G - 84, 8], [1600, G, 8], [2400, G, 8]];
    L.chests = [{ id: "coracao-selo", x: 540, y: G, value: 38 }];
    pushArena(L, 2800, t);
  } else {
    L.platforms = [
      plat(0, G, 420, 110, t),
      plat(520, G, 360, 110, t),
      plat(640, G - 30, 130, 30, t),
      plat(980, G - 50, 240, 90, t),
      plat(1320, G, 420, 110, t),
      plat(1460, G - 30, 150, 30, t),
      plat(1840, G - 46, 220, 80, t),
      plat(2160, G, 460, 110, t),
      plat(2300, G - 30, 160, 30, t),
      plat(2720, G, 420, 110, t),
    ];
    L.hazards = [
      zoneHazard(640, 130, 14),
      zoneHazard(1460, 150, 14),
      zoneHazard(2300, 160, 16),
    ];
    L.enemiesSpec = [
      [0, 220, G], [2, 660, G], [1, 1080, G - 140], [0, 1500, G], [2, 1960, G - 46], [1, 2360, G - 120], [0, 2900, G],
    ];
    L.extras = [[2, 400, G, 0], [1, 1200, G, 0], [0, 2000, G, 0], [2, 2600, G, 0]];
    L.dropsSpec = [[860, G, 10], [1700, G, 10], [2500, G, 10], [3000, G, 10]];
    L.chests = [];
    pushArena(L, 3240, t);
  }
  return L;
}

function zoneHazard(x, w, dmg) {
  return { kind: "zone", x, y: GROUND - 32, w, h: 32, dmg, life: 99999, warn: 0, spr: 6, permanent: true, next: 0, friendly: false };
}

function spawnEnemy(type, x, y, zone, tier) {
  const d = zone.enemies[type];
  return {
    type, name: d.name, ai: d.ai, shot: d.shot,
    x, y, vx: 0, vy: 0, dir: -1,
    hw: d.hw, h: d.h,
    hp: Math.round(d.hp * tier.hp),
    max: Math.round(d.hp * tier.hp),
    dmg: Math.max(1, Math.round(d.dmg * tier.dmg)),
    speed: d.speed * tier.spd,
    home: x, baseY: y - (d.ai === "flyer" ? 90 : 0),
    timer: 0.4 + Math.random(),
    state: "walk", iframe: 0, lastSwing: -1, touch: 0,
    fly: d.ai === "flyer",
  };
}

function makeBoss(zone, tier, pos) {
  return {
    def: zone, x: pos.x, y: pos.y, vx: 0, vy: 0, dir: -1,
    hp: Math.round(zone.bossHp * tier.hp),
    max: Math.round(zone.bossHp * tier.hp),
    hw: zone.bossHw, h: zone.bossH,
    phase: 1, state: "wait", t: 0, step: 0, pattern: "",
    aimX: pos.x, aimY: pos.y - 40, lastSwing: -1, dying: 0, rewarded: false, flash: 0,
  };
}

function startHub() {
  mode = "hub";
  buildHub();
  const idx = ZONES.findIndex((z) => z.id === save.pendingZone);
  const x = idx >= 0 ? PORTAL_X[idx] : 140;
  player = makePlayer(x, GROUND);
  player.hp = maxHp();
  cam.x = clamp(x - 420, 0, world.w - VW);
  if (save.pendingMsg) {
    world.banner = save.pendingMsg;
    world.bannerT = 4;
    save.pendingMsg = "";
    save.pendingZone = "";
    persist();
  }
  closePanels();
  document.getElementById("title").classList.add("hidden");
  if (!save.intro) openPanel("intro");
}

function startLevel(zone, tier, replay) {
  mode = "level";
  world = buildLevel(zone);
  world.tier = tier;
  world.replay = replay;
  world.banner = zone.name + " — " + tier.name;
  world.bannerT = 3.4;
  const list = world.enemiesSpec || [];
  world.enemies = list.map(([type, x, y]) => spawnEnemy(type, x, y, zone, tier));
  for (const [type, x, y, minTier] of world.extras || []) {
    if (tier.id >= minTier) world.enemies.push(spawnEnemy(type, x, y, zone, tier));
  }
  world.drops = (world.dropsSpec || []).map(([x, y, value]) => ({ x, y, vy: -40, value, life: 30, magnet: false }));
  world.hazards = world.hazards || [];
  for (const h of world.hazards) h.dmg = Math.round(h.dmg * tier.dmg);
  world.boss = makeBoss(zone, tier, world.bossPos);
  player = makePlayer(90, GROUND);
  player.hp = maxHp();
  world.checkpoint = { x: 90, y: GROUND };
  cam.x = 0;
  closePanels();
  document.getElementById("title").classList.add("hidden");
}

function makePlayer(x, y) {
  return {
    x, y, vx: 0, vy: 0, dir: 1, hw: 13, h: 46,
    onGround: true, coyote: 0.12, jumpBuf: 0, jumpsLeft: 1, jumpLock: 0,
    wallDir: 0, wallCoy: 0,
    atk: 0, atkCd: 0, swing: 0,
    hurt: 0, dash: 0, dashCd: 0, dashDir: 1,
    slam: false, shotCd: 0, hp: maxHp(), anim: 0,
  };
}

function overlapX(b, p) { return b.x + b.hw > p.x + 1 && b.x - b.hw < p.x + p.w - 1; }
function overlapBody(b, p) { return overlapX(b, p) && b.y > p.y && b.y - b.h < p.y + p.h; }
function rects(a, b) { return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y; }
function circleRect(cx, cy, r, p) {
  const x = clamp(cx, p.x, p.x + p.w);
  const y = clamp(cy, p.y, p.y + p.h);
  const dx = cx - x, dy = cy - y;
  return dx * dx + dy * dy <= r * r;
}

function moveBody(b, dt) {
  b.x += b.vx * dt;
  for (const p of world.platforms) {
    if (p.dead || p.oneWay) continue;
    if (b.y <= p.y + 8) continue;
    if (!overlapBody(b, p)) continue;
    if (b.x < p.x + p.w / 2) b.x = p.x - b.hw;
    else b.x = p.x + p.w + b.hw;
    b.vx = 0;
    b.blocked = true;
  }
  const prev = b.y;
  b.y += b.vy * dt;
  b.onGround = false;
  for (const p of world.platforms) {
    if (p.dead) continue;
    if (!overlapX(b, p)) continue;
    if (b.vy >= 0 && prev <= p.y + 6 && b.y >= p.y && b.y - prev <= 64) {
      b.y = p.y;
      b.vy = 0;
      b.onGround = true;
    } else if (!p.oneWay && b.vy < 0 && overlapBody(b, p)) {
      b.y = p.y + p.h + b.h;
      b.vy = 0;
    }
  }
}

function supported(x, feet) {
  return world.platforms.some((p) => !p.dead && !p.gate && x >= p.x && x <= p.x + p.w && Math.abs(feet - p.y) < 10);
}
function blockedAt(x, y) {
  return world.platforms.some((p) => !p.dead && !p.oneWay && x >= p.x && x <= p.x + p.w && y >= p.y + 8 && y <= p.y + p.h);
}

function floatText(x, y, t, color) {
  world.texts.push({ x, y, t, color: color || "#fff6df", life: 0.7 });
}
function burst(x, y, spr, n) {
  for (let i = 0; i < n; i++) {
    world.particles.push({
      x, y, spr, vx: (Math.random() - 0.5) * 180, vy: -40 - Math.random() * 140,
      life: 0.35 + Math.random() * 0.3, max: 0.6, s: 16 + Math.random() * 14,
    });
  }
}

function hurtPlayer(dmg, fromX) {
  if (player.hurt > 0 || player.hp <= 0) return;
  player.hp -= dmg;
  player.hurt = 0.85;
  player.vx = player.x < fromX ? -200 : 200;
  player.vy = -240;
  player.slam = false;
  shake = Math.max(shake, 6);
  sfx("hurt");
  floatText(player.x, player.y - 60, "-" + dmg, "#ffb0b0");
  if (player.hp <= 0) {
    player.hp = 0;
    openPanel("dead");
  }
}

function damageEnemy(e, dmg, knock) {
  if (!e || e.hp <= 0) return;
  e.hp -= dmg;
  e.iframe = 0.07;
  e.vx = knock || 0;
  e.vy = Math.min(e.vy, -80);
  floatText(e.x, e.y - e.h, String(Math.round(dmg)), "#ffe08a");
  if (e.hp <= 0) {
    const val = Math.round((6 + e.type * 2) * world.tier.reward);
    world.drops.push({ x: e.x, y: e.y - 16, vy: -80, value: val, life: 16 });
    burst(e.x, e.y - 20, 7, 4);
    sfx("kill");
    e.gone = true;
  } else sfx("hit");
}

function damageBoss(dmg) {
  const b = world.boss;
  if (!b || b.rewarded || b.state === "wait" || !world.arena.locked) return;
  b.hp -= dmg;
  b.flash = 0.08;
  shake = Math.max(shake, 5);
  floatText(b.x, b.y - b.h, String(Math.round(dmg)), "#ffe08a");
  sfx("hit");
  if (b.hp <= 0) {
    b.hp = 0;
    b.dying = 0.85;
    b.state = "dead";
    burst(b.x, b.y - 80, 7, 10);
    sfx("roar");
  } else if (b.phase === 1 && b.hp < b.max * 0.5 && b.def.id !== "industrial") {
    enterPhase(b, 2);
  } else if (b.def.id === "industrial" && b.phase === 1 && b.hp < b.max * 0.66) {
    enterPhase(b, 2);
  } else if (b.def.id === "industrial" && b.phase === 2 && b.hp < b.max * 0.33) {
    enterPhase(b, 3);
  }
}

function enterPhase(b, phase) {
  b.phase = phase;
  b.state = "roar";
  b.t = 1;
  shake = 10;
  sfx("roar");
  floatText(b.x, b.y - b.h - 20, "FASE " + phase, "#ffd0a1");
}

function landSlam() {
  player.slam = false;
  shake = 8;
  sfx("boom");
  burst(player.x, player.y, 3, 6);
  const r = 82;
  for (const e of world.enemies) {
    if (Math.hypot(e.x - player.x, e.y - player.y) < r + 20) damageEnemy(e, 18 * dmgMul(), Math.sign(e.x - player.x) * 180);
  }
  if (world.boss && Math.hypot(world.boss.x - player.x, world.boss.y - player.y) < r + 50) damageBoss(20 * dmgMul());
  for (const p of world.platforms) {
    if (p.gate === "spores" && circleRect(player.x, player.y - 10, r, p)) p.dead = true;
  }
}

function meleeBox() {
  const w = 48, h = 36;
  const x = player.dir === 1 ? player.x + 6 : player.x - 6 - w;
  return { x, y: player.y - player.h + 6, w, h };
}

function updatePlayer(dt) {
  player.jumpBuf = Math.max(0, player.jumpBuf - dt);
  player.atkCd = Math.max(0, player.atkCd - dt);
  player.dashCd = Math.max(0, player.dashCd - dt);
  player.shotCd = Math.max(0, player.shotCd - dt);
  player.hurt = Math.max(0, player.hurt - dt);
  player.atk = Math.max(0, player.atk - dt);
  if (pressed.Space || pressed.ArrowUp || pressed.KeyW) player.jumpBuf = 0.13;

  const canGround = player.coyote > 0;
  const canDouble = player.jumpsLeft > 0 && !player.onGround;
  const canWall = has("wall") && player.wallCoy > 0 && !player.onGround;
  if (player.jumpBuf > 0 && player.dash <= 0 && (canGround || canDouble || canWall)) {
    if (canWall && !canGround) {
      const away = -(player.wallDir || 1);
      player.vy = -600;
      player.vx = away * 300;
      player.dir = away;
      player.jumpsLeft = 1;
      player.wallCoy = 0;
    } else if (canGround) {
      player.vy = -620;
      player.jumpsLeft = 1;
      player.coyote = 0;
    } else {
      player.vy = has("double") ? -700 : -640;
      player.jumpsLeft -= 1;
      burst(player.x, player.y - 20, 3, 3);
    }
    player.jumpLock = 0.14;
    player.jumpBuf = 0;
    player.onGround = false;
    player.slam = false;
    sfx("jump");
  }
  player.jumpLock = Math.max(0, (player.jumpLock || 0) - dt);
  const holding = down.Space || down.ArrowUp || down.KeyW;
  if (player.jumpLock <= 0 && !holding && player.vy < -460) player.vy = -460;

  if ((pressed.ShiftLeft || pressed.ShiftRight) && has("dash") && player.dashCd <= 0 && player.dash <= 0) {
    player.dash = 0.18;
    player.dashCd = 0.52;
    player.dashDir = player.dir || 1;
    player.hurt = Math.max(player.hurt, 0.16);
    player.slam = false;
    sfx("dash");
  }
  const downHeld = down.ArrowDown || down.KeyS;
  if (pressed.KeyJ && downHeld && has("spores") && !player.onGround && !player.slam) {
    player.slam = true;
    player.vy = 840;
    sfx("boom");
  } else if (pressed.KeyJ && player.atkCd <= 0 && !player.slam) {
    player.atk = 0.18;
    player.atkCd = 0.36;
    player.swing += 1;
    sfx("swing");
  }
  if (pressed.KeyK && has("shot") && player.shotCd <= 0) {
    player.shotCd = 0.42;
    world.hazards.push({
      kind: "proj", friendly: true, x: player.x + player.dir * 24, y: player.y - 30,
      vx: player.dir * 480, vy: 0, r: 12, dmg: 14 * dmgMul(), life: 0.7, spr: 5,
    });
    sfx("shot");
  }
  if (pressed.KeyQ && mode === "level" && save.potions > 0 && player.hp < maxHp()) {
    save.potions -= 1;
    player.hp = Math.min(maxHp(), player.hp + maxHp() * 0.45);
    persist();
    sfx("heal");
    floatText(player.x, player.y - 70, "poção", "#b6ffb0");
  }

  const axis = (down.ArrowRight || down.KeyD ? 1 : 0) - (down.ArrowLeft || down.KeyA ? 1 : 0);
  if (player.dash > 0) {
    player.dash -= dt;
    player.vx = player.dashDir * 1120;
    player.vy = 0;
  } else {
    const maxSp = 215 * speedMul();
    if (axis) {
      player.dir = axis;
      player.vx += axis * 2400 * speedMul() * dt;
    } else player.vx *= Math.max(0, 1 - dt * 12);
    player.vx = clamp(player.vx, -maxSp, maxSp);
    player.vy += (player.slam ? 2600 : 1900) * dt;
    if (player.wallDir && has("wall") && !player.onGround && player.vy > 50) player.vy = 50;
    player.vy = Math.min(player.vy, 900);
  }
  player.blocked = false;
  const wasSlam = player.slam;
  moveBody(player, dt);
  if (wasSlam && player.onGround) landSlam();

  player.wallDir = 0;
  if (!player.onGround) {
    if (blockedAt(player.x + player.hw + 3, player.y - 16)) player.wallDir = 1;
    else if (blockedAt(player.x - player.hw - 3, player.y - 16)) player.wallDir = -1;
  }
  if (player.onGround) {
    player.coyote = 0.12;
    player.jumpsLeft = 1;
  } else player.coyote = Math.max(0, player.coyote - dt);
  if (player.wallDir) player.wallCoy = 0.12;
  else player.wallCoy = Math.max(0, player.wallCoy - dt);

  if (world.arena && world.arena.locked) {
    const a = world.arena;
    player.x = clamp(player.x, a.x + 24, a.x + a.w - 24);
  }
  player.x = clamp(player.x, 20, world.w - 20);

  if (player.onGround && player.y < 600) {
    const wide = world.platforms.find((p) => !p.dead && !p.gate && p.w > 140 && overlapX(player, p) && Math.abs(player.y - p.y) < 4);
    if (wide && player.x > wide.x + 40 && player.x < wide.x + wide.w - 40) {
      world.checkpoint.x = player.x;
      world.checkpoint.y = wide.y;
    }
  }
  if (player.y > 640) {
    if (mode === "hub") {
      player.x = 140;
      player.y = GROUND;
    } else {
      hurtPlayer(12, player.x);
      player.x = world.checkpoint.x;
      player.y = world.checkpoint.y;
    }
    player.vx = 0;
    player.vy = 0;
  }
}

function updateEnemies(dt) {
  for (const e of world.enemies) {
    if (e.gone) continue;
    e.iframe = Math.max(0, e.iframe - dt);
    e.touch = Math.max(0, e.touch - dt);
    e.timer -= dt;
    const see = Math.abs(player.x - e.x) < 420 && Math.abs(player.y - e.y) < 160;
    if (e.fly) {
      const goalX = see ? player.x : e.home;
      e.dir = goalX < e.x ? -1 : 1;
      e.x += e.dir * e.speed * dt;
      e.y = e.baseY + Math.sin(time * 3 + e.home) * 18;
      e.y = clamp(e.y, 160, GROUND - 20);
    } else if (e.ai === "charge") {
      if (e.state === "walk") {
        e.dir = e.x > e.home + 90 ? -1 : e.x < e.home - 90 ? 1 : e.dir;
        e.vx = e.dir * e.speed * 0.45;
        if (see && e.timer <= 0) { e.state = "wind"; e.timer = 0.38; e.dir = player.x < e.x ? -1 : 1; }
      } else if (e.state === "wind") {
        e.vx = 0;
        if (e.timer <= 0) { e.state = "dash"; e.timer = 0.42; e.vx = e.dir * 320; }
      } else {
        e.vx = e.dir * 320;
        if (e.timer <= 0 || e.blocked) { e.state = "walk"; e.timer = 1.1; e.vx = 0; }
      }
      e.vy += 1900 * dt;
      e.blocked = false;
      moveBody(e, dt);
      if (e.onGround && e.state === "walk") {
        const ahead = e.x + e.dir * (e.hw + 10);
        if (!supported(ahead, e.y) || blockedAt(ahead, e.y - 16)) e.dir *= -1;
      }
    } else if (e.ai === "shooter") {
      const want = player.x < e.x ? -1 : 1;
      const ahead = e.x + want * (e.hw + 10);
      e.dir = e.onGround && !supported(ahead, e.y) ? -want : want;
      e.vx = e.dir * e.speed * 0.35;
      if (e.timer <= 0 && see) {
        e.timer = 2.15;
        const sx = e.x, sy = e.y - e.h * 0.55;
        const dx = player.x - sx, dy = (player.y - 28) - sy;
        const m = Math.hypot(dx, dy) || 1;
        world.hazards.push({
          kind: "proj", x: sx, y: sy, vx: dx / m * 230, vy: dy / m * 230,
          r: 12, dmg: e.dmg, life: 3, spr: e.shot || 2, friendly: false,
        });
      }
      e.vy += 1900 * dt;
      moveBody(e, dt);
    } else {
      e.vx = e.dir * e.speed;
      if (e.ai === "hopper" && e.onGround && e.timer <= 0) {
        e.vy = -460;
        e.timer = 1.35;
        e.dir = player.x < e.x ? -1 : 1;
      }
      e.vy += 1900 * dt;
      moveBody(e, dt);
      if (e.onGround) {
        const ahead = e.x + e.dir * (e.hw + 10);
        if (!supported(ahead, e.y) || blockedAt(ahead, e.y - 12)) e.dir *= -1;
      }
    }
    if (!e.fly && e.y > 700) e.gone = true;
    if (e.gone) continue;
    if (e.touch <= 0 && player.hurt <= 0 && Math.abs(player.x - e.x) < e.hw + player.hw && Math.abs((player.y - player.h / 2) - (e.y - e.h / 2)) < (player.h + e.h) / 2) {
      e.touch = 0.6;
      hurtPlayer(e.dmg, e.x);
    }
  }
  if (player.atk > 0.05 && player.atk < 0.18) {
    const box = meleeBox();
    for (const e of world.enemies) {
      if (e.gone || e.lastSwing === player.swing) continue;
      const eb = { x: e.x - e.hw, y: e.y - e.h, w: e.hw * 2, h: e.h };
      if (rects(box, eb)) {
        e.lastSwing = player.swing;
        damageEnemy(e, (15 + e.type * 2) * dmgMul(), player.dir * 160);
      }
    }
    if (world.boss && world.boss.lastSwing !== player.swing) {
      const b = world.boss;
      const bb = { x: b.x - b.hw, y: b.y - b.h, w: b.hw * 2, h: b.h };
      if (rects(box, bb)) {
        b.lastSwing = player.swing;
        damageBoss(18 * dmgMul());
      }
    }
  }
  world.enemies = world.enemies.filter((e) => !e.gone);
}

function spawnPattern(b) {
  const dir = Math.sign(player.x - b.x) || -1;
  const a = world.arena;
  const floor = a.floor;
  const spr = (n, extra) => Object.assign({ kind: "proj", friendly: false, life: 3.2, r: 14, boss: true }, extra, { spr: n });
  if (b.pattern === "saws") {
    for (let i = 0; i < 3; i++) {
      world.hazards.push(spr(1, { x: b.x, y: floor - 36 - i * 34, vx: dir * 280, vy: 0, dmg: 12, spin: true }));
    }
  } else if (b.pattern === "charge" || b.pattern === "roll") {
    b.vx = dir * (b.pattern === "roll" ? 520 : 430);
    b.t = b.pattern === "roll" ? 0.7 : 0.55;
  } else if (b.pattern === "slam") {
    const r = 62;
    world.hazards.push({ kind: "zone", x: b.aimX - r, y: floor - 36, w: r * 2, h: 40, dmg: 14, warn: 0.42, life: 0.62, spr: 7, next: 0 });
  } else if (b.pattern === "spit") {
    for (let i = -1; i <= 1; i++) {
      world.hazards.push(spr(2, { x: b.x + dir * 20, y: b.y - 90, vx: dir * 180 + i * 50, vy: -300, grav: 720, dmg: 11 }));
    }
  } else if (b.pattern === "tire") {
    world.hazards.push(spr(2, { x: b.x, y: floor - 18, vx: dir * 340, vy: 0, dmg: 12, r: 16 }));
  } else if (b.pattern === "suction") {
    b.t = 1.15;
    world.hazards.push({ kind: "zone", x: b.aimX - 50, y: floor - 34, w: 100, h: 34, dmg: 10, warn: 0.35, life: 0.9, spr: 2, next: 0 });
  } else if (b.pattern === "clouds") {
    for (let i = 0; i < 3; i++) {
      world.hazards.push(spr(3, { x: b.x, y: b.y - 80, vx: dir * 90 + (i - 1) * 40, vy: -30 - i * 20, dmg: 10, life: 4, r: 18 }));
    }
  } else if (b.pattern === "hop") {
    b.vy = -560;
    b.vx = dir * 180;
    b.hop = true;
    b.t = 1.4;
  } else if (b.pattern === "rain" || b.pattern === "icicles") {
    for (let i = 0; i < 4; i++) {
      const x = a.x + 80 + Math.random() * (a.w - 160);
      world.hazards.push({ kind: "zone", x: x - 28, y: floor - 36, w: 56, h: 40, dmg: 12, warn: 0.62, life: 0.86, spr: b.pattern === "rain" ? 3 : 4, next: 0 });
    }
  } else if (b.pattern === "shards" || b.pattern === "ring") {
    const n = b.pattern === "ring" ? 8 : 5;
    for (let i = 0; i < n; i++) {
      const ang = b.pattern === "ring" ? (i / n) * Math.PI * 2 : (-0.7 + i * 0.35);
      world.hazards.push(spr(b.pattern === "ring" ? 5 : 4, {
        x: b.x, y: b.y - 80, vx: Math.cos(ang) * 230, vy: Math.sin(ang) * 230, dmg: 11,
      }));
    }
  } else if (b.pattern === "wind") {
    b.t = 1.2;
    b.wind = dir;
  } else if (b.pattern === "beam" || b.pattern === "laser") {
    const y = clamp(b.aimY, 180, floor - 50);
    const left = Math.min(b.x, b.x + dir * 640);
    world.hazards.push({ kind: "zone", x: left, y: y - 14, w: 640, h: 28, dmg: 16, warn: 0.4, life: 0.72, spr: 5, beam: true, next: 0 });
  } else if (b.pattern === "blink") {
    const nx = player.x + (player.x < b.x ? 150 : -150);
    b.x = clamp(nx, a.x + 100, a.x + a.w - 100);
    world.hazards.push({ kind: "zone", x: b.x - 60, y: floor - 40, w: 120, h: 40, dmg: 14, warn: 0.28, life: 0.5, spr: 7, next: 0 });
  } else if (b.pattern === "missile") {
    for (let i = 0; i < 2; i++) {
      world.hazards.push(spr(6, { x: b.x, y: b.y - 70 - i * 20, vx: dir * 80, vy: -40, dmg: 13, homing: true, life: 4 }));
    }
  } else if (b.pattern === "pound") {
    world.hazards.push({ kind: "zone", x: a.x + 20, y: floor - 34, w: a.w - 40, h: 34, dmg: 15, warn: 0.55, life: 0.85, spr: 7, next: 0 });
  } else if (b.pattern === "summon") {
    if (world.enemies.length < 3) {
      world.enemies.push(spawnEnemy(0, a.x + 180, floor, b.def, world.tier));
      world.enemies.push(spawnEnemy(2, a.x + a.w - 180, floor, b.def, world.tier));
    }
  }
}

function updateBoss(dt) {
  const b = world.boss;
  if (!b || b.rewarded) return;
  b.flash = Math.max(0, b.flash - dt);
  if (b.state === "dead") {
    b.dying -= dt;
    b.y += 30 * dt;
    if (b.dying <= 0) defeatBoss();
    return;
  }
  if (!world.arena.locked || b.state === "wait") return;
  b.dir = player.x < b.x ? -1 : 1;
  if (b.state !== "intro") {
    if (player.hurt <= 0 && Math.abs(player.x - b.x) < b.hw + player.hw - 8 && player.y > b.y - b.h && player.y - player.h < b.y) {
      hurtPlayer(Math.round(14 * world.tier.dmg * (b.phase > 1 ? 1.12 : 1)), b.x);
    }
    if (b.def.orbit && b.phase >= 2) {
      const ang = time * 3.2;
      for (let i = 0; i < 2; i++) {
        const ox = b.x + Math.cos(ang + i * Math.PI) * 92;
        const oy = b.y - 70 + Math.sin(ang + i * Math.PI) * 26;
        if (player.hurt <= 0 && Math.hypot(player.x - ox, (player.y - 24) - oy) < 22) hurtPlayer(Math.round(10 * world.tier.dmg), ox);
      }
    }
  }
  if (b.state === "intro") {
    b.t -= dt;
    if (b.t <= 0) { b.state = "idle"; b.t = 0.45; }
    return;
  }
  if (b.state === "roar") {
    b.t -= dt;
    if (b.t <= 0) { b.state = "idle"; b.t = 0.35; }
    return;
  }
  if (b.state === "idle") {
    const dist = player.x - b.x;
    if (Math.abs(dist) > 210) b.x += Math.sign(dist) * 55 * dt;
    b.x = clamp(b.x, world.arena.x + 90, world.arena.x + world.arena.w - 90);
    b.t -= dt;
    if (b.t <= 0) {
      const list = b.phase === 1 ? b.def.p1 : b.phase === 2 ? b.def.p2 : (b.def.p3 || b.def.p2);
      b.pattern = list[b.step % list.length];
      b.step += 1;
      b.state = "tell";
      b.t = 0.58;
      b.aimX = player.x;
      b.aimY = player.y - 24;
    }
    return;
  }
  if (b.state === "tell") {
    b.t -= dt;
    if (b.t <= 0) {
      b.state = "act";
      b.t = 0.45;
      b.wind = 0;
      b.hop = false;
      spawnPattern(b);
    }
    return;
  }
  if (b.state === "act") {
    if (b.pattern === "charge" || b.pattern === "roll") {
      b.x += b.vx * dt;
      const min = world.arena.x + 80, max = world.arena.x + world.arena.w - 80;
      if (b.x < min || b.x > max) { b.x = clamp(b.x, min, max); b.t = 0; }
    }
    if (b.hop) {
      b.vy += 1700 * dt;
      b.x += b.vx * dt;
      b.y += b.vy * dt;
      b.x = clamp(b.x, world.arena.x + 80, world.arena.x + world.arena.w - 80);
      if (b.y >= world.arena.floor) {
        b.y = world.arena.floor;
        b.hop = false;
        b.t = 0;
        world.hazards.push({ kind: "zone", x: b.x - 70, y: world.arena.floor - 40, w: 140, h: 40, dmg: 14, warn: 0.05, life: 0.28, spr: 3, next: 0 });
        shake = 8;
      }
    }
    if (b.wind) player.vx += b.wind * 420 * dt;
    if (b.pattern === "suction") player.vx += Math.sign(b.x - player.x) * 380 * dt;
    b.t -= dt;
    if (b.t <= 0) { b.state = "recover"; b.t = b.phase > 1 ? 0.42 : 0.58; b.vx = 0; }
    return;
  }
  if (b.state === "recover") {
    b.t -= dt;
    if (b.t <= 0) { b.state = "idle"; b.t = b.phase > 1 ? 0.32 : 0.5; }
  }
}

function updateHazards(dt) {
  for (const h of world.hazards) {
    if (h.permanent) { /* vive o tempo todo */ }
    else h.life -= dt;
    if (h.warn > 0) h.warn -= dt;
    if (h.kind === "proj") {
      if (h.grav) h.vy += h.grav * dt;
      if (h.homing) {
        const dx = player.x - h.x, dy = (player.y - 24) - h.y;
        const m = Math.hypot(dx, dy) || 1;
        h.vx += (dx / m) * 280 * dt;
        h.vy += (dy / m) * 280 * dt;
      }
      h.x += h.vx * dt;
      h.y += h.vy * dt;
      const inside = world.platforms.some((p) => !p.dead && h.x > p.x && h.x < p.x + p.w && h.y > p.y + 6 && h.y < p.y + p.h);
      if (inside) h.life = 0;
      if (h.friendly) {
        for (const e of world.enemies) {
          if (Math.hypot(e.x - h.x, (e.y - e.h / 2) - h.y) < e.hw + h.r) {
            damageEnemy(e, h.dmg, Math.sign(h.vx) * 80);
            h.life = 0;
          }
        }
        const b = world.boss;
        if (b && !b.rewarded && Math.hypot(b.x - h.x, (b.y - b.h / 2) - h.y) < b.hw) {
          damageBoss(h.dmg);
          h.life = 0;
        }
        for (const p of world.platforms) {
          if (p.gate === "shot" && circleRect(h.x, h.y, h.r, p)) {
            p.dead = true;
            h.life = 0;
            burst(h.x, h.y, 5, 4);
            sfx("boom");
          }
        }
      } else if (player.hurt <= 0 && Math.hypot(player.x - h.x, (player.y - 24) - h.y) < player.hw + h.r) {
        const dmg = h.boss ? Math.max(1, Math.round(h.dmg * world.tier.dmg)) : h.dmg;
        hurtPlayer(dmg, h.x);
        h.life = 0;
      }
    } else if (h.kind === "zone") {
      if (h.warn <= 0 && player.hurt <= 0) {
        h.next -= dt;
        const box = { x: player.x - player.hw, y: player.y - player.h, w: player.hw * 2, h: player.h };
        if (h.next <= 0 && rects(box, h)) {
          const scaled = h.permanent || h.dmg > 20 ? h.dmg : Math.round(h.dmg * (world.tier ? world.tier.dmg : 1));
          hurtPlayer(scaled, h.x + h.w / 2);
          h.next = 0.48;
          if (!h.permanent) h.life = Math.min(h.life, 0.05);
        }
      }
    }
  }
  world.hazards = world.hazards.filter((h) => h.permanent || h.life > 0);
  world.platforms = world.platforms.filter((p) => !p.dead);
}

function updateDrops(dt) {
  for (const d of world.drops) {
    d.life -= dt;
    d.vy = Math.min(420, d.vy + 900 * dt);
    d.y += d.vy * dt;
    if (d.y > GROUND) { d.y = GROUND; d.vy = 0; }
    const dist = Math.hypot(player.x - d.x, (player.y - 20) - d.y);
    if (dist < 70) {
      d.x += (player.x - d.x) * 8 * dt;
      d.y += ((player.y - 20) - d.y) * 8 * dt;
    }
    if (dist < 22) {
      save.crystals += d.value;
      persist();
      floatText(d.x, d.y - 10, "+" + d.value, "#9fd8ff");
      sfx("coin");
      if (healFraction(0.5)) floatText(d.x, d.y - 28, "meia vida", "#b6ffb0");
      d.life = 0;
    }
  }
  world.drops = world.drops.filter((d) => d.life > 0);
  for (const p of world.particles) {
    p.life -= dt;
    p.x += p.vx * dt;
    p.y += p.vy * dt;
  }
  world.particles = world.particles.filter((p) => p.life > 0);
  for (const t of world.texts) { t.life -= dt; t.y -= 24 * dt; }
  world.texts = world.texts.filter((t) => t.life > 0);
}

function tryChests() {
  if (!pressed.KeyE || !world.chests) return;
  for (const c of world.chests) {
    if (save.chests[c.id]) continue;
    if (Math.abs(player.x - c.x) < 36 && Math.abs(player.y - c.y) < 30) {
      save.chests[c.id] = true;
      save.crystals += c.value;
      persist();
      sfx("coin");
      floatText(c.x, c.y - 40, "+" + c.value + " baú", "#9fd8ff");
      if (healFraction(1)) floatText(c.x, c.y - 58, "vida cheia", "#b6ffb0");
    }
  }
}

function defeatBoss() {
  const b = world.boss;
  if (!b || b.rewarded) return;
  b.rewarded = true;
  const id = world.zone.id;
  const first = !save.cleared[id];
  const reward = Math.round((first ? 58 : 26) * world.tier.reward);
  save.crystals += reward;
  if (first) {
    save.cleared[id] = true;
    if (id !== "industrial") save.tierCleared[id] = world.tier.id;
    if (world.zone.ability) save.abilities[world.zone.ability] = true;
  }
  save.pendingZone = id;
  save.pendingMsg = first ? RESTORE[id] : "Você cruzou esta região de novo.";
  persist();
  if (id === "industrial" && first) openEnding(reward);
  else openUnlock(first, reward);
}

function openUnlock(first, reward) {
  const zone = world.zone;
  const ab = ABILITIES[zone.ability];
  document.getElementById("unlock-kicker").textContent = first ? "Chefe derrotado" : "Reviver";
  document.getElementById("unlock-name").textContent = first && ab ? ab.name : zone.bossName + " caiu";
  document.getElementById("unlock-desc").textContent = first && ab ? ab.desc : "Você já conhecia este lugar. +" + reward + " cristais.";
  document.getElementById("unlock-restore").textContent = (first ? RESTORE[zone.id] + " " : "") + "+" + reward + " cristais.";
  openPanel("unlock");
}
function openEnding(reward) {
  openPanel("ending");
  save.pendingMsg = RESTORE.industrial + " +" + reward + " cristais.";
  persist();
}

function updateHub(dt) {
  updatePlayer(dt);
  if (pressed.KeyE) {
    if (Math.abs(player.x - 220) < 70 && Math.abs(player.y - GROUND) < 20) openShop();
    else {
      for (let i = 0; i < ZONES.length; i++) {
        if (Math.abs(player.x - PORTAL_X[i]) < 54 && Math.abs(player.y - GROUND) < 24) openZone(ZONES[i].id);
      }
    }
  }
  if (pressed.Escape) openPanel("pause");
}

function updateLevel(dt) {
  updatePlayer(dt);
  if (uiOpen) return;
  if (world.arena && !world.arena.locked && player.x > world.arena.lock && player.x < world.arena.x + world.arena.w) {
    world.arena.locked = true;
    world.platforms.push(world.leftWall);
    world.boss.state = "intro";
    world.boss.t = 1.15;
    world.banner = world.zone.bossName;
    world.bannerT = 2.2;
    sfx("roar");
  }
  updateEnemies(dt);
  updateBoss(dt);
  updateHazards(dt);
  updateDrops(dt);
  tryChests();
  if (pressed.Escape) openPanel("pause");
}

function openShop() {
  const list = document.getElementById("shop-list");
  document.getElementById("shop-wallet").textContent = "Cristais: " + save.crystals;
  list.innerHTML = "";
  for (const item of SHOP_ITEMS) {
    const row = document.createElement("div");
    row.className = "shop-item";
    const info = document.createElement("div");
    const title = document.createElement("strong");
    const desc = document.createElement("p");
    const btn = document.createElement("button");
    btn.type = "button";
    if (item.id === "pot") {
      title.textContent = item.name;
      desc.textContent = item.desc + " Na bolsa: " + save.potions + "/3.";
      btn.textContent = save.potions >= 3 ? "Cheia" : item.price + " cristais";
      btn.disabled = save.potions >= 3 || save.crystals < item.price;
      btn.onclick = () => {
        if (save.crystals < item.price || save.potions >= 3) return;
        save.crystals -= item.price;
        save.potions += 1;
        persist();
        sfx("buy");
        openShop();
      };
    } else {
      const rank = save[item.rank] || 0;
      title.textContent = item.name + "  " + rank + "/" + item.max;
      desc.textContent = item.desc;
      if (rank >= item.max) {
        btn.textContent = "Máximo";
        btn.disabled = true;
      } else {
        const price = item.prices[rank];
        btn.textContent = price + " cristais";
        btn.disabled = save.crystals < price;
        btn.onclick = () => {
          if (save.crystals < price) return;
          save.crystals -= price;
          save[item.rank] = rank + 1;
          if (player) player.hp = maxHp();
          persist();
          sfx("buy");
          openShop();
        };
      }
    }
    info.append(title, desc);
    row.append(info, btn);
    list.append(row);
  }
  openPanel("shop");
}

function openZone(id) {
  const zone = zoneById(id);
  const tier = previewTier(id);
  const locked = id === "industrial" && clearedCount() < 5;
  const replay = !!save.cleared[id];
  const n = clearedCount();
  document.getElementById("zone-kicker").textContent = replay ? "Região restaurada" : "Escolher região";
  document.getElementById("zone-name").textContent = zone.name;
  let tierText;
  if (id === "industrial") {
    tierText = "Grau Final. Esta fase só abre depois das outras cinco e é sempre a mais dura, não importa a ordem anterior.";
  } else if (replay) {
    tierText = "Reviver no grau em que você a venceu: " + tier.name + ". A habilidade já é sua. Inimigos e o chefe voltam, com menos cristais.";
  } else {
    const ord = ["primeira", "segunda", "terceira", "quarta", "quinta"][n] || "próxima";
    tierText = "Esta será a sua " + ord + " região, então o grau é " + tier.name + ". A dificuldade segue a ordem das vitórias, não o nome do mapa.";
  }
  document.getElementById("zone-tier").textContent = tierText;
  const names = zone.enemies.map((e) => e.name).join(", ");
  document.getElementById("zone-enemies").textContent = "Três espécies: " + names + ". Chefe: " + zone.bossName + ", " + zone.bossSub + ".";
  const lock = document.getElementById("zone-lock");
  lock.textContent = locked ? "O portal ainda está selado. Restaure as outras cinco regiões." : "";
  const go = document.getElementById("zone-go");
  go.disabled = locked;
  go.onclick = () => {
    if (locked) return;
    startLevel(zone, tier, replay && id !== "industrial");
  };
  openPanel("zone");
}

function drawCover(img) {
  const scale = Math.max(VW / img.width, VH / img.height);
  const dw = img.width * scale, dh = img.height * scale;
  ctx.drawImage(img, (VW - dw) / 2, (VH - dh) / 2, dw, dh);
}
function drawParallax(img) {
  ctx.fillStyle = "#8ec8ea";
  ctx.fillRect(0, 0, VW, VH);
  if (!img) return;
  const dh = Math.floor(VH * 0.7);
  const scale = dh / img.height;
  const dw = img.width * scale;
  let shift = (cam.x * 0.28) % dw;
  if (shift < 0) shift += dw;
  for (let x = -shift; x < VW; x += dw - 1) ctx.drawImage(img, x, 0, dw + 1, dh);
  const fade = ctx.createLinearGradient(0, dh - 70, 0, dh + 8);
  fade.addColorStop(0, "rgba(142,200,234,0)");
  fade.addColorStop(1, "rgba(142,200,234,1)");
  ctx.fillStyle = fade;
  ctx.fillRect(0, dh - 70, VW, 80);
}
function blit(spr, x, y, h, flip, screen) {
  if (!spr || !spr.width) return;
  const w = h * (spr.width / spr.height);
  ctx.save();
  ctx.translate(Math.round(screen ? x : x - cam.x), Math.round(screen ? y : y - cam.y));
  if (flip) ctx.scale(-1, 1);
  ctx.drawImage(spr, Math.round(-w / 2), Math.round(-h), Math.round(w), Math.round(h));
  ctx.restore();
}
function screenText(text, x, y, size, color, align) {
  ctx.save();
  ctx.font = size + "px 'Press Start 2P', monospace";
  ctx.textAlign = align || "center";
  ctx.fillStyle = "#102018";
  ctx.fillText(text, x + 2, y + 2);
  ctx.fillStyle = color || "#f6edd4";
  ctx.fillText(text, x, y);
  ctx.restore();
}
function drawBar(x, y, w, h, ratio, fill, back) {
  ctx.fillStyle = back;
  ctx.fillRect(x, y, w, h);
  ctx.fillStyle = fill;
  ctx.fillRect(x, y, Math.max(0, w * clamp(ratio, 0, 1)), h);
  ctx.strokeStyle = "#0c121c";
  ctx.strokeRect(x + 0.5, y + 0.5, w - 1, h - 1);
}
function drawPlatform(p) {
  const tile = S.tiles[p.tile] || S.tiles[0];
  if (p.gate) {
    const spr = p.gate === "shot" ? S.tiles[4] : S.fx[3];
    ctx.drawImage(spr, p.x - cam.x, p.y - cam.y, p.w, p.h);
    return;
  }
  const size = 64;
  ctx.save();
  ctx.beginPath();
  ctx.rect(p.x - cam.x, p.y - cam.y - 16, p.w, p.h + 16);
  ctx.clip();
  for (let x = p.x; x < p.x + p.w; x += size - 1) {
    ctx.drawImage(tile, x - cam.x, p.y - cam.y - 14, size, size);
  }
  const dirtTop = p.y - 14 + size - 10;
  const dirtH = p.y + p.h - dirtTop;
  if (dirtH > 4) {
    for (let x = p.x; x < p.x + p.w; x += size - 1) {
      ctx.drawImage(tile, 0, tile.height * 0.58, tile.width, tile.height * 0.42, x - cam.x, dirtTop - cam.y, size, dirtH);
    }
  }
  ctx.restore();
}

function drawPlayer() {
  let frame = 0;
  if (player.hurt > 0.4) frame = 4;
  else if (player.atk > 0) frame = 3;
  else if (!player.onGround) frame = 2;
  else if (Math.abs(player.vx) > 20) frame = Math.floor(time * 8) % 2 === 0 ? 1 : 0;
  const spr = S.kai[frame] || S.kai[0];
  ctx.globalAlpha = 0.35;
  ctx.fillStyle = "#041018";
  ctx.beginPath();
  ctx.ellipse(player.x - cam.x, player.y - cam.y + 2, 16, 5, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.globalAlpha = player.hurt > 0 && Math.floor(time * 16) % 2 === 0 ? 0.45 : 1;
  blit(spr, player.x, player.y, 86, player.dir === -1);
  ctx.globalAlpha = 1;
  if (player.atk > 0.05) blit(S.fx[0], player.x + player.dir * 34, player.y - 16, 36, player.dir === -1);
  if (player.dash > 0) blit(S.fx[7], player.x - player.dir * 20, player.y - 20, 40, false);
}

function drawLumi() {
  const lx = player.x - player.dir * 28;
  const ly = player.y - 62 + Math.sin(time * 4) * 4;
  const frame = Math.floor(time * 3) % 3 === 2 ? 2 : 0;
  blit(S.lumi[frame], lx, ly, 42, false);
}

function renderTitle() {
  drawCover(S.bg_title[0]);
  const logo = S.logo[0];
  const lh = 210;
  const lw = lh * (logo.width / logo.height);
  ctx.drawImage(logo, 24, 8, lw, lh);
}

function renderWorld() {
  ctx.save();
  if (shake > 0.4) ctx.translate((Math.random() - 0.5) * shake, (Math.random() - 0.5) * shake);
  drawParallax(world.bg);
  ctx.fillStyle = world.mode === "hub" ? "#163628" : "#101810";
  ctx.fillRect(0, GROUND + 8, VW, VH - GROUND);
  if (world.mode === "hub") drawHubProps();
  for (const p of world.platforms) drawPlatform(p);
  if (world.chests) {
    for (const c of world.chests) {
      if (save.chests[c.id]) continue;
      blit(S.items[3], c.x, c.y, 36, false);
    }
  }
  for (const d of world.drops) blit(S.items[0], d.x, d.y, 22, false);
  for (const h of world.hazards) drawHazard(h);
  for (const e of world.enemies) drawEnemy(e);
  if (world.boss && world.arena) drawBoss(world.boss);
  drawPlayer();
  drawLumi();
  for (const p of world.particles) {
    ctx.globalAlpha = Math.max(0, p.life / p.max);
    blit(S.fx[p.spr] || S.fx[7], p.x, p.y, p.s, false);
    ctx.globalAlpha = 1;
  }
  for (const t of world.texts) {
    ctx.globalAlpha = Math.max(0, t.life * 1.4);
    screenText(t.t, t.x - cam.x, t.y - cam.y, 8, t.color);
    ctx.globalAlpha = 1;
  }
  ctx.restore();
  drawHUD();
  if (world.bannerT > 0) {
    screenText(world.banner, VW / 2, 78, 12, "#fff6df");
  }
}

function drawHubProps() {
  blit(S.hub[0], 220, GROUND, 150, false);
  blit(S.hub[1], 430, GROUND, 110, false);
  blit(S.hub[2], 620, GROUND, 120, false);
  ZONES.forEach((z, i) => {
    const x = PORTAL_X[i];
    if (i < 5) {
      const sheet = save.cleared[z.id] ? S.restored : S.ruined;
      blit(sheet[i], x, GROUND + 6, 168, false);
    }
    const open = z.id === "industrial" ? clearedCount() >= 5 : true;
    const door = save.cleared[z.id] || (z.id === "industrial" && open) ? S.items[5] : S.items[4];
    if (z.id === "industrial" && clearedCount() < 5) blit(S.items[4], x, GROUND, 132, false);
    else blit(door, x, GROUND, 132, false);
    const tier = previewTier(z.id);
    let label = save.cleared[z.id] ? "Restaurada" : tier.name;
    if (z.id === "industrial" && clearedCount() < 5) label = "Selado";
    if (z.id === "industrial" && save.cleared[z.id]) label = "Em paz";
    screenText(z.name, x - cam.x, GROUND - 168, 8, "#fff6df");
    screenText(label, x - cam.x, GROUND - 150, 8, save.cleared[z.id] ? "#b6ffb0" : "#ffe08a");
  });
  screenText("Loja", 220 - cam.x, GROUND - 160, 8, "#fff6df");
  if (!has("double")) screenText("salto duplo", 120 - cam.x, GROUND - 230, 7, "#d5e6cf");
  if (!has("dash")) screenText("correnteza", 300 - cam.x, GROUND - 120, 7, "#d5e6cf");
  if (!has("wall")) screenText("garra glacial", 3250 - cam.x, GROUND - 280, 7, "#d5e6cf");
  const nearShop = Math.abs(player.x - 220) < 70;
  let near = nearShop ? "E  Loja" : "";
  ZONES.forEach((z, i) => {
    if (Math.abs(player.x - PORTAL_X[i]) < 54) near = z.id === "industrial" && clearedCount() < 5 ? "Selado" : "E  Entrar";
  });
  if (world.chests) { /* hub has none */ }
  if (near) screenText(near, player.x - cam.x, player.y - 86, 8, "#fff6df");
}

function drawEnemy(e) {
  const sheet = S["e" + world.zone.id];
  const spr = sheet[e.type];
  blit(spr, e.x, e.y + Math.sin(time * 2 + e.x) * (e.fly ? 0 : 1), e.h + 16, e.dir === 1);
  if (e.hp < e.max) {
    drawBar(e.x - cam.x - 16, e.y - cam.y - e.h - 12, 32, 4, e.hp / e.max, "#e23d4a", "#2a1218");
  }
}

function drawBoss(b) {
  const spr = S["boss_" + b.def.id][0];
  if (b.flash > 0) ctx.globalAlpha = 0.65;
  blit(spr, b.x, b.y, b.def.drawH, b.dir === 1);
  ctx.globalAlpha = 1;
  if (b.def.orbit && b.phase >= 2 && world.arena.locked) {
    const ang = time * 3.2;
    for (let i = 0; i < 2; i++) {
      blit(S.fx[1], b.x + Math.cos(ang + i * Math.PI) * 92, b.y - 70 + Math.sin(ang + i * Math.PI) * 26, 28, false);
    }
  }
  if (!world.arena.locked) return;
  screenText(b.def.bossName, VW / 2, 22, 11, "#fff6df");
  screenText(b.def.bossSub + "  ·  fase " + b.phase, VW / 2, 40, 8, "#d5e6cf");
  const col = b.phase >= 3 ? "#ffb020" : b.phase === 2 ? "#ff7a3c" : "#e23d4a";
  drawBar(VW / 2 - 220, 50, 440, 14, b.hp / b.max, col, "#2a1218");
  if (b.state === "tell") screenText(b.pattern === "pound" ? "PULO!" : "!", b.x - cam.x, b.y - b.h - 16, 12, "#ffd0a1");
}

function drawHazard(h) {
  if (h.kind === "proj") {
    ctx.save();
    ctx.translate(h.x - cam.x, h.y - cam.y);
    if (h.spin) ctx.rotate(time * 12);
    const spr = S.fx[h.spr] || S.fx[5];
    const s = 28;
    ctx.drawImage(spr, -s / 2, -s / 2, s, s);
    ctx.restore();
  } else if (h.kind === "zone") {
    const alpha = h.warn > 0 ? 0.35 + Math.sin(time * 24) * 0.15 : 0.8;
    ctx.globalAlpha = alpha;
    if (h.beam) {
      ctx.drawImage(S.fx[5], h.x - cam.x, h.y - cam.y, h.w, h.h);
    } else if (h.permanent) {
      for (let x = h.x; x < h.x + h.w; x += 28) blit(S.fx[6], x, h.y + h.h, 26, false);
    } else {
      blit(S.fx[h.spr] || S.fx[7], h.x + h.w / 2, h.y + h.h, h.warn > 0 ? 30 : 48, false);
    }
    ctx.globalAlpha = 1;
  }
}

function drawHUD() {
  blit(S.kai[0], 58, 86, 70, false, true);
  screenText("KAI", 100, 28, 10, "#fff6df", "left");
  screenText("Nv." + (1 + clearedCount()), 100, 46, 8, "#d5e6cf", "left");
  drawBar(100, 56, 170, 12, player.hp / maxHp(), "#e23d4a", "#3a141c");
  screenText(Math.ceil(player.hp) + "/" + maxHp(), 278, 66, 8, "#fff6df", "left");
  blit(S.items[0], 118, 96, 18, false, true);
  screenText(String(save.crystals), 132, 92, 8, "#9fd8ff", "left");
  blit(S.items[2], 210, 96, 20, false, true);
  screenText(String(save.potions), 224, 92, 8, "#b6ffb0", "left");
  const icons = [
    ["pulo", "pulo", true],
    ["double", "raiz", false],
    ["dash", "dash", false],
    ["spores", "esporo", false],
    ["wall", "parede", false],
    ["shot", "tiro", false],
  ];
  let ix = 100;
  icons.forEach(([id, label, always]) => {
    if (!always && !has(id)) return;
    screenText(label, ix + 16, 112, 7, "#d5e6cf");
    ix += 78;
  });
  if (world.mode === "level" && world.tier) {
    ctx.textAlign = "right";
    screenText(world.zone.name, VW - 16, 24, 8, "#fff6df", "right");
    screenText(world.tier.name, VW - 16, 42, 8, "#ffe08a", "right");
  }
}

function interactPromptLevel() {
  if (!world.chests) return;
  for (const c of world.chests) {
    if (save.chests[c.id]) continue;
    if (Math.abs(player.x - c.x) < 36) screenText("E  Baú + vida", c.x - cam.x, c.y - 48, 8, "#fff6df");
  }
}

function loop(now) {
  const dt = Math.min(0.033, (now - (loop.last || now)) / 1000);
  loop.last = now;
  time += dt;
  if (shake > 0) shake *= Math.pow(0.04, dt);
  if (mode === "title") renderTitle();
  else if (!uiOpen) {
    if (mode === "hub") updateHub(dt);
    else updateLevel(dt);
    if (world.bannerT > 0) world.bannerT -= dt;
    const target = clamp(player.x - VW * 0.42, 0, Math.max(0, world.w - VW));
    cam.x += (target - cam.x) * Math.min(1, dt * 6);
    if (world.arena && world.arena.locked) {
      cam.x = clamp(cam.x, world.arena.x, Math.max(world.arena.x, world.arena.x + world.arena.w - VW));
    }
    ctx.clearRect(0, 0, VW, VH);
    renderWorld();
    if (mode === "level") interactPromptLevel();
  } else {
    ctx.clearRect(0, 0, VW, VH);
    renderWorld();
  }
  for (const k in pressed) delete pressed[k];
  requestAnimationFrame(loop);
}

function bootUI() {
  document.getElementById("btn-play").onclick = () => { loadSave(); startHub(); };
  document.getElementById("btn-how").onclick = () => openPanel("how");
  document.getElementById("btn-credits").onclick = () => openPanel("credits");
  document.getElementById("btn-new").onclick = () => {
    if (confirm("Apagar o progresso e começar de novo?")) {
      save = defaultSave();
      persist();
      startHub();
    }
  };
  document.getElementById("intro-ok").onclick = () => { save.intro = true; persist(); closePanels(); };
  document.getElementById("zone-back").onclick = closePanels;
  document.getElementById("shop-close").onclick = closePanels;
  document.getElementById("pause-go").onclick = closePanels;
  document.getElementById("pause-how").onclick = () => openPanel("how");
  document.getElementById("pause-hub").onclick = () => startHub();
  document.getElementById("dead-retry").onclick = () => {
    if (world && world.zone) startLevel(world.zone, world.tier, world.replay);
    else startHub();
  };
  document.getElementById("dead-hub").onclick = () => startHub();
  document.getElementById("unlock-ok").onclick = () => startHub();
  document.getElementById("ending-ok").onclick = () => startHub();
  document.querySelectorAll("[data-close]").forEach((b) => b.addEventListener("click", () => {
    if (mode === "title") closePanels();
    else openPanel("pause");
  }));
  window.addEventListener("keydown", (e) => {
    if (e.code === "Escape" && uiOpen && mode !== "title") {
      const dead = !document.getElementById("panel-dead").classList.contains("hidden");
      const unlock = !document.getElementById("panel-unlock").classList.contains("hidden");
      const ending = !document.getElementById("panel-ending").classList.contains("hidden");
      if (!dead && !unlock && !ending) closePanels();
    }
  });
}

async function boot() {
  bootUI();
  try {
    await loadAll();
    if (document.fonts && document.fonts.load) await document.fonts.load("16px 'Press Start 2P'");
    loadSave();
    const play = document.getElementById("btn-play");
    play.disabled = false;
    document.getElementById("loadstate").textContent = localStorage.getItem(SAVE_KEY)
      ? "O santuário lembra de você."
      : "A natureza precisa de novos guardiões.";
    if (localStorage.getItem(SAVE_KEY)) document.getElementById("btn-new").classList.remove("hidden");
    requestAnimationFrame(loop);
  } catch (err) {
    document.getElementById("loadstate").textContent = "Não consegui carregar um sprite: " + err.message;
  }
}

boot();
