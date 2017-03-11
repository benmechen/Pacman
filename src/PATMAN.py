# -*- coding: utf-8 -*-
# @Author: Ben
# @Date:   2017-03-03 22:23:44
# @Last Modified by:   Ben
# @Last Modified time: 2017-03-11 10:49:28
import pygame
import time
import random
import sys
from collections import Counter
from math import sqrt

class Game:
    def __init__(self):
        self.points = 0

    def check(self, player, ghosts):
        if self.points == 401:
            return False
        for ghost in ghosts:
            if player.rect.x == ghost.rect.x and player.rect.y == ghost.rect.y:
                return False
            elif player.rect.x+10 == ghost.rect.x and player.rect.y+10 == ghost.rect.y:
                return False
            elif player.rect.x-10 == ghost.rect.x and player.rect.y-10 == ghost.rect.y:
                return False
        return True

class Player:
    def __init__(self, size):
        self.rect = pygame.Rect(20, 20, size, size)

    def move(self, dy, dx, teleportcoords):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

        try:
            y = int(self.rect.y/10)
        except:
            y = int(self.rect.y)

        try:
            x = int(self.rect.x/10)
        except:
            x = int(self.rect.x)

        if [x, y] in teleportcoords:
            if teleportcoords.index([x, y]) == 0:
                self.rect.x = (teleportcoords[1][0])*10
                self.rect.y = (teleportcoords[1][1])*10
                playerdirection = 2
            elif teleportcoords.index([x, y]) == 1:
                self.rect.x = (teleportcoords[0][0])*10
                self.rect.y = (teleportcoords[0][1])*10
                playerdirection = 3

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

class Point:
    def __init__(self, pos):
        points.append(pos)

class Ghost:
    def __init__(self, pos):
        ghosts.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 20, 20)
        self.direction = 3
        self.nextdirection = 3
        self.count = 0

    def move(self, dy, dx):
        if dx != 0:
            if self.move_single_axis(dx, 0) == False:
                return False
            else:
                return True
        if dy != 0:
            if self.move_single_axis(0, dy) == False:
                return False
            else:
                return True

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
                return False
        return True

    def chase(self, player, collision):
        print(collision)
        x1 = player.rect.x
        y1 = player.rect.y

        up = down = left = right = 1000000

        #Up
        if "0" not in collision:
            x2 = self.rect.x
            y2 = self.rect.y-10
            up = sqrt(((x2-x1)**2)+((y2-y1)**2))

        #Down
        if "1" not in collision:
            x2 = self.rect.x
            y2 = self.rect.y+10
            down = sqrt(((x2-x1)**2)+((y2-y1)**2))

        #Left
        if "2" not in collision:
            x2 = self.rect.x-10
            y2 = self.rect.y
            left = sqrt(((x2-x1)**2)+((y2-y1)**2))

        #Right
        if "3" not in collision:
            x2 = self.rect.x+10
            y2 = self.rect.y
            right = sqrt(((x2-x1)**2)+((y2-y1)**2))

        distances = [up, down, left, right]
        return distances.index(min(distances))

pygame.init()
pygame.display.set_caption("PATMAN")
screen = pygame.display.set_mode((420, 420))

game = Game()

walls = []
points = []
ghosts = []
size = 20
player = Player(size)

level = open("map.txt")

x = y = 0
teleportcoords = []

xcount = ycount = 0

for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        elif col == "T":
            teleportcoords.append([xcount, ycount])
        elif col == "P":
            Point((x, y))
        elif col == "G":
            Ghost((x, y))
        x += 10
        xcount += 1
    xcount = 0
    y += 10
    x = 0
    ycount += 1

running = True

# 0 = up, 1 = down, 2 = left, 3 = right
global playerdirection
playerdirection = 3

patman_closed = pygame.image.load('patman.png')
patman_closed = pygame.transform.scale(patman_closed, (size, size))
patman_closed_flipped = pygame.transform.flip(patman_closed, True, False)

patman_open = pygame.image.load('patman_open.png')
patman_open = pygame.transform.scale(patman_open, (size, size))
patman_open_flipped = pygame.transform.flip(patman_open, True, False)

ghost_image_1 = pygame.image.load('ghost1.png')
ghost_image_1 = pygame.transform.scale(ghost_image_1, (size, size))
ghost_image_2 = pygame.image.load('ghost2.png')
ghost_image_2 = pygame.transform.scale(ghost_image_2, (size, size))
ghost_image_3 = pygame.image.load('ghost3.png')
ghost_image_3 = pygame.transform.scale(ghost_image_3, (size, size))
ghost_image_4 = pygame.image.load('ghost4.png')
ghost_image_4 = pygame.transform.scale(ghost_image_4, (size, size))

mouth_open = False
flipped = False
blocked = [False, False, False, False]

scoreText = pygame.font.SysFont("monospace", 15)

previousdirection = {0: [-1, -1], 1: [-1, -1], 2: [-1, -1], 3: [-1, -1]}

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
            running = False

    key = pygame.key.get_pressed()

    if key[pygame.K_ESCAPE]:
        pygame.display.quit()
        pygame.quit()
        sys.exit()
        running = False

    if key[pygame.K_UP]:
        player.rect.y += -10
        for wall in walls:
            if player.rect.colliderect(wall.rect):
                newplayerdirection = playerdirection
                break
            else:
                newplayerdirection = 0

        playerdirection = newplayerdirection
        player.rect.y += +10

    if key[pygame.K_DOWN]:
        player.rect.y += +10
        for wall in walls:
            if player.rect.colliderect(wall.rect):
                newplayerdirection = playerdirection
                break
            else:
                newplayerdirection = 1

        playerdirection = newplayerdirection
        player.rect.y += -10

    if key[pygame.K_LEFT]:
        player.rect.x += -10
        for wall in walls:
            if player.rect.colliderect(wall.rect):
                newplayerdirection = playerdirection
                break
            else:
                newplayerdirection = 2

        playerdirection = newplayerdirection
        player.rect.x += +10

    if key[pygame.K_RIGHT]:
        player.rect.x += +10
        for wall in walls:
            if player.rect.colliderect(wall.rect):
                newplayerdirection = playerdirection
                break
            else:
                newplayerdirection = 3

        playerdirection = newplayerdirection
        player.rect.x += -10

    if playerdirection == 0:
        player.move(-10, 0, teleportcoords)
    if playerdirection == 1:
        player.move(10, 0, teleportcoords)
    if playerdirection == 2:
        flipped = True
        player.move(0, -10, teleportcoords)
    if playerdirection == 3:
        flipped = False
        player.move(0, 10, teleportcoords)

    occured = []
    ghostnum = 0
    for ghost in ghosts:
        blockeddirections = []
        if ghost.rect.center in occured:
            ghost.direction = random.randrange(0, 4)
            if ghost.direction == 0:
                if ghost.move(-10, 0):
                    break
                # print("Can't go up")
                blockeddirections.append(ghost.direction)
                ghost.direction = ghost.chase(player, blockeddirections)
            if ghost.direction == 2:
                if ghost.move(0, -10):
                    break
                # print("Can't go left")
                blockeddirections.append(ghost.direction)
                ghost.direction = ghost.chase(player, blockeddirections)
            if ghost.direction == 3:
                if ghost.move(0, 10):
                    break
                # print("Can't go right")
                blockeddirections.append(ghost.direction)
                ghost.direction = ghost.chase(player, blockeddirections)
            if ghost.direction == 1:
                if ghost.move(10, 0):
                    break
                # print("Can't go down")
                blockeddirections.append(ghost.direction)
                ghost.direction = ghost.chase(player, blockeddirections)
        occured.append(ghost.rect.center)

        ghost.direction = ghost.chase(player, blockeddirections)
        while True:
            if ghost.direction == 0:
                if ghost.move(-10, 0):
                    break
                # print("Can't go up")
                blockeddirections.append(str(ghost.direction))
                ghost.direction = ghost.chase(player, blockeddirections)
                # print(ghost.direction)
            if ghost.direction == 1:
                if ghost.move(10, 0):
                    break
                # print("Can't go down")
                blockeddirections.append(str(ghost.direction))
                ghost.direction = ghost.chase(player, blockeddirections)
            if ghost.direction == 2:
                if ghost.move(0, -10):
                    break
                # print("Can't go left")
                blockeddirections.append(str(ghost.direction))
                ghost.direction = ghost.chase(player, blockeddirections)
            if ghost.direction == 3:
                if ghost.move(0, 10):
                    break
                # print("Can't go right")
                blockeddirections.append(str(ghost.direction))
                ghost.direction = ghost.chase(player, blockeddirections)
        ghostnum += 1
    running = game.check(player, ghosts)

    screen.fill((0,0,0))
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 255), wall.rect)

    i = 0

    for point in points:
        if player.rect.x == point[0]-10 and player.rect.y == point[1]-10:
            points.pop(i)
            game.points += 1
        else:
            pygame.draw.circle(screen, (255, 255, 255), point, 2)
        i += 1

    i = 1
    for ghost in ghosts:
        if i == 1:
            screen.blit(ghost_image_1, ghost.rect)
        if i == 2:
            screen.blit(ghost_image_2, ghost.rect)
        if i == 3:
            screen.blit(ghost_image_3, ghost.rect)
        if i == 4:
            screen.blit(ghost_image_4, ghost.rect)
        i += 1

    labelScore = scoreText.render("Score: " + str(game.points), 1, (0,0,0))
    screen.blit(labelScore, (0, -4))

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

    time.sleep(0.075)
exec(open("PATMAN.py").read())