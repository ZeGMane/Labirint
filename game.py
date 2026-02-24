from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, image, x, y, speed):
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image,(self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y , speed)
        self.rotate = 'left'
    def update_player(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < w_wedht - 65:
            self.rect.y += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < w_heigh - 70:
            self.rect.x += self.speed

class Enemy(GameSprite):
    def __init__(self, image, x, y, speed, speed_up):
        super().__init__(image, x, y , speed)
        self.direction_x = 'left'
        self.direction_y = 'down'
        self.mode = 'horizontal'
    def update_enemy(self):
        if self.mode == 'horizontal':
            if self.rect.x > w_heigh - 65:
                self.direction_x = 'left'
            elif self.rect.x <= 510:
                self.direction_x = 'right'
                self.mode = 'vertical'

            if self.direction_x == 'left':
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed

        elif self.mode == 'vertical':
            if self.rect.y > w_wedht - 65:
                self.direction_y = 'up'
            elif self.rect.y <= 300:
                self.direction_y = 'down'
                self.mode = 'horizontal'

            if self.direction_y == 'up':
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed
            

        
class Wall(sprite.Sprite):
    def __init__(self, wall_widht, wall_height, wall_color1, wall_color2,wall_color3, x , y):
        self.height = wall_height
        self.width = wall_widht
        self.color1 = wall_color1
        self.color2 = wall_color2
        self.color3 = wall_color3
        self.wall_rect = Surface((self.width, self.height))
        self.wall_rect.fill((self.color1, self.color2, self.color3))
        self.rect = self.wall_rect.get_rect()
        self.rect.x = x 
        self.rect.y = y
    def draw(self):
        win.blit(self.wall_rect,(self.rect.x, self.rect.y))


        
w_heigh = 700
w_wedht = 500

win = display.set_mode((w_heigh, w_wedht))
display.set_caption('Лабиринт')

time = time.Clock()
game = True

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

font.init()
font = font.Font(None, 70)

winner = font.render('YOU WIN', True,(255,215,0))
lose = font.render('YOU LOSE', True,(255,0,0))

bg = transform.scale(image.load('background.jpg'), (700,500))

player_sprite = transform.scale(image.load('hero.png'),(60,60))
enemy_sprite = transform.scale(image.load('cyborg.png'),(60,60))
gold_sprite = transform.scale(image.load('treasure.png'),(60,60))

gold = GameSprite(gold_sprite, 600, 380, 10)

player_exz = Player(player_sprite, 30, 400, 7)
enemy_exz = Enemy(enemy_sprite, 600, 300, 2, 0)

stena1 = Wall(10, 410, 101, 255, 87, 100, 20)
stena2 = Wall(400,10, 101, 255, 87, 110,20)
stena3 = Wall(10,350, 101, 255, 87, 200,120)
stena4 = Wall(310,10, 101, 255, 87, 200,460)
stena5 = Wall(10,350, 101, 255, 87,300 ,20)
stena6 = Wall(10,350, 101, 255, 87,400,120)
stena7 = Wall(10,350, 101, 255, 87,500,20)

finish = False
stens = [stena1, stena2, stena3, stena4, stena5, stena6, stena7]
while game:
    win.blit(bg, (0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        player_exz.reset()
        enemy_exz.reset()
        gold.reset()
        player_exz.update_player()
        enemy_exz.update_enemy()
        for i in stens:
            i.draw()
            if sprite.collide_rect(player_exz, i) or sprite.collide_rect(player_exz, enemy_exz):
                finish = True
                kick.play()
                win.blit(lose, (230, 220))
            

        if sprite.collide_rect(player_exz, gold):
            finish = True
            money.play()
            win.blit(winner, (230, 220))



        time.tick(60)
        display.update()
