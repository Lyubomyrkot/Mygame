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
wall_img = image.load("images/floor.jpg")
wall_img = transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))

floor_img = image.load("images/wall.png")
floor_img = transform.scale(floor_img, (TILE_SIZE, TILE_SIZE))

block_img = image.load("images/block.png")
block_img = transform.scale(block_img, (TILE_SIZE, TILE_SIZE))

player_img = image.load("images/player.png")
player_img = transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

coin_img = image.load("images/coin.png")
coin_img = transform.scale(coin_img, (TILE_SIZE, TILE_SIZE))

#groops
all_sprites = sprite.Group()
all_labels = sprite.Group()
walls = sprite.Group()
coins = sprite.Group()



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
    for s in all_sprites:
        s.rect.x += shift_x
        s.rect.y += shift_y
    #checking for collision with walls
    coll_list = sprite.spritecollide(player, walls, False, sprite.collide_mask)
    if len(coll_list)>0:
        for s in all_sprites:
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
        self.coins_counter = 0

    def update(self):
        shift_x, shift_y = 0, 0
        keys = key.get_pressed()

        if keys[K_a]:
           if self.rect.x <= WIDTH:
                shift_x += self.speed
        if keys[K_d]:
            if self.rect.x >= WIDTH / 3:
                shift_x -= self.speed
        if keys[K_w]:
            if self.rect.y <= HEIGHT / 2:
                shift_y += self.speed
        if keys[K_s]:
            if self.rect.y >= HEIGHT / 4:
                shift_y -= self.speed

        move_map(shift_x, shift_y)

        coll_list = sprite.spritecollide(player, coins, True, sprite.collide_mask)
        if len(coll_list) > 0:
            self.coins_counter += 1
            coins_label.set_text(f"Coins: {self.coins_counter}")




#map loading
with open("map.txt", "r") as file:
        map = file.readlines()
        x, y = 0, 0
        for row in map:
            for symbol in row:
                if symbol == "w":
                    wall = BaseSprite(wall_img, x, y, TILE_SIZE, TILE_SIZE)
                    walls.add(wall)
                if symbol == "p":
                    floor = BaseSprite(floor_img, x, y, TILE_SIZE, TILE_SIZE)
                    player = Player(player_img, x, y, TILE_SIZE-10, TILE_SIZE-10)
                    all_sprites.remove(player)
                if symbol == "c":
                    floor = BaseSprite(floor_img, x, y, TILE_SIZE, TILE_SIZE)
                    coins.add(BaseSprite(coin_img, x, y, TILE_SIZE/2, TILE_SIZE/2))
                if symbol == ".":
                    floor = BaseSprite(floor_img, x, y, TILE_SIZE, TILE_SIZE)
                if symbol == "b":
                    block = BaseSprite(block_img, x, y, TILE_SIZE, TILE_SIZE)
                 
                x += TILE_SIZE 
            x = 0
            y += TILE_SIZE 

#labels
coins_label = Label(f"Coins: {player.coins_counter}", 10, 10)

run = True
while run:
    window.fill((0, 0, 0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                run = False

            


    #window.blit()
    all_sprites.draw(window)
    player.draw(window)
    player.update()
    all_labels.draw(window)
    display.update()
    clock.tick(FPS)