from multiprocessing.connection import Listener
import sys
import pickle
import time
import os
import random
from math import sqrt

class Client:
    def __init__(self, connection, player):
        self.connection = connection
        self.player = player

class Game:
    def __init__(self):
        print(" >> Creating game", file=sys.stderr)
        self.client_list = []
        self.walls = []
        self.points = []
        self.powerpoints = []
        self.ghosts = []
        self.middle = []
        self.size = 20

        self.landscape = Graph(open(resource_path(os.path.join('../data', "MAP_SEARCH.patlayout"))), 20)
        level = open(resource_path(os.path.join('../data', "MAP_SEARCH.patlayout")))

        x = y = 0
        self.teleportcoords = []

        xcount = ycount = 0
        for row in level:
            for col in row:
                if col == "W":
                    self.walls.append((x, y))
                elif col == "T":
                    self.teleportcoords.append([xcount * 2 * 10, ycount * 2 * 10])
                elif col == "P":
                    self.points.append((x, y))
                elif col == "G":
                    self.ghosts.append(Ghost([x, y]))
                    self.middle.append((x, y))
                    self.middle.append((x-10, y))
                    self.middle.append((x, y-10))
                    self.middle.append((x-10, y-10))
                    self.middle.append((x+10, y))
                    self.middle.append((x, y+10))
                    self.middle.append((x+10, y+10))
                    self.middle.append((x+10, y-10))
                    self.middle.append((x-10, y+10))
                elif col == "B":
                    self.powerpoints.append((x, y))
                x += 20
                xcount += 1
            xcount = 0
            y += 20
            x = 0
            ycount += 1

    def createSocket(self):
        print(" >> Creating socket", file=sys.stderr)
        sock_address = ('', int(sys.argv[1]))
        self.sock = Listener(sock_address)

        print(" >> Socket created", file=sys.stderr)
        print("    ---------------", file=sys.stderr)
        print("    | Host:", sock_address[0], file=sys.stderr)
        print("    | Port:", sock_address[1], file=sys.stderr)
        print("    ---------------", file=sys.stderr)

    def connectClients(self, number_of_clients):
        start = [(20, 20), (380, 20), (20, 380), (380, 380)]
        x = 0
        while len(self.client_list) < number_of_clients:
            print(" >> Listening for connections (%s out of %s clients connected)" % (len(self.client_list), number_of_clients), file=sys.stderr)
            # self.sock.listen(1)
            conn = self.sock.accept()
            client = Client(conn, start[x])
            self.client_list.append(client)
            conn.send(pickle.dumps(self.client_list.index(client)))
            x += 1

    def broadcastToAll(self, data):
        data = pickle.dumps(data)
        for client in self.client_list:
            client.connection.send(data)

    def broadcastToIndividual(self, data, client):
        data = pickle.dumps(data)
        client.connection.send(data)

    def closeSocket(self):
        self.sock.close()
        print(" >> Socket closed")

class Queue:
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
                x += distance
                xcount += 1
            xcount = 0
            y += distance
            x = 0
            ycount += 1

    def neighbours(self, node):
        if not node in self.nodes:
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
        self.pos = pos
        self.previouspos = pos
        self.direction = 3
        self.corner = None

    def move(self, dy, dx, walls):
        if dx != 0:
            if self.move_single_axis(dx, 0, walls) == False:
                return False
        if dy != 0:
            if self.move_single_axis(0, dy, walls) == False:
                return False
        if [self.pos[0], self.pos[1]] in self.teleportcoords:
            if self.teleportcoords.index([self.pos[0], self.pos[1]]) == 0:
                if self.direction != 3:
                    self.pos[0] = self.teleportcoords[1][0]+200
                    self.pos[1] = self.teleportcoords[1][1]
                    self.direction = 2
                    self.teleporting = True
                else:
                    self.teleporting = False
            elif self.teleportcoords.index([self.pos[0], self.pos[1]]) == 1:
                if self.direction != 2:
                    self.pos[0] = self.teleportcoords[0][0]-200
                    self.pos[1] = self.teleportcoords[0][1]
                    self.direction = 3
                    self.teleporting = True
                else:
                    self.teleporting = False

        return True

    def move_single_axis(self, dx, dy, walls):
        self.pos[0] += dx
        self.pos[1] += dy
        if (self.pos[0], self.pos[1]) in self.previouscoordinates.queue:
            return False

        for wall in walls:
            top_left = (wall[0]-9, wall[1]-9)
            bottom_right = (wall[0]+9, wall[1]+9)
            if top_left[0] <= self.pos[0] and self.pos[0] <= bottom_right[0] and top_left[1] <= self.pos[1] and self.pos[1] <= bottom_right[1]:
                if dx > 0:
                    self.pos[0] = wall[0]-10
                if dx < 0:
                    self.pos[0] = wall[0]+10
                if dy > 0:
                    self.pos[1] = wall[1]-10
                if dy < 0:
                    self.pos[1] = wall[1]+10
                return False

        return True

    def chase(self, players, landscape, middle):
        player_distances = []
        for player in players.items():
            if player[1] not in middle:
                player_distances.append(abs( self.pos[0] - player[1][0] ) + abs( self.pos[1] - player[1][1] ))
        if len(player_distances) > 0:
            player = players[player_distances.index(min(player_distances))]
            self.corner = None
        else:
            corners = [(20, 20), (380, 20), (20, 380), (380, 380)]
            if self.corner == None or self.pos == self.corner:
                while True:
                    self.corner = player = random.choice(corners)
                    if not self.pos == player:
                        break
            else:
                player = self.corner
                

        start = (self.pos[0], self.pos[1])
        frontier = Queue(float("inf"))
        frontier.enqueue(start)
        came_from = {}
        came_from[start] = None
        end = False

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

        if not end:
            return [player]

        path = []
        i = 0

        ##Creates Paths##
        while end != start:
            end = came_from[end]
            path.append(end)
        return list(reversed(path))

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

game = Game()
game.createSocket()
game.connectClients(int(sys.argv[2]))

players = {}
for client in game.client_list:
    players[game.client_list.index(client)] = client.player
previous_players = players


# Check if clients ready
print(" >> Waiting for clients to be ready", file=sys.stderr)

ready = 0
while ready < len(game.client_list):
    for client in game.client_list:
        data = pickle.loads(client.connection.recv())
        if data == game.client_list.index(client):
            ready += 1

## Main game loop
try:
    print(" >> Starting main game loop", file=sys.stderr)
    other = True
    iteration = 0
    while True:
        ghost_coords = []

        if iteration == 0:
            for ghost in game.ghosts:
                ghost_coords.append(ghost.pos)
            game_state = {"WALLS" : game.walls, "TELEPORTCOORDS" : game.teleportcoords, "POINTS" : game.points, "POWERPOINTS" : game.powerpoints, "GHOSTS" : ghost_coords, "PLAYERS" : players}
        else:
            occured = []
            if iteration % 2 == 0:
                for ghost in game.ghosts:
                    ghost.previouspos = ghost.pos
                    next_coord = ghost.chase(players, game.landscape, game.middle)
                    if len(next_coord) > 1:
                        next_coord = next_coord[1]
                    elif len(next_coord) == 1:
                        if not ghost.corner:
                            player_distances = []
                            for player in game_state['PLAYERS'].items():
                                player_distances.append(abs( ghost.pos[0] - player[1][0] ) + abs( ghost.pos[1] - player[1][1] ))
                            next_coord = game_state['PLAYERS'][player_distances.index(min(player_distances))]
                        else:
                            next_coord = next_coord[0]
                    else:
                        next_coord = ghost.pos

                    occured = False
                    # if iteration > 10:
                    for checkghost in game.ghosts:
                        if not ghost == checkghost and next_coord == checkghost.pos:
                            occured = True

                    if not occured:
                        ghost.pos = next_coord

                    for player in players.items():
                        if (ghost.pos[0]+10 > player[1][0] and ghost.pos[0]-10 < player[1][0]) and (ghost.pos[1]+10 > player[1][1] and ghost.pos[1]-10 < player[1][1]):
                            players[player[0]] = (190, 190)

            ghost_coords = [game.ghosts[0].pos, game.ghosts[1].pos, game.ghosts[2].pos, game.ghosts[3].pos]

            game_state = {"PLAYERS" : game_state['PLAYERS'], "POINTS" : game.points, "GHOSTS" : ghost_coords}
        previous_players = game_state['PLAYERS']
        game.broadcastToAll(game_state)
        for client in game.client_list:
            data = pickle.loads(client.connection.recv())
            game_state['PLAYERS'][game.client_list.index(client)] = data['PLAYER']
            if game_state['PLAYERS'][game.client_list.index(client)] in game.points:
                game.points.remove(game_state['PLAYERS'][game.client_list.index(client)])
        iteration += 1

except EOFError:
    game.closeSocket()

except ConnectionResetError:
    game.closeSocket()