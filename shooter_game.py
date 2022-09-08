#Create your own shooter

from pygame import *
from random import randint
# create the window object
WIDTH = 800
HEIGHT = 640
window = display.set_mode((WIDTH, HEIGHT))
# create the clock object
clock = time.Clock()
lives = 5 
font.init()
class ImageSprite(sprite.Sprite):
    def __init__(self, file_name, pos, size, speed): # constructor (a function that runs when a new object is created)
        super().__init__()
        self.image = image.load(file_name)
        self.image = transform.scale(self.image, size)
        self.rect = Rect(pos, size)
        self.speed = Vector2(speed)
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
class Player(ImageSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed.x
        if keys[K_d]:
            self.rect.x += self.speed.x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        #if keys[K_SPACE]:
            #self.shoot()
    def shoot(self):
        b = Bullet(file_name='bullet.png', pos=(0,0), size = (8,12), speed = (0,-12))
        b.rect.center = self.rect.midtop
        bullets.add(b)
        b = Bullet(file_name='bullet.png', pos=(0,0), size = (8,12), speed = (1,-12))
        b.rect.center = self.rect.midtop
        bullets.add(b)
        b = Bullet(file_name='bullet.png', pos=(0,0), size = (8,12), speed = (-1,-12))
        b.rect.center = self.rect.midtop
        bullets.add(b)
        b = Bullet(file_name='bullet.png', pos=(0,0), size = (8,12), speed = (3,-12))
        b.rect.center = self.rect.midtop
        bullets.add(b)
        b = Bullet(file_name='bullet.png', pos=(0,0), size = (8,12), speed = (-3,-12))
        b.rect.center = self.rect.midtop
        bullets.add(b)
    def shootMissile(self):
        m = Missile(file_name='Missile.png', pos=(0,0), size = (32,48), speed = (0,-12))
        m.rect.center = self.rect.midtop
        missiles.add(m)
    def shootMissile2(self):
        n = Missile2(file_name='Missile2.png', pos=(0,0), size = (32,48), speed = (0,-12))
        n.rect.center = self.rect.midtop
        missiles.add(n)
    def shootNuke(self):
        n = Missile2(file_name='nuke.png', pos=(0,0), size = (60,110), speed = (0,-12))
        n.rect.center = self.rect.midtop
        nukes.add(n)
class Enemy(ImageSprite):
    def update(self):
        if self.rect.top >= HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIDTH-self.rect.width)
        self.rect.topleft += self.speed

class Enemy2(ImageSprite):
    def update(self):
        if self.rect.top >= HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIDTH-self.rect.width)
        if self.rect.right <= 0:
            self.rect.left = WIDTH
        self.rect.topleft += self.speed
missiles = sprite.Group()

nukes = sprite.Group()

bullets = sprite.Group()
class Bullet(ImageSprite):
    def update(self):
        if self.rect.bottom <= 0:
            self.kill()
        self.rect.topleft += self.speed

class Missile(ImageSprite):
    def update(self):
        if self.rect.bottom <= 0:
            self.kill()
        self.rect.topleft += self.speed

class Missile2(ImageSprite):
    def update(self):
        if self.rect.bottom <= 0:
            self.kill()
        self.rect.topleft += self.speed

class Text(sprite.Sprite):
    def __init__(self, words, color, position, font_size):
        self.words = words
        self.color = color
        self.position = position
        self.font_size = font_size
        self.font = font.SysFont(None, self.font_size)
        self.update_text(self.words)
    def update_text(self, new_words):
        self.image = self.font.render(new_words, True, self.color)
    def draw(self, surface):
        surface.blit(self.image, self.position)

score = 0

lives_counter =Text(words="lives = 5", color="lightblue", position = (30,30), font_size = 100)
score_counter =Text(words="score = 0", color="darkgreen", position=(90,30), font_size =50)
bg = ImageSprite(file_name="galaxy.jpg", pos=(0,0), size=(WIDTH,HEIGHT), speed=(0,0))
lose = ImageSprite(file_name="lose.png", pos=(250,200), size=(300,300), speed=(0,0))
boom = ImageSprite(file_name="boom.png", pos=(250,200), size=(300,300), speed=(0,0))
p1 = Player(file_name="rocket.png",pos=(0,0), size=(60,80), speed=(10,0))
p1.rect.centerx = WIDTH/2
p1.rect.bottom = HEIGHT - 10



enemies = sprite.Group()
def create_enemy():
    new_enemy = Enemy(file_name="ufo.png",pos=(0,0), size=(60,80), speed=(0, randint(1,5)))
    new_enemy.rect.x = randint(0, WIDTH-new_enemy.rect.width)
    enemies.add(new_enemy)

enemies2 = sprite.Group()
def create_enemy2():
    new_enemy = Enemy2(file_name="asteroid.png",pos=(0,0), size=(50,50), speed=(randint(-4,0), randint(1,5)))
    new_enemy.rect.x = randint(0, WIDTH-new_enemy.rect.width)
    enemies2.add(new_enemy)

for _ in range(randint(5,8)):
    create_enemy()
    create_enemy2()
boom_counter = -1
# create the MAIN loop (stops when the QUIT event happens)
while not event.peek(QUIT):
    for ev in event.get():
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                p1.shoot()
            if ev.key == K_LSHIFT:
                p1.shootMissile()
            if ev.key == K_RSHIFT:
                p1.shootMissile2()
            if ev.key == K_x:
                p1.shootNuke()
    bg.draw(window)
    p1.update()
    bullets.update()
    missiles.update()
    nukes.update()
    enemies.update()
    enemies2.update()
    enemy_hits_bullet = sprite.groupcollide(bullets, enemies, True, True)
    for hit in enemy_hits_bullet:
        create_enemy()
    enemy_hits_missile = sprite.groupcollide(missiles, enemies2, True, True)
    for hit in enemy_hits_missile:
        create_enemy2()
    enemy_hits_nuke1 = sprite.groupcollide(nukes, enemies2, True, True)
    for hit in enemy_hits_nuke1:
        create_enemy2()
    enemy_hits_nuke2 = sprite.groupcollide(nukes, enemies, True, True)
    for hit in enemy_hits_nuke2:
        create_enemy()
    player_hits = sprite.spritecollide(p1, enemies, True)
    player_hits2 = sprite.spritecollide(p1, enemies2, True)
    p1.draw(window)
    bullets.draw(window)
    missiles.draw(window)
    nukes.draw(window)
    enemies.draw(window)
    enemies2.draw(window)
    for hit in player_hits:
        lives = lives - 1
        lives_counter.update_text('lives = '+ str (lives))
        display.update()
        create_enemy()
        boom_counter = 60
    for hit in player_hits2:
        lives = lives - 1
        lives_counter.update_text('lives = '+ str (lives))
        display.update()
        create_enemy2()
        boom_counter = 60
    lives_counter.draw(window)
    if lives <  1:  
        break
    for hit in enemy_hits_bullet:
        score = score + 1
        score_counter.update_text('score = '+ str (score))
        display.update()
        boom_counter = 60
    boom_counter -=1
    if boom_counter >= 0 and boom_counter <=60:
        boom.draw(window)
    score_counter.draw(window)
    # update the display
    display.update()
    # tick the clock
    clock.tick(60)
if lives < 1:
    window.fill("black")
    lose.draw(window)
    display.update()
    mixer.init()
    mixer.music.load("lose.mp3")
    mixer.music.play()
    time.delay(5000)