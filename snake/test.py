import pygame
import sys
from main import *

pygame.init()
player_width = 30
screen = pygame.display.set_mode((20*player_width, 20*player_width))
clock = pygame.time.Clock()

player = Snake()
food = Food()
player_x_render = [i * player_width for i in player.pos_x]
player_y_render = [i * player_width for i in player.pos_y]

running = True
while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.direction = "left"
    if keys[pygame.K_RIGHT]:
        player.direction = "right"
    if keys[pygame.K_UP]:
        player.direction = "up"
    if keys[pygame.K_DOWN]:
        player.direction = "down"
    player.move()
    if player.pos_y[-1] == food.pos_y and player.pos_x[-1] == food.pos_x:
        player.grow = True
        del food
        food = Food()
    else:
        player.grow = False
    player.tail_pop()

    player_x_render = [i * player_width for i in player.pos_x]
    player_y_render = [i * player_width for i in player.pos_y]

    screen.fill((0, 0, 0)) # Clear screen
    for i in range(len(player_x_render)):
        pygame.draw.rect(screen, (0, 255, 0), (player_x_render[i], player_y_render[i], 30, 30))
    pygame.draw.rect(screen, (255, 0, 0), (food.pos_x * player_width, food.pos_y * player_width, 30, 30))
    pygame.display.flip()

pygame.quit()
sys.exit()

