' COLORS '
GRAY1 = (223, 230, 233)
GRAY2 = (178, 190, 195)
GRAY3 = (99, 110, 114)
GRAY4 = (45, 52, 54)
BLUE = (74, 105, 189)

' GAME SETTINGS '
FPS = 60
TITLE = "Sliding Puzzle Solver"
BGCOLOR = GRAY3
TOPLEFT = (50,100) #where the game zone begins
SCREEN_BORDER = 50
TILESIZE = 100
FONT_NAME = "Calibri"

TILESIDECOUNT = 3
WIDTH = TOPLEFT[0] +SCREEN_BORDER + TILESIZE * TILESIDECOUNT
HEIGHT = TOPLEFT[1] + SCREEN_BORDER+ TILESIZE * TILESIDECOUNT
BORDER = 2
GAMEBORDER = 5
ANIM_SPEED = 0 #goes from 0 to 2
SOLVE_DELAY = 100
NUMTOGOAL = {}
for i in range(1,TILESIDECOUNT*TILESIDECOUNT):
    NUMTOGOAL[i] = [(i-1)%TILESIDECOUNT,int((i-1)/TILESIDECOUNT)]
NUMTOGOAL[0] = [TILESIDECOUNT-1,TILESIDECOUNT-1]
