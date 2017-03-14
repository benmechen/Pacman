# -*- coding: utf-8 -*-
# @Author: Ben
# @Date:   2017-03-03 22:23:44
# @Last Modified by:   Ben
# @Last Modified time: 2017-03-14 17:38:06
import os
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
            elif player.rect.x == ghost.rect.x and player.rect.y+10 == ghost.rect.y:
                return False
            elif player.rect.x == ghost.rect.x and player.rect.y-10 == ghost.rect.y:
                return False
            elif player.rect.x-10 == ghost.rect.x and player.rect.y == ghost.rect.y:
                return False
            elif player.rect.x+10 == ghost.rect.x and player.rect.y == ghost.rect.y:
                return False
            elif player.rect.x-10 == ghost.rect.x and player.rect.y-10 == ghost.rect.y:
                return False
            elif player.rect.x+10 == ghost.rect.x and player.rect.y+10 == ghost.rect.y:
                return False
            elif player.rect.x-10 == ghost.rect.x and player.rect.y+10 == ghost.rect.y:
                return False
            elif player.rect.x+10 == ghost.rect.x and player.rect.y-10 == ghost.rect.y:
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

    def isFull(self):
        len = self.end - self.start
        if len+1 == self.maxsize:
            return True

    def enqueue(self, item):
        if self.isFull() == True:
            self.dequeue()
        self.end += 1
        self.queue.insert(self.start, item)

    def dequeue(self):
        if self.isEmpty() != True:
            self.queue.pop(self.end)
            self.end -= 1
        else:
            return False


class Player:
    def __init__(self, size):
        self.rect = pygame.Rect(20, 20, size, size)
        self.direction = 3
        self.previouscoordinates = Queue(2)

    def move(self, dy, dx,teleportcoords):
        if dx != 0:
            if self.move_single_axis(dx, 0) == False:
                return False
        if dy != 0:
            if self.move_single_axis(0, dy) == False:
                return False

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
        self.previouscoordinates.enqueue([self.rect.x, self.rect.y])
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

    def chase(self, ghosts, collision):
        directions = []
        for ghost in ghosts:
            x1 = ghost.rect.x
            y1 = ghost.rect.y

            up = down = left = right = 0

            #Up
            if "0" not in collision:
                x2 = self.rect.x
                y2 = self.rect.y-10
                coordinates = [x2, y2]
                if coordinates == [210, 170] or coordinates == [220, 170] or coordinates == [210, 180] or coordinates == [220, 180]:
                    return 0
                else:
                    if coordinates not in self.previouscoordinates.queue:
                        up = sqrt(((x2-x1)**2)+((y2-y1)**2))
                    else:
                        up = 0

            #Down
            if "1" not in collision:
                x2 = self.rect.x
                y2 = self.rect.y+10
                coordinates = [x2, y2]
                if coordinates == [210, 170] or coordinates == [220, 170] or coordinates == [210, 180] or coordinates == [220, 180]:
                    return 0
                else:
                    if coordinates not in self.previouscoordinates.queue:
                        down = sqrt(((x2-x1)**2)+((y2-y1)**2))
                    else:
                        down = 0

            #Left
            if "2" not in collision:
                x2 = self.rect.x-10
                y2 = self.rect.y
                coordinates = [x2, y2]
                if coordinates == [210, 170] or coordinates == [220, 170] or coordinates == [210, 180] or coordinates == [220, 180]:
                    return 0
                else:
                    if coordinates not in self.previouscoordinates.queue:
                        left = sqrt(((x2-x1)**2)+((y2-y1)**2))
                    else:
                        left = 0

            #Right
            if "3" not in collision:
                x2 = self.rect.x+10
                y2 = self.rect.y
                coordinates = [x2, y2]
                if coordinates == [210, 170] or coordinates == [220, 170] or coordinates == [210, 180] or coordinates == [220, 180]:
                    return 0
                else:
                    if coordinates not in self.previouscoordinates.queue:
                        right = sqrt(((x2-x1)**2)+((y2-y1)**2))
                    else:
                        right = 0

            distances = [up, down, left, right]
            directions.append(distances.index(max(distances)))
        
        occurances = []
        for i in range(len(ghosts)):
            occurances.append(0)
            occurances[i] += 1
        return directions[0]

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
        self.previouscoordinates = Queue(4)
        self.count = 0

    def move(self, dy, dx):
        if dx != 0:
            if self.move_single_axis(dx, 0) == False:
                return False
        if dy != 0:
            if self.move_single_axis(0, dy) == False:
                return False
        self.previouscoordinates.enqueue([self.rect.x, self.rect.y])
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

        up = down = left = right = 1000000

        #Up
        if "0" not in collision:
            x2 = self.rect.x
            y2 = self.rect.y-10
            coordinates = [x2, y2]
            if coordinates == [210, 170] or coordinates == [220, 170] or coordinates == [210, 180] or coordinates == [220, 180]:
                return 0
            else:
                if coordinates not in self.previouscoordinates.queue:
                    up = sqrt(((x2-x1)**2)+((y2-y1)**2))
                else:
                    up = 1000000

        #Down
        if "1" not in collision:
            x2 = self.rect.x
            y2 = self.rect.y+10
            coordinates = [x2, y2]
            if coordinates == [210, 170] or coordinates == [220, 170] or coordinates == [210, 180] or coordinates == [220, 180]:
                return 0
            else:
                if coordinates not in self.previouscoordinates.queue:
                    down = sqrt(((x2-x1)**2)+((y2-y1)**2))
                else:
                    down = 1000000

        #Left
        if "2" not in collision:
            x2 = self.rect.x-10
            y2 = self.rect.y
            coordinates = [x2, y2]
            if coordinates == [210, 170] or coordinates == [220, 170] or coordinates == [210, 180] or coordinates == [220, 180]:
                return 0
            else:
                if coordinates not in self.previouscoordinates.queue:
                    left = sqrt(((x2-x1)**2)+((y2-y1)**2))
                else:
                    left = 1000000

        #Right
        if "3" not in collision:
            x2 = self.rect.x+10
            y2 = self.rect.y
            coordinates = [x2, y2]
            if coordinates == [210, 170] or coordinates == [220, 170] or coordinates == [210, 180] or coordinates == [220, 180]:
                return 0
            else:
                if coordinates not in self.previouscoordinates.queue:
                    right = sqrt(((x2-x1)**2)+((y2-y1)**2))
                else:
                    right = 1000000

        distances = [up, down, left, right]
        return distances.index(min(distances))

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

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

pygame.mixer.pre_init(44000, -16, 2, 512)
pygame.mixer.init()
pygame.init()
pygame.display.set_caption("PATMAN")
screen = pygame.display.set_mode((420, 420))
waca = pygame.mixer.Sound(resource_path(os.path.join('data', 'Waca.wav')))

game = Game()

walls = []
points = []
ghosts = []
size = 20
player = Player(size)
player.rect.x = 190
player.rect.y = 130

level = open(resource_path(os.path.join('data', "map.txt")))

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
##global playerdirection
##playerdirection = 3

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

mouth_open = False
flipped = False
retreat = True

scoreText = pygame.font.SysFont("monospace", 15)
x = 1
while running:
    if x % 4 == 0:
        waca.play()
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
    
    blockeddirections = []
    player.direction = player.chase(ghosts, blockeddirections)

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

    for i in range(3):
        print(player.direction)
        if player.direction == 0:
            if player.move(-10, 0, teleportcoords):
                print("player going up")
                break
            print("player can't go up")
            blockeddirections.append(str(player.direction))
            player.direction = player.chase(ghosts, blockeddirections)
        if player.direction == 1:
            if player.move(10, 0, teleportcoords):
                print("player going down")
                break
            print("player can't go down")
            blockeddirections.append(str(player.direction))
            player.direction = player.chase(ghosts, blockeddirections)
        if player.direction == 2:
            if player.move(0, -10, teleportcoords):
                print("player going left")
                break
            print("player can't go left")
            blockeddirections.append(str(player.direction))
            player.direction = player.chase(ghosts, blockeddirections)
        if player.direction == 3:
            if player.move(0, 10, teleportcoords):
                print("player going right")
                break
            print("player can't go right")
            blockeddirections.append(str(player.direction))
            player.direction = player.chase(ghosts, blockeddirections)

    occured = []
    ghostnum = 1
    # retreat = False
    if x > 0:
        for ghost in ghosts:
            if x % 100 == 0:
                retreat = True
            elif x % 50 == 0:
                retreat = False
            blockeddirections = []
            if ghost.rect.center in occured:
                print("Ghost in my way")
                ghost.direction = random.randrange(0, 4)
                if ghost.direction == 0:
                    if ghost.move(-10, 0):
                        print("Ghost", ghostnum, "going up")
                        break
                    print("Ghost", ghostnum, "can't go up")
                    blockeddirections.append(ghost.direction)
                    ghost.direction = ghost.chase(player, blockeddirections)
                if ghost.direction == 1:
                    if ghost.move(10, 0):
                        print("Ghost", ghostnum, "going down")
                        break
                    print("Ghost", ghostnum, "can't go down")
                    blockeddirections.append(ghost.direction)
                    ghost.direction = ghost.chase(player, blockeddirections)
                if ghost.direction == 2:
                    if ghost.move(0, -10):
                        print("Ghost", ghostnum, "going Left")
                        break
                    print("Ghost", ghostnum, "can't go left")
                    blockeddirections.append(ghost.direction)
                    ghost.direction = ghost.chase(player, blockeddirections)
                if ghost.direction == 3:
                    if ghost.move(0, 10):
                        print("Ghost", ghostnum, "going right")
                        break
                    print("Ghost", ghostnum, "can't go right")
                    blockeddirections.append(ghost.direction)
                    ghost.direction = ghost.chase(player, blockeddirections)
            occured.append(ghost.rect.center)

            if retreat == True:
                ghost.retreat(ghostnum, player, blockeddirections)
            else:
                ghost.direction = ghost.chase(player, blockeddirections)

            for i in range(3):
                if ghost.direction == 0:
                    if ghost.move(-10, 0):
                        print("Ghost", ghostnum, "going up")
                        break
                    print("Ghost", ghostnum, "can't go up")
                    blockeddirections.append(str(ghost.direction))
                    if retreat == True:
                        ghost.retreat(ghostnum, player, blockeddirections)
                    else:
                        ghost.direction = ghost.chase(player, blockeddirections)
                if ghost.direction == 1:
                    if ghost.move(10, 0):
                        print("Ghost", ghostnum, "going down")
                        break
                    print("Ghost", ghostnum, "can't go down")
                    blockeddirections.append(str(ghost.direction))
                    if retreat == True:
                        ghost.retreat(ghostnum, player, blockeddirections)
                    else:
                        ghost.direction = ghost.chase(player, blockeddirections)
                if ghost.direction == 2:
                    if ghost.move(0, -10):
                        print("Ghost", ghostnum, "going left")
                        break
                    print("Ghost", ghostnum, "can't go left")
                    blockeddirections.append(str(ghost.direction))
                    if retreat == True:
                        ghost.retreat(ghostnum, player, blockeddirections)
                    else:
                        ghost.direction = ghost.chase(player, blockeddirections)
                if ghost.direction == 3:
                    if ghost.move(0, 10):
                        print("Ghost", ghostnum, "going right")
                        break
                    print("Ghost", ghostnum, "can't go right")
                    blockeddirections.append(str(ghost.direction))
                    if retreat == True:
                        ghost.retreat(ghostnum, player, blockeddirections)
                    else:
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
    # if x % 4 == 0:
        # waca.stop()
    x += 1
    time.sleep(0.075)
exec(open('PATMAN_AI.py').read())
