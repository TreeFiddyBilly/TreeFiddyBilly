import pygame

class Wizard(pygame.sprite.Sprite):
    def __init__(self, x, y, wizzo_speech):
        super().__init__()
        self.image = pygame.image.load('assets/images/wizard.png')
        self.image = pygame.transform.scale(self.image, (85, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.channel = None
        self.wizzo_speech = wizzo_speech
        self.talking = False
        self.fading = False
        self.fade_alpha = 255
        self.original_image = self.image.copy()

    def update(self):
        if self.talking and not self.channel.get_busy():
            self.stop_talking()
        if self.fading:
            self.fade_alpha -= 5
            if self.fade_alpha <= 0:
                self.kill()
            else:
                # fade effect
                self.image = self.original_image.copy()
                self.image.set_alpha(self.fade_alpha)

    def speak(self, screen):
        # Draw the textbox
        text_box = pygame.Rect(100, 100, 700, 185)
        pygame.draw.rect(screen, (0, 0, 0), text_box)
        pygame.draw.rect(screen, (255, 255, 255), text_box, 2)

        # Draw the text
        font = pygame.font.Font('freesansbold.ttf', 20)

        message = (
            "Frogtomus Prime, if you want to be a Prince again you must find the princess. "
            "However, your first obstacles ahead are common house cats! Defeat them, collect their kibble, "
            "then bribe the boat master to continue. Don't ask me why he needs kibble, just go for it."
        )

        import textwrap
        lines = textwrap.wrap(message, width=65)

        y = text_box.y + 20
        for line in lines:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (text_box.x + 20, y))
            y += font.get_height() + 5

    def start_talking(self):
        self.talking = True
        self.channel = self.wizzo_speech.play()

    def stop_talking(self):
        if self.channel and self.channel.get_busy():
            self.channel.stop()
        self.talking = False
        self.fading = True
