from pygame import *
import random 

init()
font.init()


FONT = "Play-Bold.ttf"

FPS = 60

TILE_SIZE = 40
MAP_WIDTH, MAP_HEIGHT = 34.2, 19.2
WIDTH, HEIGHT = TILE_SIZE*MAP_WIDTH, TILE_SIZE*MAP_HEIGHT

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("PixelGame")
clock = time.Clock()


#sprite 
wall = image.load("images/wall.png")
wall_img = transform.scale(wall, (TILE_SIZE, TILE_SIZE))
player = image.load("images/player.png")
player_img = transform.scale(player, (TILE_SIZE, TILE_SIZE))
waall = image.load("images/waall.png")
waall_img = transform.scale(waall, (TILE_SIZE, TILE_SIZE))

#groops
all_sprites = sprite.Group()
all_labels = sprite.Group()
walls = sprite.Group()


camera_x, camera_y = 0, 0


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
neew_movs = 0
#class for player
class Player(BaseSprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image, True, False)
        self.speed = 4
        self.hp = 100
        self.coins = 0

    def update(self):
        old_pos = self.rect.x, self.rect.y
        keys = key.get_pressed()
        if keys[K_a]:
            camera_x -= self.speed
        if keys[K_d]:
            camera_x += self.speed
        if keys[K_w]:
            camera_y -= self.speed
        if keys[K_s]:
            camera_y += self.speed


        #checking for collision with walls
        coll_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(coll_list)>0:
            self.rect.x, self.rect.y = old_pos





#map loading
with open("map.txt", "r") as file:
        map = file.readlines()
        x, y = 0, 0
        for row in map:
            for symbol in row:
                if symbol == "w":
                    walls.add(BaseSprite(wall_img, x + neew_movs, y, TILE_SIZE, TILE_SIZE))
                if symbol == "p":
                    player = Player(player_img, x, y, TILE_SIZE, TILE_SIZE)
                x += TILE_SIZE 
            x = 0
            y += TILE_SIZE 


run = True
while run:
    window.fill((0, 0, 0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                run = False
            if e.key == K_SPACE:
                neew_movs += 10
            


    #window.blit()
    all_sprites.draw(window)
    all_labels.draw(window)
    player.update()
    display.update()
    clock.tick(FPS)