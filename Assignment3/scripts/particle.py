import pygame
class Particle:
    def __init__(self, game, p_type, pos, velocity=[0, 0], frame=0):
        self.game = game
        self.type = p_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation = self.game.assets['particle/' + p_type].copy()
        self.animation.frame = frame

    def update(self):
        kill = False
        if self.animation.done:
            kill = True

        if not self.game.player.isTimeStop():
            self.pos[0] += self.velocity[0]
            self.pos[1] += self.velocity[1]
            self.animation.update()

        return kill

    def render(self, surf, offset=(0, 0)):
        img = self.animation.img()
        surf.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))


class Item:
    def __init__(self, game, type,pos):
        self.game = game
        self.pos = list(pos)
        self.img = self.game.assets[type]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.img.get_width(), self.img.get_height())

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.img, (self.pos[0] - offset[0] - self.img.get_width() // 2, self.pos[1] - offset[1] - self.img.get_height() // 2))

class Coin(Item):
    def __init__(self, game, pos, flag):
        super().__init__(game, "money", pos)
        self.velocity = 2 if flag else -2

    def update(self):
        if self.velocity == 0:
            kill = False
            if self.game.player.rect().colliderect(self.rect()):
                self.game.totalMoney += 1
                kill = True
            return kill
        else:
            self.pos[0] -= self.velocity
            self.velocity = max(0, self.velocity - 0.1)

            return False
class Star(Item):
    def __init__(self, game, pos):
        super().__init__(game, "star", pos)
        self.velocity = 2

    def update(self):
        if self.velocity == 0:
            kill = False
            if self.game.player.rect().colliderect(self.rect()):
                self.game.player.teleport['enable'] += 1
                self.game.player.bomb += 1
                kill = True

            return kill
        else:
            self.pos[1] -= self.velocity
            self.velocity = max(0, self.velocity - 0.1)

            return False



