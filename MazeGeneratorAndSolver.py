import pygame
import random
from MazeOutputting import Initialize, UpdateScreen, PrintMaze

global PygameList
global fps
global visualise


#Generator Functions

def MazeGenerator(size, io=None):
    maze = []

    if io == None:
        inSide = random.randint(0,3)
        inPos = (random.randint(0,((size-3)/2))*2)+1
        outSide = random.randint(0,3)
        outPos = (random.randint(0,((size-3)/2))*2)+1

        while True:
            if inSide == outSide or inPos == outPos:
                inSide = random.randint(0,3)
                inPos = (random.randint(0,((size-3)/2))*2)+1
                outSide = random.randint(0,3)
                outPos = (random.randint(0,((size-3)/2))*2)+1
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

    #Start Plotting Paths
    maze = CreatePath(maze, size, startPos)

    return maze

def CreatePath(maze, size, pos):
    if visualise[1] == 0 or visualise[1] == 2:
        if visualise[0] == 1:
            PrintMaze(maze)
        elif visualise[0] == 2:
            UpdateScreen(pygameList, maze, size, fps)
    
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

        #Start making paths
        #Pick side from available ones
        if availableSides:
            side = random.randint(1, 4)
            while True:
                if side == 1 and availabilityDict["N"] == True:
                    break
                if side == 2 and availabilityDict["E"] == True:
                    break
                if side == 3 and availabilityDict["S"] == True:
                    break
                if side == 4 and availabilityDict["W"] == True:
                    break
                side = random.randint(1, 4)
        else:
            maze[pos[0]][pos[1]] = " "
            return maze

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


#Solver Functions

def MazeSolver(maze, size = None, entrance = None):
    if size == None:
        size = len(maze)

    if entrance == None:
        columnNum = 0
        for column in maze:
            rowNum = 0
            for tile in column:
                if tile == "s":
                    entrance = [columnNum, rowNum]
                rowNum+=1
            columnNum+=1
    
    if entrance[0] == 0:
        startPos = [1, entrance[1]]
    elif entrance[0] == size-1:
        startPos = [size-2, entrance[1]]
    elif entrance[1] == 0:
        startPos = [entrance[0], 1]
    elif entrance[1] == size-1:
        startPos = [entrance[0], size-2]
    
    return Search(maze, startPos, size)

def Search(maze, pos, size):
    solved = False

    #Fill current position
    maze[pos[0]][pos[1]] = "o"

    if visualise[0] == 1:
        PrintMaze(maze)
    elif visualise[0] == 2:
        UpdateScreen(pygameList, maze, size, fps)
    
    #Check for adjacent exit
    if maze[pos[0]][pos[1]-1] == "e":
        return True, maze
    if maze[pos[0]][pos[1]+1] == "e":
        return True, maze
    if maze[pos[0]-1][pos[1]] == "e":
        return True, maze
    if maze[pos[0]+1][pos[1]] == "e":
        return True, maze

    #defile default availability list
    availableDict = {"N":False, "E":False, "S":False, "W":False}

    #Check which directions are free
    if maze[pos[0]][pos[1]-1] == " ":
        availableDict["E"] = True
    if maze[pos[0]][pos[1]+1] == " ":
        availableDict["W"] = True
    if maze[pos[0]-1][pos[1]] == " ":
        availableDict["N"] = True
    if maze[pos[0]+1][pos[1]] == " ":
        availableDict["S"] = True
    
    #Search each available neighboring tile
    if availableDict["N"] and not solved:
        solved, maze = Search(maze, [pos[0]-1, pos[1]], size) #Search postion 1 up
    if availableDict["E"] and not solved:
        solved, maze = Search(maze, [pos[0], pos[1]-1], size) #Search postion 1 right
    if availableDict["S"] and not solved:
        solved, maze = Search(maze, [pos[0]+1, pos[1]], size) #Search postion 1 down
    if availableDict["W"] and not solved:
        solved, maze = Search(maze, [pos[0], pos[1]+1], size) #Search postion 1 left

    if not solved:
        maze[pos[0]][pos[1]] = " " #Empty current postion
        return False, maze
    else:
        return True, maze


#Running it all

# Visualise
# 0: Only Final Text, 1: All Text, 2: Full Graphical
# 0: Only Generate, 1: Only Solve, 2: Both

visualise = [2, 0] 
size = 69
fps = 0

if visualise[0] == 2:
    pygameList = Initialize()

maze = MazeGenerator(size)

if visualise[0] == 1:
    PrintMaze(maze)
elif visualise[0] == 2:
    UpdateScreen(pygameList, maze, size, fps)

if visualise[1] == 1 or visualise[1] == 2:
    MazeSolver(maze)

if visualise[0] == 0 or visualise[0] == 1:
    PrintMaze(maze)
else:
    UpdateScreen(pygameList, maze, size, fps)
    while True:
        pygame.display.update()
