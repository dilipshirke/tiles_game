import pygame
from pygame.locals import *
import sys
import random

# Predefined colors
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (102, 178, 255)
INDIGO = (0, 0, 255)
VIOLATE = (25, 0, 51)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLATE]

FPS = 30
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
BOARD_WIDTH, BOARD_HEIGHT = 160, 160
tilePosOffset = [320, 120]

pygame.init()
font = pygame.font.SysFont("Verdana", 20)
font_small = pygame.font.SysFont("Verdana", 12)
matched = font.render("YOU WON!", True, GREEN)
tryagain = font.render("TRY AGAIN!", True, RED)
atbeginning = font_small.render('At the beginning : ', True, BLACK)
newGame = font_small.render('NewGame', True, GREEN)
replayImage = pygame.image.load("restartGame.png")
reboot = pygame.image.load("newGame.png")

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Tiles")
Tile1 = pygame.Surface((60, 60))
Tile2 = pygame.Surface((20, 20))

def getRandomTiles(difficulty="medium"):
    # Generate a list of random tile indices based on difficulty level.
    n = {"easy": 2, "medium": 4, "hard": 8}.get(difficulty, 4)
    return [random.randint(0, 6) for _ in range(n * n)]

def minDist(arr, n, t1, t2):
    # Calculate the minimum circular distance between two tile indices in arr.
    x_pos = arr.index(t1)
    y_pos = arr.index(t2)
    x = y = 0
    for _ in range(n):
        if arr[x_pos] == arr[y_pos]:
            break
        x += 1
        y_pos = (y_pos + 1) % n
    y_pos = arr.index(t2)
    for _ in range(n):
        if arr[x_pos] == arr[y_pos]:
            break
        y += 1
        y_pos = (y_pos - 1) % n
    return min(x, y)

def getBestScore(ltiles):
    # Compute the best possible score for a given tile arrangement.
    ltiles = sorted(ltiles)
    commonTile = max(set(ltiles), key=ltiles.count)
    ltiles.remove(commonTile)
    return sum(minDist(list(range(7)), 7, commonTile, n) for n in ltiles)

def updateScore(surface, bscore, uscore):
    # Render and display the current and best scores on the surface.
    scores = font_small.render(f"YOUR SCORE : {uscore}", True, BLACK)
    bsSurface = font_small.render(f"BEST SCORE : {bscore}", True, BLACK)
    surface.blit(bsSurface, (10, 10))
    surface.blit(scores, (10, 30))

def displayTile0(surface, frame, difficulty="medium"):
    # Display the initial reference tiles on the left side of the screen.
    x, y = 20, 140
    count = {"medium": 4, "expert": 8}.get(difficulty, 2)
    surface.blit(atbeginning, (x, y - 20))
    t = 0
    for i in range(count):
        for j in range(count):
            Tile2.fill(COLOR[frame[t]])
            surface.blit(Tile2, (x + j * 20, y + i * 20))
            t += 1

def displayCurrentFrame(surface, frame, boundries, difficulty="medium"):
    # Display the current state of the main tile grid.
    t = 0
    x0, y0 = boundries[0][0]
    for i in range(4):
        for j in range(4):
            Tile1.fill(COLOR[frame[t]])
            surface.blit(Tile1, (x0 + j * 60, y0 + i * 60))
            t += 1

def displayRefBar(surface):
    # Display a reference bar showing all possible tile colors.
    x, y = 20, 370
    refTilesSurf = pygame.Surface((20, 25))
    forref = font_small.render('For reference : ', True, BLACK)
    surface.blit(forref, (20, y))
    for i in range(7):
        refTilesSurf.fill(COLOR[i])
        surface.blit(refTilesSurf, (x + i * 20, y + 20))

def display(surface, frame0_tiles, currentFrame, flag, score, bestscore, boundries):
    # Draw all game elements and update the display.
    surface.fill(WHITE)
    surface.blit(replayImage, (SCREEN_WIDTH - 32, 10))
    surface.blit(reboot, (SCREEN_WIDTH - 64, 10))
    displayTile0(surface, frame0_tiles, "medium")
    displayCurrentFrame(surface, currentFrame, boundries)
    displayRefBar(surface)
    updateScore(surface, bestscore, score)
    if flag == 1:
        surface.blit(matched, (320, 370))
        surface.blit(newGame, (320, 390))
    elif flag == -1:
        surface.blit(tryagain, (320, 370))
    pygame.display.update()
    FramePerSec.tick(FPS)

def getTile(mousePos, keyPressed, boundries):
    # Identify which tile was clicked based on mouse position.
    for n, (lower, upper) in boundries.items():
        if lower[0] <= mousePos[0] <= upper[0] and lower[1] <= mousePos[1] <= upper[1]:
            return n

def isAllTilesColorMatched(tiles):
    # Check if all tiles have the same color.
    return int(len(set(COLOR[tile] for tile in tiles)) == 1)

def gameLoop(tiles, boundries, bestscore):
    # Main game loop handling user input and game state.
    flag = score = 0
    while flag != 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                keyPressed = pygame.mouse.get_pressed()
                tileIdentified = getTile(mousePos, keyPressed, boundries)
                if SCREEN_WIDTH - 68 <= mousePos[0] <= SCREEN_WIDTH and 4 <= mousePos[1] <= 68:
                    return 1
                elif any(keyPressed):
                    if tileIdentified is None:
                        continue

                    tiles[tileIdentified] += 1 if keyPressed[0] else -1
                    tiles[tileIdentified] = (0 if(tiles[tileIdentified] > 6) else ( 6 if(tiles[tileIdentified] < 0) else tiles[tileIdentified]))     
                    score += 1
        currentframe = tiles[:16]
        flag = isAllTilesColorMatched(tiles)
        if score > bestscore:
            flag = -1
        frame0_tiles = tiles[:]
        display(DISPLAYSURF, frame0_tiles, currentframe, flag, score, bestscore, boundries)
        if flag == 1:
            return 1
        elif flag == -1:
            print("You lost!", flag, score)
            return -1
    return flag

def getTileBoundries(difficulty="medium"):
    """
    Returns a dictionary mapping tile indices to their screen coordinate boundaries.
    The boundaries are used for detecting mouse clicks on tiles.
    The number of tiles per row/column is determined by the difficulty level.
    Each entry in the dictionary is of the form:
        tile_index: (lower_left_corner, upper_right_corner)
    """
    # ...existing code...
    boundries = {}
    noTilesInRow = {"medium": 4, "expert": 8}.get(difficulty, 2)
    tileSize = [60, 60]
    tileNos = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    count = 0
    for x in range(noTilesInRow):
        for y in range(noTilesInRow):
            lower = [int(x * tileSize[0]) + tilePosOffset[0], int(y * tileSize[1]) + tilePosOffset[1]]
            upper = [int((x + 1) * tileSize[0]) + tilePosOffset[0], int((y + 1) * tileSize[1]) + tilePosOffset[1]]
            boundries[tileNos[count]] = (lower, upper)
            count += 1
    return boundries

def main():
    # Entry point for the game; manages game state and restarts.
    tiles = getRandomTiles("medium")
    frame0_tiles = tiles[:]
    bscore = getBestScore(tiles)
    boundries = getTileBoundries("medium")
    while True:
        print("New Game Started!")
        flag = gameLoop(tiles, boundries, bscore)
        if flag == 0:
            tiles = getRandomTiles("medium")
            bscore = getBestScore(tiles)
        elif flag == -1:
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousePos = pygame.mouse.get_pos()
                        keyPressed = pygame.mouse.get_pressed()
                        if SCREEN_WIDTH - 68 <= mousePos[0] <= SCREEN_WIDTH and 4 <= mousePos[1] <= 68 and any(keyPressed):
                            tiles = frame0_tiles[:]
                            bscore = getBestScore(frame0_tiles)
                            boundries = getTileBoundries("medium")
                            break
                else:
                    continue
                break
        elif flag == 1:
            # Wait for mouse event on "New Game" button before starting a new game
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousePos = pygame.mouse.get_pos()
                        keyPressed = pygame.mouse.get_pressed()
                        if SCREEN_WIDTH - 68 <= mousePos[0] <= SCREEN_WIDTH and 4 <= mousePos[1] <= 68 and any(keyPressed):
                            tiles = getRandomTiles("medium")
                            bscore = getBestScore(tiles)
                            boundries = getTileBoundries("medium")
                            break
                else:
                    continue
                break
        else:
            print("Game Over!")
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousePos = pygame.mouse.get_pos()
                        keyPressed = pygame.mouse.get_pressed()
                        if SCREEN_WIDTH - 68 <= mousePos[0] <= SCREEN_WIDTH and 4 <= mousePos[1] <= 68 and any(keyPressed):
                            tiles = getRandomTiles("medium")
                            bscore = getBestScore(tiles)
                            boundries = getTileBoundries("medium")
                            break
                else:
                    continue
                break

if __name__ == "__main__":
    main()