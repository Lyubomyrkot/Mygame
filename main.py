from pygame import *
import random

init()
font.init()
mixer.init()

FONT = "Play-Regular.ttf"

FPS = 60

TILE_SIZE = 35

scr_info = display.Info()
WIDTH, HEIGHT = scr_info.current_w, scr_info.current_h
window = display.set_mode((WIDTH, HEIGHT), flags=FULLSCREEN)
display.set_caption("PixelGame")
clock = time.Clock()


#sprite 
wall_img = image.load("images/wall.png")
wall_img = transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))

floor_img = image.load("images/floor.png")
floor_img = transform.scale(floor_img, (TILE_SIZE, TILE_SIZE))

block_img = image.load("images/block.png")
block_img = transform.scale(block_img, (TILE_SIZE, TILE_SIZE))

player_img = image.load("images/player/player_down.png")
player_img = transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

coin_img = image.load("images/coin.png")
coin_img = transform.scale(coin_img, (TILE_SIZE, TILE_SIZE))

diamond_img = image.load("images/diamond.png")
diamond_img = transform.scale(diamond_img, (TILE_SIZE, TILE_SIZE))

health_img = image.load("images/health/health_full.png")
health_img = transform.scale(health_img, (TILE_SIZE, TILE_SIZE))

health_half = image.load("images/health/health_half.png")
health_half = transform.scale(health_half, (TILE_SIZE, TILE_SIZE))

health_zero = image.load("images/health/health_zero.png")
health_zero = transform.scale(health_zero, (TILE_SIZE, TILE_SIZE))

hp_help_img = image.load("images/hp_help.png")
hp_help_img = transform.scale(hp_help_img, (TILE_SIZE, TILE_SIZE))

star_img = image.load("images/star/star_full.png")
star_zero_img = image.load("images/star/star_zero.png")

menu_img = image.load("images/menu/menu.png")
stop_menu_img = image.load("images/menu/stop_menu.png")
vining_img = image.load("images/menu/vining_menu.png")
defeat_img = image.load("images/menu/defeat_menu.png")
level_img = image.load("images/menu/level_menu.png")

stop_btn_img = image.load("images/stop_btn.png")
stop_btn_img = transform.scale(stop_btn_img, (TILE_SIZE, TILE_SIZE))

close_door_img = image.load("images/close_door.png")
open_door_img = image.load("images/open_door.png")

enemy_tree_img = image.load("images/enemies/enemy_tree.png")
enemy_tree_img = transform.scale(enemy_tree_img, (TILE_SIZE, TILE_SIZE))

enemy_skeleton_img = image.load("images/enemies/enemy_skeleton.png")
enemy_skeleton_img = transform.scale(enemy_skeleton_img, (TILE_SIZE, TILE_SIZE))

enemy_zombie_img = image.load("images/enemies/enemy_zombie.png")
enemy_zombie_img = transform.scale(enemy_zombie_img, (TILE_SIZE, TILE_SIZE))

#groops
all_sprites = sprite.Group()
all_map_sprite = sprite.Group()
all_labels = sprite.Group()
walls = sprite.Group()
coins = sprite.Group()
hp_helpers = sprite.Group()
enemies = sprite.Group()
blood_stains = sprite.Group()
diamonds = sprite.Group()


#завантаження музики
mixer.music.load("audio/background_music1.mp3")
mixer.music.set_volume(0.2)
#mixer.music.play()

damage_sound = mixer.Sound("audio/player_damage.mp3")
money_sound = mixer.Sound("audio/coin_collect.mp3")
health_sound = mixer.Sound("audio/potion_drink.mp3")
kill_enemy_sound = mixer.Sound("audio/kill_enemy.mp3")
button_click_sound = mixer.Sound("audio/button_click.mp3")

#class for text
class Label(sprite.Sprite):
    def __init__(self, text, x, y, fontsize = 30, color = (255, 255, 255), font_name = FONT):
        super().__init__()
        self.color = color
        self.font = font.Font(FONT, fontsize)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_labels.add(self)

    def set_text(self, new_text,color=(255, 255, 255)):
        self.image = self.font.render(new_text, True, color)


class Area(sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = image
        self.rect = Rect(x, y, width, height)

    def draw(self, window):
        window.blit(self.image, self.rect)

#class for sprites
class BaseSprite(sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image, (width, height))
        self.rect = Rect(x, y, width, height)
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)

    def draw(self, window):
        window.blit(self.image, self.rect)

def move_map(shift_x= 0, shift_y=0):
    for s in all_map_sprite:
        s.rect.x += shift_x
        s.rect.y += shift_y
    #checking for collision with walls
    coll_list = sprite.spritecollide(player, walls, False, sprite.collide_mask)
    if len(coll_list)>0:
        for s in all_map_sprite:
            s.rect.x -= shift_x
            s.rect.y -= shift_y

#class for player
class Player(BaseSprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image, True, False)
        self.speed = 4
        self.hp = 100
        self.damage = 10
        self.coins_counter = 0
        self.diamonds_counter = 0
        self.damage_timer = time.get_ticks()

    def update(self):
        shift_x, shift_y = 0, 0
        keys = key.get_pressed()

        if keys[K_a]:
            self.image = image.load("images/player/player_left.png")
            self.image = transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            if self.rect.x <= WIDTH:
                shift_x += self.speed
        if keys[K_d]:
            self.image = image.load("images/player/player_right.png")
            self.image = transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            if self.rect.x >= WIDTH / 3:
                shift_x -= self.speed
        if keys[K_w]:
            self.image = image.load("images/player/player_up.png")
            self.image = transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            if self.rect.y <= HEIGHT / 2:
                shift_y += self.speed
        if keys[K_s]:
            self.image = image.load("images/player/player_down.png")
            self.image = transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            if self.rect.y >= HEIGHT / 4:
                shift_y -= self.speed

        move_map(shift_x, shift_y)

        coll_list = sprite.spritecollide(player, coins, True, sprite.collide_mask)
        if len(coll_list) > 0:
            self.coins_counter += 1
            money_sound.play()
            coins_label.set_text(f"Coins: {self.coins_counter}")
        
        coll_list = sprite.spritecollide(player, diamonds, True, sprite.collide_mask)
        if len(coll_list) > 0:
            self.diamonds_counter += 1
            money_sound.play()
            diamonds_label.set_text(f"Diamonds: {self.diamonds_counter}")

        coll_list = sprite.spritecollide(player, hp_helpers, True, sprite.collide_mask)
        if len(coll_list) > 0:
            self.hp += 20
            health_sound.play()
            if self.hp > 100:
                self.hp = 100
            health_bar.hp = self.hp

        coll_list = sprite.spritecollide(player, enemies, False, sprite.collide_mask)
        if len(coll_list) > 0:
            for s in all_map_sprite:
                s.rect.x -= shift_x
                s.rect.y -= shift_y

    def attack(self, enemies_group):
        for enemy in enemies_group:
            if self.rect.colliderect(enemy.rect):  # Перевірка зіткнення
                enemy.hp -= self.damage
                damage_sound.play()
                if enemy.hp <= 0:
                    blood_stains.add(BloodStain(enemy.rect.centerx, enemy.rect.centery))
                    all_map_sprite.add(blood_stains)
                    kill_enemy_sound.play()
                    enemy.kill()

class Health(sprite.Sprite):
    def __init__(self, x, y, hp):
        super().__init__()
        self.x = x
        self.y = y
        self.hp = hp
        self.full = health_img
        self.half = health_half
        self.zero = health_zero

    def draw(self, window):
        x = self.x
        for i in range(0, 5):
            current_hp = self.hp - i * 20
            if current_hp >= 20:
                window.blit(self.full, (x, self.y))
            elif current_hp >= 10:
                window.blit(self.half, (x, self.y))
            else:
                window.blit(self.zero, (x, self.y))
            
            x += TILE_SIZE + 5

class Stars(sprite.Sprite):
    def __init__(self, x, y, count):
        super().__init__()
        self.x = x
        self.y = y
        self.count = count
        self.full = star_img
        self.zero = star_zero_img

    def draw(self, window):
        x = self.x  
        for i in range(3):
            if i < self.count:
                window.blit(self.full, (x, self.y))
            else:
                window.blit(self.zero, (x, self.y))

            x += TILE_SIZE + 40

class Enemy(BaseSprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image, True, False)
        self.dir_list = ['left', 'right', 'up', 'down']
        self.dir = random.choice(self.dir_list)
        self.damage_timer = time.get_ticks()
        all_sprites.remove(self)
        self.speed = 2
        self.hp = 20
        self.damage = 10

    def attack(self, player):
        now = time.get_ticks()
        if self.rect.colliderect(player.rect) and now - self.damage_timer > 1000:
            self.damage_timer = time.get_ticks()
            player.hp -= self.damage
            health_bar.hp = player.hp

    def update(self, player):
        old_pos = self.rect.x, self.rect.y

        if self.dir == 'up':
            self.rect.y -= self.speed
        elif self.dir == 'down':
            self.rect.y += self.speed
        elif self.dir == 'left':
            self.rect.x -= self.speed
            self.image = self.left_image
        elif self.dir == 'right':
            self.rect.x += self.speed
            self.image = self.right_image

        coll_list = sprite.spritecollide(self, walls, False)
        if len(coll_list)>0:
            self.rect.x, self.rect.y = old_pos
            self.dir = random.choice(self.dir_list)

    


class SkeletonEnemy(Enemy):
    def __init__(self, x, y, width, height):
        super().__init__(enemy_skeleton_img, x, y, width, height)
        self.dir_list = ['left', 'right', 'up', 'down']
        self.dir = random.choice(self.dir_list)
        self.speed = 2
        self.hp = 40
        self.damage = 10
        
    def update(self, player):
        old_pos = self.rect.x, self.rect.y

        if self.dir == 'up':
            self.rect.y -= self.speed
        elif self.dir == 'down':
            self.rect.y += self.speed
        elif self.dir == 'left':
            self.rect.x -= self.speed
            self.image = self.left_image
        elif self.dir == 'right':
            self.rect.x += self.speed
            self.image = self.right_image

        coll_list = sprite.spritecollide(self, walls, False)
        if len(coll_list)>0:
            self.rect.x, self.rect.y = old_pos
            self.dir = random.choice(self.dir_list)
        
        self.attack(player)


class ZombieEnemy(Enemy):
    def __init__(self, x, y, width, height):
        super().__init__(enemy_zombie_img, x, y, width, height)
        self.dir_list = ['left', 'right', 'up', 'down']
        self.dir = random.choice(self.dir_list)
        self.change_dir_timer = time.get_ticks()
        self.change_dir_timer_interval = 1000
        self.attack_cooldown = 2000
        self.last_attack_time = 0

        self.speed = 3
        self.hp = 20
        self.damage = 10

    def update(self, player):
        now = time.get_ticks()
        if now - self.change_dir_timer > self.change_dir_timer_interval:
            self.change_dir_timer = now
            self.dir = random.choice(self.dir_list)
        
        if self.dir == 'up':
            self.rect.y -= self.speed
            if len(sprite.spritecollide(self, walls, False)) > 0:
                self.rect.y += self.speed
                self.dir = random.choice(self.dir_list)

        elif self.dir == 'down':
            self.rect.y += self.speed
            if len(sprite.spritecollide(self, walls, False)) > 0:
                self.rect.y -= self.speed
                self.dir = random.choice(self.dir_list)

        elif self.dir == 'left':
            self.rect.x -= self.speed
            self.image = self.left_image
            if len(sprite.spritecollide(self, walls, False)) > 0:
                self.rect.x += self.speed
                self.dir = random.choice(self.dir_list)

        elif self.dir == 'right':
            self.rect.x += self.speed
            self.image = self.right_image
            if len(sprite.spritecollide(self, walls, False)) > 0:
                self.rect.x -= self.speed
                self.dir = random.choice(self.dir_list)
        
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        distance_sq = dx ** 2 + dy ** 2

        if distance_sq < 60 ** 2 and now - self.last_attack_time > self.attack_cooldown:
            player.hp -= self.damage
            health_bar.hp = player.hp
            self.last_attack_time = now
    


class TreeEnemy(Enemy):
    def __init__(self, x, y, width, height):
        super().__init__(enemy_tree_img, x, y, width, height)
        self.dir_list = ['left', 'right', 'up', 'down']
        self.dir = random.choice(self.dir_list)
        self.change_dir_timer = time.get_ticks()
        self.change_dir_timer_interval = 1000
        self.attack_cooldown = 2000
        self.last_attack_time = 0

        self.speed = 1
        self.hp = 50
        self.damage = 20

    def update(self, player):
        now = time.get_ticks()
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        distance_sq = dx ** 2 + dy ** 2

        if distance_sq < 30 ** 2 and now - self.last_attack_time > self.attack_cooldown:
            player.hp -= self.damage
            health_bar.hp = player.hp
            self.last_attack_time = now

        if distance_sq < 100 ** 2:
            if now - self.change_dir_timer > self.change_dir_timer_interval:
                self.change_dir_timer = now
                self.dir = random.choice(self.dir_list)
        
            if self.dir == 'up':
                self.rect.y -= self.speed
                if len(sprite.spritecollide(self, walls, False)) > 0:
                    self.rect.y += self.speed
                    self.dir = random.choice(self.dir_list)

            elif self.dir == 'down':
                self.rect.y += self.speed
                if len(sprite.spritecollide(self, walls, False)) > 0:
                    self.rect.y -= self.speed
                    self.dir = random.choice(self.dir_list)

            elif self.dir == 'left':
                self.rect.x -= self.speed
                self.image = self.left_image
                if len(sprite.spritecollide(self, walls, False)) > 0:
                    self.rect.x += self.speed
                    self.dir = random.choice(self.dir_list)

            elif self.dir == 'right':
                self.rect.x += self.speed
                self.image = self.right_image
                if len(sprite.spritecollide(self, walls, False)) > 0:
                    self.rect.x -= self.speed
                    self.dir = random.choice(self.dir_list)

class BloodStain(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = image.load("images/blood_stain.png")
        self.image = transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))

def state_star():
    stars = 0
    if player.coins_counter >= 10:
        stars += 1
    if len(enemies) == 0:
        stars += 1
    if player.hp > 0:
        stars += 1
    return stars

#map loading
def game_start():
    global player, screen, run, all_map_sprite, all_sprites, walls, coins, hp_helpers, enemies, finish_block

    all_map_sprite.empty()
    all_sprites.empty()
    walls.empty()
    coins.empty()
    hp_helpers.empty()
    enemies.empty()
    blood_stains.empty()

    #mixer.music.play()
    run = True
    

    with open("map.txt", "r") as file:
            map = file.readlines()
            x, y = 0, 0
            for row in map:
                for symbol in row:
                    map_object = None
                    if symbol == "w":
                        map_object = BaseSprite(wall_img, x, y, TILE_SIZE, TILE_SIZE)
                        walls.add(map_object)
                    if symbol == "p":
                        map_object = BaseSprite(floor_img, x, y, TILE_SIZE, TILE_SIZE)
                        player = Player(player_img, x, y, TILE_SIZE, TILE_SIZE)
                        player.hp = 100
                        player.coins_counter = 0
                    if symbol == "c":
                        all_map_sprite.add(BaseSprite(floor_img, x, y, TILE_SIZE, TILE_SIZE))
                        map_object = BaseSprite(coin_img, x, y, TILE_SIZE/1.5, TILE_SIZE/1.5)
                        coins.add(map_object)
                    if symbol == "d":
                        all_map_sprite.add(BaseSprite(floor_img, x, y, TILE_SIZE, TILE_SIZE))
                        map_object = BaseSprite(diamond_img, x, y, TILE_SIZE/1.5, TILE_SIZE/1.5)
                        diamonds.add(map_object)
                    if symbol == ".":
                        map_object = BaseSprite(floor_img, x, y, TILE_SIZE, TILE_SIZE)
                    if symbol == "b":
                        finish_block = BaseSprite(open_door_img, x, y, TILE_SIZE, TILE_SIZE)
                        map_object = finish_block
                    if symbol == "h":
                        all_map_sprite.add(BaseSprite(floor_img, x, y, TILE_SIZE, TILE_SIZE))
                        map_object = BaseSprite(hp_help_img, x, y, TILE_SIZE/1.5, TILE_SIZE/1.5)
                        hp_helpers.add(map_object)
                    if symbol == "e":
                        enemy_type = random.choice([SkeletonEnemy, ZombieEnemy, TreeEnemy])
                        all_map_sprite.add(BaseSprite(floor_img, x, y, TILE_SIZE, TILE_SIZE))
                        map_object = enemy_type(x, y, TILE_SIZE, TILE_SIZE)
                        enemies.add(map_object)
                    if map_object:
                        all_map_sprite.add(map_object)
                    x += TILE_SIZE 
                x = 0
                y += TILE_SIZE 

game_start()

#labels
coins_label = Label(f"Coins: {player.coins_counter}", 10, 60)
diamonds_label = Label(f"Diamonds: {player.diamonds_counter}", 10, 100)
health_bar = Health(10, 10, player.hp)

stop_btn_img = Area(stop_btn_img, WIDTH-TILE_SIZE-5, 5, TILE_SIZE, TILE_SIZE)
stop_btn = Rect(WIDTH-TILE_SIZE-5, 5, TILE_SIZE, TILE_SIZE)

menu = Area(menu_img, 550, 185, WIDTH, HEIGHT)
play_btn = Rect(622, 260, 150, 38)
exit_btn = Rect(622, 499, 150, 38)
shop_btn = Rect(622, 340, 150, 38)
level_btn = Rect(622, 420, 150, 38)

stop_menu = Area(stop_menu_img, 550, 185, WIDTH, HEIGHT)
continue_btn = Rect(632, 308, 150, 38)
restart_btn = Rect(632, 388, 150, 38)
exit_stop_btn = Rect(632, 468, 150, 38)

vining_img = Area(vining_img, 550, 185, WIDTH, HEIGHT)
restart_btnvn = Rect(665, 477, 35, 40)
menu_btn = Rect(600, 477, 35, 40)
level_btnvl = Rect(730, 477, 35, 40)

defeat_img = Area(defeat_img, 550, 185, WIDTH, HEIGHT)

level_img = Area(level_img, 530, 185, WIDTH, HEIGHT)
level_1_btn = Rect(584, 304, 37, 40)
menu_btnlvl = Rect(686, 529, 37, 40)

screen = "menu"

while run:
    if screen == "game":
        window.fill((0, 0, 0))
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    screen = "stop" 
                if e.key == K_SPACE:
                    player.attack(enemies)
                

            if e.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                if stop_btn.collidepoint(x, y):
                    button_click_sound.play()
                    screen = "stop"

            
        if player.rect.colliderect(finish_block.rect):
            screen = "end_game"

        all_sprites.draw(window)
        blood_stains.draw(window)
        player.draw(window)
        player.update()
        all_labels.draw(window)
        health_bar.draw(window)
        enemies.draw(window)
        stop_btn_img.draw(window)
        for enemy in enemies:
            enemy.update(player)
        
       

        if player.hp <= 0:
            mixer.music.stop()
            screen = "stop"
            player.kill()

        

    if screen == "menu":
        window.fill((82, 99, 115))
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    run = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                print(x, y)
                if play_btn.collidepoint(x, y):
                    button_click_sound.play()
                    screen = "game"
                    game_start()
                    coins_label.set_text(f"Coins: {player.coins_counter}")
                    diamonds_label.set_text(f"Diamonds: {player.diamonds_counter}")
                    health_bar.hp = player.hp

                if shop_btn.collidepoint(x, y):
                    button_click_sound.play()
                    screen = "shop"

                if level_btn.collidepoint(x, y):
                    button_click_sound.play()
                    screen = "level"

                if exit_btn.collidepoint(x, y):
                    button_click_sound.play()
                    run = False


        menu.draw(window)
    if screen == "shop":
        window.fill((122, 199, 215))
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:

                    screen = "menu"


    if screen == "level":
        window.fill((82, 99, 115))
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    screen = "menu"
            if e.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                print(x, y)
                if level_1_btn.collidepoint(x, y):
                    button_click_sound.play()
                    screen = "game"
                    game_start()
                    coins_label.set_text(f"Coins: {player.coins_counter}")
                    diamonds_label.set_text(f"Diamonds: {player.diamonds_counter}")
                    health_bar.hp = player.hp
                if menu_btnlvl.collidepoint(x, y):
                    button_click_sound.play()
                    screen = "menu"
        level_img.draw(window)

    if screen == "stop":
        window.fill((82, 99, 115))
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    run = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                print(x, y)
                if continue_btn.collidepoint(x, y):
                    button_click_sound.play()
                    screen = "game"

                if restart_btn.collidepoint(x, y):
                    button_click_sound.play()
                    game_start()
                    coins_label.set_text(f"Coins: {player.coins_counter}")
                    diamonds_label.set_text(f"Diamonds: {player.diamonds_counter}")
                    health_bar.hp = player.hp
                    screen = "game"

                if exit_stop_btn.collidepoint(x, y):
                    button_click_sound.play()
                    run = False
            
        stop_menu.draw(window)
    
    if screen == "end_game":
        window.fill((82, 99, 115))
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    run = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                print(x, y)
                if restart_btnvn.collidepoint(x, y):
                    button_click_sound.play()
                    game_start()
                    coins_label.set_text(f"Coins: {player.coins_counter}")
                    diamonds_label.set_text(f"Diamonds: {player.diamonds_counter}")
                    health_bar.hp = player.hp
                    screen = "game"
                if menu_btn.collidepoint(x, y):
                    button_click_sound.play()
                    screen = "menu"
                if level_btnvl.collidepoint(x, y):
                    button_click_sound.play()
                    screen = "level"
        vining_img.draw(window)
        star_count = state_star()
        stars_bar = Stars(574, 307, star_count)
        stars_bar.draw(window)
    
    display.update()
    clock.tick(FPS)