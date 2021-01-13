#Eric Chou 95408627
#Project #5: The Fall of the World's Own Optimist (Part 2)
# project5.py
# main program of project 5
# All sound effect downloaded from Youtube Licence Copyright clean library.
#
import sys
import pygame
import random
from columnboard import *

# gloabal settings
DEBUG = False            # output text mode or not
row, col = 12, 6         # number of rows and column
block_size = 50          # block size each block will be painted in one cell, 50 has good visual effect
cycle_time = 700         # 300 ticks (300 milli-sec per game board redraw cycle)
cycle_shift_rotate = 50  # make shift and rotate faster with shorter cycle time
cycle_normal = 700       # used to return to normal cycle time
delay = 50               # delay used to adjust animation effect
match_delay = 300        # delay time after matched blocks
faller_length = 3        # 3 blocks in a faller
colors = 4               # maximum 12 colors
gap = 3                  # gap between blocks

# graphic settings
zero = (block_size/2, block_size/2)            # first block's center point, used as a reference point for the whole cellx array
wing = block_size/2 - gap                      # half the length of a block side
width, height = col*block_size, row*block_size # window size width and height

# initialize game GUI
pygame.init()                                           # start the pygame window and event loop
root = pygame.display.set_mode((width, height))         # root surface object
pygame.display.set_caption('Prj 5: Eric Chou 95408627') # set caption of the window

# color settings: 13 colors, black reserved for clearing blocks. other colors used for blocks.
color = {'BLACK': (0, 0, 0),
         'WHITE': (255, 255, 255),
         'RED':   (255, 0, 0),
         'ORANGE':(255, 128, 0),
         'YELLOW':(255, 255, 0),
         'APPLE':(128, 255, 0),
         'GREEN':(0, 255, 0),
         'LAKE':(0, 128, 128),
         'CYAN':(0, 255, 255),
         'TEAL':(0, 128, 255),
         'PURPLE':(128, 0, 255),
         'MAGENTA':(255, 0, 255),
         'DEEPPINK':(255, 0, 128)
         }

# color_code list: quick access to the right color. This make shuffling colors easier
color_code = [color['RED'], color['ORANGE'], color['YELLOW'], color['APPLE'], color['GREEN'],
              color['LAKE'], color['CYAN'], color['TEAL'], color['PURPLE'], color['MAGENTA'], color['DEEPPINK'], color['WHITE'], color['BLACK']]

# color shuffling (To make color more random
for i in range(len(color_code)-1):
    j = random.randint(0, len(color_code)-2)
    tmp = color_code[i]
    color_code[i] = color_code[j]
    color_code[j] = tmp

# draw a block at certain array indice location with array index i and j with a color
def draw_block(i, j, color):
    global wing, root
    pygame.draw.rect(root, color, ((zero[0]-wing+j*block_size), (zero[1]-wing+i*block_size), wing*2, wing*2))

# cleas a block at certain indice location
def clear_block(i, j):
    global color, root
    draw_block(i, j, color['BLACK'])

# clear a region ia the window
def clear_region(left, top, width, height):
    global root, color
    pygame.draw.rect(root, color['BLACK'], ((left, top, width, height)))

# clear whole screen
def clear_screen():
    global root, width, height
    clear_region(0, 0, width, height)

# place cells from data model to window surface
def build_graphic_board(row, col):
    global cellx, root
    for i in range(row):
        for j in range(col):
            cellx[i][j] = cellx[i][j].upper()
            if (cellx[i][j]==" "):
                clear_block(i, j)
            else:
                color_index = ord(cellx[i][j])-ord('A')
                draw_block(i, j, color_code[color_index])

# game board data (data model)
b = 0                  # global board object
cellx = [[" " for i in range(col)] for j in range(row)]  # cell array with faller

# initialize the game board data model
def data_init():
    global b, cellx
    b = board(row, col)
    b.reset()
    cellx = b.draw(0, DEBUG)

# draw title page for this game (optional)
def draw_title_page():
    global width, height
    clear_screen()
    pygame.display.update()

    myfont = pygame.font.SysFont("Calibri", 24, True, False)
    label = myfont.render("UC Irvine", 1, color['TEAL'])
    root.blit(label, (20, height*2//3-20))
    label = myfont.render("Eric Chou, Jr.", 1, color['YELLOW'])
    root.blit(label, (44, height*2//3+10))
    label = myfont.render("ID: 95408627", 1, color['YELLOW'])
    root.blit(label, (44, height*2//3+40))

    myfont = pygame.font.SysFont("Calibri", 36, True, False)
    texton = True
    for i in range(12):
        if (texton):
            label = myfont.render("Project 5", 1, color['ORANGE'])
            root.blit(label, (20, 48))
            texton = False
        else:
            pygame.draw.rect(root, (0, 0, 0), ((0, 0, width, height//3+20)))
            texton = True

        pygame.display.update()
        pygame.time.delay(200)
    pygame.time.delay(200)
    clear_screen()
    pygame.display.update()
    myfont = pygame.font.SysFont("Calibri", 30, True, False)
    label = myfont.render("Starting Soon...", 1, color['YELLOW'])
    root.blit(label, (20, height//3))
    pygame.display.update()
    pygame.time.delay(2400)
    clear_screen()
    pygame.display.update()

# draw game over page (optional)
def draw_game_over_page():
    global width, height
    clear_screen()
    pygame.display.update()
    myfont = pygame.font.SysFont("Calibri", 48, True, False)
    label = myfont.render("Game Over....", 1, color['RED'])
    root.blit(label, (8, height//3))
    pygame.display.update()

def main():
    global root, b, row, col, block_size, width, height, cycle_time, delay, cellx
    draw_title_page()

    # initialize game board and other data
    data_init()
    game_over = False

    while True:
        if (b.no_faller()):
            j = random.randint(0, col-1)                 # random column for faller
            blocks = [i for i in range(faller_length)]
            for i in range(faller_length):
                blocks[i] = chr(ord('A')+random.randint(0, colors-1))  # generation of random character
            fobj = fall_object(j, blocks, row)
            b.fobj = fobj

        drop_success = True
        no_op = True

        for event in pygame.event.get((pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT)):
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_DOWN:
                #    cycle_time = delay
                #    continue
                if event.key == pygame.K_SPACE:
                    no_op = False
                    b.fobj.rotate()
                    cycle_time = cycle_shift_rotate
                    #pygame.time.delay(delay)
                    continue
                elif event.key == pygame.K_RIGHT:
                    no_op = False
                    b.shift_right()
                    cycle_time = cycle_shift_rotate
                    #pygame.time.delay(delay)
                    continue
                elif event.key == pygame.K_LEFT:
                    no_op = False
                    b.shift_left()
                    cycle_time = cycle_shift_rotate
                    #pygame.time.delay(delay)
                    continue
            elif event.type == pygame.KEYUP:
                pass

        # when no comand within a clock cycle
        if (no_op):
            cycle_time = cycle_normal
            drop_success = b.drop()
            if (drop_success):
                cellx = b.draw(0, DEBUG)
            else:
                cellx = b.draw(0, DEBUG)

                #pygame.time.delay(delay)
                over = b.check_game()
                if (over):  # drop fail and game over
                    if (not game_over):
                        game_over = True
                        draw_game_over_page()
                        if (DEBUG): print("Game Over")

                        try:
                            pygame.mixer.music.load('game_over.mp3')
                        except:
                            pass
                        else:
                            pygame.mixer.music.play(0, 0.0)
                            pygame.time.delay(4000)
                            pygame.mixer.music.stop()

                else:  # drop fail and falling object stops.
                    cellx = b.draw(1, DEBUG)

                    b.attach()  # attach the falling object to board
                    cellx = b.draw(0, DEBUG)
                    load_success = False
                    try:
                        pygame.mixer.music.load('tada.mp3')
                    except:
                        load_success = False
                    else:
                        load_success = True

                    adjust_done = False

                    while not adjust_done:
                        adjust_done = b.adjust()
                        cellx = b.draw(0, DEBUG)
                        build_graphic_board(row, col)
                        if (load_success and not adjust_done):
                            pygame.mixer.music.play(0, 0.0)
                            pygame.time.delay(1500)
                            pygame.mixer.music.stop()
                        else:
                            pygame.time.delay(match_delay)
                        pygame.display.update()
                        #
                    cellx = b.draw(0, DEBUG)
        if (game_over): clear_screen()
        else: build_graphic_board(row, col)
        pygame.display.update()
        pygame.time.delay(cycle_time)
    pygame.quit()

if __name__== "__main__":
    main()