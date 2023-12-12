import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
playerSize = 40
playerSpeed = 5
jumpSpeed = 10
gravity = 0.5
score = 0

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump game")
clock = pygame.time.Clock()

player = pygame.Rect(30, HEIGHT - playerSize * 2, playerSize, playerSize)
playerSpeedY = 0
on_ground = False
playerImage = pygame.image.load('mario.png').convert_alpha()
playerImage = pygame.transform.scale(playerImage, (playerSize, playerSize))

background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

fallingObject = pygame.Rect(HEIGHT - 40, 0, 20, 20)
fallingSpeed = 5
fallingGravity = 0.05
fallingObjectImage = pygame.image.load('bomb.png').convert_alpha()
fallingObjectImage = pygame.transform.scale(fallingObjectImage, (30, 30))

coin = pygame.Rect(random.randint(0, WIDTH - 20), 250, 20, 20)
coinSpeed = 5
coinImage = pygame.image.load('coin.png').convert_alpha()
coinImage = pygame.transform.scale(coinImage, (30, 30))

pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.Font(None, 36)

running = True
collision = False

while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.USEREVENT:
            print("Score: ", score)

    scoreText = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(scoreText, (10, 10))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x - playerSpeed > 0:
        player.x -= playerSpeed
    if keys[pygame.K_RIGHT] and player.x + playerSpeed < WIDTH - playerSize:
        player.x += playerSpeed

    if not on_ground:
        player.y += playerSpeedY
        playerSpeedY += gravity

        if player.y >= HEIGHT - playerSize * 2:
            on_ground = True
            player.y = HEIGHT - playerSize * 2
            playerSpeedY = 0
    else:
        if keys[pygame.K_SPACE]:
            on_ground = False
            playerSpeedY = -jumpSpeed

    screen.blit(playerImage, (player.x, player.y))
    screen.blit(fallingObjectImage, (fallingObject.x, fallingObject.y))
    screen.blit(coinImage, (coin.x, coin.y))

    fallingObject.y += fallingSpeed
    fallingSpeed += fallingGravity

    if not collision:
        score += 1

    if player.colliderect(fallingObject):
        collision = True

    if collision:
        playerSpeed = 0
        fallingSpeed = 0
        text = font.render('Press SPACE to restart', True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        if keys[pygame.K_SPACE]:
            player.x = 30
            player.y = HEIGHT - playerSize * 2
            fallingObject.y = 0
            fallingObject.x = random.randint(0, WIDTH - 20)
            score = 0
            collision = False
            playerSpeedY = 0
            playerSpeed = 5

    if fallingObject.y > HEIGHT:
        fallingObject.y = 0
        fallingObject.x = random.randint(0, WIDTH - 20)
        fallingSpeed = 5

        if score >= 500:
            fallingSpeed = 8
        if score >= 800:
            fallingSpeed = 10
        if score >= 1100:
            fallingSpeed = 13
        if score >= 1600:
            fallingSpeed = 16

    if player.colliderect(coin):
        coin.y = random.randint(max(HEIGHT // 2, HEIGHT - 100), HEIGHT - coin.height)
        coin.x = random.randint(0, WIDTH - coin.width)
        score += 100
    while coin.y < HEIGHT // 2 or coin.y > HEIGHT - 70:
        coin.y = random.randint(HEIGHT // 2, HEIGHT - 70)

    pygame.display.flip()
    clock.tick(60)
