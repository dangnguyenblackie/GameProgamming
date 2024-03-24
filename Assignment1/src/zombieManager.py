import pygame
import random
from mole import Mole
from sound import SoundManager
from config import *
from utils import Timer

class ZombieManager:
    def __init__(self, zombie_images, zombieDeathImages ,spawn_interval, hole_positions, despawn_interval, loopFrames: tuple=None):
        self.zombies = pygame.sprite.Group()
        self.images = zombie_images
        self.zombieDeathImages = zombieDeathImages
        self.loopFrames = loopFrames

        self.zombie_images = self.images[:self.loopFrames[0]] + (FPS*despawn_interval - len(self.images[:self.loopFrames[0]]) - len(self.images[self.loopFrames[1]+1:]))//(len(self.images[self.loopFrames[0]:self.loopFrames[1]+1])) * self.images[self.loopFrames[0]:self.loopFrames[1]+1] + self.images[self.loopFrames[1]+1:]
        self.spawn_interval = spawn_interval
        self.spawnTimer = Timer(spawn_interval)

        self.despawn_interval = despawn_interval
        self.despawnTimer = Timer(despawn_interval)

        self.hole_positions = hole_positions
        self.used_hole = [False]*6
        self.totalZombie = 0

        self.isSpawning = False

    def spawn_zombie(self):
        available_holes = [i for i in range(6) if not self.used_hole[i]]
        if available_holes:
            self.totalZombie += 1
            selected_hole = random.choice(available_holes)
            self.used_hole[selected_hole] = 1
            zombie = Mole(self.zombie_images, self.hole_positions[selected_hole], deathFrames=self.zombieDeathImages)
            zombie.hole = selected_hole
            zombie.animate()
            self.zombies.add(zombie)

    def despawn_zombies(self):
        if self.despawnTimer.getFlag():
            self.isSpawning = False
            if self.zombies:
                zombie = self.zombies.sprites()[0]
                self.used_hole[zombie.hole] = False
                self.zombies.remove(zombie)
            self.despawnTimer.resetTimer()

        for zombie in self.zombies:
            if not zombie.isAnimate:
                self.used_hole[zombie.hole] = 0
                self.zombies.remove(zombie)
                self.isSpawning = False
                self.despawnTimer.resetTimer()

    def update_zombies(self, click_pos, mouse, sound_manager, score, speed=1):
        self.zombies.update(click_pos, mouse, sound_manager, score, speed=speed)
        self.despawn_zombies()

        # print(self.spawn_interval)

        if self.isSpawning:
            self.despawnTimer.runTimer()
        else: self.spawnTimer.runTimer()

        # self.spawnTimer.runTimer()
        # self.despawnTimer.runTimer()


    def draw_zombies(self, screen):
        self.zombies.draw(screen)

    def manage_spawn(self):
        # Kiểm tra và quản lý việc spawn zombie
        if self.spawnTimer.getFlag():
            self.spawn_zombie()
            self.spawnTimer.resetTimer()
            self.isSpawning = True

    def reset(self):
        self.isSpawning = False
        self.used_hole = [False]*6

        for zombie in self.zombies:
            self.zombies.remove(zombie)

        self.spawnTimer.resetTimer()
        self.despawnTimer.resetTimer()
        self.totalZombie = 0

    def setMode(self, mode=2):

        if mode == 1:
            self.spawn_interval = 2.5
            self.despawn_interval = 3.5
        elif mode == 2:
            self.spawn_interval = 2
            self.despawn_interval = 3
        else:
            self.spawn_interval = 1
            self.despawn_interval = 1

        self.zombie_images = self.images[:self.loopFrames[0]] +\
            (
                int(FPS*self.despawn_interval) - len(self.images[:self.loopFrames[0]]) -\
                len(self.images[self.loopFrames[1]+1:]))//(len(self.images[self.loopFrames[0]:self.loopFrames[1]+1])
            ) * \
            self.images[self.loopFrames[0]:self.loopFrames[1]+1] + \
            self.images[self.loopFrames[1]+1:]

        self.spawnTimer = Timer(self.spawn_interval)
        self.despawnTimer = Timer(self.despawn_interval)
        self.reset()