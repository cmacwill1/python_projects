import pygame
import sys
import random
from supplemental import *

pygame.init()
player_width = 30
map_size = 15

screen = pygame.display.set_mode((map_size*player_width, map_size*player_width))
clock = pygame.time.Clock()
food = Food(random.randint(0,map_size - 1),random.randint(0,map_size - 1))
player = Snake(map_size)
player_render = player_width * player.pos

running = True
while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        if player.direction == "right":
            pass
        else:
            player.direction = "left"
    if keys[pygame.K_RIGHT]:
        if player.direction == "left":
            pass
        else:
            player.direction = "right"
    if keys[pygame.K_UP]:
        if player.direction == "down":
            pass
        else:
            player.direction = "up"
    if keys[pygame.K_DOWN]:
        if player.direction == "up":
            pass
        else:
            player.direction = "down"

    player.move()
    if player.pos[-1][0] > map_size - 1 or player.pos[-1][0] < 0 or player.pos[-1][1] > map_size - 1 or player.pos[-1][1] < 0:
        pygame.quit()
    elif player.maxlen > 4 and (player.pos[-1] == player.pos[0:-2]).all(axis=1).any():
        pygame.quit()
    elif np.array_equal(player.pos[-1], food.pos):
        player.grow = True
        player.maxlen += 1
        del food
        food = Food(random.randint(0,map_size - 1),random.randint(0,map_size - 1))
        print((player.pos[-1] == player.pos[0:-2]).all(axis=1))
    else:
        player.grow = False
    player.tail_pop()

    player_render = player_width * player.pos
    screen.fill((0, 0, 0)) # Clear screen
    for i in range(len(player_render)):
        pygame.draw.rect(screen, (0, 255, 0), (player_render[i][0], player_render[i][1], 30, 30))
    pygame.draw.rect(screen, (255, 0, 0), (food.pos[0] * player_width, food.pos[1] * player_width, 30, 30))
    pygame.display.flip()

pygame.quit()
sys.exit()

