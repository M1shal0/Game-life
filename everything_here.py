import numpy as np
import cv2 as cv
from enum import IntFlag, auto


HEIGHT_FIELD = 50
WIDTH_FIELD = 50
SIZE_SQUARE = 10
THICKNESS = 1

class CellType(IntFlag):
    empty = 0
    full = auto()
    choose_square = auto()
    choose_square_full = full | choose_square

def game(start_field: list) -> list:
    field1 = [x for x in start_field]
    field2 = [[0] * (WIDTH_FIELD + 2) for _ in range(HEIGHT_FIELD + 2)]
    cnt_neibrs = 0
    for i in range(1, HEIGHT_FIELD + 1):
        for j in range(1, WIDTH_FIELD + 1):
            # if 0 < i < 4 and 0 < j < 4: 
            if field1[i - 1][j - 1] == 1:
                cnt_neibrs += 1
            if field1[i - 1][j] == 1:
                cnt_neibrs += 1
            if field1[i - 1][j + 1] == 1:
                cnt_neibrs += 1
            if field1[i][j - 1] == 1:
                cnt_neibrs += 1
            if field1[i][j + 1] == 1:
                cnt_neibrs += 1
            if field1[i + 1][j - 1] == 1:
                cnt_neibrs += 1
            if field1[i + 1][j] == 1:
                cnt_neibrs += 1
            if field1[i + 1][j + 1] == 1:
                cnt_neibrs += 1
            if field1[i][j] == 1:
                if cnt_neibrs == 2 or cnt_neibrs == 3:
                    field2[i][j] = 1
                else:
                    field2[i][j] = 0
            else:
                if cnt_neibrs == 3:
                    field2[i][j] = 1
            cnt_neibrs = 0
    return field2

def draw_game(field: list, img):
    xs = 0
    xe = SIZE_SQUARE
    ys = 0
    ye = SIZE_SQUARE
    chos_xs = 0
    chos_ys = 0
    chos_xe = 0
    chos_ye = 0
    for x in range(1, HEIGHT_FIELD + 1):
        for y in range(1, WIDTH_FIELD + 1):
            a = field[y][x]
            if a == 0:
                # img[ys:ye, xs:xe, :] = tiles[CellType.full]
                cv.rectangle(img, (xs, ys), (xe, ye), (0,0,0), THICKNESS)
            elif a == 1:
                # img[ys:ye, xs:xe, :] = tiles[CellType.empty]
                cv.rectangle(img, (xs, ys), (xe, ye), (0,0,0), -1)
            elif a == 2:
                # img[ys:ye, xs:xe, :] = tiles[CellType.choose_square]
                cv.rectangle(img, (xs, ys), (xe, ye), (255,128,0), THICKNESS)
                chos_xs = xs
                chos_ys = ys
                chos_xe = xe
                chos_ye = ye               
            elif a == 3:
                # img[ys:ye, xs:xe, :] = tiles[CellType.choose_square_full]
                cv.rectangle(img, (xs, ys), (xe, ye), (255,128,0), THICKNESS)
                cv.rectangle(img, (xs + THICKNESS, ys + THICKNESS), (xe - THICKNESS, ye - THICKNESS), (0,0,0), -1)
                chos_xs = xs
                chos_ys = ys
                chos_xe = xe
                chos_ye = ye
            ys += SIZE_SQUARE
            ye += SIZE_SQUARE
        xs += SIZE_SQUARE
        xe += SIZE_SQUARE
        ys = 0
        ye = SIZE_SQUARE
    cv.rectangle(img, (chos_xs, chos_ys), (chos_xe, chos_ye), (255,128,0), THICKNESS)
    chos_xs = 0
    chos_ys = 0
    chos_xe = 0
    chos_ye = 0

def get_start_position(field: list) -> list:
    x,y = 1, 1
    oldx, oldy = 1,1
    while True:
        img1[...] = 0
        img1.fill(255)
        draw_game(field, img1)
        cv.imshow('Get start field', img1)
        ch = cv.waitKeyEx(0)
        # get_start_position(ch)
        if ch == ord('w') or ch == 2490368:
            y = max((y - 1), 1)
        elif ch == ord('d') or ch == 2555904:
            x = min((x + 1), WIDTH_FIELD + 1)
        elif ch == ord('s') or ch == 2621440:
            y = min((y + 1), HEIGHT_FIELD + 1)
        elif ch == ord('a') or ch == 2424832:
            x = max((x - 1), 1)
        elif ch == ord(' '):
            field[y][x] = 1
        if field[oldy][oldx] == 1 or field[oldy][oldx] == 3:
            was_full = True
        else:
            was_full = False
        if was_full:
            field[oldy][oldx] = 1
        else:
            field_start[oldy][oldx] = 0
        if field[y][x] == 1:
            field[y][x] = 3
        elif field[y][x] == 0:
            field[y][x] = 2
        oldx = x
        oldy = y
        if ch == 27:
            break
    if was_full:
        field[oldy][oldx] = 1
    else:
        field_start[oldy][oldx] = 0
    return field

img = np.zeros((HEIGHT_FIELD * SIZE_SQUARE, WIDTH_FIELD * SIZE_SQUARE, 3), np.uint8)
img.fill(255)

# full = cv.imread('C:/Rabota/PythonSamples/Programming/To_write_smth/Python/Game life/Squares.png')

# tiles = {}
# tiles[CellType.empty] = full[:, 0:100, :]
# tiles[CellType.full] = full[:, 100:200, :]
# tiles[CellType.choose_square] = full[:, 200:300, :]
# tiles[CellType.choose_square_full] = full[:, 300:400, :]

field_start = [[0] * (WIDTH_FIELD + 2) for _ in range(HEIGHT_FIELD + 2)]
img1 = np.zeros((HEIGHT_FIELD * SIZE_SQUARE, WIDTH_FIELD * SIZE_SQUARE, 3), np.uint8)
img1.fill(255)

field_start = get_start_position(field_start)
output = game(field_start)
while True:
    img[...] = 0
    img.fill(255)
    draw_game(output, img)
    cv.imshow('Game life', img)
    ch = cv.waitKeyEx()
    if ch == 27:
        break
    temp = output
    output = game(output)

    
