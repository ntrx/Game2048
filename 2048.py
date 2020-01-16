import random
from sys import exit
from copy import deepcopy
import pygame as pg
from pygame.locals import *
import os
from time import strftime, gmtime
 
table = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
 
pg.init()

width = 445
height = 575

scr = pg.display.set_mode((width, height), 0, 32)
pg.display.set_caption("Game 2048")
background = pg.image.load(os.path.join('background.png'))
score = 0

black   = (0,0,0)
gold    =  (255,215,0)
green = (51,102,0)
gray    = (211,211,211)
white = (255,255,255)

time = strftime("%H%M", gmtime())
if time>="0600" and time<="1159":
    print("MODE: Morning, blue palette")
    colors = {
        0: white,
        2: (239,239,255),
        4: (223,223,255),
        8: (207,207,255),
        16: (191,191,255),
        32: (175,175,255),
        64: (159,159,255),
        128: (143,143,255),
        256: (127,127,255),
        512: (111,111,255),
        1024: (95,95,255),
        2048: (79,79,255),
        4096: (63,63,255),
        8192: (47,47,255),
        16384: (31,31,255),
        32768: (15,15,255),
        65536: (0,0,255),
    }
if time>="1200" and time<="1759":
    print("MODE: Afternoon, green palette")
    colors = {
        0: white,
        2: (239,247,239),
        4: (223,239,223),
        8: (207,231,207),
        16: (191,223,191),
        32: (175,215,175),
        64: (159,207,159),
        128: (143,199,143),
        256: (127,191,127),
        512: (111,183,111),
        1024: (95,175,95),
        2048: (79,167,79),
        4096: (63,159,63),
        8192: (47,151,47),
        16384: (31,143,31),
        32768: (15,135,15),
        65536: green,
    }
if time>="1800" and time<="2359":
    print("MODE: Evening, red palette")
    colors = {
        0: white,
        2: (255,238,238),
        4: (255,221,221),
        8: (255,204,204),
        16: (255,187,187),
        32: (255,170,170),
        64: (255,153,153),
        128: (255,136,136),
        256: (255,119,119),
        512: (255,102,102),
        1024: (255,85,85),
        2048: (255,68,68),
        4096: (255,51,51),
        8192: (255,34,34),
        16384: (255,17,17),
        32768: (255,15,15),
        65536: (255,0,0),
    }
if time>="0000" and time<="0559":
    print("MODE: Night, black palette")
    colors = {
        0: white,
        2: (239,239,239),
        4: (223,223,223),
        8: (207,207,207),
        16: (191,191,191),
        32: (175,175,175),
        64: (159,159,159),
        128: (143,143,143),
        256: (127,127,127),
        512: (111,111,111),
        1024: (95,95,95),
        2048: (79,79,79),
        4096: (63,63,63),
        8192: (47,47,47),
        16384: (31,31,31),
        32768: (15,15,15),
        65536: black,
    }


class Box:
    def __init__(self, topleft, text, color):
        self.topleft = topleft
        self.text = text
        self.color = color
    def render(self, surface, height):
        size = 100
        x, y = self.topleft
        pg.draw.rect(surface, self.color, (x, y, size, size))
        font     = pg.font.Font(None, height)
        text_surface = font.render(self.text, True, black)
        text_rect    = text_surface.get_rect()
        text_rect.center = (x+size / 2, y+size / 2)
        surface.blit(text_surface, text_rect)
 
def init_box():
    global table
 
    x = 20
    y = 120
    size = 405
    
    pg.draw.rect(scr, black, (x, y, size, size))
    x += 1
    y += 1
    
    for i in range(4):
        for j in range(4):
            index = table[i][j]
            if index == 0:
                text = ""
            else:
                text = str(index)
            if index > 65536: 
                index = 65536
            color = colors[index]
            box = Box((x, y), text, color)
            if index<=8:
                box.render(scr,100)
            elif index<=64:
                box.render(scr,80)
            elif index<=512:
                box.render(scr,60)
            elif index<=8192:
                box.render(scr,40)
            elif index<=65536:
                box.render(scr,20)
            x += 101
        x = 21
        y += 101
 
 
def generate():
    line = []
    for i in range(4):
        for j in range(4):
            if table[i][j] == 0:
                line.append((i, j))
    m = random.choice(line)
    line.remove(m)
    value = random.uniform(0, 1)
    if value < 0.1:
        table[m[0]][m[1]] = 4
    else:
        table[m[0]][m[1]] = 2

 
def init_table():
    for i in range(2):
        generate()
 
def proceed(n):
    global score
    line = [0, 0, 0, 0]
    work = []
    for i in n:
        if i != 0:
            work.append(i)
    length = len(work)
    if length == 4:
        if work[0] == work[1]:
            line[0] = work[0] + work[1]
            score += line[0]
            if work[2] == work[3]:
                line[1] = work[2] + work[3]
                score += line[1]
            else:
                line[1] = work[2]
                line[2] = work[3]
        elif work[1] == work[2]:
            line[0] = work[0]
            line[1] = work[1] + work[2]
            line[2] = work[3]
            score += line[1]
        elif work[2] == work[3]:
            line[0] = work[0]
            line[1] = work[1]
            line[2] = work[2] + work[3]
            score += line[2]
        else:
            for i in range(length):
                line[i] = work[i]
    elif length == 3:
        if work[0] == work[1]:
            line[0] = work[0] + work[1]
            line[1] = work[2]
            score += line[0]
        elif work[1] == work[2]:
            line[0] = work[0]
            line[1] = work[1] + work[2]
            score += line[1]
        else:
            for i in range(length):
                line[i] = work[i]
    elif length == 2:
        if work[0] == work[1]:
            line[0] = work[0] + work[1]
            score += line[0]
        else:
            for i in range(length):
                line[i] = work[i]
    elif length == 1:
        line[0] = work[0]
    else:
        pass
    return line
 
def move_left():
    for i in range(4):
        tmp = proceed(table[i])
        for j in range(4):
            table[i][j] = tmp[j]

def move_up():
    for i in range(4):
        to_comb = []
        for j in range(4):
            to_comb.append(table[j][i])
        tmp = proceed(to_comb)
        for k in range(4):
            table[k][i] = tmp[k]
     
def move_right():
    for i in range(4):
        tmp = proceed(table[i][::-1])
        for j in range(4):
            table[i][3-j] = tmp[j]
 
def move_down():
    for i in range(4):
        to_comb = []
        for j in range(4):
            to_comb.append(table[3-j][i])
        tmp = proceed(to_comb)
        for k in range(4):
            table[3-k][i] = tmp[k]

def caption(msg, color, height):   
    font = pg.font.Font(None, height)
    text = font.render(msg, True, color)
    text = text.convert_alpha()
    return text
 
def if_end():
    for i in range(4):
        for j in range(4):
            if table[i][j] == 0:
                return False
 
    for i in range(4):
        for j in range(3):
            if table[i][j] == table[i][j+1]:
                return False
 
    for i in range(3):
        for j in range(4):
            if table[i][j] == table[i+1][j]:
                return False
 
    return True
 
def file_load():
    try:
        f = open('best.txt', 'r')
        best = int(f.read())
        f.close()
    except:
        time = strftime("%H:%M:%S", gmtime())
        print("["+time+"]: Old best result not found, makes default equiv to zero.")
        best = 0
    return best
 
def file_save(best):
    try:
        f = open('best.txt', 'w')
        f.write(str(best))
        f.close()
    except IOError:
        time = strftime("%H:%M:%S", gmtime())
        print("["+time+"]: I/O error")
        pass
 
def main():
    global score
    time = strftime("%H:%M:%S", gmtime())
    print("Started at "+time)
    print("Sizes height-", height," width-",width)
    scr.blit(background, (0, 0))
    init_table()
    newtable = deepcopy(table)
    gameover = if_end()
      
    init_box()
    scr.blit(caption("2048", height=100, color=gold), (20, 10))
 
    scr.blit(caption("Score", height=25, color=green), (250, 15))
    button1 = pg.draw.rect(scr, green, (250, 40, 60, 20))
    text1 = caption(str(score), height=25, color=gold)
    text1_rect = text1.get_rect()
    text1_rect.center = (280, 50)
    scr.blit(text1, text1_rect)
 
    scr.blit(caption("Record", height=25, color=green), (320, 15))
    button2 = pg.draw.rect(scr, green, (320, 40, 60, 20))
    best = file_load()
    if best < score:
        best = score
    text2 = caption(str(best), height=25, color=gold)
    text2_rect = text2.get_rect()
    text2_rect.center = (350, 50)
    scr.blit(text2, text2_rect)

    while True:
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                file_save(best)
                time = strftime("%H:%M:%S", gmtime())
                print("Terminated at "+time)
                pg.quit()
                exit()
            elif not gameover:
                if event.type == KEYUP and event.key == K_UP:
                    move_up()
                elif event.type == KEYUP and event.key == K_DOWN:
                    move_down()
                elif event.type == KEYUP and event.key == K_LEFT:
                    move_left()
                elif event.type == KEYUP and event.key == K_RIGHT:
                    move_right()
                if newtable != table:
                    generate()
                    newtable = deepcopy(table)
                    init_box()
                gameover = if_end()
                 
                rect1 = pg.draw.rect(scr, green, (250, 40, 60, 20))
                text1 = caption(str(score), height=25, color=gold)
                text_rect = text1.get_rect()
                text_rect.center = (280, 50)
                scr.blit(text1, text_rect)
 
                rect2 = pg.draw.rect(scr, green, (320, 40, 60, 20))
                if best < score:
                    best = score
                text2 = caption(str(best), height=25, color=gold)
                text2_rect = text2.get_rect()
                text2_rect.center = (350, 50)
                scr.blit(text2, text2_rect)
 
            else:
                file_save(best)
                scr.blit(caption("Game Over!", height=100, color=gold), (20, 288))
             
             
        pg.display.update()
 
if __name__ == "__main__":
    main()
