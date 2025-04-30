import pygame
from pygame.sprite import Sprite

class Tongue(Sprite):
    def __init__(self, player, screen):
        """A class to manage Frogtomus Prime's tongue attack"""
        super().__init__()
        self.screen = screen
        self.color = (255, 0, 0)  # red
        self.max_width = 150 # how far the tongue goes
        self.height = 7

        self.player = player
        self.facing_left = player.facing_left

        # set the starting point
        if self.facing_left:
            self.starting_position = player.rect.topleft
        else:
            self.starting_position = player.rect.topright

        # build the tongue
        self.width = 0
        self.retracting = False
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.midright = self.starting_position if self.facing_left else self.starting_position

    def update(self, cats):
        if not self.retracting:
            self.width += 10
            if self.width >= self.max_width:
                self.retracting = True
        else:
            self.width -= 10
            if self.width <= 0:
                self.kill()

        # rebuild the tongue
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        if self.facing_left:
            self.rect.midright = self.starting_position
        else:
            self.rect.midleft = self.starting_position

            # check for collisions with cats
        if self.retracting:
            for cat in cats:
                if self.rect.colliderect(cat.rect):
                    if cat.take_damage():
                        print("Tongue hit a cat!")
                    # add sound for dead cat here

