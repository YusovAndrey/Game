from random import randint as rand


def randbool(r, mxr):
    t = rand(0, mxr)
    return(t <= r)

def rand_num(x):
    n = rand(0, x)
    return(n)

def randcell(w, h):
    tw = rand(0, w - 1)
    th = rand(0, h - 1)
    return(tw, th)

def new_river(x, y, w, h):      # новая река генерируется на противоположенной стороне карты                   
    if x == 0:
        tw = rand(10, w - 1)
        th = rand(0, h - 1)
    elif x == w - 1:
        tw = rand(0, 9)
        th = rand(0, h - 1)
    elif y == 0:
        tw = rand(0, w - 1)
        th = rand(10, h - 1)
    elif y == h - 1:
        tw = rand(0, w - 1)
        th = rand(0, 9)
    return(tw, th)

def riverflow(x, y, w, h, rs): 
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    if rs[0] == 0:                                                      # чтобы река не возвращалась к началу
        del moves[0]
    elif rs[0] == w - 1:
        del moves[2]
    elif rs[1] == 0:
        del moves[3]
    elif rs[1] == h - 1:
        del moves[1]    
    t = rand(0, 2)
    dx, dy = moves[t][0], moves[t][1]
    if (x + dx in range(1, w - 1)) and (y + dy in range(1, h - 1)):     # чтобы река не шла вдоль края карты
        return(x + dx, y + dy)
    else:
        return riverflow(x, y, w, h, rs)