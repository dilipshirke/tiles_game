import pygame
import pygame_gui
from pygame.locals import *
import sys
import random, time
import copy

# Predefined some colors
RED         = (255, 0, 0)
ORANGE      = (255, 128, 0)
YELLOW      = (255, 255, 0)
GREEN       = (0, 255, 0)
BLUE        = (102, 178, 255)
INDIGO      = (0, 0, 255)
VIOLATE     = (25, 0, 51)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

COLOR = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLATE]

FPS = 30
FramePerSec = pygame.time.Clock()

# Screen information
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BOARD_WIDTH = 160
BOARD_HEIGHT = 160
SCORE = 0
tileSize = [BOARD_WIDTH/2, BOARD_HEIGHT/2]
tilePosOffset = [320, 120]


pygame.init()
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 20)
font_small = pygame.font.SysFont("Verdana", 12)
matched = font.render("YOU WON!", True, GREEN)
payagain = font.render("PAY AGAIN", True, GREEN)
tryagain = font.render("TRY AGAIN!", True, RED)
tryagain1 = font_small.render("Replay", True, RED)
atbeginning = font_small.render('At the beginning : ' , True , BLACK)
replay = font_small.render('Replay' , True , BLACK)
newGame = font_small.render('NewGame' , True , GREEN)
replayImage = pygame.image.load("restartGame.png")
reboot = pygame.image.load("newGame.png")
bsSurface = font_small.render(str("BEST SCORE : ")+str(0), True, BLACK)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Tiles")
# TODO : change the tile1 size based on difficulty.
Tile1 = pygame.Surface((60, 60))
Tile2 = pygame.Surface((20, 20))



def getRandomTiles(difficulty = "medium"):
    match difficulty:
        case "easy":
            n = 2
        case "medium": 
            n = 4
        case "hard":
            n = 8
        case default:
            n = 4
    tiles = []
    for i in range(0, n):
        for j in range(0, n):
            tiles.append(random.randint(0, 6))
    return tiles

def minDist(arr, n, t1, t2) :
    x_pos = arr.index(t1)
    y_pos = arr.index(t2)
    x = 0
    y = 0
    #import pdb;pdb.set_trace()
    for i in range(n):
        if(arr[x_pos] == arr[y_pos]):            
            break
        else:
            x += 1
        
        y_pos += 1
        if(y_pos >= n): 
            y_pos = 0    
            
    x_pos = arr.index(t1)
    y_pos = arr.index(t2)
    #import pdb;pdb.set_trace()
    for i in range(n):
        if(arr[x_pos] == arr[y_pos]):
            break
        else:
            y += 1
        
        y_pos -= 1
        if(y_pos < 0): 
            y_pos = (n-1)

    #import pdb;pdb.set_trace()
    return min(x , y)

def getBestScore(ltiles):
    # Calculate best score
    #print("getBestScore")        
    ltiles.sort()
    bestsum = 0
    commonTile = max(set(ltiles), key=(ltiles).count)
    ltiles.remove(commonTile)
    for n in ltiles:
        bestsum += minDist([0, 1, 2 ,3 ,4, 5, 6], 7, commonTile, n)

    return bestsum

def updateScore(surface, bscore, uscore):
    scores = font_small.render(str("YOUR SCORE : ")+str(uscore), True, BLACK)
    bsSurface = font_small.render(str("BEST SCORE : ")+str(bscore), True, BLACK)
    surface.blit(bsSurface, (10,10))
    surface.blit(scores, (10,30))

def displayTile0(surface, frame, difficulty="medium"):
    # Tiles at the beginning    
    x = 20
    y = 140
    if(difficulty == "medium"):
        count = 4
    elif(difficulty == "expert"):
        count = 8
    else:
        count = 2

    surface.blit(atbeginning, (x,y-20))    
    t = 0 
    for i in range(0, count):
        for j in range(0, count):
            Tile2.fill(COLOR[frame[t]])
            surface.blit(Tile2, (x, y))
            t+=1            
            x += 20
        y += 20
        x = 20

    

def displayCurrentFrame(surface, frame, boundries, difficulty="medium"):
    #frame = []
         
    t = 0 
    x = boundries[0][0][0]
    y = boundries[0][0][1]
        
    for i in range(0, 4):           
        for j in range(0, 4):
            Tile1.fill(COLOR[frame[t]])
            surface.blit(Tile1, (x, y))
            x += 60
            t += 1
        y += 60
        x = boundries[0][0][0]   
 

def displayRefBar(surface):
    x = 20
    y = 370
    refTilesSurf = pygame.Surface((20, 25))
    forref = font_small.render('For reference : ' , True , BLACK)
    surface.blit(forref, (20,y))
    for i in range(0, 7):
        refTilesSurf.fill(COLOR[i])
        surface.blit(refTilesSurf, (x, y+20))
        x += 20

def display(surface, frame0_tiles, currentFrame, flag, score, bestscore, boundries):          
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(replayImage, (SCREEN_WIDTH-32, 10))
    DISPLAYSURF.blit(reboot, (SCREEN_WIDTH-64, 10))    
    displayTile0(DISPLAYSURF, frame0_tiles, "medium")

    displayCurrentFrame(surface, currentFrame, boundries)
    displayRefBar(surface)
    updateScore(surface, bestscore, score)

    if(flag==1):
        surface.blit(matched, (320,370))
        surface.blit(newGame, (320, 390))
    elif(flag == -1):
        surface.blit(tryagain, (320,370))   

    pygame.display.update()
    FramePerSec.tick(FPS)

def getTile(mousePos, keyPressed, boundries):
    count = len(boundries)        
    for n in range(0, count):
        lower = boundries[n][0]
        upper = boundries[n][1]        
        if((lower[0] <= mousePos[0] <= upper[0]) and
           (lower[1] <= mousePos[1] <= upper[1])):
            #print("tile: %d, mouse = %dx%d"%(n, mousePos[0], mousePos[1]))            
            return n
        
def isAllTilesColorMatched(tiles):
    tileColors = set()
    for tile in tiles:
        tileColors.add(COLOR[tile])    
    
    if(len(tileColors) == 1):        
        return 1
    else:
        return 0


def gameLoop(tiles, boundries, bestscore):    
    flag = 0
    score = 0
    while (flag != 1):
        for event in pygame.event.get():
            x = 320
            y = 120               
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:           
                mousePos = pygame.mouse.get_pos()            
                keyPressed = pygame.mouse.get_pressed()                
                tileIdentified = getTile(mousePos, keyPressed, boundries)
                if(mousePos[0] >= (SCREEN_WIDTH-68) and mousePos[0] <= (SCREEN_WIDTH) and mousePos[1] >= 4 and mousePos[1] <= 68):                                   
                    #print("New Game clicked")
                    return 1
                elif(keyPressed[0] or keyPressed[1] or keyPressed[2]):
                    if(tileIdentified == None):
                        #print("No tile identified")
                        continue
                    tiles[tileIdentified] += 1 if(keyPressed[0]) else -1
                    tiles[tileIdentified] = (0 if(tiles[tileIdentified] > 6) else ( 6 if(tiles[tileIdentified] < 0) else tiles[tileIdentified])) 
                    score += 1                    
                
            #print("score = ", score)                        
       
        currentframe = []
        for i in range (0, 4*4):
            currentframe.append(tiles[i])                
        
        flag = 0
        if(isAllTilesColorMatched(tiles)):
            flag = 1
        
        if(score > bestscore):
            flag = -1   
        
        frame0_tiles = copy.deepcopy(tiles) 
        display(DISPLAYSURF, frame0_tiles, currentframe, flag, score, bestscore, boundries)
        if(flag == 1):
            #print("You won!", flag, score)
            return 1 
        elif(flag == -1):
            print("You lost!", flag, score)
            #import pdb; pdb.set_trace()
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
    boundries = {}
    if difficulty == "medium":
        noTilesInRow = 4
    elif difficulty == "expert":
        noTilesInRow = 8
    else:
        noTilesInRow = 2

    tileSize = [60, 60]
    tileNos = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    count = 0
    for x in range(0, noTilesInRow):
        for y in range(0, noTilesInRow):
            lower = [int(x * tileSize[0])+tilePosOffset[0], int(y * tileSize[1])+tilePosOffset[1]]
            upper = [int((x+1) * tileSize[0])+tilePosOffset[0], int((y+1) * tileSize[1])+tilePosOffset[1]]
            boundries[tileNos[count]] = (lower, upper)
            count += 1
    
    return boundries  

def main():
    # List that is displayed while selecting the difficulty 
    difficulty = [("Easy", "Easy"), 
                  ("Medium", "Medium"), 
                  ("Expert", "Expert")]
    tiles = getRandomTiles("medium")   
    frame0_tiles = copy.deepcopy(tiles) 
    bscore = getBestScore(list(tiles))
    boundries = getTileBoundries("medium")
    reset = False
    while True:   
        print("New Game Started!")  
        flag = gameLoop(tiles, boundries, bscore)     
        if( flag == 0):
            tiles = getRandomTiles("medium")
            bscore = getBestScore(list(tiles))
        elif(flag == -1):
            # check for mouse click to reset the game
            reset = True            
            while reset:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:                        
                        mousePos = pygame.mouse.get_pos()
                        keyPressed = pygame.mouse.get_pressed()
                        if(mousePos[0] >= (SCREEN_WIDTH-68) and mousePos[0] <= (SCREEN_WIDTH) and mousePos[1] >= 4 and mousePos[1] <= 68) \
                            and (keyPressed[0] or keyPressed[1] or keyPressed[2]):
                            tiles = copy.deepcopy(frame0_tiles)
                            bscore = getBestScore(list(frame0_tiles))
                            boundries = getTileBoundries("medium")                                                    
                            reset = False                                           
            continue;         
        elif(flag == 1):            
            tiles = getRandomTiles("medium")    
            bscore = getBestScore(list(tiles))
            boundries = getTileBoundries("medium")                            
            continue;
        else:               
            print("Game Over!")                
            # wait for a mouse click to start a new game
            reset = True
            while reset:
                # dont reset in case of replay                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:                        
                        mousePos = pygame.mouse.get_pos()
                        keyPressed = pygame.mouse.get_pressed()
                        if(mousePos[0] >= (SCREEN_WIDTH-68) and mousePos[0] <= (SCREEN_WIDTH) and mousePos[1] >= 4 and mousePos[1] <= 68) \
                            and (keyPressed[0] or keyPressed[1] or keyPressed[2]):
                            reset = True
                            tiles = getRandomTiles("medium")    
                            bscore = getBestScore(list(tiles))
                            boundries = getTileBoundries("medium")                            
                            break
                    if reset:
                        break                   
                               


if __name__ == "__main__":
    
    main()

