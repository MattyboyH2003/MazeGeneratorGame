import random as _random

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
    
    print(io, "\n")

    #Add entrance and exit
    if io[0] == 0: #N
        maze[io[1]][0] = " "
        startPos = [io[1], 1]
    elif io[0] == 1: #E
        maze[size-1][io[1]] = " "
        startPos = [size-2, io[1]]
    elif io[0] == 2: #S
        maze[io[1]][size-1] = " "
        startPos = [io[1], size-2]
    elif io[0] == 3: #W
        maze[0][io[1]] = " "
        startPos = [1, io[1]]
    
    if io[2] == 0: #N
        maze[io[3]][0] = " "
    elif io[2] == 1: #E
        maze[size-1][io[3]] = " "
    elif io[2] == 2: #S
        maze[io[3]][size-1] = " "
    elif io[2] == 3: #W
        maze[0][io[3]] = " "

    #Start Plotting Paths
    maze = CreatePath(maze, size, startPos)

    return maze

def CreatePath(maze, size, pos):

    PrintMaze(maze, size)
    print(pos)
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

        print(availabilityDict)

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

        print(availabilityDict)

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

        print(side)

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

if __name__ == "__main__":
    size = 69

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
    PrintMaze(MazeGenerator(size, io), size)
