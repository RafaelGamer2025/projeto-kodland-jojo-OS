import random
import string

batalhas = {}

battles = {
    "Star Platinum vs The World": {
        "player": "Star Platinum",
        "enemy": "The World"
    },
    "Killer Queen vs D4C": {
        "player": "Killer Queen",
        "enemy": "D4C"
    },
    "Wonder of U vs Star Platinum": {
        "player": "Wonder of U",
        "enemy": "Star Platinum"
    }
}


STANDS = {

    "Star Platinum": {

        "power": 9,
        "speed": 10,
        "range": 3,

        "skill": "ORA ORA BARRAGE",
        "desc": "Uma sequência absurda de socos.",

        "crit": 0.30,

        "color": "#4361EE"
    },

    "The World": {

        "power": 10,
        "speed": 9,
        "range": 4,

        "skill": "ZA WARUDO",
        "desc": "Para o tempo por 1 turno.",

        "time_stop": True,

        "color": "#FFD60A"
    },

    "Killer Queen": {

        "power": 8,
        "speed": 7,
        "range": 5,

        "skill": "BITE THE DUST",
        "desc": "Explosão devastadora.",

        "bomb": True,

        "color": "#FF4D6D"
    },

    "D4C": {

        "power": 8,
        "speed": 7,
        "range": 8,

        "skill": "LOVE TRAIN",
        "desc": "Desvia dano automaticamente.",

        "love_train": True,

        "color": "#80ED99"
    },

    "Wonder of U": {

        "power": 7,
        "speed": 8,
        "range": 10,

        "skill": "CALAMITY",
        "desc": "Reflete ataques.",

        "reflect": True,

        "color": "#9D4EDD"
    }
}

def criar_lutador(stand):
    return {
        "stand": stand,
        "hp": 100
    }

def turno_batalha(player, enemy):
    p = STANDS[player["stand"]]
    e = STANDS[enemy["stand"]]

    log = []

    # dano base
    dano_p = random.randint(10, 20) + p["power"]
    dano_e = random.randint(10, 20) + e["power"]

    # crítico
    if random.random() < p.get("crit", 0):
        dano_p *= 2
        log.append("💥 CRÍTICO DO PLAYER!")

    if random.random() < e.get("crit", 0):
        dano_e *= 2
        log.append("💥 CRÍTICO DO INIMIGO!")

    # ZA WARUDO
    if e.get("time_stop") and random.random() < 0.3:
        log.append("⏱️ ZA WARUDO! Inimigo atacou sozinho!?")
        player["hp"] -= dano_e
        return log

    # LOVE TRAIN
    if p.get("love_train") and random.random() < 0.4:
        log.append("🌈 LOVE TRAIN desviou o dano!")
        dano_e = 0

    # REFLECT
    if e.get("reflect"):
        reflect = int(dano_p * 0.3)
        player["hp"] -= reflect
        log.append(f"🔁 Reflect causou {reflect} de dano!")

    # BOMB
    if p.get("bomb") and random.random() < 0.3:
        dano_p += 15
        log.append("💣 BITE THE DUST!")

    # aplicar dano
    enemy["hp"] -= dano_p
    player["hp"] -= dano_e

    log.append(f"⚔️ Você causou {dano_p}")
    log.append(f"🩸 Inimigo causou {dano_e}")

    return log