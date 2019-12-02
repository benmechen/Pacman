# -*- coding: utf-8 -*-
# @Author: Ben
# @Date:   2017-03-03 22:23:44
# @Last Modified by:   Ben
# @Last Modified time: 2017-11-02 12:50:35
# /Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 PATMAN.py

import os
import pygame
import time
import random
import sys
from math import sqrt
import operator
import pickle

class Game:
    def __init__(self):
        self.points = 0
        self.previouspoints = 0

    def check(self, player, ghost):
        if sqrt((ghost.rect.x - player.rect.x) ** 2 + (ghost.rect.y - player.rect.y) ** 2) <= 10:
            return False
        return True

class Queue():
    def __init__(self, maxsize):
        self.queue = []
        self.start = 0
        self.end = -1
        self.maxsize = maxsize

    def isEmpty(self):
        len = self.end - self.start
        if len < 0:
            return True
        return False

    def isFull(self):
        len = self.end - self.start
        if len+1 == self.maxsize:
            return True
        return False

    def enqueue(self, item):
        if self.isFull() == True:
            self.dequeue()
        self.end += 1
        self.queue.insert(self.end, item)

    def dequeue(self):
        if self.isEmpty() != True:
            self.end -= 1
            return self.queue.pop(self.start)
        else:
            return False

class Ghost:
    def __init__(self, pos):
        ghosts.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 20, 20)
        self.direction = 3
        self.previouscoordinates = Queue(4)
        self.count = 0
        self.scared = False
        self.scaredCount = 0
        self.previousPath = []
        self.teleporting = False
        self.teleportcoords = []

    def move(self, dy, dx):
        if dx != 0:
            if self.move_single_axis(dx, 0) == False:
                return False
        if dy != 0:
            if self.move_single_axis(0, dy) == False:
                return False
        self.previouscoordinates.enqueue([self.rect.x, self.rect.y])
        if [self.rect.x, self.rect.y] in self.teleportcoords:
            if self.teleportcoords.index([self.rect.x, self.rect.y]) == 0:
                if self.direction != 3:
                    self.rect.x = self.teleportcoords[1][0]+200
                    self.rect.y = self.teleportcoords[1][1]
                    self.direction = 2
                    self.teleporting = True
                else:
                    self.teleporting = False
            elif self.teleportcoords.index([self.rect.x, self.rect.y]) == 1:
                if self.direction != 2:
                    self.rect.x = self.teleportcoords[0][0]-200
                    self.rect.y = self.teleportcoords[0][1]
                    self.direction = 3
                    self.teleporting = True
                else:
                    self.teleporting = False

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
        x1 = player.rect.x
        y1 = player.rect.y

        if self.scared:
            up = down = left = right = 0
        else:
            up = down = left = right = 1000000

        #Up
        if "0" not in collision:
            x2 = self.rect.x
            y2 = self.rect.y-10
            coordinates = [x2, y2]
            # print(coordinates)
            if False:
                return 0
            else:
                if coordinates not in self.previouscoordinates.queue:
                    up = abs( x2 - x1 ) + abs( y2 - y1 )
                else:
                    if self.scared:
                        up = 0
                    else:
                        up = 1000000


        #Down
        if "1" not in collision:
            x2 = self.rect.x
            y2 = self.rect.y+10
            coordinates = [x2, y2]
            if False:
                return 0
            else:
                if coordinates not in self.previouscoordinates.queue:
                    down = abs( x2 - x1 ) + abs( y2 - y1 )
                else:
                    if self.scared:
                        down = 0
                    else:
                        down = 1000000

        #Left
        if "2" not in collision:
            x2 = self.rect.x-10
            y2 = self.rect.y
            coordinates = [x2, y2]
            if False:
                return 0
            else:
                if coordinates not in self.previouscoordinates.queue:
                    left = abs( x2 - x1 ) + abs( y2 - y1 )
                else:
                    if self.scared:
                        left = 0
                    else:
                        left = 1000000

        #Right
        if "3" not in collision:
            x2 = self.rect.x+10
            y2 = self.rect.y
            coordinates = [x2, y2]
            if False:
                return 0
            else:
                if coordinates not in self.previouscoordinates.queue:
                    right = abs( x2 - x1 ) + abs( y2 - y1 )
                else:
                    if self.scared:
                        right = 0
                    else:
                        right = 1000000

        distances = [up, down, left, right]
        while str(distances.index(min(distances))) in collision:
            distances[distances.index(min(distances))] = 1000000000
        if not self.teleporting:
            return distances.index(min(distances))
        else:
            return self.direction

    def retreat(self, corner, player, blockeddirections):
        if corner == 1:
            x = player.rect.x
            y = player.rect.y
            player.rect.x = 40
            player.rect.y = 30
            self.direction = self.chase(player, blockeddirections)
            player.rect.x = x
            player.rect.y = y
        if corner == 2:
            x = player.rect.x
            y = player.rect.y
            player.rect.x = 390
            player.rect.y = 30
            self.direction = self.chase(player, blockeddirections)
            player.rect.x = x
            player.rect.y = y
        if corner == 3:
            x = player.rect.x
            y = player.rect.y
            player.rect.x = 50
            player.rect.y = 390
            self.direction = self.chase(player, blockeddirections)
            player.rect.x = x
            player.rect.y = y
        if corner == 4:
            x = player.rect.x
            y = player.rect.y
            player.rect.x = 370
            player.rect.y = 390
            self.direction = self.chase(player, blockeddirections)
            player.rect.x = x
            player.rect.y = y


class Player:
    def __init__(self, size):
        self.rect = pygame.Rect(20, 20, size, size)
        self.previouscoordinates = (self.rect.x, self.rect.y)
        self.direction = 3

    def move(self, dy, dx, teleportcoords):
        if dx != 0:
            if self.move_single_axis(dx, 0) == False:
                return False
        if dy != 0:
            if self.move_single_axis(0, dy) == False:
                return False

        if [self.rect.x, self.rect.y] in teleportcoords:
            if teleportcoords.index([self.rect.x, self.rect.y]) == 0:
                self.rect.x = teleportcoords[1][0]-10
                self.rect.y = teleportcoords[1][1]
                self.direction = 2
            elif teleportcoords.index([self.rect.x, self.rect.y]) == 1:
                self.rect.x = teleportcoords[0][0]+10
                self.rect.y = teleportcoords[0][1]
                # if self.direction == 3:
                #     self.move_single_axis(0, 10)
                self.direction = 3

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

    def randomW(self, choices):
        total = sum(w for c, w in choices)
        r = random.uniform(0, total)
        upto = 0
        for c, w in choices:
            if upto + w >= r:
                return c
            upto += w
        assert False, "Shouldn't get here"

class Wall:
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 20, 20)

class Point:
    def __init__(self, pos):
        points.append((pos[0]+10, pos[1]+10))

class PowerPoint:
    def __init__(self, pos):
        powerpoints.append(pos)

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

def flatten(seq,container=None):
    if container is None:
        container = []
    for s in seq:
        if hasattr(s,'__iter__'):
            flatten(s,container)
        else:
            container.append(s)
    return container

def pause():
    time.sleep(1)
    while True:
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

        if key[pygame.K_p]:
            return

class Pipe:
    def __init__(self, file="PAT.pipe"):
        self.file = file
        self.iter = 0

    def push(self, value, done=False):
        self.pipe = open(self.file, "wb")
        pipeval = [self.iter, value, done]
        self.pipe.write(pickle.dumps(pipeval))
        self.iter += 1
        self.pipe.close()

pygame.init()
pygame.display.set_caption("PATMAN")
global screen
screen = pygame.display.set_mode((420, 420))
global pipe
pipe = Pipe()
pipe.push(0)

def Main():
    game = Game()
    # landscape = Graph(open(resource_path(os.path.join('data', "MAP_SEARCH.patlayout"))), 20)
    global walls
    walls = []
    global points
    points = []
    global powerpoints
    powerpoints = []
    global ghosts
    ghosts = []
    size = 20
    player = Player(size)
    player.rect.x = 20
    player.rect.y = 20

    level = open(resource_path(os.path.join('../data', "MAP.patlayout")))

    x = y = 0
    teleportcoords = []

    xcount = ycount = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            elif col == "T":
                teleportcoords.append([xcount * 2 * 10, ycount * 2 * 10])
            elif col == "P":
                Point((x, y))
            elif col == "G":
                Ghost((x, y))
            elif col == "B":
                PowerPoint((x, y));
            x += 20
            xcount += 1
        xcount = 0
        y += 20
        x = 0
        ycount += 1

    for ghost in ghosts:
        ghost.teleportcoords = teleportcoords

    teleport_path = [[(-10, 430), (430, 430), (430, 180)], [(430, 430), (-10, 430), (-10, 180)]]

    running = True
    patman_closed = pygame.image.load(resource_path(os.path.join('../data', 'patman.png')))
    patman_closed = pygame.transform.scale(patman_closed, (size, size))
    patman_closed_flipped = pygame.transform.flip(patman_closed, True, False)

    patman_open = pygame.image.load(resource_path(os.path.join('../data', 'patman_open.png')))
    patman_open = pygame.transform.scale(patman_open, (size, size))
    patman_open_flipped = pygame.transform.flip(patman_open, True, False)

    ghost_image_1 = pygame.image.load(resource_path(os.path.join('../data', 'ghost1.png')))
    ghost_image_1 = pygame.transform.scale(ghost_image_1, (size, size))
    ghost_image_2 = pygame.image.load(resource_path(os.path.join('../data', 'ghost2.png')))
    ghost_image_2 = pygame.transform.scale(ghost_image_2, (size, size))
    ghost_image_3 = pygame.image.load(resource_path(os.path.join('../data', 'ghost3.png')))
    ghost_image_3 = pygame.transform.scale(ghost_image_3, (size, size))
    ghost_image_4 = pygame.image.load(resource_path(os.path.join('../data', 'ghost4.png')))
    ghost_image_4 = pygame.transform.scale(ghost_image_4, (size, size))
    ghost_image_scared = pygame.image.load(resource_path(os.path.join('../data', 'ghostscared.png')))
    ghost_image_scared = pygame.transform.scale(ghost_image_scared, (size, size))

    mouth_open = False
    flipped = False
    retreat = False

    scoreText = pygame.font.SysFont("monospace", 15)
    finishText = pygame.font.SysFont("freesansbold.ttf", 60)
    x = 1
    time.sleep(1)
    sleep = 0.06
    gameStart = time.time()

    while running:
        game.previouspoints = game.points
        player.previouscoordinates = (player.rect.x, player.rect.y)
        for ghost in ghosts:
            if ghost.scared == True:
                if game.checkScared(player, ghost):
                    game.points += 10
                    ghost.scared = False
                    ghost.rect.x = 200
                    ghost.rect.y = 180
            else:
                if game.check(player, ghost) == False:
                    running = False
                    return False

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

        if key[pygame.K_p]:
            pause()
            time.sleep(1)

        if key[pygame.K_UP]:
            player.rect.y += -10
            for wall in walls:
                if player.rect.colliderect(wall.rect):
                    newplayerdirection = player.direction
                    break
                else:
                    newplayerdirection = 0

            player.direction = newplayerdirection
            player.rect.y += +10

        if key[pygame.K_DOWN]:
            player.rect.y += +10
            for wall in walls:
                if player.rect.colliderect(wall.rect):
                    newplayerdirection = player.direction
                    break
                else:
                    newplayerdirection = 1

            player.direction = newplayerdirection
            player.rect.y += -10

        if key[pygame.K_LEFT]:
            player.rect.x += -10
            for wall in walls:
                if player.rect.colliderect(wall.rect):
                    newplayerdirection = player.direction
                    break
                else:
                    newplayerdirection = 2

            player.direction = newplayerdirection
            player.rect.x += +10
        if key[pygame.K_RIGHT]:
            player.rect.x += +10
            for wall in walls:
                if player.rect.colliderect(wall.rect):
                    newplayerdirection = player.direction
                    break
                else:
                    newplayerdirection = 3

            player.direction = newplayerdirection
            player.rect.x += -10

        if player.direction == 0:
            player.move(-10, 0, teleportcoords)
        if player.direction == 1:
            player.move(--10, 0, teleportcoords)
        if player.direction == 2:
            flipped = True
            player.move(0, -10, teleportcoords)
        if player.direction == 3:
            flipped = False
            player.move(0, 10, teleportcoords)

        occured = []
        ghostnum = 1
        retreat = False
        if x > 0:
            for ghost in ghosts:
                if x % 100 == 0:
                    retreat = False
                elif x % 50 == 0:
                    retreat = False

                # previouscoordinates = []
                # previouscoordinates.append(player.rect.x)
                # previouscoordinates.append(player.rect.y)

                # for teleportcoord in teleport_path:
                #     print(teleportcoord)
                #     if (ghost.rect.x, ghost.rect.y) in teleportcoord:
                #         print()
                #         print("THERERERERE")
                #         print()
                #         ghost.n += 1
                #         if ghost.n > len(teleportcoord) - 1:
                #             ghost.n = 0

                # if not ghost.teleportcoord == -1:
                #     player.rect.x = teleport_path[ghost.teleportcoord][ghost.n][0]
                #     player.rect.y = teleport_path[ghost.teleportcoord][ghost.n][1]
                #     print("Going to:", (player.rect.x, player.rect.y))
                #     print("Currently At:", (ghost.rect.x, ghost.rect.y))

                blockeddirections = []
                if ghost.rect.center in occured:
                    ghost.direction = random.randrange(0, 4)
                    if ghost.direction == 0:
                        if ghost.move(-10, 0):
                            break
                        blockeddirections.append(ghost.direction)
                        ghost.direction = ghost.chase(player, blockeddirections)
                    if ghost.direction == 1:
                        if ghost.move(10, 0):
                            break
                        blockeddirections.append(ghost.direction)
                        ghost.direction = ghost.chase(player, blockeddirections)
                    if ghost.direction == 2:
                        if ghost.move(0, -10):
                            break
                        blockeddirections.append(ghost.direction)
                        ghost.direction = ghost.chase(player, blockeddirections)
                    if ghost.direction == 3:
                        if ghost.move(0, 10):
                            break
                        blockeddirections.append(ghost.direction)
                        ghost.direction = ghost.chase(player, blockeddirections)
                occured.append(ghost.rect.center)

                if retreat == True:
                    ghost.retreat(ghostnum, player, blockeddirections)
                else:
                    ghost.direction = ghost.chase(player, blockeddirections)
                blockeddirections = []
                for i in range(3):
                    if ghost.direction == 0:
                        if ghost.move(-10, 0):
                            break
                        blockeddirections.append(str(ghost.direction))
                        if retreat == True:
                            ghost.retreat(ghostnum, player, blockeddirections)
                        else:
                            ghost.direction = ghost.chase(player, blockeddirections)
                    if ghost.direction == 1:
                        if ghost.move(10, 0):
                            break
                        blockeddirections.append(str(ghost.direction))
                        if retreat == True:
                            ghost.retreat(ghostnum, player, blockeddirections)
                        else:
                            ghost.direction = ghost.chase(player, blockeddirections)
                    if ghost.direction == 2:
                        if ghost.move(0, -10):
                            break
                        blockeddirections.append(str(ghost.direction))
                        if retreat == True:
                            ghost.retreat(ghostnum, player, blockeddirections)
                        else:
                            ghost.direction = ghost.chase(player, blockeddirections)
                    if ghost.direction == 3:
                        if ghost.move(0, 10):
                            break
                        blockeddirections.append(str(ghost.direction))
                        if retreat == True:
                            ghost.retreat(ghostnum, player, blockeddirections)
                        else:
                            ghost.direction = ghost.chase(player, blockeddirections)

                # if not ghost.teleportcoord == -1:
                #     player.rect.x = previouscoordinates[0]
                #     player.rect.y = previouscoordinates[1]
                ghostnum += 1

        screen.fill((0,0,0))
        for wall in walls:
            pygame.draw.rect(screen, (0, 0, 255), wall.rect)

        i = 0

        for point in points:
            if player.rect.x == point[0]-10 and player.rect.y == point[1]-10:
                point = None
                points.pop(i)
                game.points += 1
                sleep -= 0.0001
            else:
                if point[0] == 0 and point[1] == 0:
                    pygame.draw.circle(screen, (255, 0, 0), point, 3)
                else:
                    pygame.draw.circle(screen, (255, 255, 255), point, 3)
            i += 1

        i = 0
        for powerpoint in powerpoints:
            if player.rect.x == powerpoint[0]-10 and player.rect.y == powerpoint[1]-10:
                powerpoints.pop(i)
            else:
                pygame.draw.circle(screen, (255, 255, 255), powerpoint, 5)
            i += 1

        x = 1
        for ghost in ghosts:
            if ghost.scared:
                screen.blit(ghost_image_scared, ghost.rect)
                if ghost.scaredCount == 200:
                    ghost.scared = False
                    ghost.scaredCount = 0
                else:
                    ghost.scaredCount += 1
            if x == 1:
                screen.blit(ghost_image_1, ghost.rect)
            if x == 2:
                screen.blit(ghost_image_2, ghost.rect)
            if x == 3:
                screen.blit(ghost_image_3, ghost.rect)
            if x == 4:
                screen.blit(ghost_image_4, ghost.rect)
            x += 1

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
        if len(points) == 0:
           running = False
        x += 1
        ###########
        # input() #
        ###########
        if game.points - game.previouspoints > 0:
            pipe.push(2)
        else:
            if (player.rect.x, player.rect.y) == player.previouscoordinates:
                pipe.push(-1)
            else:
                pipe.push(0)

        time.sleep(sleep)
        if len(points) == 0:
            return True

while True:
    if Main():
        pipe.push(10, True)
    else:
        pipe.push(-10, True)