import pygame
#import MazeGenerator
import random as _random
import sys

sys.setrecursionlimit(100000)

#Pygame Things
pygame.init()
resolution = (1280, 720)
pygame.display.set_caption("Maze Generator")
window = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

class Player:
    def __init__(self, startPos, maze, size):
        self.maze = maze
        self.pos = startPos
        self.size = size

    def MoveNorth(self):
        if self.maze[self.pos[0]-1][self.pos[1]] == " " or self.maze[self.pos[0]-1][self.pos[1]] == "e":
            self.pos[0] -= 1
    def MoveEast(self):
        if self.maze[self.pos[0]][self.pos[1]+1] == " " or self.maze[self.pos[0]][self.pos[1]+1] == "e":
            self.pos[1] +=1
    def MoveSouth(self):
        if self.maze[self.pos[0]+1][self.pos[1]] == " " or self.maze[self.pos[0]+1][self.pos[1]] == "e":
            self.pos[0] += 1
    def MoveWest(self):
        if self.maze[self.pos[0]][self.pos[1]-1] == " " or self.maze[self.pos[0]][self.pos[1]-1] == "e":
            self.pos[1] -= 1

    def GetPos(self):
        return self.pos

def MazeGenerator(size, io=None):
    maze = []

    if io == None:
        inSide = _random.randint(0,3)
        inPos = (_random.randint(0,((size-3)/2))*2)+1
        outSide = _random.randint(0,3)
        outPos = (_random.randint(0,((size-3)/2))*2)+1

        while True:
            if inSide == outSide or inPos == outPos:
                inSide = _random.randint(0,3)
                inPos = (_random.randint(0,((size-3)/2))*2)+1
                outSide = _random.randint(0,3)
                outPos = (_random.randint(0,((size-3)/2))*2)+1
            else:
                break

        io = [inSide, inPos, outSide, outPos]

    #Create Grid
    for i in range(0,size):
        maze.append([])
        for x in range(0,size):
            if i == 0 or i == size-1 or x == 0 or x == size-1:
                maze[i].append("#")
            elif i%2 == 0 or x%2 == 0:
                maze[i].append("#")
            else:
                maze[i].append("o")
    
    #print(io, "\n")

    #Add entrance and exit
    if io[0] == 0: #N
        maze[io[1]][0] = "s"
        startPos = [io[1], 1]
    elif io[0] == 1: #E
        maze[size-1][io[1]] = "s"
        startPos = [size-2, io[1]]
    elif io[0] == 2: #S
        maze[io[1]][size-1] = "s"
        startPos = [io[1], size-2]
    elif io[0] == 3: #W
        maze[0][io[1]] = "s"
        startPos = [1, io[1]]
    
    if io[2] == 0: #N
        maze[io[3]][0] = "e"
    elif io[2] == 1: #E
        maze[size-1][io[3]] = "e"
    elif io[2] == 2: #S
        maze[io[3]][size-1] = "e"
    elif io[2] == 3: #W
        maze[0][io[3]] = "e"
    
    PrintMaze(maze, size)

    #Start Plotting Paths
    maze = CreatePath(maze, size, startPos)

    
    window.fill((60, 80, 38)) #Clears the screen

    tileSize = resolution[1]/size

    columnNum = 0
    for column in maze:
        rowNum = 0
        for tile in column:
            if tile == "#":
                colour = (0, 0, 0)
            elif tile == "o":
                colour = (255, 255, 255)
            elif tile == " ":
                colour = (60, 80, 38)
            elif tile == "s":
                colour = (0, 255 ,0)
            elif tile == "e":
                colour = (255, 0, 0)
            pygame.draw.rect(window, colour, pygame.Rect((resolution[0]-resolution[1])/2+(rowNum*tileSize), columnNum*tileSize, tileSize, tileSize))

            rowNum+=1
        columnNum+=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Check if user is trying to exit the game
            quit()

    pygame.display.update()
    #clock.tick(30)

    MazeGame(maze, size, startPos)

    return maze

def CreatePath(maze, size, pos):
    
    window.fill((60, 80, 38)) #Clears the screen

    tileSize = resolution[1]/size

    columnNum = 0
    for column in maze:
        rowNum = 0
        for tile in column:
            if tile == "#":
                colour = (0, 0, 0)
            elif tile == "o":
                colour = (255, 255, 255)
            elif tile == " ":
                colour = (60, 80, 38)
            elif tile == "s":
                colour = (0, 255 ,0)
            elif tile == "e":
                colour = (255, 0, 0)
            pygame.draw.rect(window, colour, pygame.Rect((resolution[0]-resolution[1])/2+(rowNum*tileSize), columnNum*tileSize, tileSize, tileSize))

            rowNum+=1
        columnNum+=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Check if user is trying to exit the game
            quit()

    pygame.display.update()
    #clock.tick(30)
    
    #PrintMaze(maze, size)
    #print(pos)
    while True:
        availabilityDict = {"N":True, "E":True, "S":True, "W":True}
        availableSides = 4

        #Check which sides are available
        #Check if the space is on the edge
        if pos[0] == 1:
            availabilityDict["N"] = False
            availableSides -= 1
        if pos[0] == size-2:
            availabilityDict["S"] = False
            availableSides -= 1
        if pos[1] == 1:
            availabilityDict["W"] = False
            availableSides -= 1
        if pos[1] == size-2:
            availabilityDict["E"] = False
            availableSides -= 1

        #print(availabilityDict)

        #Check if there is a path already there
        if availabilityDict["N"] == True:
            if maze[pos[0]-2][pos[1]] == " ":
                availabilityDict["N"] = False
                availableSides -= 1
        
        if availabilityDict["E"] == True:
            if maze[pos[0]][pos[1]+2] == " ":
                availabilityDict["E"] = False
                availableSides -= 1
        
        if availabilityDict["S"] == True:
            if maze[pos[0]+2][pos[1]] == " ":
                availabilityDict["S"] = False
                availableSides -= 1
        
        if availabilityDict["W"] == True:
            if maze[pos[0]][pos[1]-2] == " ":
                availabilityDict["W"] = False
                availableSides -= 1

        #print(availabilityDict)

        #Start making paths
        #Pick side from available ones
        if availableSides:
            side = _random.randint(1, 4)
            while True:
                if side == 1 and availabilityDict["N"] == True:
                    break
                if side == 2 and availabilityDict["E"] == True:
                    break
                if side == 3 and availabilityDict["S"] == True:
                    break
                if side == 4 and availabilityDict["W"] == True:
                    break
                side = _random.randint(1, 4)
        else:
            maze[pos[0]][pos[1]] = " "
            return maze

        #print(side)

        if side == 1: #N
            maze[pos[0]][pos[1]] = " "
            maze[pos[0]-1][pos[1]] = " "
            CreatePath(maze, size, [pos[0]-2, pos[1]])
        elif side == 2: #E
            maze[pos[0]][pos[1]] = " "
            maze[pos[0]][pos[1]+1] = " "
            CreatePath(maze, size, [pos[0], pos[1]+2])
        elif side == 3: #S
            maze[pos[0]][pos[1]] = " "
            maze[pos[0]+1][pos[1]] = " "
            CreatePath(maze, size, [pos[0]+2, pos[1]])
        elif side == 4: #W
            maze[pos[0]][pos[1]] = " "
            maze[pos[0]][pos[1]-1] = " "
            CreatePath(maze, size, [pos[0], pos[1]-2])

def PrintMaze(maze, size):
    for i in range(0,size):
        output = ""
        for x in range(0,size):
            output += maze[i][x]
        print(output)

def MazeGame(maze, size, startPos):
    player = Player(startPos, maze, size)

    while True:
        window.fill((60, 80, 38)) #Clears the screen

        tileSize = resolution[1]/size

        columnNum = 0
        for column in maze:
            rowNum = 0
            for tile in column:
                if tile == "#":
                    colour = (0, 0, 0)
                elif tile == "o":
                    colour = (255, 255, 255)
                elif tile == " ":
                    colour = (60, 80, 38)
                elif tile == "s":
                    colour = (0, 255 ,0)
                elif tile == "e":
                    colour = (255, 0, 0)
                pygame.draw.rect(window, colour, pygame.Rect((resolution[0]-resolution[1])/2+(rowNum*tileSize), columnNum*tileSize, tileSize, tileSize))

                rowNum+=1
            columnNum+=1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Check if user is trying to exit the game
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.MoveNorth()

                if event.key == pygame.K_s:
                    player.MoveSouth()

                if event.key == pygame.K_a:
                    player.MoveWest()

                if event.key == pygame.K_d:
                    player.MoveEast()
        
        pygame.draw.rect(window, (69, 0, 69), pygame.Rect((resolution[0]-resolution[1])/2+(player.GetPos()[1]*tileSize), player.GetPos()[0]*tileSize, tileSize, tileSize))

        if maze[player.GetPos()[0]][player.GetPos()[1]] == "e":
            print("Well done")
            quit()

        pygame.display.update()

if __name__ == "__main__":
    size = 9

    inSide = _random.randint(0,3)
    inPos = (_random.randint(0,((size-3)/2))*2)+1
    outSide = _random.randint(0,3)
    outPos = (_random.randint(0,((size-3)/2))*2)+1

    while True:
        if inSide == outSide or inPos == outPos:
            inSide = _random.randint(0,3)
            inPos = (_random.randint(0,((size-3)/2))*2)+1
            outSide = _random.randint(0,3)
            outPos = (_random.randint(0,((size-3)/2))*2)+1
        else:
            break

    io = [inSide, inPos, outSide, outPos]
    MazeGenerator(size, io)

"""
def Main(maze):
    #Main game loop to run the pygame window

    while True:
        window.fill((60, 80, 38)) #Clears the screen

        tileSize = resolution[1]/size

        columnNum = 0
        for column in maze:
            rowNum = 0
            for tile in column:
                if tile == "#":
                    colour = (0, 0, 0)
                elif tile == "o":
                    colour = (255, 255, 255)
                elif tile == " ":
                    colour = (60, 80, 38)
                pygame.draw.rect(window, colour, pygame.Rect(rowNum*tileSize, columnNum*tileSize, tileSize, tileSize))

                rowNum+=1
            columnNum+=1

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Check if user is trying to exit the game
                quit()

        pygame.display.update()
        #clock.tick(30)

size = 21
Main(MazeGenerator.MazeGenerator(size))
"""
