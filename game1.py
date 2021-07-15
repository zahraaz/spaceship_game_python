#my space ship first moving game 🥳🤩🌺🌈🌸
import pygame
import random
import math
from pygame import mixer
#intilize the pygame
pygame.init()

#create the screen
screen=pygame.display.set_mode((1000,550))

#background 
background = pygame.image.load('bd.png')

#background sound 
mixer.music.load('background.wav')
mixer.music.play(-1)
#title and icon
pygame.display.set_caption("Space shooter")
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = [] 
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('plt.png'))
    enemyX.append(random.randint(0,935))
    enemyY.append(random.randint(50,250))
    enemyX_change.append(2)
    enemyY_change.append(40)

#ready - you can not see the bullet on the screen 
# fire - the bullet is currently moving 
#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render(" score :"+str(score_value), True , (255,255,255))
    screen.blit(score, (x,y))

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16,y + 10))


def game_over():
    over_end = over_font.render("GAME END ", True , (255,255,255))
    screen.blit(over_end, (400,240))

def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+ (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#game loop
running = True
while running:
    #RGB red,green,blue
    screen.fill((50,50,50))
    #background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if keystroke is pressed check whether is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletsound = mixer.Sound("laser.wav")
                    bulletsound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    
    if playerX <=0:
        playerX = 0
    elif playerX >= 936:
        playerX = 936

#enemy movement 
    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 340:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
           enemyX_change[i] = 2
           enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 936:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        
        #collision
        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,935)
            enemyY[i] = random.randint(50,250)

        enemy(enemyX[i], enemyY[i], i)


#bullet movement 
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    player(playerX,playerY)
    show_score(textX, textY)
    pygame.display.update()
