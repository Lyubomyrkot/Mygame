from pygame import *
import random 

init()
font.init()

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

player_img = image.load("images/player_down.png")
player_img = transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

coin_img = image.load("images/coin.png")
coin_img = transform.scale(coin_img, (TILE_SIZE, TILE_SIZE))

health_img = image.load("images/health_full.png")
health_img = transform.scale(health_img, (TILE_SIZE, TILE_SIZE))

health_half = image.load("images/health_half.png")
health_half = transform.scale(health_half, (TILE_SIZE, TILE_SIZE))

health_zero = image.load("images/health_zero.png")
health_zero = transform.scale(health_zero, (TILE_SIZE, TILE_SIZE))

hp_help_img = image.load("images/hp_help.png")
hp_help_img = transform.scale(hp_help_img, (TILE_SIZE, TILE_SIZE))

menu_img = image.load("images/menu.png")
stop_menu_img = image.load("images/stop_menu.png")

stop_btn_img = image.load("images/stop_btn.png")
stop_btn_img = transform.scale(stop_btn_img, (TILE_SIZE, TILE_SIZE))


#groops
all_sprites = sprite.Group()
all_map_sprite = sprite.Group()
all_labels = sprite.Group()
walls = sprite.Group()
coins = sprite.Group()
hp_helpers = sprite.Group()



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
        now = time.get_ticks()
        if now-player.damage_timer > 1000:
            player.damage_timer = time.get_ticks()
            player.hp -= 10
            health_bar.hp = player.hp

#class for player
class Player(BaseSprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image, True, False)
        self.speed = 4
        self.hp = 100
        self.coins_counter = 0
        self.damage_timer = time.get_ticks()

    def update(self):
        shift_x, shift_y = 0, 0
        keys = key.get_pressed()

        if keys[K_a]:
            self.image = image.load("images/player_left.png")
            self.image = transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            if self.rect.x <= WIDTH:
                shift_x += self.speed
        if keys[K_d]:
            self.image = image.load("images/player_right.png")
            self.image = transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            if self.rect.x >= WIDTH / 3:
                shift_x -= self.speed
        if keys[K_w]:
            self.image = image.load("images/player_up.png")
            self.image = transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            if self.rect.y <= HEIGHT / 2:
                shift_y += self.speed
        if keys[K_s]:
            self.image = image.load("images/player_down.png")
            self.image = transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            if self.rect.y >= HEIGHT / 4:
                shift_y -= self.speed

        move_map(shift_x, shift_y)

        coll_list = sprite.spritecollide(player, coins, True, sprite.collide_mask)
        if len(coll_list) > 0:
            self.coins_counter += 1
            coins_label.set_text(f"Coins: {self.coins_counter}")

        coll_list = sprite.spritecollide(player, hp_helpers, True, sprite.collide_mask)
        if len(coll_list) > 0:
            self.hp += 20
            if self.hp > 100:
                self.hp = 100
            health_bar.hp = self.hp

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



#map loading
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
                if symbol == "c":
                    all_map_sprite.add(BaseSprite(floor_img, x, y, TILE_SIZE, TILE_SIZE))
                    map_object = BaseSprite(coin_img, x, y, TILE_SIZE/1.5, TILE_SIZE/1.5)
                    coins.add(map_object)
                if symbol == ".":
                    map_object = BaseSprite(floor_img, x, y, TILE_SIZE, TILE_SIZE)
                if symbol == "b":
                    map_object = BaseSprite(block_img, x, y, TILE_SIZE, TILE_SIZE)
                if symbol == "h":
                    all_map_sprite.add(BaseSprite(floor_img, x, y, TILE_SIZE, TILE_SIZE))
                    map_object = BaseSprite(hp_help_img, x, y, TILE_SIZE/1.5, TILE_SIZE/1.5)
                    hp_helpers.add(map_object)
                if map_object:
                    all_map_sprite.add(map_object)
                x += TILE_SIZE 
            x = 0
            y += TILE_SIZE 

#labels
coins_label = Label(f"Coins: {player.coins_counter}", 10, 60)
health_bar = Health(10, 10, player.hp)

stop_btn = BaseSprite(stop_btn_img, WIDTH-TILE_SIZE-5, 5, TILE_SIZE, TILE_SIZE)
stop_btn = Rect(WIDTH-TILE_SIZE-5, 5, TILE_SIZE, TILE_SIZE)

menu = Area(menu_img, 550, 185, WIDTH, HEIGHT)
play_btn = Rect(622, 260, 150, 38)
exit_btn = Rect(622, 499, 150, 38)
shop_btn = Rect(622, 340, 150, 38)
options_btn = Rect(622, 420, 150, 38)

stop_menu = Area(stop_menu_img, 550, 185, WIDTH, HEIGHT)
continue_btn = Rect(632, 308, 150, 38)
restart_btn = Rect(632, 388, 150, 38)
exit_stop_btn = Rect(632, 468, 150, 38)

screen = "menu"
run = True
while run:
    if screen == "game":
        window.fill((0, 0, 0))
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    screen = "stop"
            if e.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                if stop_btn.collidepoint(x, y):
                    screen = "stop"

        all_sprites.draw(window)
        player.draw(window)
        player.update()
        all_labels.draw(window)
        health_bar.draw(window)

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
                    screen = "game"

                if shop_btn.collidepoint(x, y):
                    screen = "shop"

                if options_btn.collidepoint(x, y):
                    screen = "options"

                if exit_btn.collidepoint(x, y):
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


    if screen == "options":
        window.fill((182, 49, 195))
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    screen = "menu"

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
                    screen = "game"

                if restart_btn.collidepoint(x, y):
                    screen = "shop"

                if exit_stop_btn.collidepoint(x, y):
                    run = False
            
        stop_menu.draw(window)

                



            


    #window.blit()
    
    display.update()
    clock.tick(FPS)