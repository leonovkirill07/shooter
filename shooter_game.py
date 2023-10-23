#Создай собственный Шутер!

from pygame import *
from random import *

window = display.set_mode((700, 500))
display.set_caption('Шутер')

background = transform.scale(image.load('galaxy.jpg'), (700, 500))

clock = time.Clock()

mixer.init()


sound = mixer.Sound('fire.ogg')



'''mixer.music.load('space.ogg')
mixer.music.play()'''

FPS = 60

x1 = 100

x2 = 100

y1 = 50

y2 = 50

speed = 2

finish = False

font.init()
font1 = font.Font(None, 30)
font = font.Font(None, 70)
win = font.render('YOU WON!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (255, 0, 0))

lost = 0

score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x= player_x
        self.rect.y = player_y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= 10
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += 10
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 25, 25, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 600:
            self.rect.y = 0
            lost = lost + 1
            self.rect.x = randint(10, 500)


    

shuttle = Player('rocket.png', 100, 420, 50, 50, 5)

bullets = sprite.Group()



monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(10, 500), -40, 65, 65, randint(1, 5))
    monsters.add(monster)
  


game = True
while game:



    if finish != True:
        window.blit(background, (0, 0))
        shuttle.reset()
        shuttle.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)

        for i in sprite_list:
            score += 1
            monster = Enemy('ufo.png', randint(10, 500), -40, 65, 65, randint(1, 5))
            monsters.add(monster)
    
        if score >= 10:
            finish = True
            window.blit(win, (230, 250))
        
        if lost >= 3 or sprite.spritecollide(shuttle, monsters, False):
            finish = True
            window.blit(lose, (230, 250))
           
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 100))
        window.blit(text_lose, (10, 50))
        text_lose = font1.render('Счёт:' + str(score), 1, (255, 255, 100))
        window.blit(text_lose, (10, 20))

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                shuttle.fire()
                sound.play()


    display.update()
    clock.tick(FPS)