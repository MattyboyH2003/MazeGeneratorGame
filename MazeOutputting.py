import pygame
import sys

def Initialize():
    sys.setrecursionlimit(100000)

    #Pygame Things
    pygame.init()
    resolution = (1280, 720)
    pygame.display.set_caption("Maze Generator")
    window = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    return [window, resolution, clock]

def UpdateScreen(pygameList, maze, size, clockTick = 0):
    pygameList[0].fill((60, 80, 38)) #Clears the screen

    tileSize = pygameList[1][1]/size

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
            pygame.draw.rect(pygameList[0], colour, pygame.Rect((pygameList[1][0]-pygameList[1][1])/2+(rowNum*tileSize), columnNum*tileSize, tileSize, tileSize))

            rowNum+=1
        columnNum+=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Check if user is trying to exit the game
            quit()

    pygame.display.update()
    pygameList[2].tick(clockTick)

def PrintMaze(maze, size = None):
    size = len(maze)

    for i in range(0,size):
        output = ""
        for x in range(0,size):
            output += maze[i][x]
        print(output)
