# -*- coding: utf-8 -*-
# @Author: Ben
# @Date:   2017-03-03 22:23:44
# @Last Modified by:   Ben
# @Last Modified time: 2018-05-18 23:12:52
# /Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 PATMAN.py

import os
import pygame
import time
import random
import sys
from math import sqrt
import operator

class Game:
    def __init__(self):
        self.points = 0

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


class Graph:
    def __init__(self, grid, distance):
        self.distance = distance
        self.nodes = []
        x = y = xcount = ycount = 0
        for row in grid:
            for col in row:
                if not col == "W":
                    self.nodes.append((x, y))
                    # pygame.draw.rect(screen, (0, 255, 0), frontierdisplay[str((x, y))].rect)
                    # pygame.display.update()

                x += distance
                xcount += 1
            xcount = 0
            y += distance
            x = 0
            ycount += 1
        time.sleep(1)
        for node in self.nodes:
            pygame.draw.rect(screen, (0, 255, 0), frontierdisplay[str((node[0], node[1]))])
            pygame.display.flip()
            # time.sleep(0.1)

        input()

    def neighbours(self, node):
        if node not in self.nodes:
            return None
        directions = [[self.distance, 0], [-self.distance, 0], [0, self.distance], [0, -self.distance]]
        neighbours = []
        for direction in directions:
            neighbour = (node[0] + direction[0], node[1] + direction[1])
            if neighbour in self.nodes:
                neighbours.append(neighbour)
        return neighbours


class Ghost:
    def __init__(self, pos):
        ghosts.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 20, 20)
        self.previouspos = (self.rect.x, self.rect.y)
        self.direction = 3
        self.corner = None
        # self.previouscoordinates = Queue(4)
        # self.count = 0
        # self.scared = False
        # self.scaredCount = 0
        # self.previousPath = []
        # self.teleporting = False
        # self.teleportcoords = []

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


    def pursue(self, player, landscape, middle):
        if player not in middle:
            self.corner = None
        else:
            corners = [(20, 20), (380, 20), (20, 380), (380, 380)]
            if self.corner == None or (self.rect.x, self.rect.y) == self.corner:
                while True:
                    self.corner = player = random.choice(corners)
                    if not (self.rect.x, self.rect.y) == player:
                        break
            else:
                player = self.corner
                

        start = (self.rect.x, self.rect.y)
        frontier = Queue(float("inf"))
        frontier.enqueue(start)
        came_from = {}
        came_from[start] = None
        end = False

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        while not frontier.isEmpty():
            current = frontier.dequeue()
            temp = (current[0] + 10, current[1] + 10)
            if (player[0]-10 <= temp[0] and player[0]+10 >= temp[0]) and (player[1]-10 <= temp[1] and player[1]+10 >= temp[1]):
                end = current
                break
            neighbours = landscape.neighbours(current)
            
            if neighbours is not None:
                for next in neighbours:
                    if next not in came_from:
                        frontier.enqueue(next)
                        came_from[next] = current
                        # time.sleep(0.01)
        #                 pygame.draw.rect(screen, (r, g, b), frontierdisplay[str(next)].rect)
        # pygame.display.flip()

        if not end:
            return [player]

        path = []
        i = 0

        ##Creates Paths##
        while end != start:
            end = came_from[end]
            path.append(end)
        return list(reversed(path))

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


class Wall:
    def __init__(self, pos, frontier=False):
        if not frontier:
            walls.append(self)

        # print(pos)
        frontierdisplay[str(pos)] = self

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
        if hasattr(s, '__iter__'):
            flatten(s, container)
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

pygame.init()
pygame.display.set_caption("PATMAN")
global screen
screen = pygame.display.set_mode((420, 420))
global waca
waca = pygame.mixer.Sound("data/Waca.wav")

game = Game()
global walls
walls = []
global points
points = []
global powerpoints
powerpoints = []
global ghosts
ghosts = []
global frontierdisplay
frontierdisplay = {}
size = 20
player = Player(size)
player.rect.x = 20
player.rect.y = 20

level = open(resource_path(os.path.join('data', "MAP.patlayout")))
middle = []

x = y = 0
teleportcoords = []

xcount = ycount = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        else:
            Wall((x, y), True)
        
        if col == "T":
            teleportcoords.append([xcount * 2 * 10, ycount * 2 * 10])
        elif col == "P":
            Point((x, y))
        elif col == "G":
            Ghost((x, y))
            middle.append((x, y))
            middle.append((x-10, y))
            middle.append((x, y-10))
            middle.append((x-10, y-10))
            middle.append((x+10, y))
            middle.append((x, y+10))
            middle.append((x+10, y+10))
            middle.append((x+10, y-10))
            middle.append((x-10, y+10))
        elif col == "B":
            PowerPoint((x, y));
        x += 20
        xcount += 1
    xcount = 0
    y += 20
    x = 0
    ycount += 1


def Main():
    pointlength = len(points)

    for ghost in ghosts:
        ghost.teleportcoords = teleportcoords

    teleport_path = [[(-10, 430), (430, 430), (430, 180)], [(430, 430), (-10, 430), (-10, 180)]]

    patman_closed = pygame.image.load(resource_path(os.path.join('data', 'patman.png')))
    patman_closed = pygame.transform.scale(patman_closed, (size, size))
    patman_closed_flipped = pygame.transform.flip(patman_closed, True, False)

    patman_open = pygame.image.load(resource_path(os.path.join('data', 'patman_open.png')))
    patman_open = pygame.transform.scale(patman_open, (size, size))
    patman_open_flipped = pygame.transform.flip(patman_open, True, False)

    ghost_image_1 = pygame.image.load(resource_path(os.path.join('data', 'ghost1.png')))
    ghost_image_1 = pygame.transform.scale(ghost_image_1, (size, size))
    ghost_image_2 = pygame.image.load(resource_path(os.path.join('data', 'ghost2.png')))
    ghost_image_2 = pygame.transform.scale(ghost_image_2, (size, size))
    ghost_image_3 = pygame.image.load(resource_path(os.path.join('data', 'ghost3.png')))
    ghost_image_3 = pygame.transform.scale(ghost_image_3, (size, size))
    ghost_image_4 = pygame.image.load(resource_path(os.path.join('data', 'ghost4.png')))
    ghost_image_4 = pygame.transform.scale(ghost_image_4, (size, size))
    ghost_image_scared = pygame.image.load(resource_path(os.path.join('data', 'ghostscared.png')))
    ghost_image_scared = pygame.transform.scale(ghost_image_scared, (size, size))

    mouth_open = False
    flipped = False
    retreat = False

    scoreText = pygame.font.SysFont("monospace", 15)
    
    finishText = pygame.font.SysFont("freesansbold.ttf", 60)

    x = 1
    ghostinc = 0
    # time.sleep(1)
    sleep = 0.06
    gameStart = time.time()


    landscape = Graph(open(resource_path(os.path.join('data', "MAP.patlayout"))), 20)
    print(" >> Graph created")
    running = True
    while running:
        for ghost in ghosts:
            # if ghost.scared == True:
            #     if game.checkScared(player, ghost):
            #         game.points += 10
            #         ghost.scared = False
            #         ghost.rect.x = 200
            #         ghost.rect.y = 180
            # else:
            if game.check(player, ghost) == False:
                running = False

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

        screen.fill((0, 0, 0))
        colours = [(246, 0, 0), (249, 141, 0), (244, 145, 207), (70, 251, 244)]

        for ghost in ghosts:
            if x > 0 and ghostinc % 2 == 0:
                ghost.previouspos = (ghost.rect.x, ghost.rect.y)
                next_coord = ghost.pursue((player.rect.x, player.rect.y), landscape, middle)

                for coord in next_coord:
                    try:
                        pygame.draw.rect(screen, colours[ghosts.index(ghost)], frontierdisplay[str(coord)].rect)
                    except:
                        pass

                if len(next_coord) > 1:
                    next_coord = next_coord[1]
                elif len(next_coord) == 1:
                    if not ghost.corner:
                        next_coord = (player.rect.x, player.rect.y)
                    else:
                        next_coord = next_coord[0]
                else:
                    next_coord = (ghost.rect.x, ghost.rect.y)


                ghost.rect.x = next_coord[0]
                ghost.rect.y = next_coord[1]

                ghostnum += 1

        for wall in walls:
            pygame.draw.rect(screen, (0, 0, 255), wall.rect)

        i = 0

        for point in points:
            if player.rect.x == point[0] - 10 and player.rect.y == point[1] - 10:
                point = None
                points.pop(i)
                game.points += 1
            else:
                if point[0] == 0 and point[1] == 0:
                    pygame.draw.circle(screen, (255, 0, 0), point, 3)
                else:
                    pygame.draw.circle(screen, (255, 255, 255), point, 3)
            i += 1

        i = 0
        for powerpoint in powerpoints:
            if player.rect.x == powerpoint[0] - 10 and player.rect.y == powerpoint[1] - s10:
                powerpoints.pop(i)
            else:
                pygame.draw.circle(screen, (255, 255, 255), powerpoint, 5)
            i += 1

        x = 1
        for ghost in ghosts:
            # if ghost.scared:
            #     screen.blit(ghost_image_scared, ghost.rect)
            #     if ghost.scaredCount == 200:
            #         ghost.scared = False
            #         ghost.scaredCount = 0
            #     else:
            #         ghost.scaredCount += 1
            if x == 1:
                screen.blit(ghost_image_1, ghost.rect)
            if x == 2:
                screen.blit(ghost_image_2, ghost.rect)
            if x == 3:
                screen.blit(ghost_image_3, ghost.rect)
            if x == 4:
                screen.blit(ghost_image_4, ghost.rect)
            x += 1

        labelScore = scoreText.render("Score: " + str(game.points), 1, (0, 0, 0))
        screen.blit(labelScore, (0, -4))

        if mouth_open:
            if flipped:
                screen.blit(patman_open_flipped, player.rect)
            else:
                screen.blit(patman_open, player.rect)
            mouth_open = False
        else:
            if flipped:
                screen.blit(patman_closed_flipped, player.rect)
            else:
                screen.blit(patman_closed, player.rect)
            mouth_open = True
        pygame.display.flip()
        if len(points) == 0:
            running = False
        x += 1
        ghostinc += 1
        ###########
        # input() #
        ###########
        if ghostinc % 2 == 0:
            time.sleep(sleep)
        pygame.mixer.Sound.play(waca)
        time.sleep(sleep)
        sleep = abs((pointlength - game.points / 2) / 5000)
        pygame.display.flip()

while True:
    Main()
