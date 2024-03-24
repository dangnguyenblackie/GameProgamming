import os
import sys
import math
import random

import pygame

from scripts.utils import load_image, load_images, Animation, Timer, drawTextOnScreen
from scripts.entities import PhysicsEntity, Player, Enemy, Boss
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle, Coin, Star
from scripts.spark import Spark
from scripts.config import *
from scripts.button import Button
from scripts.menu import Menu
from scripts.gamestate import GameState

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Assignment3')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        self.stopTimer = Timer(5)
        self.alphaTimer = Timer(0.5)

        self.movement = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'boss/idle': Animation(load_images('entities/boss/idle'), img_dur=6),
            'boss/take_hit': Animation(load_images('entities/boss/slide'), img_dur=4),
            'boss/run': Animation(load_images('entities/boss/run'), img_dur=4),
            'boss/shoot': Animation(load_images('entities/boss/wall_slide'), img_dur=4),
            'boss/slash': Animation(load_images('entities/boss/wall_slide'), img_dur=4),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'money': load_image('money.png', 1/4),
            'projectile': load_image('projectile.png'),
            'star': load_image("star.png", 1/6),

            'menuBackgroundImage': pygame.image.load("data/images/menu/menu.png").convert(),
            'menuWeaponBackgroundImage': pygame.image.load("data/images/menu/weapon.png").convert(),
            'swordImage': pygame.image.load("data/images/menu/sword.png").convert(),
            'gunImage': pygame.image.load("data/images/menu/gun.png").convert(),
            'coinImage': pygame.image.load("data/images/menu/coin.png").convert(),
            'startButtonImage': pygame.image.load("data/images/buttons/start.png").convert(),
            'pauseButtonImage': pygame.image.load("data/images/buttons/pause.png").convert(),
            'exitButtonImage': pygame.image.load("data/images/buttons/exit.png").convert(),
            'continueButtonImage': pygame.image.load("data/images/buttons/continue.png").convert(),
            'storeButtonImage': pygame.image.load("data/images/buttons/store.png").convert(),
            'backButtonImage': pygame.image.load("data/images/buttons/back.png").convert(),

            'abilities/slash': Animation(load_images('abilities/slash', 1/8), img_dur=2, loop=False),
            'abilities/boom': Animation(load_images('abilities/boom', 1/2), img_dur=2, loop=False),
        }

        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
            'timeStop': pygame.mixer.Sound('data/sfx/timestop.mp3'),
            'timeResume': pygame.mixer.Sound('data/sfx/timeresume.mp3'),
            'boom': pygame.mixer.Sound('data/sfx/boom.mp3')
        }

        self.buttons = {
            'startButton': Button(self.assets['startButtonImage'], padding=(0,150)),
            'continueButton': Button(self.assets['continueButtonImage'], padding=(0,150)),
            'exitButton': Button(self.assets['exitButtonImage'], padding=(0,30)),
            'storeButton': Button(self.assets['storeButtonImage'], padding=(0,90)),
            'backButton': Button(self.assets['backButtonImage'], padding=(0,-180)),
            'swordButton': Button(self.assets['swordImage'], padding=(-120, 0)),
            'gunButton': Button(self.assets['gunImage'], padding=(120, 0))
        }

        self.menus = {
            'startMenu': Menu(buttons = [self.buttons['startButton'], self.buttons['storeButton'], self.buttons['exitButton']],menuBackground = self.assets['menuBackgroundImage'],size = (640,480)),
            'pauseMenu': Menu(buttons = [self.buttons['startButton'], self.buttons['exitButton']],size = (320,240)),
            'weaponMenu': Menu(buttons = [self.buttons['backButton'], self.buttons['swordButton'], self.buttons['gunButton']],menuBackground = self.assets['menuWeaponBackgroundImage'],size = (640,480))
        }

        self.gameState = GameState.IS_START

        self.font = {
            'menu': pygame.font.Font('data/font/OpenDyslexicAltNerdFont-Bold.otf', size=20),
            'normal': pygame.font.Font('data/font/BigBlueTermPlusNerdFont-Regular.ttf', size=10)
        }

        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)

        self.screenshake = 0
        self.totalMoney = 1000

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        # self.tilemap.load('data/maps/3.json')
        self.money = []
        self.star = []
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.enemies = []
        self.boss = None
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1),  ('spawners', 2)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            elif spawner['variant'] == 2:
                self.boss = Boss(self, spawner['pos'], size=[8,15])
                self.player.teleport["enable"] += 2
                self.player.bomb += 2
                self.player.bullets = 10
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))



        self.enemyProjectiles = []
        self.playerProjectiles = []
        self.slashes = []
        self.enemySlashes = []
        self.booms = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30
        self.alpha = 0

    def run(self):
        self.playMusic()

        self.menus['startMenu'].setIsDisplay(True)
        weaponFlag = 0

        while self.gameState:

            if self.gameState == GameState.IS_START:
                mouse = 0
                mousePosition = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameState = GameState.IS_EXIT
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse = 1
                startMenuButtonValues = self.menus['startMenu'].draw(self.screen, mousePosition, mouse)['buttons']
                if startMenuButtonValues[0]: # Click Start button
                    self.menus['startMenu'].setIsDisplay(False)
                    self.menus['startMenu'].setButtonValue2False()
                    self.level = 0
                    self.load_level(self.level)
                    self.gameState =  GameState.IS_PLAY
                elif startMenuButtonValues[1]: # Click Store button
                    self.menus['startMenu'].setIsDisplay(False)
                    self.menus['weaponMenu'].setIsDisplay(True)
                    self.menus['startMenu'].setButtonValue2False()
                    self.gameState =  GameState.IS_WEAPON
                elif startMenuButtonValues[2]: # Click exit button
                    self.menus['startMenu'].setIsDisplay(False)
                    self.gameState = GameState.IS_EXIT

            elif self.gameState == GameState.IS_WEAPON:
                mouse = 0
                mousePosition = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameState = GameState.IS_EXIT
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse = 1
                weaponMenuButtonValues = self.menus['weaponMenu'].draw(self.screen, mousePosition, mouse)['buttons']
                if weaponMenuButtonValues[0]: # Click Back button
                    self.menus['weaponMenu'].setIsDisplay(False)
                    self.menus['startMenu'].setIsDisplay(True)
                    self.menus['weaponMenu'].setButtonValue2False()
                    self.gameState =  GameState.IS_START
                if weaponMenuButtonValues[1]:
                    weaponFlag = 1
                    self.player.weapon = 0
                if weaponMenuButtonValues[2]:
                    weaponFlag = 2
                    self.player.weapon = 1

                if weaponFlag == 2:
                    drawTextOnScreen(self.screen, "You chose this", self.font['menu'], (0,0,0) , self.buttons['gunButton'].rectangle.x, self.buttons['gunButton'].rectangle.y)
                elif weaponFlag == 1:
                    drawTextOnScreen(self.screen, "You chose this", self.font['menu'], (0,0,0) , self.buttons['swordButton'].rectangle.x, self.buttons['swordButton'].rectangle.y)


            elif self.gameState == GameState.IS_PLAY:
                self.display.fill((self.alpha*2, 0, 0, self.alpha))

                self.display_2.blit(self.assets['background'], (0, 0))

                self.screenshake = max(0, self.screenshake - 1)

                if (not len(self.enemies) and not len(self.money) and not len(self.star)):
                    self.player.reset()
                    self.transition += 1
                    if self.transition > 30:
                        self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                        self.load_level(self.level)

                if self.transition < 0:
                    self.transition += 1


                if self.dead:
                    if self.player.isTimeStop():
                        self.dead = 0
                        self.player.tele()
                    else:
                        self.player.reset()
                        self.player.resetTele()
                        self.dead += 1
                        if self.dead >= 10:
                            self.transition = min(30, self.transition + 1)
                        if self.dead > 40:
                            self.load_level(self.level)

                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

                for rect in self.leaf_spawners:
                    if random.random() * 49999 < rect.width * rect.height:
                        pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                        self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

                if not self.player.isTimeStop():
                    self.clouds.update()
                self.clouds.render(self.display_2, offset=render_scroll)

                self.tilemap.render(self.display, offset=render_scroll)

                for enemy in self.enemies.copy():
                    enemy.update(self.tilemap, (0, 0))
                    enemy.render(self.display, offset=render_scroll)
                    if enemy.isDead:
                        pos = 6
                        for i in range(random.choices([0,1,2], [1,1,1], k = 1)[0]):
                            self.money.append(Coin(self, (enemy.pos[0] + pos, enemy.pos[1] + 4), pos>0))
                            pos -= pos
                        for i in range(random.choices([0,1], [3,1], k = 1)[0]):
                            self.star.append(Star(self, (enemy.rect().centerx, enemy.rect().centery)))
                        if self.player.weapon:
                            self.player.bullets += 1
                        self.enemies.remove(enemy)

                if self.boss:
                    self.boss.update(self.tilemap, (0, 0))
                    self.boss.render(self.display, offset=render_scroll)

                    if self.boss.isDead:
                        print("Boss Dead")
                        self.player.reset()
                        self.transition += 1
                        if self.transition > 30:
                            self.gameState = GameState.IS_START
                            self.level = 0
                            continue

                if not self.dead:
                    self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                    self.player.render(self.display, offset=render_scroll)

                self.checkCollisions(render_scroll)

                for spark in self.sparks.copy():
                    kill = spark.update()
                    spark.render(self.display, offset=render_scroll)
                    if kill:
                        self.sparks.remove(spark)

                if self.player.isTimeStop():

                    if self.alphaTimer.getFlag():
                        self.alpha -= 5

                    if self.stopTimer.getFlag():
                        self.player.tele()
                        self.alpha = 0


                display_mask = pygame.mask.from_surface(self.display)
                display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
                for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    self.display_2.blit(display_sillhouette, offset)

                for particle in self.particles.copy():
                    kill = particle.update()
                    particle.render(self.display, offset=render_scroll)
                    if particle.type == 'leaf':
                        particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                    if kill:
                        self.particles.remove(particle)

                for coin in self.money.copy():
                    coin.render(self.display, offset=render_scroll)
                    if coin.update():
                        self.money.remove(coin)

                for star in self.star.copy():
                    star.render(self.display, offset=render_scroll)
                    if star.update():
                        self.star.remove(star)

                self.drawMoney()
                self.drawStop()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameState = GameState.IS_EXIT
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            self.movement[0] = True
                        if event.key == pygame.K_d:
                            self.movement[1] = True
                        if event.key == pygame.K_w:
                            if self.player.jump():
                                self.sfx['jump'].play()
                        if event.key == pygame.K_f:
                            self.player.defaultSkill()
                        if event.key == pygame.K_e:
                            self.player.tele()
                        if event.key == pygame.K_r:
                            self.player.boom()
                        if event.key == pygame.K_SPACE:
                            self.player.dash()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            self.movement[0] = False
                        if event.key == pygame.K_d:
                            self.movement[1] = False

                if self.transition:
                    transition_surf = pygame.Surface(self.display.get_size())
                    pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                    transition_surf.set_colorkey((255, 255, 255))
                    self.display.blit(transition_surf, (0, 0))

                self.display_2.blit(self.display, (0, 0))
                screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
                self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def checkCollisions(self, render_scroll):
        self.enemyProjectilesCollision(render_scroll)
        self.playerProjectilesCollision(render_scroll)

    def playerProjectilesCollision(self, render_scroll):
        # player shoot
        # [[x, y], direction, timer]
        for projectile in self.playerProjectiles.copy():
            projectile[0][0] += projectile[1]
            projectile[2] += 1
            img = self.assets['projectile']
            self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
            if self.tilemap.solid_check(projectile[0]):
                self.playerProjectiles.remove(projectile)
                for i in range(4):
                    self.sparks.append(Spark(self, projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
            elif projectile[2] > 360:
                self.playerProjectiles.remove(projectile)

        for slash in self.slashes.copy():
            if slash.update():
                self.slashes.remove(slash)
            slash.render(self.display, render_scroll)

        for boom in self.booms.copy():
            if boom.update():
                self.booms.remove(boom)
            boom.render(self.display, render_scroll)

        if self.player.health == 0:
            self.dead += 1


    def enemyProjectilesCollision(self, render_scroll):
        # enemy shoot
        # [[x, y], direction, timer]
        for projectile in self.enemyProjectiles.copy():
            if not self.player.isTimeStop():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
            img = self.assets['projectile']
            self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
            if self.tilemap.solid_check(projectile[0]):
                self.enemyProjectiles.remove(projectile)
                for i in range(4):
                    self.sparks.append(Spark(self, projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
            elif projectile[2] > 360:
                self.enemyProjectiles.remove(projectile)
            elif abs(self.player.dashing) < 50:
                if self.player.rect().collidepoint(projectile[0]):
                    self.enemyProjectiles.remove(projectile)
                    self.sfx['hit'].play()
                    self.screenshake = max(16, self.screenshake)
                    if self.player.isTimeStop(): self.player.tele()
                    else: self.player.health -= 1
                    for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self, self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))

        for slash in self.enemySlashes.copy():
            if slash.update():
                self.enemySlashes.remove(slash)
            slash.render(self.display, render_scroll)

    def playMusic(self):
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.sfx['ambience'].play(-1)

    def drawMoney(self):
        drawTextOnScreen(self.display, "Money: " + str(self.totalMoney), self.font['normal'], (0,0,0), 0, 0)
        drawTextOnScreen(self.display, "Star: " + str(self.player.teleport['enable']), self.font['normal'], (0,0,0), 0, 10)
        drawTextOnScreen(self.display, "Bomb: " + str(self.player.bomb), self.font['normal'], (0,0,0), 0, 20)
        if self.player.weapon:
            drawTextOnScreen(self.display, "Bullets: " + str(self.player.bullets), self.font['normal'], (0,0,0), 0, 30)
    def drawStop(self):
        if self.player.isTimeStop():
            drawTextOnScreen(self.display, "Time Stop", self.font['normal'], (255,255,255), 320 - 70, 0)


if __name__ == "__main__":
    Game().run()