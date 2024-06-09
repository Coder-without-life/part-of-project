from pygame import *
window = display.set_mode((1250,900))
display.set_caption('labirint')
cyan = (60,228,255)
DARK_COLOR = (25,0,25)
win = transform.scale(image.load('winner.jpg'), (1250, 900))
loose = transform.scale(image.load('dislike.jpg'), (1250, 900))

class GameSpirite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image=transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSpirite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x ,y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        if self.x_speed > 0 and self.rect.x < 1250-110 or self.x_speed < 0 and self.rect.x > 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if self.y_speed > 0 and self.rect.y < 900-150 or self.y_speed < 0 and self.rect.y > 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSpirite):
    def __init__(self, picture, w, h, x, y, speed):
        GameSpirite.__init__(self, picture, w, h, x, y)
        self.speed = speed
        self.direction = 'left'
    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        if self.rect.x <= 600:
            self.direction = 'right'
        if self.rect.x >= 1150:
            self.direction = 'left'

class Bullet(GameSpirite):
    def __init__(self, picture, x, y, w, h, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 1250:
            self.kill()

wall_1 = GameSpirite('bigwall.jpg', 70, 800, 200, 200)
wall_2 = GameSpirite('bigwall.jpg',70, 650, 500, 0)
wall_3 = GameSpirite('bigwall.jpg', 70, 800, 800, 200)

barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)
barriers.add(wall_3)

bullets = sprite.Group()

final_sprite = GameSpirite('thanos.jpg', 200, 250, 950, 600)
enemy_sprite = Enemy('enemy.png', 100, 200, 600, 0, 3)
player = Player('superman.jpg', 110, 150, 30, 70, 0, 0)  

monsters = sprite.Group()
monsters.add(enemy_sprite)

players = sprite.Group()
players.add(player)

run = True
finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                player.y_speed = -5
            elif e.key == K_s:
                player.y_speed = 5
            elif e.key == K_a:
                player.x_speed = -5
            elif e.key == K_d:
                player.x_speed = 5
            elif e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key == K_w:
                player.y_speed = 0
            elif e.key == K_s:
                player.y_speed = 0
            elif e.key == K_a:
                player.x_speed = 0
            elif e.key == K_d:
                player.x_speed = 0

    if finish != True:
        window.fill(cyan)
        barriers.draw(window)
        bullets.draw(window)
        player.reset()
        final_sprite.reset()
        sprite.groupcollide(bullets, barriers, True, False)
        monsters.draw(window)
        sprite.groupcollide(bullets, monsters, True, True)
        monsters.update()
        bullets.update()
        time.delay(50)
        if sprite.collide_rect(player, final_sprite):
            finish = True
            window.fill(DARK_COLOR) 
            window.blit(win, (0,0))
        elif sprite.groupcollide(players, monsters, True, True):
            finish = True
            window.fill(DARK_COLOR)
            window.blit(loose, (0,0))


    player.update()
    display.update()
#игра готова