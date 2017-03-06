# -*- coding: utf-8 -*-
# @Author: Ben
# @Date:   2017-03-03 22:23:44
# @Last Modified by:   Ben
# @Last Modified time: 2017-03-05 22:30:00
import pygame
import time

class Player:
    def __init__(self, size):
        self.rect = pygame.Rect(20, 20, size, size)

    def move(self, dy, dx):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom

class Wall:
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 10, 10)

pygame.init()
pygame.display.set_caption("PATMAN")
screen = pygame.display.set_mode((420, 420))

walls = []
size = 20
player = Player(size)

level = open("map.txt")



x = y = 0

for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        x += 10
    y += 10
    x = 0

running = True

# 0 = up, 1 = down, 2 = left, 3 = right
direction = 3

patman_closed = pygame.image.load('patman.png')
patman_closed = pygame.transform.scale(patman_closed, (size, size))
patman_closed_flipped = pygame.transform.flip(patman_closed, True, False)

patman_open = pygame.image.load('patman_open.png')
patman_open = pygame.transform.scale(patman_open, (size, size))
patman_open_flipped = pygame.transform.flip(patman_open, True, False)

mouth_open = False
flipped = False

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
##        print(player.rect.y, walls[player.rect.y].rect.y)
##        print(walls[player.rect[0]].rect[1])
        print(walls[player.rect.y].rect.y)
        print(player.rect.y)
        if player.rect.y+10 != walls[player.rect.y].rect.y:
##        print(walls[player.rect.x].rect)
##        print(player.rect)
            direction = 0
        if player.rect.y+10 in walls:
            direction = 0
    if key[pygame.K_DOWN]:
        if player.rect.y-10 != walls[player.rect.x].rect.y:
            direction = 1
    if key[pygame.K_LEFT]:
        if player.rect.x-10 != walls[player.rect.x].rect.x:
            direction = 2
    if key[pygame.K_RIGHT]:
        if player.rect.x+10 != walls[player.rect.x].rect.x:
            direction = 3

    if direction == 0:
        player.move(-10, 0)
    if direction == 1:
        player.move(10, 0)
    if direction == 2:
        flipped = True
        player.move(0, -10)
    if direction == 3:
        flipped = False
        player.move(0, 10)

    ##print(player.rect.x, player.rect.y)

    screen.fill((0,0,0))
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 255), wall.rect)
    # pygame.draw.rect(screen, (255, 200, 0), player.rect)
    if mouth_open:
        if flipped == True:
            screen.blit(patman_open_flipped, player.rect)
        else:
            screen.blit(patman_open, player.rect)
        mouth_open = False
    else:
        if flipped == True:
            screen.blit(patman_closed_flipped, player.rect)
        else:
            screen.blit(patman_closed, player.rect)
        mouth_open = True
    pygame.display.flip()

    time.sleep(0.15)