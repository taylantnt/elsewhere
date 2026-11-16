################################################################################
## ORBIT DEFENDER — ARCADE SHOOTER
################################################################################
##
## An endless arcade wave shooter built from Ren'Py screen displayables.
## Waves keep arriving until the ship is destroyed; the level count is endless.
##
## Controls: Hold Left/Right arrows or A/D to move. The ship fires automatically.
## Story use: call minigame_arcade_shooter
## Test: jump test_arcade_shooter
##

init python:
    import math
    import random

    # NOTE: do not write `import renpy.foo` at this scope. Store-level imports
    # rebind the name `renpy` from Ren'Py's exports alias to the bare package,
    # which lacks music/sound/get_side_image and breaks every later init block.
    # Use the already-exposed aliases instead: renpy.sound.play(...),
    # renpy.music.*, etc.

    # Sprite offset / size relative to the 32x24 enemy hitbox.
    ARCADE_ENEMY_GEO = {
        "grunt": (8, 2, 46, 36),
        "striker": (8, 2, 42, 34),
        "bulwark": (7, 2, 44, 34),
        "sentinel": (9, 2, 64, 50),
    }

    class ArcadeShooterEngine(object):

        FORMATIONS = ("grid", "wedge", "diamond", "columns", "arc", "brick")
        FORMATION_LABELS = {
            "grid": "STANDARD GRID",
            "wedge": "WEDGE",
            "diamond": "DIAMOND",
            "columns": "TWIN COLUMNS",
            "arc": "CRESCENT",
            "brick": "STAGGERED",
        }
        ENEMY_ROWS = ("grunt", "striker", "bulwark", "sentinel")
        ENEMY_STATS = {
            "grunt": {"hp": 1, "score": 10},
            "striker": {"hp": 1, "score": 20},
            "bulwark": {"hp": 2, "score": 30},
            "sentinel": {"hp": 2, "score": 50},
        }

        def __init__(self):
            self.playfield_width = 960
            self.playfield_height = 500

            self.player_width = 46
            self.player_height = 26
            self.player_y = 452
            self.player_x = (self.playfield_width - self.player_width) / 2.0
            self.player_speed = 370.0

            self.player_bullets = []
            self.enemy_bullets = []
            self.powerups = []
            self.explosions = []
            self.sparks = []

            self.fire_cooldown = 0.0
            self.muzzle_timer = 0.0
            self.invulnerable_timer = 0.0
            self.rapid_fire_timer = 0.0
            self.spread_shot_timer = 0.0
            self.armor = 0
            self.lives = 3

            self.score = 0
            self.level = 1
            self.elapsed = 0.0
            self.phase = "playing"
            self.status_message = ""
            self.level_banner_timer = 0.0
            self.wave_timer = 0.0
            self.shake_timer = 0.0

            self.player_thrust = 0.25
            self.enemy_direction = 1
            self.enemy_speed = 44.0
            self.enemy_fire_timer = 0.95

            self.formation = "grid"
            self.formation_label = "STANDARD GRID"
            self.wave_enemy_count = 0
            self.enemies_left = 0

            self.stars = []
            for _ in range(72):
                size = random.choice((1, 1, 1, 2, 3))
                self.stars.append({
                    "x": random.uniform(0.0, self.playfield_width),
                    "y": random.uniform(0.0, self.playfield_height),
                    "speed": 20.0 + size * 22.0 + random.uniform(0.0, 26.0),
                    "size": size,
                })

            self.spawn_wave()

        # ---------------------------------------------------------------- waves

        def formation_slots(self, formation):
            rows = min(4 + (self.level - 1) // 3, 6)
            cols = 8
            spacing = 104.0
            top = 48.0
            step_y = 54.0
            slots = []

            def centered(count, shift=0.0):
                width = (count - 1) * spacing + 32.0
                return (self.playfield_width - width) / 2.0 + shift

            if formation == "wedge":
                for row in range(rows):
                    count = max(4, cols - row)
                    start = centered(count)
                    for column in range(count):
                        slots.append((start + column * spacing, top + row * step_y, row))

            elif formation == "diamond":
                for row in range(rows):
                    distance = abs(row - (rows - 1) / 2.0)
                    count = max(4, cols - int(distance * 2))
                    start = centered(count)
                    for column in range(count):
                        slots.append((start + column * spacing, top + row * step_y, row))

            elif formation == "columns":
                for row in range(rows):
                    start = centered(cols)
                    for column in (0, 1, 2, 5, 6, 7):
                        slots.append((start + column * spacing, top + row * step_y, row))

            elif formation == "arc":
                for row in range(rows):
                    start = centered(cols)
                    for column in range(cols):
                        arc = (abs(column - (cols - 1) / 2.0) ** 1.6) * 3.6
                        slots.append((start + column * spacing, top + row * step_y + arc, row))

            elif formation == "brick":
                for row in range(rows):
                    count = 7
                    start = centered(count, spacing * 0.5 if row % 2 else 0.0)
                    for column in range(count):
                        slots.append((start + column * spacing, top + row * step_y, row))

            else:  # grid
                start = centered(cols)
                for row in range(rows):
                    for column in range(cols):
                        slots.append((start + column * spacing, top + row * step_y, row))

            return slots

        def spawn_wave(self):
            self.player_bullets = []
            self.enemy_bullets = []
            self.powerups = []
            self.enemies = []

            index = (self.level - 1) % len(self.FORMATIONS)
            self.formation = self.FORMATIONS[index]
            self.formation_label = self.FORMATION_LABELS[self.formation]

            for enemy_id, (x, y, row) in enumerate(self.formation_slots(self.formation)):
                enemy_type = self.ENEMY_ROWS[min(row, len(self.ENEMY_ROWS) - 1)]
                self.enemies.append({
                    "id": enemy_id,
                    "x": x,
                    "y": y,
                    "row": row,
                    "type": enemy_type,
                    "hp": self.ENEMY_STATS[enemy_type]["hp"],
                    "alive": True,
                    "flash": 0.0,
                    "phase": random.uniform(0.0, math.tau),
                })

            self.wave_enemy_count = len(self.enemies)
            self.enemies_left = self.wave_enemy_count
            self.enemy_direction = 1
            self.enemy_speed = min(118.0, 44.0 + (self.level - 1) * 6.0)
            self.enemy_fire_timer = max(0.32, 0.95 - (self.level - 1) * 0.05)
            self.level_banner_timer = 2.2

        def begin_wave_clear(self):
            bonus = 50 * self.level
            self.score += bonus
            self.level += 1
            self.phase = "wave_clear"
            self.wave_timer = 1.35
            self.status_message = "LEVEL CLEARED   +%d" % bonus
            self.player_bullets = []
            self.enemy_bullets = []
            self.powerups = []
            self.enemies_left = 0
            self.level_banner_timer = 0.0
            renpy.sound.play("audio/SFX/arcade_wave.wav")

        # ------------------------------------------------------------- effects

        def add_explosion(self, x, y, scale=1.0):
            self.explosions.append({
                "x": x,
                "y": y,
                "life": 0.38,
                "duration": 0.38,
                "scale": scale,
            })

        def add_sparks(self, x, y, count=6):
            for _ in range(count):
                angle = random.uniform(0.0, math.tau)
                speed = random.uniform(40.0, 150.0)
                self.sparks.append({
                    "x": x,
                    "y": y,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": 0.32,
                    "duration": 0.32,
                })

        def update_effects(self, dt):
            for explosion in self.explosions:
                explosion["life"] -= dt
            self.explosions = [e for e in self.explosions if e["life"] > 0.0]

            for spark in self.sparks:
                spark["life"] -= dt
                spark["x"] += spark["vx"] * dt
                spark["y"] += spark["vy"] * dt
                damping = max(0.0, 1.0 - 2.6 * dt)
                spark["vx"] *= damping
                spark["vy"] *= damping
            self.sparks = [s for s in self.sparks if s["life"] > 0.0]

            for enemy in self.enemies:
                enemy["flash"] = max(0.0, enemy["flash"] - dt)
            self.enemies = [e for e in self.enemies if e["alive"] or e["flash"] > 0.0]

        def update_stars(self, dt):
            for star in self.stars:
                star["y"] += star["speed"] * dt
                if star["y"] >= self.playfield_height:
                    star["y"] = 0.0
                    star["x"] = random.uniform(0.0, self.playfield_width)

        # -------------------------------------------------------------- player

        def move_player(self, direction, dt=0.06):
            if self.phase == "lost":
                return
            self.player_x += direction * self.player_speed * dt
            self.player_x = max(8.0, min(self.playfield_width - self.player_width - 8.0, self.player_x))

        def fire(self):
            if self.phase != "playing" or self.fire_cooldown > 0.0:
                return

            center_x = self.player_x + self.player_width / 2.0
            offsets = (-16.0, 0.0, 16.0) if self.spread_shot_timer > 0.0 else (0.0,)
            for offset in offsets:
                self.player_bullets.append({
                    "x": center_x + offset,
                    "y": self.player_y - 12.0,
                    "previous_y": self.player_y - 12.0,
                })

            self.fire_cooldown = 0.13 if self.rapid_fire_timer > 0.0 else 0.30
            self.muzzle_timer = 0.07
            renpy.sound.play("audio/SFX/arcade_laser.wav")

        def collect_powerup(self, powerup):
            if powerup["kind"] == "rapid":
                self.rapid_fire_timer = 8.0
            elif powerup["kind"] == "spread":
                self.spread_shot_timer = 8.0
            else:
                self.armor = min(2, self.armor + 1)

            self.score += 25
            self.add_explosion(self.player_x + self.player_width / 2.0, self.player_y + 10.0, 0.7)
            renpy.sound.play("audio/SFX/arcade_powerup.wav")

        def damage_player(self):
            line_x = self.player_x + self.player_width / 2.0
            line_y = self.player_y + self.player_height / 2.0
            self.shake_timer = 0.3

            if self.armor > 0:
                self.armor -= 1
                self.invulnerable_timer = 0.8
                self.add_explosion(line_x, line_y, 0.8)
                renpy.sound.play("audio/SFX/arcade_shield_hit.wav")
                return

            self.lives -= 1
            self.invulnerable_timer = 1.2
            self.add_explosion(line_x, line_y, 1.1)
            self.add_sparks(line_x, line_y, 12)
            renpy.sound.play("audio/SFX/arcade_hit.wav")

            if self.lives <= 0:
                self.phase = "lost"
                self.status_message = "SHIP DISABLED"
                renpy.sound.play("audio/SFX/arcade_gameover.wav")

        # ---------------------------------------------------------------- enemy

        def kill_enemy(self, enemy):
            enemy["alive"] = False
            enemy["flash"] = 0.1
            self.enemies_left = max(0, self.enemies_left - 1)
            self.score += self.ENEMY_STATS[enemy["type"]]["score"]
            self.add_explosion(enemy["x"] + 16.0, enemy["y"] + 12.0)
            self.add_sparks(enemy["x"] + 16.0, enemy["y"] + 12.0, 7)
            renpy.sound.play("audio/SFX/arcade_explosion.wav")

            if len(self.powerups) < 2 and random.random() < 0.2:
                self.powerups.append({
                    "x": enemy["x"] + 16.0,
                    "y": enemy["y"] + 12.0,
                    "previous_y": enemy["y"] + 12.0,
                    "kind": random.choice(("rapid", "spread", "armor")),
                })

        # ----------------------------------------------------------------- tick

        def tick(self, dt):
            if self.phase == "lost":
                return

            dt = max(0.0, min(dt, 0.1))
            self.elapsed += dt
            self.shake_timer = max(0.0, self.shake_timer - dt)
            self.muzzle_timer = max(0.0, self.muzzle_timer - dt)
            self.invulnerable_timer = max(0.0, self.invulnerable_timer - dt)
            self.rapid_fire_timer = max(0.0, self.rapid_fire_timer - dt)
            self.spread_shot_timer = max(0.0, self.spread_shot_timer - dt)
            self.level_banner_timer = max(0.0, self.level_banner_timer - dt)

            self.update_stars(dt)
            self.update_effects(dt)

            if self.phase == "wave_clear":
                self.wave_timer -= dt
                if self.wave_timer <= 0.0:
                    self.phase = "playing"
                    self.spawn_wave()
                return

            pressed_keys = renpy.pygame.key.get_pressed()
            moving_left = pressed_keys[renpy.pygame.K_LEFT] or pressed_keys[renpy.pygame.K_a]
            moving_right = pressed_keys[renpy.pygame.K_RIGHT] or pressed_keys[renpy.pygame.K_d]
            direction = 1 if moving_right else -1 if moving_left else 0
            if direction != 0:
                self.move_player(direction, dt)
                self.player_thrust = random.uniform(0.72, 1.0)
            else:
                self.player_thrust = 0.25

            self.fire_cooldown = max(0.0, self.fire_cooldown - dt)
            if self.fire_cooldown <= 0.0:
                self.fire()

            alive_enemies = [enemy for enemy in self.enemies if enemy["alive"]]
            if not alive_enemies:
                self.begin_wave_clear()
                return

            left_edge = min(enemy["x"] for enemy in alive_enemies)
            right_edge = max(enemy["x"] for enemy in alive_enemies) + 32.0
            step = self.enemy_speed * dt
            if (self.enemy_direction > 0 and right_edge + step >= self.playfield_width - 12) or (
                self.enemy_direction < 0 and left_edge - step <= 12
            ):
                self.enemy_direction *= -1
                drop = 14.0 + min(10.0, self.level * 0.8)
                for enemy in alive_enemies:
                    enemy["y"] += drop
            else:
                for enemy in alive_enemies:
                    enemy["x"] += self.enemy_direction * step

            killed = self.wave_enemy_count - len(alive_enemies)
            self.enemy_speed = min(150.0, 44.0 + (self.level - 1) * 6.0 + killed * 1.4)

            for bullet in self.player_bullets:
                bullet["previous_y"] = bullet["y"]
                bullet["y"] -= 520.0 * dt
            self.player_bullets = [bullet for bullet in self.player_bullets if bullet["y"] > -2.0]

            for bullet in self.enemy_bullets:
                bullet["previous_y"] = bullet["y"]
                bullet["y"] += bullet["speed"] * dt
            self.enemy_bullets = [
                bullet for bullet in self.enemy_bullets
                if bullet["y"] < self.playfield_height + 2.0
            ]

            for powerup in self.powerups:
                powerup["previous_y"] = powerup["y"]
                powerup["y"] += 120.0 * dt
            self.powerups = [
                powerup for powerup in self.powerups
                if powerup["y"] < self.playfield_height + 6.0
            ]

            for powerup in self.powerups[:]:
                if (
                    powerup["x"] - 15.0 < self.player_x + self.player_width
                    and powerup["x"] + 15.0 > self.player_x
                    and powerup["previous_y"] - 15.0 <= self.player_y + self.player_height
                    and powerup["y"] + 15.0 >= self.player_y
                ):
                    self.powerups.remove(powerup)
                    self.collect_powerup(powerup)

            destroyed_ids = set()
            for bullet in self.player_bullets[:]:
                for enemy in alive_enemies:
                    if (
                        enemy["x"] - 2.0 <= bullet["x"] <= enemy["x"] + 34.0
                        and bullet["y"] <= enemy["y"] + 26.0
                        and bullet["previous_y"] + 10.0 >= enemy["y"]
                    ):
                        enemy["hp"] -= 1
                        enemy["flash"] = 0.1
                        self.player_bullets.remove(bullet)
                        if enemy["hp"] <= 0:
                            destroyed_ids.add(enemy["id"])
                            self.kill_enemy(enemy)
                        else:
                            self.add_sparks(bullet["x"], enemy["y"] + 6.0, 2)
                            renpy.sound.play("audio/SFX/arcade_ui.wav")
                        break

            if destroyed_ids:
                self.enemy_bullets = [
                    bullet for bullet in self.enemy_bullets
                    if bullet.get("source_id") not in destroyed_ids
                ]

            alive_enemies = [enemy for enemy in self.enemies if enemy["alive"]]
            self.enemy_fire_timer -= dt
            if self.enemy_fire_timer <= 0.0 and alive_enemies:
                shooter = random.choice(alive_enemies)
                bullet_y = shooter["y"] + 26.0
                self.enemy_bullets.append({
                    "x": shooter["x"] + 16.0,
                    "y": bullet_y,
                    "previous_y": bullet_y,
                    "source_id": shooter["id"],
                    "speed": min(310.0, 200.0 + self.level * 7.0),
                })
                self.enemy_fire_timer = max(
                    0.3,
                    random.uniform(0.55, 1.05) - (self.level - 1) * 0.03,
                )
                renpy.sound.play("audio/SFX/arcade_enemy_laser.wav")

            if self.invulnerable_timer <= 0.0:
                player_right = self.player_x + self.player_width
                for bullet in self.enemy_bullets[:]:
                    if (
                        bullet["x"] - 3.0 < player_right
                        and bullet["x"] + 3.0 > self.player_x
                        and bullet["previous_y"] <= self.player_y + self.player_height
                        and bullet["y"] + 22.0 >= self.player_y
                    ):
                        self.enemy_bullets.remove(bullet)
                        self.damage_player()
                        break

            if self.phase == "lost":
                return

            if any(enemy["y"] + 26.0 >= self.player_y for enemy in alive_enemies):
                self.phase = "lost"
                self.status_message = "INVADERS REACHED THE SHIP"
                renpy.sound.play("audio/SFX/arcade_gameover.wav")


screen arcade_shooter(engine):
    modal True
    zorder 130

    $ shake_amount = 0.0 if engine.shake_timer <= 0.0 else gui.scale(7) * (engine.shake_timer / 0.3)
    $ shake_x = int(math.sin(engine.elapsed * 131.0) * shake_amount)
    $ shake_y = int(math.cos(engine.elapsed * 97.0) * shake_amount * 0.6)

    add Solid("#050910")

    frame:
        background Solid("#0b1420")
        xalign 0.5
        yalign 0.5
        xsize gui.scale(1040)
        ysize gui.scale(704)
        padding (gui.scale(24), gui.scale(14))

        vbox:
            xfill True
            spacing gui.scale(10)

            fixed:
                xfill True
                ysize gui.scale(16)
                text "ELSEWHERE // ARCADE" size gui.scale(11) bold True color "#7b98b1" kerning gui.scale(2) yalign 0.5
                text "SCORE  [engine.score]" size gui.scale(15) bold True color "#5fb8ff" xalign 1.0 yalign 0.5

            fixed:
                xfill True
                ysize gui.scale(30)
                text "ORBIT DEFENDER" size gui.scale(24) bold True color "#e4f1fa" kerning gui.scale(1) yalign 0.5
                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing gui.scale(16)
                    text "LEVEL  [engine.level]" size gui.scale(13) bold True color "#8ca0b3"
                    text "HOSTILES  [engine.enemies_left]" size gui.scale(13) bold True color "#8ca0b3"
                    text "ARMOR  [engine.armor]" size gui.scale(13) bold True color "#77d98b"
                    text "SHIPS  [engine.lives]" size gui.scale(14) bold True color "#f0b85a"

            fixed:
                xfill True
                ysize gui.scale(16)
                hbox:
                    spacing gui.scale(18)
                    if engine.rapid_fire_timer > 0.0:
                        text "RAPID FIRE  [int(engine.rapid_fire_timer + 0.99)]s" size gui.scale(10) bold True color "#f0b85a"
                    if engine.spread_shot_timer > 0.0:
                        text "SPREAD SHOT  [int(engine.spread_shot_timer + 0.99)]s" size gui.scale(10) bold True color "#5fb8ff"
                    if engine.armor > 0:
                        text "ARMOR ACTIVE" size gui.scale(10) bold True color "#77d98b"

            frame:
                background Solid("#03070d")
                xsize gui.scale(960)
                ysize gui.scale(500)
                padding (0, 0)

                fixed:
                    xysize (gui.scale(960), gui.scale(500))
                    xoffset shake_x
                    yoffset shake_y

                    add "images/arcade/bg_space.png" xysize (gui.scale(960), gui.scale(500))

                    for star in engine.stars:
                        if star["size"] == 3:
                            $ star_color = "#c9e6ff"
                        elif star["size"] == 2:
                            $ star_color = "#7393ad"
                        else:
                            $ star_color = "#36506a"
                        add Solid(star_color) xpos gui.scale(star["x"]) ypos gui.scale(star["y"]) xsize gui.scale(star["size"]) ysize gui.scale(star["size"])

                    add Solid("#16283c") xpos 0 ypos gui.scale(34) xsize gui.scale(960) ysize gui.scale(1)
                    add Solid("#101b29") xpos 0 ypos gui.scale(484) xsize gui.scale(960) ysize gui.scale(1)

                    # Enemies -------------------------------------------------
                    for enemy in engine.enemies:
                        if enemy["alive"] or enemy["flash"] > 0.0:
                            $ enemy_ox, enemy_oy, enemy_w, enemy_h = ARCADE_ENEMY_GEO[enemy["type"]]
                            $ enemy_bob = math.sin(engine.elapsed * 3.0 + enemy["phase"]) * 3.0
                            $ enemy_image = "images/arcade/enemy_%s%s.png" % (enemy["type"], "_flash" if enemy["flash"] > 0.0 else "")
                            $ enemy_alpha = 1.0 if enemy["alive"] else max(0.0, enemy["flash"] / 0.1)
                            add enemy_image:
                                xpos gui.scale(enemy["x"] + enemy_ox)
                                ypos gui.scale(enemy["y"] + enemy_oy + enemy_bob)
                                xysize (gui.scale(enemy_w), gui.scale(enemy_h))
                                alpha enemy_alpha

                    # Ship ----------------------------------------------------
                    $ ship_x = gui.scale(engine.player_x - 1)
                    $ ship_y = gui.scale(engine.player_y - 12)
                    $ ship_alpha = 1.0 if engine.invulnerable_timer <= 0.0 else (0.35 if int(engine.elapsed * 16) % 2 else 1.0)
                    add "images/arcade/glow.png" xpos ship_x + gui.scale(6) ypos ship_y + gui.scale(2) xysize (gui.scale(60), gui.scale(56)) alpha (0.16 * ship_alpha)
                    add "images/arcade/ship.png" xpos ship_x ypos ship_y xysize (gui.scale(48), gui.scale(42)) alpha ship_alpha
                    add "images/arcade/flame.png":
                        xpos gui.scale(engine.player_x + 17)
                        ypos gui.scale(engine.player_y + 26)
                        xysize (max(1, int(gui.scale(14) * engine.player_thrust)), max(1, int(gui.scale(28) * engine.player_thrust)))
                        alpha (0.55 + 0.4 * engine.player_thrust)

                    if engine.muzzle_timer > 0.0:
                        $ muzzle_alpha = engine.muzzle_timer / 0.07
                        add "images/arcade/glow.png" xpos gui.scale(engine.player_x + 11) ypos gui.scale(engine.player_y - 24) xysize (gui.scale(24), gui.scale(24)) alpha (0.55 * muzzle_alpha)

                    if engine.armor > 0:
                        add Solid("#77d98b") xpos gui.scale(engine.player_x + 8) ypos gui.scale(engine.player_y + 2) xsize gui.scale(30) ysize gui.scale(2)
                        add Solid("#77d98b") xpos gui.scale(engine.player_x + 8) ypos gui.scale(engine.player_y + 22) xsize gui.scale(30) ysize gui.scale(2)
                        add Solid("#77d98b") xpos gui.scale(engine.player_x + 5) ypos gui.scale(engine.player_y + 5) xsize gui.scale(2) ysize gui.scale(16)
                        add Solid("#77d98b") xpos gui.scale(engine.player_x + 39) ypos gui.scale(engine.player_y + 5) xsize gui.scale(2) ysize gui.scale(16)

                    # Player shots --------------------------------------------
                    for bullet in engine.player_bullets:
                        $ bullet_x = gui.scale(bullet["x"])
                        $ bullet_y = gui.scale(bullet["y"])
                        add Solid("#42d8c633") xpos bullet_x - gui.scale(4) ypos bullet_y - gui.scale(2) xsize gui.scale(8) ysize gui.scale(22)
                        add Solid("#5fe0ff") xpos bullet_x - gui.scale(1) ypos bullet_y xsize gui.scale(2) ysize gui.scale(18)
                        add Solid("#eaffff") xpos bullet_x ypos bullet_y + gui.scale(3) xsize gui.scale(1) ysize gui.scale(12)

                    # Enemy lasers --------------------------------------------
                    for bullet in engine.enemy_bullets:
                        $ laser_x = gui.scale(bullet["x"])
                        $ laser_y = gui.scale(bullet["y"])
                        add Solid("#ff2d5526") xpos laser_x - gui.scale(4) ypos laser_y xsize gui.scale(8) ysize gui.scale(24)
                        add Solid("#ff456a") xpos laser_x - gui.scale(1) ypos laser_y xsize gui.scale(2) ysize gui.scale(22)
                        add Solid("#ffd9e2") xpos laser_x ypos laser_y + gui.scale(3) xsize gui.scale(1) ysize gui.scale(13)
                        add Solid("#ff8fa6") xpos laser_x - gui.scale(1) ypos laser_y + gui.scale(20) xsize gui.scale(3) ysize gui.scale(3)

                    # Powerups -------------------------------------------------
                    for powerup in engine.powerups:
                        $ powerup_bob = math.sin(engine.elapsed * 6.0 + powerup["x"] * 0.1) * 3.0
                        $ powerup_pulse = 0.5 + 0.5 * math.sin(engine.elapsed * 8.0 + powerup["x"] * 0.2)
                        $ powerup_image = "images/arcade/powerup_%s.png" % powerup["kind"]
                        $ powerup_x = gui.scale(powerup["x"])
                        $ powerup_y = gui.scale(powerup["y"] + powerup_bob)
                        add "images/arcade/glow.png" xpos powerup_x - gui.scale(13) ypos powerup_y - gui.scale(13) xysize (gui.scale(52), gui.scale(52)) alpha (0.10 + 0.10 * powerup_pulse)
                        add "images/arcade/ring.png":
                            xpos powerup_x - gui.scale(17) - int(gui.scale(2) * powerup_pulse)
                            ypos powerup_y - gui.scale(17) - int(gui.scale(2) * powerup_pulse)
                            xysize (gui.scale(34) + int(gui.scale(4) * powerup_pulse), gui.scale(34) + int(gui.scale(4) * powerup_pulse))
                            alpha (0.12 + 0.18 * powerup_pulse)
                        add powerup_image xpos powerup_x - gui.scale(16) ypos powerup_y - gui.scale(16) xysize (gui.scale(32), gui.scale(32))

                    # Explosions / sparks -------------------------------------
                    for explosion in engine.explosions:
                        $ progress = 1.0 - explosion["life"] / explosion["duration"]
                        $ frame_index = min(9, int(progress * 10))
                        $ explosion_size = int(gui.scale(48 + progress * 42) * explosion["scale"])
                        add ("images/arcade/explosion/frame_%02d.png" % frame_index):
                            xpos gui.scale(explosion["x"]) - explosion_size / 2
                            ypos gui.scale(explosion["y"]) - explosion_size / 2
                            xysize (explosion_size, explosion_size)
                            alpha max(0.0, 1.0 - progress * 0.55)

                    for spark in engine.sparks:
                        $ spark_alpha = max(0.0, spark["life"] / spark["duration"])
                        add "images/arcade/spark.png" xpos gui.scale(spark["x"]) - gui.scale(3) ypos gui.scale(spark["y"]) - gui.scale(3) xysize (gui.scale(6), gui.scale(6)) alpha spark_alpha

                    add "images/arcade/vignette.png" xysize (gui.scale(960), gui.scale(500))
                    add Solid("#0d1524") xysize (gui.scale(960), gui.scale(500)) alpha 0.18

                    # Banners ------------------------------------------------
                    if engine.level_banner_timer > 0.0 and engine.phase != "lost":
                        $ banner_alpha = min(1.0, engine.level_banner_timer / 0.4)
                        frame:
                            background Solid("#03070dd9")
                            padding (gui.scale(14), gui.scale(4))
                            xalign 0.5
                            ypos gui.scale(5)
                            at Transform(alpha=banner_alpha)
                            text "LEVEL [engine.level]   //   [engine.formation_label]" size gui.scale(12) bold True color "#cfe6f5" kerning gui.scale(2)

                    if engine.phase == "wave_clear":
                        frame:
                            background Solid("#03070de6")
                            padding (gui.scale(22), gui.scale(12))
                            xalign 0.5
                            ypos gui.scale(196)
                            text engine.status_message size gui.scale(20) bold True color "#77d98b"

                    if engine.phase == "lost":
                        add Solid("#03070dcc") xysize (gui.scale(960), gui.scale(500))
                        frame:
                            background Solid("#0b1420f2")
                            padding (gui.scale(30), gui.scale(22))
                            xalign 0.5
                            yalign 0.5
                            vbox:
                                spacing gui.scale(10)
                                text "SHIP DISABLED" size gui.scale(26) bold True color "#ff7890" xalign 0.5
                                text "REACHED LEVEL [engine.level]" size gui.scale(15) color "#8ca0b3" xalign 0.5
                                text "FINAL SCORE  [engine.score]" size gui.scale(18) bold True color "#e4f1fa" xalign 0.5
                                textbutton "CONTINUE":
                                    xalign 0.5
                                    action Return(False)
                                    background Solid("#22628f")
                                    hover_background Solid("#3188c4")
                                    padding (gui.scale(24), gui.scale(10))
                                    text_size gui.scale(13)
                                    text_bold True
                                    text_color "#ffffff"

            hbox:
                xfill True
                text "HOLD TO MOVE: ← → / A D     AUTO-FIRE     POWERUPS: RAPID / SPREAD / ARMOR     ESC: LEAVE" size gui.scale(11) color "#8ca0b3" yalign 0.5

                hbox:
                    spacing gui.scale(8)
                    textbutton "◀":
                        action Function(engine.move_player, -1)
                        background Solid("#16232e")
                        hover_background Solid("#294052")
                        padding (gui.scale(14), gui.scale(6))
                        text_size gui.scale(13)
                        text_color "#dce9f5"
                    textbutton "▶":
                        action Function(engine.move_player, 1)
                        background Solid("#16232e")
                        hover_background Solid("#294052")
                        padding (gui.scale(14), gui.scale(6))
                        text_size gui.scale(13)
                        text_color "#dce9f5"

    key "K_ESCAPE" action Return(False)

    timer 0.04 repeat True action Function(engine.tick, 0.04)


label minigame_arcade_shooter:
    window hide
    $ _arcade_engine = ArcadeShooterEngine()
    play sound "audio/SFX/arcade_wave.wav"
    call screen arcade_shooter(_arcade_engine)
    $ _arcade_success = _return
    return _arcade_success


label test_arcade_shooter:
    scene black with Dissolve(0.4)
    "Orbit Defender: hold Left/Right to dodge. The waves keep coming until the ship is destroyed."
    call minigame_arcade_shooter from _call_minigame_arcade_shooter
    "Run over — level [_arcade_engine.level], score [_arcade_engine.score]."
    return
