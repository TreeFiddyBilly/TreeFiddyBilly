import pygame
import random

class Rock(pygame.sprite.Sprite):
    """birds drop rocks at random...they hurt"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/images/rock.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # when rock falls off screen, kill it
        if self.rect.top > 600:
            self.kill()

class Bird(pygame.sprite.Sprite):
    def __init__(self, all_sprites, rocks):
        super().__init__()
        self.image = pygame.image.load('assets/images/bird.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (125, 65))

        # right facing bird
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(-15, 815)
        self.rect.y = 75
        self.speedx = random.choice([-3, 3])

        self.all_sprites = all_sprites
        self.rocks = rocks

        self.facing_left = self.speedx < 0
        self.update_image()


    def update(self):
        self.rect.x += self.speedx

        if (self.speedx < 0 and not self.facing_left) or (self.speedx > 0 and self.facing_left):
            self.facing_left = not self.facing_left  # flip direction
            self.update_image()

    def update_image(self):
        if not self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)  # flip
        else:
            self.image = pygame.image.load('assets/images/bird.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (125, 65))  # og

        # respawn bird when it flies away
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()

        # randomly drop rock
        if random.randint(0, 25) < 1:  # odds per frame
            rock = Rock(self.rect.centerx, self.rect.bottom)
            self.all_sprites.add(rock)
            self.rocks.add(rock)




