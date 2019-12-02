# -*- coding: utf-8 -*-
# @Author: Ben
# @Date:   2017-03-03 22:23:44
# @Last Modified by:   Ben
# @Last Modified time: 2018-05-18 22:55:27
# /Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 PATMAN.py

import os
import pygame
from multiprocessing.connection import Client
import select
import time
import random
import sys
from math import sqrt
import operator
import pickle

class Player:
    def __init__(self, size, pos):
        print("Pos:", pos)
        self.rect = pygame.Rect(20, 20, size, size)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.direction = 3
        self.points = 0

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

class Ghost:
    def __init__(self, pos, size, image):
        self.rect = pygame.Rect(pos[0], pos[1], size, size)
        self.image = image

class Wall:
    def __init__(self, pos, size):
        self.rect = pygame.Rect(pos[0], pos[1], size, size)

def Point(pos):
    return (pos[0]+10, pos[1]+10)

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

## Connect to server
server_address = ('', int(sys.argv[1]))

print(" >> Connecting to server on %s on port %s" % server_address, file=sys.stderr)
sock = Client((server_address))
client_number = pickle.loads(sock.recv())
print(" >> Client Number:", client_number, file=sys.stderr)

## Setup game
pygame.init()
pygame.display.set_caption("PATMAN")
global screen
screen = pygame.display.set_mode((420, 420))

global walls
walls = []
global points
points = []
global powerpoints
powerpoints = []
global ghosts
ghosts = []
global players
players = {}
global teleportcoords
teleportcoords = []

patman_closed = pygame.image.load(resource_path(os.path.join('../data', 'patman.png')))
patman_closed = pygame.transform.scale(patman_closed, (20, 20))
patman_closed_flipped = pygame.transform.flip(patman_closed, True, False)

patman_open = pygame.image.load(resource_path(os.path.join('../data', 'patman_open.png')))
patman_open = pygame.transform.scale(patman_open, (20, 20))
patman_open_flipped = pygame.transform.flip(patman_open, True, False)


ghost_images = []
for i in range(4):
    ghost_images.append(pygame.image.load(resource_path(os.path.join('../data', 'ghost' + str(i+1) + '.png'))))
    ghost_images[i] = pygame.transform.scale(ghost_images[i], (20, 20))

# ghost_image_scared = pygame.image.load(resource_path(os.path.join('../data', 'ghostscared.png')))
# ghost_image_scared = pygame.transform.scale(ghost_image_scared, (20, 20))

mouth_open = False
flipped = False

# Tell server client ready
print(" >> Telling server client ready", file=sys.stderr)
data = pickle.dumps(client_number)
sock.send(data)
print(" >> Starting game", file=sys.stderr)
## Main game loop
try:
    while True:
        start = time.time()
        data = pickle.loads(sock.recv())
        if len(players) == 0:
            for player in data['PLAYERS'].items():
                players[player[0]] = Player(20, player[1])
        else:
            for i in range(len(players)):
                players[i].rect.x = data['PLAYERS'][i][0]
                players[i].rect.y = data['PLAYERS'][i][1]

        if len(ghosts) == 0:
            i = 0
            for ghost in data['GHOSTS']:
                ghosts.append(Ghost(ghost, 20, ghost_images[i]))
                i += 1
        else:
            print("GHOSTS:", data['GHOSTS'])
            for ghost in ghosts:
                ghost.rect.x = data['GHOSTS'][ghosts.index(ghost)][0]
                ghost.rect.y = data['GHOSTS'][ghosts.index(ghost)][1]

        if len(walls) == 0:
            for wall in data['WALLS']:
                walls.append(Wall((wall[0], wall[1]), 20))

        if len(teleportcoords) == 0:
            teleportcoords = data['TELEPORTCOORDS']

        points = []
        for point in data['POINTS']:
            points.append(Point(point))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                running = False

        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            players[client_number].rect.y += -10
            for wall in walls:
                if players[client_number].rect.colliderect(wall.rect):
                    newplayerdirection = players[client_number].direction
                    break
                else:
                    newplayerdirection = 0

            players[client_number].direction = newplayerdirection
            players[client_number].rect.y += +10

        if key[pygame.K_DOWN]:
            players[client_number].rect.y += +10
            for wall in walls:
                if players[client_number].rect.colliderect(wall.rect):
                    newplayerdirection = players[client_number].direction
                    break
                else:
                    newplayerdirection = 1

            players[client_number].direction = newplayerdirection
            players[client_number].rect.y += -10

        if key[pygame.K_LEFT]:
            players[client_number].rect.x += -10
            for wall in walls:
                if players[client_number].rect.colliderect(wall.rect):
                    newplayerdirection = players[client_number].direction
                    break
                else:
                    newplayerdirection = 2

            players[client_number].direction = newplayerdirection
            players[client_number].rect.x += +10

        if key[pygame.K_RIGHT]:
            players[client_number].rect.x += +10
            for wall in walls:
                if players[client_number].rect.colliderect(wall.rect):
                    newplayerdirection = players[client_number].direction
                    break
                else:
                    newplayerdirection = 3

            players[client_number].direction = newplayerdirection
            players[client_number].rect.x += -10

        if players[client_number].direction == 0:
            players[client_number].move(-10, 0, teleportcoords)
        if players[client_number].direction == 1:
            players[client_number].move(--10, 0, teleportcoords)
        if players[client_number].direction == 2:
            flipped = True
            players[client_number].move(0, -10, teleportcoords)
        if players[client_number].direction == 3:
            flipped = False
            players[client_number].move(0, 10, teleportcoords)

        screen.fill((0,0,0))
        for wall in walls:
            pygame.draw.rect(screen, (0, 0, 255), wall.rect)

        i = 0

        for point in points:
            if point[0] == 0 and point[1] == 0:
                pygame.draw.circle(screen, (255, 0, 0), point, 3)
            else:
                pygame.draw.circle(screen, (255, 255, 255), point, 3)
            i += 1

        if mouth_open:
            if flipped == True:
                for player in players.items():
                    screen.blit(patman_open_flipped, player[1].rect)
            else:
                for player in players.items():
                    screen.blit(patman_open, player[1].rect)
            mouth_open = False
        else:
            if flipped == True:
                for player in players.items():
                    screen.blit(patman_closed_flipped, player[1].rect)
            else:
                for player in players.items():
                    screen.blit(patman_closed, player[1].rect)
            mouth_open = True

        for ghost in ghosts:
            screen.blit(ghost.image, ghost.rect)

        ## Send game state back to server
        game_state = {'PLAYER' : (players[client_number].rect.x, players[client_number].rect.y)}
        data = pickle.dumps(game_state)
        sock.send(data)

        pygame.display.flip()
        print(" >> FPS:", 1 / (time.time()-start), file=sys.stderr)
        time.sleep(0.05)
except ConnectionResetError:
    sock.close()
    print(" >> Connection closed by server")
