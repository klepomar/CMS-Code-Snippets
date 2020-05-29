import pyglet
from pyglet.sprite import Sprite
from pyglet.window import key, FPSDisplay
from gameObject import GameObject, preload, load_high_score, save_high_score
from random import randint, choice
import numpy as np


class GameWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(400,50)
        self.frame_rate = 1/60.0
        self.fps_display = FPSDisplay(self)
        self.main_batch = pyglet.graphics.Batch()

        self.right = False
        self.left = False
        self.fire = False
        self.player_speed = 300
        self.player_fire_rate = 0
        self.player_is_alive = True
        self.load_player('ship1.png', 'blueShot.png')
        self.load_enemy('104.png', '355.png', 'greenShot.png')

        self.load_labels()

        self.destroyed_enemies = 0
        self.next_wave = 0
        self.score = 0

        self.explode_time = 2
        self.enemy_explode = False
        self.shake_time = 0
        self.game = False
        self.flash_time = 1
        self.player_flash = False

        self.load_explosion('explosion.png')
        self.background = list()
        self.background_img = preload('space.jpg')
        self.directions = [1, -1]

        for i in range(2):
            self.background.append(GameObject(0, i * 1200, Sprite(self.background_img)))
            self.background[i].vel_y = -100

    # Function called in __init__
    def load_player(self, imagaPlayer, imageLaser):
        player_spr = Sprite(preload(imagaPlayer),batch=self.main_batch)
        self.player = GameObject(500, 100, player_spr, health=5)

        self.player_laser_img = preload(imageLaser)
        self.player_laser = list()

        self.player_gun_sound = pyglet.media.load('./res/sounds/player_gun.wav', streaming=False)

        self.player_speed = 300
        self.player_fire_rate = 0

    # Function called in __init__
    def load_enemy(self, image_enemyA, image_EnemyB, image_laser):
        self.enemy_imgA = preload(image_enemyA)
        self.enemy_imgB = preload(image_EnemyB)
        self.enemy_list = list()

        self.enemy_laser_img = preload(image_laser)
        self.enemy_laser = list()

        self.enemy_fire_rate = 0
        self.enemy_typeA_spawner = 0
        self.enemy_typeB_spawner = 0
        self.enemy_typeA_counter = 5
        self.enemy_typeB_counter = 10

    # Function called in __init__
    def load_explosion(self, image):
        explosion_seq = pyglet.image.ImageGrid(preload(image), 4, 5, item_width=96, item_height=96)
        self.explosion_textures = pyglet.image.TextureGrid(explosion_seq)
        self.explosion_anim = pyglet.image.Animation.from_image_sequence(self.explosion_textures[0:], 0.05, loop=True)

        self.explosion_sound = pyglet.media.load('./res/sounds/exp_01.wav', streaming=False)
        self.explosion_list = list()

    # Function called in __init__
    def load_labels(self):
        self.enemies_destroyed = pyglet.text.Label("enemies destroyed", x=600, y=75, batch=self.main_batch)
        self.enemies_destroyed.italic = True
        self.enemies_destroyed.bold = True
        self.enemies_destroyed.font_size = 16

        self.score_text = pyglet.text.Label("score", x=850, y=75, batch=self.main_batch)
        self.score_text.italic = True
        self.score_text.bold = True
        self.score_text.font_size = 16

        self.player_health = pyglet.text.Label("player health", x=1000, y=75, batch=self.main_batch)
        self.player_health.italic = True
        self.player_health.bold = True
        self.player_health.font_size = 16

        self.high_score_text = pyglet.text.Label("high score", x=400, y=75, batch=self.main_batch)
        self.high_score_text.italic = True
        self.high_score_text.bold = True
        self.high_score_text.font_size = 20

        self.high_score = load_high_score("./res/score.txt")
        self.high_score_value = pyglet.text.Label(self.high_score, x=500, y=25, batch=self.main_batch)
        self.high_score_value.color = (120, 200, 150, 255)
        self.high_score_value.font_size = 24

        self.num_enemies_destroyed = pyglet.text.Label(str(0), x=750, y=25, batch=self.main_batch)
        self.num_enemies_destroyed.color = (80, 200, 200, 255)
        self.num_enemies_destroyed.font_size = 22

        self.num_score = pyglet.text.Label(str(0), x=900, y=25, batch=self.main_batch)
        self.num_score.color = (200, 120, 150, 255)
        self.num_score.font_size = 22

        self.numb_player_health = pyglet.text.Label(str(5), x=1100, y=25, batch=self.main_batch)
        self.numb_player_health.color = (0, 100, 50, 255)
        self.numb_player_health.font_size = 22

        self.intro_text = pyglet.text.Label("press space to start", x=600, y=450)
        self.intro_text.anchor_x = "center"
        self.intro_text.anchor_y = "center"
        self.intro_text.italic = True
        self.intro_text.bold = True
        self.intro_text.font_size = 40

        self.reload_text = pyglet.text.Label("press r to reload", x=600, y=350)
        self.reload_text.anchor_x = "center"
        self.reload_text.anchor_y = "center"
        self.reload_text.italic = True
        self.reload_text.bold = True
        self.reload_text.font_size = 40

        self.game_over_text = pyglet.text.Label("game over", x=600, y=500)
        self.game_over_text.anchor_x = "center"
        self.game_over_text.anchor_y = "center"
        self.game_over_text.italic = True
        self.game_over_text.bold = True
        self.game_over_text.font_size = 60

    # Window event function
    def on_key_press(self, symbol, modifier):
        if symbol == key.RIGHT:
            self.right = True
        if symbol == key.LEFT:
            self.left = True
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        if symbol == key.SPACE:
            self.fire = True
            if not self.game:
                self.game = True
                self.fire = False
        if symbol == key.R:
            self.reload()

    # Window event function
    def on_key_release(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.right = False
        if symbol == key.LEFT:
            self.left = False
        if symbol == key.SPACE:
            self.fire = False

    # Function for operating of player entity, movement and shooting
    def player_behavior(self, dt):
        self.player.update(dt)
        if self.right and self.player.pos_x < 1000 - self.player.sprite.width:
            self.player.pos_x += self.player_speed * dt
        if self.left and self.player.pos_x > 1:
            self.player.pos_x -= self.player_speed * dt
        if self.fire:
            self.player_fire_rate -= dt
            if self.player_fire_rate <= 0:
                self.player_laser.append(GameObject(self.player.pos_x + 7, self.player.pos_y + 30, Sprite(self.player_laser_img, batch=self.main_batch)))
                self.player_fire_rate += 0.4
                self.player_gun_sound.play()

    # Function which handle player damage
    def player_hit(self):
        self.player.health -= 1
        self.numb_player_health.text = str(self.player.health)
        self.player_flash = True
        if self.player.health <= 0:
            self.player.sprite.batch = None
            self.game_over()

    # Function for operating of enemy entities, movement and shooting
    def enemy_behavior(self, dt):
        for enemy in self.enemy_list:
            if enemy.pos_x >= 1000:
                enemy.pos_x = 1000
                enemy.vel_x *= -1

            if enemy.pos_x <= 100:
                enemy.pos_x = 100
                enemy.vel_x *= -1

            enemy.pos_y -= enemy.vel_y * dt
            enemy.pos_x += enemy.vel_x * dt
            enemy.sprite.x = enemy.pos_x
            enemy.sprite.y = enemy.pos_y
            if 450 >= enemy.pos_y >= 449.4 and self.player_is_alive:
                self.score -= 1
                self.num_score.text = str(self.score)

            if enemy.pos_y <= -100:
                self.enemy_list.remove(enemy)

            self.enemy_fire_rate -= dt

            if self.enemy_fire_rate <= 0:
                for enemy in self.enemy_list:
                    if randint(0, 10) >= 5:
                        self.enemy_laser.append(
                            GameObject(enemy.pos_x + 50,enemy.pos_y, Sprite(self.enemy_laser_img, batch=self.main_batch)))

                self.enemy_fire_rate += 10

    # Function which handle player damage
    def enemy_hit(self, entity):
        entity.health -= 1

        if entity.health == 0 and self.player_is_alive:
            self.enemy_explode = True
            self.explosion_list.append(Sprite(self.explosion_anim, x=entity.pos_x, y=entity.pos_y, batch=self.main_batch))
            self.enemy_list.remove(entity)  # remove the enemy from enemy list when gets shot two times
            self.explosion_sound.play()
            self.destroyed_enemies += 1  # this is only for displaying the stats
            self.next_wave += 1
            self.score += 1
            self.num_enemies_destroyed.text = str(self.destroyed_enemies)
            self.num_score.text = str(self.score)

    # Spawning of enemy depends on dt
    def enemy_spawn(self, dt):

        self.enemy_typeA_spawner -= dt
        self.enemy_typeB_spawner -= dt
        if self.player_is_alive:
            if self.enemy_typeA_spawner <= 0:
                self.enemy_list.append(GameObject(1000, 800, Sprite(self.enemy_imgA, batch=self.main_batch), health=2))
                self.enemy_list[-1].vel_x = randint(100, 300) * choice(self.directions)  # last spawned entity in entity list
                self.enemy_list[-1].vel_y = 30

                self.enemy_typeA_spawner += self.enemy_typeA_counter

            if self.enemy_typeB_spawner <= 0:
                self.enemy_list.append(GameObject(600, 950, Sprite(self.enemy_imgB, batch=self.main_batch), health=5))
                self.enemy_list[-1].vel_x = randint(100, 300) * choice(self.directions)  # last spawned entity in entity list
                self.enemy_list[-1].vel_y = 30

                self.enemy_typeB_spawner += self.enemy_typeB_counter

        if self.next_wave >= 20:
            self.enemy_typeA_counter -= 0.05
            self.enemy_typeB_counter -= 0.2
            self.next_wave = 0

    # Moving laser shots for update function
    def laser_shot(self, dt):
        for laser in self.player_laser:
            laser.update(dt)
            laser.pos_y += 400 * dt
            if laser.pos_y > 1000:
                self.player_laser.remove(laser)

        for laser in self.enemy_laser:
            laser.update(dt)
            laser.pos_y -= 300 * dt
            laser.sprite.y = laser.pos_y
            if laser.pos_y < -50:
                self.enemy_laser.remove(laser)

    # Function which find collision with laser if exist
    def laser_collision(self, entity, fires_list):
        for lsr in fires_list:
            if lsr.pos_x < entity.pos_x + entity.sprite.width and lsr.pos_x + lsr.sprite.width > entity.pos_x and lsr.pos_y < entity.pos_y + entity.sprite.height and lsr.sprite.height + lsr.pos_y > entity.pos_y:
                fires_list.remove(lsr)  # remove the laser from laser list when colliding with an enemy

                return True

    # Function which will move with background if enemy destroyed
    def screen_shake(self):
        self.shake_time -= 0.1
        x = randint(-10, 10)

        if self.shake_time <= 0:
            self.background[0].sprite.x = x
            self.background[1].sprite.x = x
            self.shake_time += 0.11

        elif self.shake_time >= 0:
            self.background[0].sprite.x = 0
            self.background[1].sprite.x = 0
            self.enemy_explode = False

    # Function which update flash which will occur if player is destroyed
    def update_flash(self):
        self.flash_time -= 0.2
        self.player.sprite.color = (255, 0, 0)

        if self.flash_time <= 0:
            self.player.sprite.color = (255, 255, 255)
            self.flash_time = 1
            self.player_flash = False

    # Function which update explosion after destroying enemy
    def update_explosion(self):
        self.explode_time -= 0.1

        if self.explode_time <= 0:

            for exp in self.explosion_list:
                self.explosion_list.remove(exp)

                exp.delete()

            self.explode_time = np.add(self.explode_time, 2)

    # Function for ending game
    def game_over(self):
        self.player_is_alive = False

        if self.score > int(self.high_score):
            save_high_score('./res/score.txt', self.score)

        self.enemy_list.clear()

    # Function which handle reload after restart
    def reload(self):
        self.next_wave = 0
        self.score = 0
        self.player.health = 5
        self.player_fire_rate = 0
        self.enemy_fire_rate = 0
        self.enemy_typeA_spawner = 0
        self.enemy_typeB_spawner = 0
        self.enemy_typeA_counter = 5
        self.enemy_typeB_counter = 10
        self.explode_time = 2
        self.enemy_explode = False
        self.shake_time = 0
        self.flash_time = 1
        self.player_is_alive = True
        self.player.pos_x, self.player.pos_y = 500, 100
        self.player.sprite.batch = self.main_batch

    # Windows event function for drawing into the window
    def on_draw(self):
        self.clear()
        for sheet in self.background:
            sheet.draw()
        if self.game:
            self.main_batch.draw()
        else:
            self.intro_text.draw()

        if not self.player_is_alive:
            self.game_over_text.draw()
            self.reload_text.draw()

        self.fps_display.draw()

    # Windows event function for updating of movement etc.
    def update(self, dt):
        if self.game:
            self.player_behavior(dt)
            self.enemy_behavior(dt)
            self.laser_shot(dt)

            for entity in self.enemy_list:
                if self.laser_collision(entity, self.player_laser):
                    self.enemy_hit(entity)

            if self.laser_collision(self.player, self.enemy_laser) and self.player_is_alive:
                self.player_hit()

            if self.player_flash:
                self.update_flash()

            self.update_explosion()
            self.enemy_spawn(dt)

            if self.enemy_explode:
                self.screen_shake()

            self.enemy_spawn(dt)

        for sheet in self.background:
            sheet.update(dt)
            if sheet.pos_y <= -1300:
                self.background.remove(sheet)
                self.background.append(GameObject(0, 1100, Sprite(self.background_img)))
            sheet.vel_y = -100


if __name__ == "__main__":

    window = GameWindow(1200, 900, "Galaxy Destroyer", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()