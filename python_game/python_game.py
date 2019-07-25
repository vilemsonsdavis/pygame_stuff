import pygame
import random 
pygame.init()

screenWidth = 500
screenHeight = 480

win = pygame.display.set_mode((screenWidth, screenHeight)) #sets display size

pygame.display.set_caption("Villy vs Aliens")

#loading all images
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('bullet.wav')
hitSound = pygame.mixer.Sound('hit.wav')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1) #play music without stopping

score = 0

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x +17, self.y+11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount//3],(self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3],(self.x, self.y))
                self.walkCount += 1
        else :
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))# 80 220 370

        self.hitbox = (self.x +17, self.y+11, 29, 52) # 0 -80 120-220 260-370 410 - 436

    def dontDrawOnGoblin(self):
        goblinsX = []
        possible_coord = []
        for goblin in goblins:
            goblinsX.append(goblin.x)

        goblinsX.sort()
        
        for i in range(len(goblinsX)): #to draw in range where arent goblin
            if i == 0:
                if goblinsX[i] > 40:
                    possible_coord.append([0, goblinsX[0]])
            elif i == 3:
                if screenWidth - 64 > goblinsX[2]+40:
                    possible_coord.append([goblinsX[2]+40, screenWidth-64])
            elif ((goblinsX[i] - 20) - (goblinsX[i-1]+40)) >= 40:
                possible_coord.append([goblinsX[i-1]+40, goblinsX[i]-20])

        random_range = random.choice(possible_coord)
        randomX = random.randrange(random_range[0], random_range[1])

        return randomX
    
    def hit(self):

        self.isJump = False
        self.jumpCount = 10 # fixes bug for displaying char under app after hit when jumping
        self.x = self.dontDrawOnGoblin()
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (screenWidth/2 - text.get_width()/2, screenHeight/2 - text.get_height()/2))
        pygame.display.update()
        i = 0
        while i < 50:
            pygame.time.delay(10) # it holds for 0.01 sec the game
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()



class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing

        if self.facing == -1:
            self.vel = -8
        else:
            self.vel = 8

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = vel * 3
        self.hitbox = (self.x +17, self.y +2, 31, 57)
        self.health = 10
        self.visible = True


    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3],(self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3],(self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0] - 10, self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,255,0), (self.hitbox[0] - 10, self.hitbox[1] - 20, 5 * self.health, 10))
    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else :
            if self.x - self.vel > 0:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0

        self.hitbox = (self.x +17, self.y +2, 31, 57)
        
    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
            goblins.pop(goblins.index(self))



def makeGoblin():
    x = random.randrange(10, 450)
    vel = random.choice([-1, 1])
    goblins.append(enemy(x, 410, 64, 64, 450, vel))

def redrawGameWindow():
    win.blit(bg, (0,0)) #fill background with bg pic
    text = font.render('Score: ' + str(score), 1, (255, 0, 0))
    win.blit(text, (380, 10))
    villy.draw(win)
    for goblin in goblins:
        goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update() #refresh display    

#main loop
font = pygame.font.SysFont('comicsans', 30, True) #font, size, bold(true), italic 
villy = player(300, 410, 64, 64)
goblins = []
makeGoblin()
makeGoblin()
makeGoblin()
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27) #setting 27fps

    for goblin in goblins:
        if villy.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and villy.hitbox[1] + villy.hitbox[3] > goblin.hitbox[1]:
            if villy.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2] and villy.hitbox[0] + villy.hitbox[2] > goblin.hitbox[0]:
                villy.hit()
                score -= 5

    if shootLoop > 0: #we can shoot only when shotloop is 0, so it basically works like cooldown while it will run through whil and be >3
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get(): # gets a list of all movements thats happens - keyboard or mouse or whatever
        if event.type == pygame.QUIT: # red X button
            run = False

    for bullet in bullets:
        for goblin in goblins:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2] and bullet.x + bullet.radius > goblin.hitbox[0]:
                    hitSound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet)) #TODO - check what happens when hitting bullet into 2 goblins, some error happens
            
        if bullet.x < screenWidth and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet)) #finds the index of current bullet and pops it out of a list
    
    keys = pygame.key.get_pressed() #get all keys which pressed

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play() #to play sound
        if villy.right:
            facing = 1
        else:
            facing = -1
        if len(bullets) < 5:
            bullets.append(projectile(round(villy.x + villy.width //2), round(villy.y + villy.height //2), 6, (0,0,0), facing)) # creating new bullet, rounding for better drawing with only ints

        shootLoop = 1

    if keys[pygame.K_LEFT] and villy.x > 0: #access left arrow key when pressed
        villy.x -= villy.vel
        villy.left = True
        villy.right = False
        villy.standing = False
    elif keys[pygame.K_RIGHT] and villy.x < screenWidth - villy.width:
        villy.x += villy.vel
        villy.left = False
        villy.right = True
        villy.standing = False
    else:
        villy.standing = True
        villy.walkCount = 0

    if not(villy.isJump): # in if statement cause not allowing to move down or up while jumping
        if keys[pygame.K_UP]:
            villy.isJump = True
            villy.left = False
            villy.right = False 
            villy.walkCount = 0
    else:
        if villy.jumpCount >= -10:
            neg = 1
            if villy.jumpCount < 0:
                neg = -1
            villy.y -= (villy.jumpCount ** 2) * 0.5 * neg
            villy.jumpCount -= 1
        else:
            villy.isJump = False
            villy.jumpCount = 10

    redrawGameWindow()

pygame.quit() #quits game without any error
    
