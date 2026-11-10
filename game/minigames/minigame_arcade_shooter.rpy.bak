################################################################################
## ORBIT DEFENDER — SMALL, STANDALONE ARCADE SHOOTER
################################################################################
##
## A short arcade-style minigame built from Ren'Py screen displayables.
## No shared artwork is resized or modified.
##
## Controls: Hold Left/Right arrows or A/D to move. The ship fires automatically.
## Story use: call minigame_arcade_shooter
## Test: jump test_arcade_shooter
##

init python:
    import random

    class ArcadeShooterEngine:
        def __init__(self):
            self.playfield_width = 960
            self.playfield_height = 500
            self.player_width = 46
            self.player_height = 24
            self.player_y = 456
            self.player_x = (self.playfield_width - self.player_width) / 2.0
            self.player_speed = 360.0
            self.player_bullets = []
            self.enemy_bullets = []
            self.enemies = []
            self.powerups = []
            self.enemy_direction = 1
            self.enemy_speed = 42.0
            self.enemy_fire_timer = 0.8
            self.fire_cooldown = 0.0
            self.invulnerable_timer = 0.0
            self.rapid_fire_timer = 0.0
            self.spread_shot_timer = 0.0
            self.armor = 0
            self.level = 1
            self.level_banner_timer = 0.0
            self.elapsed = 0.0
            self.stars = [
                {
                    "x": random.uniform(0.0, self.playfield_width),
                    "y": random.uniform(0.0, self.playfield_height),
                    "speed": random.uniform(18.0, 100.0),
                    "size": random.choice((1, 1, 2)),
                }
                for _ in range(64)
            ]
            self.explosions = []
            self.score = 0
            self.lives = 3
            self.phase = "playing"
            self.status_message = "CLEAR THE WAVE"

            self.spawn_wave()

        def spawn_wave(self):
            self.enemies = []
            rows = min(4 + (self.level - 1) // 2, 6)
            for row in range(4):
                for column in range(8):
                    self.enemies.append({
                        "id": row * 8 + column,
                        "x": 74.0 + column * 108.0,
                        "y": 54.0 + row * 58.0,
                        "row": row,
                        "alive": True,
                    })
            if rows > 4:
                for row in range(4, rows):
                    for column in range(8):
                        self.enemies.append({
                            "id": row * 8 + column,
                            "x": 74.0 + column * 108.0,
                            "y": 54.0 + row * 48.0,
                            "row": row,
                            "alive": True,
                        })
            self.enemy_direction = 1
            self.enemy_speed = 42.0 + (self.level - 1) * 7.0
            self.enemy_fire_timer = max(0.35, 0.8 - (self.level - 1) * 0.06)
            self.player_bullets = []
            self.enemy_bullets = []
            self.powerups = []
            self.level_banner_timer = 1.8

        def move_player(self, direction, dt=0.06):
            if self.phase != "playing":
                return
            self.player_x += direction * self.player_speed * dt
            self.player_x = max(
                8.0,
                min(self.playfield_width - self.player_width - 8.0, self.player_x)
            )

        def fire(self):
            if self.phase != "playing" or self.fire_cooldown > 0.0:
                return
            center_x = self.player_x + self.player_width / 2.0 - 2.0
            offsets = (-14.0, 0.0, 14.0) if self.spread_shot_timer > 0.0 else (0.0,)
            for offset in offsets:
                bullet_y = self.player_y - 10.0
                self.player_bullets.append({
                    "x": center_x + offset,
                    "y": bullet_y,
                    "previous_y": bullet_y,
                })
            self.fire_cooldown = 0.12 if self.rapid_fire_timer > 0.0 else 0.28

        def collect_powerup(self, powerup):
            if powerup["kind"] == "rapid":
                self.rapid_fire_timer = 8.0
            elif powerup["kind"] == "spread":
                self.spread_shot_timer = 8.0
            elif powerup["kind"] == "armor":
                self.armor = min(2, self.armor + 1)
            self.score += 25
            self.explosions.append({
                "x": self.player_x + self.player_width / 2.0,
                "y": self.player_y,
                "life": 0.3,
                "duration": 0.3,
                "color": powerup["color"],
            })

        def tick(self, dt):
            if self.phase != "playing":
                return

            dt = min(dt, 0.1)
            pressed_keys = renpy.pygame.key.get_pressed()
            moving_left = pressed_keys[renpy.pygame.K_LEFT] or pressed_keys[renpy.pygame.K_a]
            moving_right = pressed_keys[renpy.pygame.K_RIGHT] or pressed_keys[renpy.pygame.K_d]
            if moving_left != moving_right:
                self.move_player(1 if moving_right else -1, dt)

            self.elapsed += dt
            self.invulnerable_timer = max(0.0, self.invulnerable_timer - dt)
            self.rapid_fire_timer = max(0.0, self.rapid_fire_timer - dt)
            self.spread_shot_timer = max(0.0, self.spread_shot_timer - dt)
            self.level_banner_timer = max(0.0, self.level_banner_timer - dt)
            for star in self.stars:
                star["y"] += star["speed"] * dt
                if star["y"] >= self.playfield_height:
                    star["y"] = 0.0
                    star["x"] = random.uniform(0.0, self.playfield_width)
            for explosion in self.explosions:
                explosion["life"] -= dt
            self.explosions = [e for e in self.explosions if e["life"] > 0.0]

            self.fire_cooldown = max(0.0, self.fire_cooldown - dt)
            if self.fire_cooldown <= 0.0:
                self.fire()

            alive_enemies = [enemy for enemy in self.enemies if enemy["alive"]]
            if not alive_enemies:
                self.level += 1
                self.spawn_wave()
                alive_enemies = self.enemies

            left_edge = min(enemy["x"] for enemy in alive_enemies)
            right_edge = max(enemy["x"] for enemy in alive_enemies) + 32.0
            if (self.enemy_direction > 0 and right_edge + self.enemy_speed * dt >= self.playfield_width - 12) or (
                self.enemy_direction < 0 and left_edge - self.enemy_speed * dt <= 12
            ):
                self.enemy_direction *= -1
                for enemy in alive_enemies:
                    enemy["y"] += 18.0
            else:
                for enemy in alive_enemies:
                    enemy["x"] += self.enemy_direction * self.enemy_speed * dt

            self.enemy_speed = 42.0 + (self.level - 1) * 7.0 + (len(self.enemies) - len(alive_enemies)) * 1.4

            for bullet in self.player_bullets:
                bullet["previous_y"] = bullet["y"]
                bullet["y"] -= 480.0 * dt
            self.player_bullets = [
                bullet for bullet in self.player_bullets if bullet["y"] > -12.0
            ]

            for bullet in self.enemy_bullets:
                bullet["previous_y"] = bullet["y"]
                bullet["y"] += 245.0 * dt
            self.enemy_bullets = [
                bullet for bullet in self.enemy_bullets
                if bullet["y"] < self.playfield_height + 12.0
            ]

            for powerup in self.powerups:
                powerup["previous_y"] = powerup["y"]
                powerup["y"] += 115.0 * dt
            self.powerups = [
                powerup for powerup in self.powerups
                if powerup["y"] < self.playfield_height + 20.0
            ]
            for powerup in self.powerups[:]:
                overlaps_ship = (
                    powerup["x"] < self.player_x + self.player_width
                    and powerup["x"] + 20.0 > self.player_x
                    and powerup["previous_y"] <= self.player_y + self.player_height
                    and powerup["y"] + 20.0 >= self.player_y
                )
                if overlaps_ship:
                    self.powerups.remove(powerup)
                    self.collect_powerup(powerup)

            destroyed_enemy_ids = set()
            for bullet in self.player_bullets[:]:
                for enemy in alive_enemies:
                    if (
                        bullet["x"] < enemy["x"] + 32.0
                        and bullet["x"] + 4.0 > enemy["x"]
                        and bullet["y"] <= enemy["y"] + 24.0
                        and bullet["previous_y"] + 12.0 >= enemy["y"]
                    ):
                        enemy["alive"] = False
                        destroyed_enemy_ids.add(enemy["id"])
                        self.player_bullets.remove(bullet)
                        self.score += (4 - enemy["row"]) * 10
                        self.explosions.append({
                            "x": enemy["x"] + 16.0,
                            "y": enemy["y"] + 12.0,
                            "life": 0.32,
                            "duration": 0.32,
                            "color": "#ffca72",
                        })
                        if random.random() < 0.22:
                            kind = random.choice(("rapid", "spread", "armor"))
                            powerup_colors = {
                                "rapid": "#f0b85a",
                                "spread": "#5fb8ff",
                                "armor": "#77d98b",
                            }
                            self.powerups.append({
                                "x": enemy["x"] + 13.0,
                                "y": enemy["y"] + 24.0,
                                "previous_y": enemy["y"] + 24.0,
                                "kind": kind,
                                "color": powerup_colors[kind],
                            })
                        break

            if destroyed_enemy_ids:
                # Shots already on screen are removed with their firing ship.
                self.enemy_bullets = [
                    bullet for bullet in self.enemy_bullets
                    if bullet.get("source_id") not in destroyed_enemy_ids
                ]

            # Player shots may have destroyed a ship this frame. Never select a
            # stale entry from the pre-collision list as a firing enemy.
            alive_enemies = [enemy for enemy in self.enemies if enemy["alive"]]
            self.enemy_fire_timer -= dt
            if self.enemy_fire_timer <= 0.0 and alive_enemies:
                shooter = random.choice(alive_enemies)
                self.enemy_bullets.append({
                    "x": self.player_x + self.player_width / 2.0 - 2.5,
                    "y": shooter["y"] + 24.0,
                    "previous_y": shooter["y"] + 24.0,
                    "source_id": shooter["id"],
                })
                self.enemy_fire_timer = random.uniform(0.65, 1.2)

            player_left = self.player_x
            player_right = self.player_x + self.player_width
            if self.invulnerable_timer <= 0.0:
                for bullet in self.enemy_bullets[:]:
                    overlaps_ship = (
                        bullet["x"] < player_right
                        and bullet["x"] + 5.0 > player_left
                        and bullet["previous_y"] <= self.player_y + self.player_height
                        and bullet["y"] + 11.0 >= self.player_y
                    )
                    if overlaps_ship:
                        self.enemy_bullets.remove(bullet)
                        if self.armor > 0:
                            self.armor -= 1
                            self.invulnerable_timer = 0.65
                            hit_color = "#77d98b"
                        else:
                            self.lives -= 1
                            self.invulnerable_timer = 1.0
                            hit_color = "#ff7890"
                        self.explosions.append({
                            "x": self.player_x + self.player_width / 2.0,
                            "y": self.player_y + self.player_height / 2.0,
                            "life": 0.42,
                            "duration": 0.42,
                            "color": hit_color,
                        })
                        if self.lives <= 0:
                            self.phase = "lost"
                            self.status_message = "SHIP DISABLED"
                        break

            if any(enemy["y"] + 24.0 >= self.player_y for enemy in alive_enemies):
                self.phase = "lost"
                self.status_message = "INVADERS REACHED THE SHIP"


screen arcade_shooter(engine):
    modal True
    zorder 130

    add Solid("#050910")

    frame:
        background Solid("#0b1420")
        xalign 0.5
        yalign 0.5
        xsize gui.scale(1040)
        ysize gui.scale(700)
        padding (gui.scale(24), gui.scale(16))

        vbox:
            xfill True
            spacing gui.scale(12)

            hbox:
                text "ELSEWHERE // ARCADE" size gui.scale(11) bold True color "#7b98b1" kerning gui.scale(2)
                text "SCORE  [engine.score]" size gui.scale(15) bold True color "#5fb8ff" xalign 1.0

            hbox:
                text "ORBIT DEFENDER" size gui.scale(24) bold True color "#e4f1fa" kerning gui.scale(1)
                text "LEVEL  [engine.level]" size gui.scale(13) bold True color "#8ca0b3" xalign 1.0
                text "ARMOR  [engine.armor]" size gui.scale(13) bold True color "#77d98b"
                text "SHIPS  [engine.lives]" size gui.scale(14) bold True color "#f0b85a" xalign 1.0

            hbox:
                xfill True
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
                    xsize gui.scale(960)
                    ysize gui.scale(500)

                    add Solid("#07111d") xysize (gui.scale(960), gui.scale(500))

                    for star in engine.stars:
                        $ star_color = "#36506a" if star["size"] == 1 else "#7393ad"
                        add Solid(star_color) xpos gui.scale(star["x"]) ypos gui.scale(star["y"]) xsize gui.scale(star["size"]) ysize gui.scale(star["size"])

                    add Solid("#173047") xpos 0 ypos gui.scale(34) xsize gui.scale(960) ysize gui.scale(1)
                    add Solid("#13283a") xpos 0 ypos gui.scale(432) xsize gui.scale(960) ysize gui.scale(1)

                    for enemy in engine.enemies:
                        if enemy["alive"]:
                            $ enemy_color = "#ff7890" if enemy["row"] == 0 else "#f0b85a" if enemy["row"] < 3 else "#73d6c3"
                            $ enemy_shadow = "#402631"
                            $ enemy_bob = 2 if int(engine.elapsed * 7 + enemy["row"] * 2) % 2 else 0
                            $ enemy_y = enemy["y"] + enemy_bob

                            # Layered hull, fins, armor and cockpit give each
                            # sprite a little depth without relying on external art.
                            add Solid(enemy_shadow) xpos gui.scale(enemy["x"] + 3) ypos gui.scale(enemy_y + 5) xsize gui.scale(32) ysize gui.scale(20)
                            add Solid(enemy_color) xpos gui.scale(enemy["x"] + 6) ypos gui.scale(enemy_y) xsize gui.scale(20) ysize gui.scale(6)
                            add Solid(enemy_color) xpos gui.scale(enemy["x"]) ypos gui.scale(enemy_y + 6) xsize gui.scale(32) ysize gui.scale(12)
                            add Solid("#ffd9cb") xpos gui.scale(enemy["x"] + 11) ypos gui.scale(enemy_y + 3) xsize gui.scale(10) ysize gui.scale(3)
                            add Solid("#7f4053") xpos gui.scale(enemy["x"] + 4) ypos gui.scale(enemy_y + 17) xsize gui.scale(7) ysize gui.scale(6)
                            add Solid("#7f4053") xpos gui.scale(enemy["x"] + 21) ypos gui.scale(enemy_y + 17) xsize gui.scale(7) ysize gui.scale(6)
                            add Solid("#ffe7a8") xpos gui.scale(enemy["x"] + 3) ypos gui.scale(enemy_y + 10) xsize gui.scale(3) ysize gui.scale(3)
                            add Solid("#ffe7a8") xpos gui.scale(enemy["x"] + 26) ypos gui.scale(enemy_y + 10) xsize gui.scale(3) ysize gui.scale(3)

                    for bullet in engine.player_bullets:
                        add Solid("#42d8c6") xpos gui.scale(bullet["x"] - 3) ypos gui.scale(bullet["y"] - 3) xsize gui.scale(10) ysize gui.scale(18)
                        add Solid("#e8fff8") xpos gui.scale(bullet["x"]) ypos gui.scale(bullet["y"]) xsize gui.scale(4) ysize gui.scale(12)

                    for bullet in engine.enemy_bullets:
                        add Solid("#fa426b") xpos gui.scale(bullet["x"] - 4) ypos gui.scale(bullet["y"] - 3) xsize gui.scale(13) ysize gui.scale(19)
                        add Solid("#fff0f2") xpos gui.scale(bullet["x"]) ypos gui.scale(bullet["y"]) xsize gui.scale(5) ysize gui.scale(11)

                    for powerup in engine.powerups:
                        $ powerup_letter = "R" if powerup["kind"] == "rapid" else "S" if powerup["kind"] == "spread" else "A"
                        add Solid(powerup["color"] + "66") xpos gui.scale(powerup["x"] - 4) ypos gui.scale(powerup["y"] - 4) xsize gui.scale(28) ysize gui.scale(28)
                        add Solid(powerup["color"]) xpos gui.scale(powerup["x"]) ypos gui.scale(powerup["y"]) xsize gui.scale(20) ysize gui.scale(20)
                        text powerup_letter size gui.scale(12) bold True color "#07111d" xpos gui.scale(powerup["x"] + 5) ypos gui.scale(powerup["y"] + 2)

                    for explosion in engine.explosions:
                        $ explosion_progress = 1.0 - explosion["life"] / explosion["duration"]
                        $ explosion_radius = gui.scale(6 + explosion_progress * 22)
                        $ explosion_x = gui.scale(explosion["x"]) - explosion_radius / 2.0
                        $ explosion_y = gui.scale(explosion["y"]) - explosion_radius / 2.0
                        add Solid(explosion["color"]) xpos explosion_x ypos explosion_y xysize (explosion_radius, explosion_radius)
                        add Solid("#fff4d6") xpos explosion_x + explosion_radius * 0.3 ypos explosion_y + explosion_radius * 0.3 xysize (explosion_radius * 0.4, explosion_radius * 0.4)

                    $ engine_flicker = 8 + int(engine.elapsed * 25) % 7
                    if engine.invulnerable_timer <= 0.0 or int(engine.elapsed * 12) % 2 == 0:
                        # The ship is assembled from shaded panels; its animated
                        # exhaust and canopy create a faux 2.5D arcade-sprite look.
                        add Solid("#ff9a54") xpos gui.scale(engine.player_x + 18) ypos gui.scale(engine.player_y + 21) xsize gui.scale(10) ysize gui.scale(engine_flicker)
                        add Solid("#ffdf86") xpos gui.scale(engine.player_x + 21) ypos gui.scale(engine.player_y + 22) xsize gui.scale(4) ysize gui.scale(engine_flicker - 2)
                        add Solid("#234a72") xpos gui.scale(engine.player_x + 2) ypos gui.scale(engine.player_y + 10) xsize gui.scale(42) ysize gui.scale(14)
                        add Solid("#5fb8ff") xpos gui.scale(engine.player_x + 8) ypos gui.scale(engine.player_y + 5) xsize gui.scale(30) ysize gui.scale(15)
                        add Solid("#a8e7ff") xpos gui.scale(engine.player_x + 18) ypos gui.scale(engine.player_y) xsize gui.scale(10) ysize gui.scale(19)
                        add Solid("#d9f7ff") xpos gui.scale(engine.player_x + 21) ypos gui.scale(engine.player_y + 2) xsize gui.scale(4) ysize gui.scale(10)
                        add Solid("#397ba8") xpos gui.scale(engine.player_x + 5) ypos gui.scale(engine.player_y + 19) xsize gui.scale(36) ysize gui.scale(5)

                    if engine.invulnerable_timer > 0.0:
                        add Solid("#ff789022") xysize (gui.scale(960), gui.scale(500))

                    if engine.armor > 0:
                        add Solid("#77d98b") xpos gui.scale(engine.player_x + 8) ypos gui.scale(engine.player_y + 2) xsize gui.scale(30) ysize gui.scale(2)
                        add Solid("#77d98b") xpos gui.scale(engine.player_x + 8) ypos gui.scale(engine.player_y + 29) xsize gui.scale(30) ysize gui.scale(2)
                        add Solid("#77d98b") xpos gui.scale(engine.player_x + 5) ypos gui.scale(engine.player_y + 5) xsize gui.scale(2) ysize gui.scale(22)
                        add Solid("#77d98b") xpos gui.scale(engine.player_x + 39) ypos gui.scale(engine.player_y + 5) xsize gui.scale(2) ysize gui.scale(22)

                    if engine.phase != "playing":
                        add Solid("#03070dbb") xysize (gui.scale(960), gui.scale(500))
                        vbox:
                            xalign 0.5
                            yalign 0.5
                            spacing gui.scale(12)
                            text engine.status_message size gui.scale(25) bold True color ("#77d98b" if engine.phase == "won" else "#ff7890") xalign 0.5
                            text "FINAL SCORE  [engine.score]" size gui.scale(16) color "#e4f1fa" xalign 0.5
                            textbutton "CONTINUE":
                                xalign 0.5
                                action Return(engine.phase == "won")
                                background Solid("#22628f")
                                hover_background Solid("#3188c4")
                                padding (gui.scale(24), gui.scale(10))
                                text_size gui.scale(13)
                                text_bold True
                                text_color "#ffffff"
                    elif engine.level_banner_timer > 0.0:
                        text "LEVEL [engine.level]" size gui.scale(20) bold True color "#e4f1fa" xalign 0.5 ypos gui.scale(220) outlines [(gui.scale(2), "#07111d", 0, gui.scale(1))]

            hbox:
                xfill True
                text "HOLD TO MOVE: ← → / A D     AUTO-FIRE     R: RAPID  S: SPREAD  A: ARMOR" size gui.scale(11) color "#8ca0b3" yalign 0.5

                hbox:
                    spacing gui.scale(8)
                    textbutton "◀":
                        action Function(engine.move_player, -1)
                        background Solid("#16232e")
                        hover_background Solid("#294052")
                        padding (gui.scale(14), gui.scale(6))
                        text_color "#dce9f5"
                    textbutton "▶":
                        action Function(engine.move_player, 1)
                        background Solid("#16232e")
                        hover_background Solid("#294052")
                        padding (gui.scale(14), gui.scale(6))
                        text_color "#dce9f5"

    if engine.phase == "playing":
        key "K_ESCAPE" action Return(False)
        timer 0.04 repeat True action Function(engine.tick, 0.04)


label minigame_arcade_shooter:
    window hide
    $ _arcade_engine = ArcadeShooterEngine()
    call screen arcade_shooter(_arcade_engine)
    $ _arcade_success = _return
    return _arcade_success


label test_arcade_shooter:
    scene black with Dissolve(0.4)
    "A quick arcade test: clear the wave, or leave with Escape."
    call minigame_arcade_shooter
    if _return:
        "The arcade screen flashes a victory message."
    else:
        "The round ends, but the story can continue."
    return


# Press 0 at any time during development to launch the standalone test.
init python:
    config.underlay.append(
        renpy.Keymap(
            K_0=lambda: renpy.jump_out_of_context("test_arcade_shooter")
        )
    )
