import pygame
import random

class Cat(pygame.sprite.Sprite):
    def __init__(self, all_sprites, player):
        super().__init__()
        self.player = player
        self.images = {
            "idle": pygame.image.load('assets/images/cat.png').convert_alpha(),
            "angry": pygame.image.load('assets/images/cat_2.png').convert_alpha(),
            "attack": pygame.image.load('assets/images/cat_3.png').convert_alpha()
        }
        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], (150, 175))

        # left facing cat
        self.state = "idle"
        self.image = self.images[self.state]
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(800, 900)
        self.rect.y = player.rect.y
        self.rect.center = self.player.rect.center
        self.speedx = random.choice([-1, 1])

        self.all_sprites = all_sprites
        self.facing_left = self.speedx < 0
        self.update_image()
        self.health = 1 # cat's health

    def set_state(self, new_state):
        if new_state in self.images:
            self.state = new_state
            self.update_image()

    def update_image(self):
        self.image = self.images[self.state]
        if not self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)  # flip

    def update(self):
        self.rect.x += self.speedx

        if (self.speedx < 0 and not self.facing_left) or (self.speedx > 0 and self.facing_left):
            self.facing_left = not self.facing_left
            self.update_image()

        # update cat's position relative to frog
        if abs(self.rect.centerx - self.player.rect.centerx) < 100:
            self.set_state("attack")
        elif abs(self.rect.centerx - self.player.rect.centerx) < 250:
            self.set_state("angry")
        else:
            self.set_state("idle")

            # wrangle the cats back
            if self.rect.x < -100:
                self.rect.x = random.randint(800, 900)
            elif self.rect.x > 900:
                self.rect.x = random.randint(-100, -50)

        # going to add cat damage sound
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            print("cat killed!")
            self.kill()
            return True
        return False