from settings import *
import pygame as pg
import random as r
import copy
import math
import time
import heapq

class Tile:
    def __init__(self,pos,num):
        self.pos = pos #coordinate of tile
        self.num = num #number on the tile, 0 == blank
        if self.num == 0:
            self.goal = self.pos
        else:
            self.goal = NUMTOGOAL[num]

    def get_distance(self): #finds manhattan distance
        self.goal = NUMTOGOAL[self.num]
        return abs(self.goal[0]-self.pos[0]) + abs(self.goal[1]-self.pos[1])

class Node: #board state
    def __init__(self,tile_list,prev_move = None,cost = 0,prev_node = None):
        self.tile_list = tile_list #list of tiles
        self.prev_move = prev_move #direction of move to get to this state
        self.prev_node = prev_node #points to the last node for retracing
        self.cost = cost #steps taken
        self.hash = 0
        self.gScore = 999 #cost to get to this node
        self.fScore = 999 #gscore + heuristic (manhattan in this case)
        for i in range(len(self.tile_list)):
            self.hash += (10**(len(self.tile_list)-i-1))*self.tile_list[i].num
            if self.tile_list[i].num == 0:
                self.missing_coord = self.tile_list[i].pos

    def __lt__(self,other):#compares node to others based on fscore
        return self.fScore < other.fScore

    def numToString(self,dir):
        if dir == 0:
            return 'up'
        if dir == 1:
            return 'right'
        if dir == 2:
            return 'down'
        if dir == 3:
            return 'left'

    def print_node(self):
        print(self.hash)
        print('Distance:',self.getDistance(),' Cost:',self.cost, 'Last move:',self.numToString(self.prev_move))
        count = 0
        for i in range(TILESIDECOUNT*TILESIDECOUNT):
            if i % TILESIDECOUNT == 0 and i > 0:
                print('')
            print(self.tile_list[count].num,end = ' ')
            count+= 1
        print('\n-----')

    def isSolution(self):
        if self.getDistance() == 0:
            return True
        else:
            return False

    def getDistance(self):
        total = 0
        for tile in self.tile_list:
            total += tile.get_distance()
        return total

class Graph:
    def __init__(self): #creates root of scrambled puzzle
        self.nodes = {}
        tiles = []
        missing = r.randrange(TILESIDECOUNT*TILESIDECOUNT-1)
        self.missing_coord = tuple((missing%TILESIDECOUNT,int(missing/TILESIDECOUNT)))
        num_list = [] #list from 1 - max
        'find solvable start state'
        for i in range(TILESIDECOUNT * TILESIDECOUNT-1):
            num_list.append(i+1)
        r.shuffle(num_list)
        while not self.solvable(num_list):
            print(str(num_list),'is not solvable')
            r.shuffle(num_list)
        print('found solvable:',num_list)
        'assign to tiles'
        count = 0
        for i in range(TILESIDECOUNT*TILESIDECOUNT):
            if i != missing: #if there is a tile
                tiles.append(Tile([i%TILESIDECOUNT, int(i/TILESIDECOUNT)],num_list[count]))
                count += 1
            else:
                tiles.append(Tile([i%TILESIDECOUNT, int(i/TILESIDECOUNT)],0))
        self.start_node = Node(tiles)
        self.nodes[self.start_node.hash]=self.start_node

    def find_moves(self,node):#returns a list of up to 4 nodes for the 4 neighbors
        missing_coord = TILESIDECOUNT*node.missing_coord[1] + node.missing_coord[0]
        output = []
        'up'
        if missing_coord < (TILESIDECOUNT-1)*TILESIDECOUNT: #if not on the bottom row
            tile_list = copy.deepcopy(node.tile_list)
            tile_list[missing_coord].num = tile_list[missing_coord+TILESIDECOUNT].num
            tile_list[missing_coord+TILESIDECOUNT].num = 0
            new_node = Node(tile_list,0,node.cost+1,node)
            if self.exists(new_node): #if node already exists, return that instead
                output.append(self.nodes[new_node.hash])
            else:
                output.append(new_node)
        'right'
        if missing_coord % TILESIDECOUNT != 0: #if not on the left column
            tile_list = copy.deepcopy(node.tile_list)
            tile_list[missing_coord].num = tile_list[missing_coord-1].num
            tile_list[missing_coord-1].num = 0
            new_node = Node(tile_list,1,node.cost+1,node)
            if self.exists(new_node): #if node already exists, return that instead
                output.append(self.nodes[new_node.hash])
            else:
                output.append(new_node)
        'down'
        if missing_coord > TILESIDECOUNT: #if not on the top row
            tile_list = copy.deepcopy(node.tile_list)
            tile_list[missing_coord].num = tile_list[missing_coord-TILESIDECOUNT].num
            tile_list[missing_coord-TILESIDECOUNT].num = 0
            new_node = Node(tile_list,2,node.cost+1,node)
            if self.exists(new_node): #if node already exists, return that instead
                output.append(self.nodes[new_node.hash])
            else:
                output.append(new_node)
        'left'
        if missing_coord % TILESIDECOUNT != TILESIDECOUNT-1: #if not on the left column
            tile_list = copy.deepcopy(node.tile_list)
            tile_list[missing_coord].num = tile_list[missing_coord+1].num
            tile_list[missing_coord+1].num = 0
            new_node = Node(tile_list,3,node.cost+1,node)
            if self.exists(new_node): #if node already exists, return that instead
                output.append(self.nodes[new_node.hash])
            else:
                output.append(new_node)
        return output

    def solvable(self,num_list):
        inversions = 0
        for i in range(TILESIDECOUNT * TILESIDECOUNT - 1):
            for j in range(i+1,TILESIDECOUNT*TILESIDECOUNT-1):
                if num_list[i] > num_list[j]:
                    inversions += 1
        if TILESIDECOUNT % 2 == 0: # if even width
            if inversions % 2 == 0: #if inversions is even
                if self.missing_coord[1] % 2 == 1: #blank on an even row
                    return True
            if inversions % 2 == 1:
                if self.missing_coord[1] % 2 == 0:
                    return True
        else: #if odd width
            if inversions % 2 == 0:
                return True
        return False

    def exists(self,node): #checks if node already exists in self.nodes
        if node.hash in self.nodes:
            return True
        return False

    def a_star(self):
        self.start_node.gScore = 0 #g(n): cost of cheapest path from start to n currently known
        self.start_node.fScore = self.start_node.getDistance() #f(n): guess of how short path will be if it goes through n
        current = self.start_node
        count = 0
        node_list = list(self.nodes.values())
        heapq.heapify(node_list)#min heap to track lowest fScore in log(n) rather than n time
        while True:
            count += 1
            current = heapq.heappop(node_list)
            if current.isSolution():
                print('searched:',count)
                return self.traceBack(current)
            self.nodes.pop(current.hash)
            for neighbor in self.find_moves(current):
                if current.gScore + 1 < neighbor.gScore:
                    neighbor.gScore = current.gScore + 1
                    neighbor.fScore = neighbor.gScore + neighbor.getDistance()
                    if not self.exists(neighbor):
                        self.nodes[neighbor.hash] = neighbor
                        heapq.heappush(node_list,neighbor)

    def traceBack(self,node):
        steps = []
        while node.hash != self.start_node.hash:
            steps.append(node.prev_move)
            node = node.prev_node
        steps.reverse()
        return steps
