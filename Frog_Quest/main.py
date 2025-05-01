import sys

import pygame
import random

from Frog_Quest import cowboy
from Frog_Quest.attack import Tongue
from Frog_Quest.bird import Bird
from Frog_Quest.cowboy import Cowboy
from Frog_Quest.wizard import Wizard
from Frog_Quest.cat import Cat
from Frog_Quest.boatmaster import Boatmaster


pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Frog Quest")

# tunes
background_music = pygame.mixer.Sound('assets/sounds/background_music.mp3')
background_music.set_volume(0.3)
background_music.play(loops=-1)

# sfx - recorded by me
hit_sound = pygame.mixer.Sound('assets/sounds/hit_sound.wav')
attack_sound = pygame.mixer.Sound('assets/sounds/attack_sound.wav')
death_sound = pygame.mixer.Sound('assets/sounds/death_sound.wav')
intro_dialog = pygame.mixer.Sound('assets/sounds/intro_dialog.wav')
wizzo_speech = pygame.mixer.Sound('assets/sounds/wizzo_speech.wav')
victory_sound = pygame.mixer.Sound('assets/sounds/victory_sound.mp3')
cat_hiss_sound = pygame.mixer.Sound('assets/sounds/cat_hiss.mp3')
wizzo_speech_2 = pygame.mixer.Sound('assets/sounds/wizzo_speech_2.wav')
boatmaster_speech_1 = pygame.mixer.Sound('assets/sounds/boatmaster_no_kibble.wav')
boatmaster_speech_2 = pygame.mixer.Sound('assets/sounds/boatmaster_kibble.wav')
wizzo_speech_3 = pygame.mixer.Sound('assets/sounds/wizzo_speech_3.wav')
cowboy_speech_1 = pygame.mixer.Sound('assets/sounds/cowboy_speech_1.wav')
cowboy_hurt = pygame.mixer.Sound('assets/sounds/cowboy_hurt.wav')
cliff_hanger = pygame.mixer.Sound('assets/sounds/cliff_hanger.wav')


class BackgroundTrees(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (125, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, scroll_speed):
        self.rect.x += scroll_speed
        if self.rect.right < 0:
            self.rect.left = 800
        elif self.rect.left > 800:
            self.rect.right = 0

class BackgroundCloud(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (175, 125))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1.5

class BackgroundCactus(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (125, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, scroll_speed):
        self.rect.x += scroll_speed
        if self.rect.right < 0:
            self.rect.left = 800
        elif self.rect.left > 800:
            self.rect.right = 0

# player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_still = pygame.transform.scale(pygame.image.load('assets/images/frog.png').convert_alpha(), (75, 75))
        self.image_move = pygame.transform.scale(pygame.image.load('assets/images/frog_2.png').convert_alpha(), (120, 100))
        self.image = self.image_still
        self.rect = self.image.get_rect()
        self.rect.center = (200, 500)
        self.starting_position = self.rect.x
        self.distance_traveled = 0
        self.facing_left = False
        self.facing_right = True
        self.last_hop_time = 0
        self.vy = 0
        self.on_ground = True
        self.max_x = 575
        self.min_x = 225
        self.last_hit_time = 0
        self.invincibility_time = 2000
        self.is_attacking_tongue = False

        # movement speed
        self.speed = 125
        self.jump_height = 75
        self.hop_duration = 200
        self.is_moving = False

        # health
        self.health = 5 # health points
        self.health_bar = pygame.Rect(10, 10, 100, 10)

    def frog_boundary(self):
        if self.rect.left < self.min_x:
            self.rect.left = self.min_x
        if self.rect.right > self.max_x:
            self.rect.right = self.max_x

    # health bar drawn
    def draw_health(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.health_bar)
        pygame.draw.rect(screen, (0, 255, 0), (self.health_bar.x, self.health_bar.y,
        self.health_bar.width * (self.health / 5), self.health_bar.height))

# move the frog
    def update(self):

        hop_distance = self.speed
        hop_force = -15
        gravity = 0.6
        hop_cooldown = self.hop_duration
        current_time = pygame.time.get_ticks()

        moved = False
        previous_position = self.rect.x

        # horizontal movement with hopping
        if current_time - self.last_hop_time >= hop_cooldown:
            if keys[pygame.K_LEFT]:
                if self.rect.x > self.min_x:
                    self.rect.x -= hop_distance

                if self.on_ground:
                    self.vy = hop_force
                    self.on_ground = False
                if not self.facing_left:
                    self.image = pygame.transform.flip(self.image_still, True, False)
                    self.facing_left = True
                    self.facing_right = False
                self.last_hop_time = current_time
                moved = True

            elif keys[pygame.K_RIGHT]:
                if self.rect.x < self.max_x:
                    self.rect.x += hop_distance

                if self.on_ground:
                    self.vy = hop_force
                    self.on_ground = False
                if not self.facing_right:
                    self.image = self.image_still
                    self.facing_right = True
                    self.facing_left = False
                self.last_hop_time = current_time
                moved = True

        if moved:

            distance_change = self.rect.x - previous_position
            self.distance_traveled += distance_change


        # gravity
        self.vy += gravity
        self.rect.y += self.vy

        # land on ground
        if self.rect.y >= 500:
            self.rect.y = 500
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

        if not self.on_ground:
            if self.facing_left:
                self.image =  self.image = pygame.transform.flip(self.image_move, True, False)
            else:
                self.image = self.image_move
        else:
            if self.facing_left:
                self.image = self.image = pygame.transform.flip(self.image_still, True, False)
            else:
                self.image = self.image_still

# sprite groups
all_sprites = pygame.sprite.Group()
background_objects = pygame.sprite.Group()
tongues = pygame.sprite.Group()
birds = pygame.sprite.Group()
rocks = pygame.sprite.Group()
cats = pygame.sprite.Group()
wizard = pygame.sprite.Group()
cowboys = pygame.sprite.Group()

# player instance
player = Player()
all_sprites.add(player)

# trees
tree_positions = [(-10, 302), (35, 315), (60, 295), (100, 300), (130, 310),(175, 290),
(215, 285), (250, 315), (300, 299), (345, 310), (360, 299), (400, 289),
(430, 301), (450, 295), (487, 311), (515, 300), (551, 294), (582, 302),
(600, 305), (636, 299), (650, 300), (677, 311), (700, 300),
(715,302), (745, 302), (770, 287), (799, 300)]
for pos in tree_positions:
    tree = BackgroundTrees('assets/images/tree.png', pos[0], pos[1])
    background_objects.add(tree)

cactus_positions = [(200, 400), (330, 380), (600, 415)]
cactuses = []
for pos in cactus_positions:
    cactus = BackgroundCactus('assets/images/cactus.png', pos[0], pos[1])
    cactuses.append(cactus)

cloud = BackgroundCloud('assets/images/cloud.png', 400, 125)
background_objects.add(cloud)


def transition_to_new_background(screen, player, background_objects):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))
    print("transitioning")
    if 'bird' in globals(): bird.kill()
    if 'tree' in globals(): tree.kill()
    if boatmaster: boatmaster.kill()
    background_objects.empty()
    background_objects.empty()
    # fade to black
    for alpha in range(0, 255, 5):
        background_objects.draw(screen)
        screen.blit(fade_surface, (0, 0))
        fade_surface.set_alpha(alpha)
        pygame.display.update()
        #pygame.time.delay(10)
    # gotta have a cactus or 3
    for cactus in cactuses:
        background_objects.add(cactus)

    #pygame.draw.rect(screen, (115, 230, 0), (0, 237, 201, 175))
    background_objects.draw(screen)

    # Move player to starting position
    player.rect.center = (200, 500)
    for alpha in range(255, 0, -5):
        background_objects.draw(screen)
        screen.blit(fade_surface, (0, 0))
        fade_surface.set_alpha(alpha)
        pygame.display.update()
        pygame.time.delay(10)
    if boatmaster:
        boatmaster.stop_talking_1()
        boatmaster.stop_talking_2()
        boatmaster_speech_1.stop()
        boatmaster_speech_2.stop()
        boatmaster.fading = True
        boatmaster.kill()

    pygame.time.delay(1500)
    wizzo_speech_3.play()
    return True

# Game loop ---v--------v--below--v--------v-------v------------------------------
running = True
clock = pygame.time.Clock()
frame_count = 0
intro_dialog.play()
scroll_speed = 0
wizard_spawned = False
wizard = None
wizard_has_spoken = False
distance_traveled = 0
player.is_moving = False
cat_spawned = False
cat_probability = 0.05
max_cats = 6
cat_count = 0
cats_defeated = 0
player.is_attacking_tongue = False
kibble_collected = False
boatmaster_spawned = False
boatmaster_has_spoken = False
boatmaster_met_without_kibble = False
boatmaster_completed_1 = False
boatmaster_completed_2 = False
boatmaster = None
transition_complete = False
cowboy_spawned = False


# wizzo distance
wizard_distance = 300
# boatmaster distance
boatmaster_distance = -600
# cats
cat_distance = 500
#boss
cowboy_distance = 0

while running:

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        scroll_speed = 2
        distance_traveled -= 1
        player.is_moving = True
        #print(f"Distance traveled: {distance_traveled}")
    elif keys[pygame.K_RIGHT]:
        scroll_speed = -2
        distance_traveled += 1
        player.is_moving = True
        #print(f"Distance traveled: {distance_traveled}")
    else:
        player.is_moving = False
        scroll_speed = 0

    player.frog_boundary()
    background_objects.update(scroll_speed )
    player.update()
    all_sprites.update()

    #reset captain no-boat
    if boatmaster_spawned and boatmaster and not boatmaster.alive() and not boatmaster_completed_2:
        boatmaster = None
        boatmaster_spawned = False

    # collision detection with rock & cats
    rock_hits = pygame.sprite.spritecollide(player, rocks, True)
    cat_hits = pygame.sprite.spritecollide(player, cats, False)
    cowboy_hits = pygame.sprite.spritecollide(player, cowboys, False)

    if player.is_attacking_tongue:
        tongue = Tongue(player, screen)
        tongue.update(cats)
        hit_cats = pygame.sprite.spritecollide(tongue, cats, False)
        hit_cowboy = pygame.sprite.spritecollide(tongue, cowboys, False)
        for cat in hit_cats:
            cat.take_damage()
            cat_hiss_sound.set_volume(0.5)
            cat_hiss_sound.play()
            cats_defeated += 1
            print(f"Cats defeated: {cats_defeated}")
            if cats_defeated >= max_cats - 3:
                for cat in cats:
                    cat.kill()
                cat_hiss_sound.stop()
                kibble_collected = True
                boatmaster_distance = -200
                print(f"kibble_collected: {kibble_collected}")
                victory_sound.set_volume(0.5)
                victory_sound.play()
                victory_sound.fadeout(1250)
                wizzo_speech_2.set_volume(0.7)
                wizzo_speech_2.play()
        for cowboy in hit_cowboy:
            cowboy.take_damage()
            cowboy_hurt.play()
            if cowboy.cowboy_dead:
                cowboy.kill()
                cowboy_hurt.stop()
                kibble_collected = True
                victory_sound.set_volume(0.5)
                victory_sound.play()
                victory_sound.fadeout(1250)
                cliff_hanger.play()
        player.is_attacking_tongue = False

        # get wizzo
    if distance_traveled >= wizard_distance and not wizard_spawned and not wizard_has_spoken:
       wizard = Wizard(player.rect.centerx + 150, 500, wizzo_speech) #where wizard goes
       all_sprites.add(wizard)
       wizard_spawned = True
       wizard.start_talking()
       print("Spawning wizard!")

    # setting flag to STOP this menace
    if wizard_spawned and wizard and not wizard.alive():
        wizard = None
        wizard_spawned = False
        wizard_has_spoken = True

    if wizard_spawned and wizard and not wizard.talking and not wizard_has_spoken:
        wizard_has_spoken = True
        wizard.kill()
        wizard = None
        wizard_spawned = False

    # get boatmaster
    if distance_traveled <= boatmaster_distance:
        if not boatmaster_spawned and not (boatmaster_completed_1 and boatmaster_completed_2):
            boatmaster = Boatmaster(player.rect.centerx - 150, 500)
            all_sprites.add(boatmaster)
            boatmaster_spawned = True

        if boatmaster:
            if boatmaster.fading:
                boatmaster.update()
            elif not boatmaster.talking:
                if not boatmaster_completed_1 and kibble_collected == False:
                    boatmaster.start_talking(kibble_collected, screen, False)
                    boatmaster_completed_1 = True
                    boatmaster_distance = -300

                elif not boatmaster_completed_2 and kibble_collected == True:
                    boatmaster.start_talking(kibble_collected, screen, True)
                    boatmaster_completed_2 = True

            # part 2 starts here
            if boatmaster_completed_2 and boatmaster.finished_second_speech:
                boatmaster.stop_talking_2()
                #boatmaster_distance = 10000 # overkill
                #all_sprites.remove(boatmaster)
                #boatmaster.kill()
                boatmaster = None
                boatmaster_spawned = False
                transition_complete = True
                transition_to_new_background(screen, player, background_objects)

    if transition_complete and distance_traveled >= cowboy_distance:
        cowboy = Cowboy(all_sprites, player)
        all_sprites.add(cowboy)
        cowboys.add(cowboy)
        cowboy.rect.topleft = (player.rect.centerx + 150, 300)
        cowboy_speech_1.play()
        cowboy_distance = 600
        cowboy_spawned = False

        # spawn cat
    if distance_traveled >= cat_distance:
        if random.random() < cat_probability and cat_count < max_cats:
            cat = Cat(all_sprites, player)
            all_sprites.add(cat)
            cat_count += 1
            cats.add(cat)
            cat_spawned = True

    current_time = pygame.time.get_ticks()
    if rock_hits or cat_hits and current_time - player.last_hit_time > player.invincibility_time:
        print("Ouch!")
        player.health -= 1
        player.last_hit_time = current_time
        hit_sound.set_volume(1.0)
        hit_sound.play()

        if player.health <= 0:
            death_sound.play()
            print("Game Over")
            pygame.time.delay(2200)
            running = False

    # spawn birdy at random
    if random.randint(0, 150) < 2:  # adjust the number to make more or less frequent
        bird = Bird(all_sprites, rocks)
        all_sprites.add(bird)
        birds.add(bird)

    # blue background/sky... i'm colorblind so I have to spell it out
    screen.fill((0, 191, 255))
    # health
    player.draw_health(screen)
    # bottom half color...lawn green
    if not transition_complete:
        pygame.draw.rect(screen, (115, 230, 0), (0, 300, 800, 300))
    else:
        pygame.draw.rect(screen, (237, 201, 175), (0, 300, 800, 300))
    # draw background stuff & sprites
    background_objects.draw(screen)
    all_sprites.draw(screen)
    #update & draw tongues
    tongues.update(cats)
    tongues.draw(screen)

    if wizard and wizard.talking:
        wizard.speak(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # attack
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tongue = Tongue(player, screen)
                tongues.add(tongue)
                attack_sound.play()
                player.is_attacking_tongue = True

        # speech skip
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if wizard and wizard.talking:
                    print("Wizard is talking!")
                    wizard.stop_talking()
                    wizzo_speech.stop()  # overkill
                    wizard.fading = True
                if boatmaster:
                    boatmaster.stop_talking_1()
                    boatmaster.stop_talking_2()
                    boatmaster_speech_1.stop()
                    boatmaster_speech_2.stop()
                    boatmaster.fading = True
                    boatmaster.kill()
                    boatmaster = None

        # quit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()