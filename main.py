import math
import random
import time
import pygame
from pygame import mixer

#Credit to attreyabhatt for the base space invaders code
# https://github.com/attreyabhatt/Space-Invaders-Pygame

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Score
score_value = 0

font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Elites
elitesImg = []
elitesX = []
elitesY = []
elitesX_change = []
elitesY_change = []
elites_current_hits = []

num_of_elites = 0

#Boss
bossImg = []
bossX = []
bossY = []
bossX_change = []
bossY_change = []
boss_current_hits = []

num_of_boss = 0


# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

upgraded_bulletImg = pygame.image.load('bullet.png')
upgraded_bullet2Img = pygame.image.load('bullet.png')
upgraded_bullet3Img = pygame.image.load('bullet.png')
upgraded_bulletX = 0
upgraded_bullet2X = 0
upgraded_bullet3X = 0
upgraded_bulletY = 480
upgraded_bullet2Y = 480
upgraded_bullet3Y = 480
upgraded_bulletX_change = 0
upgraded_bullet2X_change = 0
upgraded_bullet3X_change = 0
upgraded_bulletY_change = 10
upgraded_bullet2Y_change = 10
upgraded_bullet3Y_change = 10



# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Victroy
victory_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def victory_text():
    for j in range(num_of_enemies):
        enemyX_change[j] = 0
    for j in range(num_of_elites):
        elitesX_change[j] = 0
    for j in range(num_of_boss):
        bossX_change[j] = 0
    vic_text = victory_font.render("YOU WIN", True, (255, 255, 255))
    screen.blit(vic_text, (200, 250))
    

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def elites(x, y, i):
    screen.blit(elitesImg[i], (x, y))

def boss(x, y, i):
    screen.blit(bossImg[i], (x, y))

def spawnElites():
    global num_of_elites
    num_of_elites+=1
   
    elitesImg.append(pygame.image.load('elites.png'))
    elitesX.append(random.randint(0, 736))
    elitesY.append(random.randint(50, 150))
    elitesX_change.append(4)
    elitesY_change.append(40)
    elites_current_hits.append(0)

def spawnBoss():
    global num_of_boss
    num_of_boss+=1
   
    bossImg.append(pygame.image.load('boss.png'))
    bossX.append(random.randint(0, 736))
    bossY.append(random.randint(50, 150))
    bossX_change.append(4)
    bossY_change.append(40)
    boss_current_hits.append(0)


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if (distance < 27):
        return True
    else:
        return False
   

def isCollision2(enemyX, enemyY, upgraded_bullet2X, upgraded_bullet2Y):
    distance2 = math.sqrt(math.pow(enemyX - (upgraded_bullet2X - 16), 2) + (math.pow(enemyY - (upgraded_bullet2Y + 25), 2)))
    if (distance2 < 27):
        return True
    else:
        return False

def isCollision3(enemyX, enemyY, upgraded_bullet3X, upgraded_bullet3Y):
    distance3 = math.sqrt(math.pow(enemyX - (upgraded_bullet3X + 48), 2) + (math.pow(enemyY - (upgraded_bullet3Y + 25), 2)))
    if (distance3 < 27):
        return True
    else:
        return False
    

bullet_upgrade = False

def upgrade():
    global bullet_upgrade
    bullet_upgrade = True



def message_display(x, y):
    score = font.render("Weapon Upgrade!", True, (255, 255, 255))
    screen.blit(score, (x, y))

def multi_bullet(x, y, x2, y2, x3, y3):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    screen.blit(upgraded_bullet2Img, (x2 - 16, y2 + 25))
    screen.blit(upgraded_bullet3Img, (x3 + 48, y3 + 25))

# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    upgraded_bullet2X = playerX
                    upgraded_bullet3X = playerX
                    
                    if bullet_upgrade == True:
                        multi_bullet(bulletX, bulletY, upgraded_bullet2X, upgraded_bullet2Y, upgraded_bullet3X, upgraded_bullet3Y)
                    else:    
                        fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            if score_value < 5:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif score_value < 10:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif score_value >= 10:
                enemyX_change[i] = 6
                enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            if score_value < 5:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]
            elif score_value < 10:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]
            elif score_value >= 10:
                enemyX_change[i] = -6
                enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            upgraded_bullet2Y = 480
            upgraded_bullet3Y = 480
            bullet_state = "ready"
            score_value += 1
            
            if score_value == 5:
                spawnElites()
                
            elif score_value == 10:
                spawnElites()
            
            elif score_value == 12:
                upgrade()

            elif score_value == 15:
                spawnBoss()
            
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

        collision2 = isCollision2(enemyX[i], enemyY[i], upgraded_bullet2X, upgraded_bullet2Y)
        if collision2:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            upgraded_bullet2Y = 480
            upgraded_bullet3Y = 480
            bullet_state = "ready"
            score_value += 1
            
            if score_value == 5:
                spawnElites()
                
            elif score_value == 10:
                spawnElites()
            
            elif score_value == 12:
                upgrade()

            elif score_value == 15:
                spawnBoss()
            
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

        collision3 = isCollision3(enemyX[i], enemyY[i], upgraded_bullet3X, upgraded_bullet3Y)
        if collision3:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            upgraded_bullet2Y = 480
            upgraded_bullet3Y = 480
            bullet_state = "ready"
            score_value += 1
            
            if score_value == 5:
                spawnElites()
                
            elif score_value == 10:
                spawnElites()
            
            elif score_value == 12:
                upgrade()

            elif score_value == 15:
                spawnBoss()
            
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # elites Movement
    for i in range(num_of_elites):

        # Game Over
        if elitesY[i] > 440:
            for j in range(num_of_elites):
                elitesY[j] = 2000
                
            game_over_text()
            break

        elitesX[i] += elitesX_change[i]
        if elitesX[i] <= 0:
            elitesX_change[i] = 4
            elitesY[i] += elitesY_change[i]
        elif elitesX[i] >= 736:
            elitesX_change[i] = -4
            elitesY[i] += elitesY_change[i]

        # Collision
        collision = isCollision(elitesX[i], elitesY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            upgraded_bullet2Y = 480
            upgraded_bullet3Y = 480
            bullet_state = "ready"
            elites_current_hits[i] += 1
            print(elites_current_hits)
            if elites_current_hits[i] == 2:
                elites_current_hits[i] = 0
                score_value += 1
                elitesX[i] = random.randint(0, 736)
                elitesY[i] = random.randint(50, 150)
                if score_value == 5:
                    spawnElites()
                
                elif score_value == 10:
                    spawnElites()
            
                elif score_value == 12:
                    upgrade()

                elif score_value == 15:
                    spawnBoss()
            
        elites(elitesX[i], elitesY[i], i)

        collision2 = isCollision2(elitesX[i], elitesY[i], upgraded_bullet2X, upgraded_bullet2Y)
        if collision2:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            upgraded_bullet2Y = 480
            upgraded_bullet3Y = 480
            bullet_state = "ready"
            elites_current_hits[i] += 1
            print(elites_current_hits)
            if elites_current_hits[i] == 2:
                elites_current_hits[i] = 0
                score_value += 1
                elitesX[i] = random.randint(0, 736)
                elitesY[i] = random.randint(50, 150)
            
            if score_value == 5:
                spawnElites()
                
            elif score_value == 10:
                spawnElites()
            
            elif score_value == 12:
                upgrade()

            elif score_value == 15:
                spawnBoss()
            
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        elites(elitesX[i], elitesY[i], i)

        collision3 = isCollision3(elitesX[i], elitesY[i], upgraded_bullet3X, upgraded_bullet3Y)
        if collision3:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            upgraded_bullet2Y = 480
            upgraded_bullet3Y = 480
            bullet_state = "ready"
            elites_current_hits[i] += 1
            print(elites_current_hits)
            if elites_current_hits[i] == 2:
                elites_current_hits[i] = 0
                score_value += 1
                elitesX[i] = random.randint(0, 736)
                elitesY[i] = random.randint(50, 150)
            
            if score_value == 5:
                spawnElites()
                
            elif score_value == 10:
                spawnElites()
            
            elif score_value == 12:
                upgrade()

            elif score_value == 15:
                spawnBoss()
            
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        elites(elitesX[i], elitesY[i], i)

    # boss Movement
    for i in range(num_of_boss):

        # Game Over
        if bossY[i] > 440:
            for j in range(num_of_boss):
                bossY[j] = 2000
                
            game_over_text()
            break

        bossX[i] += bossX_change[i]
        if bossX[i] <= 0:
            bossX_change[i] = 4
            bossY[i] += bossY_change[i]
        elif bossX[i] >= 736:
            bossX_change[i] = -4
            bossY[i] += bossY_change[i]

        # Collision
        collision = isCollision(bossX[i], bossY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            upgraded_bullet2Y = 480
            upgraded_bullet3Y = 480
            bullet_state = "ready"
            boss_current_hits[i] += 1
            print(boss_current_hits)
            
            if boss_current_hits[i] == 5:
                victory_text()
                
                break                
                
            
        boss(bossX[i], bossY[i], i)

        collision2 = isCollision2(bossX[i], bossY[i], upgraded_bullet2X, upgraded_bullet2Y)
        if collision2:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            upgraded_bullet2Y = 480
            upgraded_bullet3Y = 480
            bullet_state = "ready"
            boss_current_hits[i] += 1
            print(boss_current_hits)
            if boss_current_hits[i] == 5:
                victory_text()
                break

            
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        boss(bossX[i], bossY[i], i)

        collision3 = isCollision3(bossX[i], bossY[i], upgraded_bullet3X, upgraded_bullet3Y)
        if collision3:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            upgraded_bullet2Y = 480
            upgraded_bullet3Y = 480
            bullet_state = "ready"
            boss_current_hits[i] += 1
            print(boss_current_hits)
            if boss_current_hits[i] == 5:
                victory_text()
                break

            
            

        boss(bossX[i], bossY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        upgraded_bullet2Y = 480
        upgraded_bullet3Y = 480
        bullet_state = "ready"

        

    if bullet_state is "fire":
        if bullet_upgrade == True:
            multi_bullet(bulletX, bulletY, upgraded_bullet2X, upgraded_bullet2Y, upgraded_bullet3X, upgraded_bullet3Y)
            bulletY -= bulletY_change
            upgraded_bullet2Y -= upgraded_bullet2Y_change
            upgraded_bullet3Y -= upgraded_bullet3Y_change
        else:   
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
