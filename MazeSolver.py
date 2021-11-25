import pygame

from MazeGenerator import MazeGenerator, PrintMaze
from MazeOutputting import Initialize, UpdateScreen

global PygameList
global fps

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

size = 69
fps = 0

pygameList = Initialize()

maze = MazeGenerator(size)
UpdateScreen(pygameList, maze, size, fps)

MazeSolver(maze)

while True:
    pygame.display.update()