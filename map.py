from util import randbool, randcell, riverflow, new_river, rand_num

CELL_TYPES = "🟩🌳🌊🏥🔧🔥"
TREE_BONUS = 100
UPGRADE_COST = 500
LIFE_COST = 1000


class Map:
    
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range (w)] for j in range (h)]
        self.generate_forest(7, 10)
        self.generate_river(10)
        self.generate_river(20)
        self.generate_upgrade_shop()
        self.generate_workshop()

    def checkbounds(self, x, y):
        if (x < 0 or y < 0) or (x >= self.h or y >= self.w):
            return False
        else:
            return True

    def print_map(self, helico, clouds):
        print("🟦" * (self.w + 2))
        for ri in range(self.h):
            print("🟦", end="")
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if (clouds.cells[ri][ci] == 1):
                    print("☁️ ", end="")
                elif (clouds.cells[ri][ci] == 2):
                    print("⚡", end="")
                    if cell == 2 and randbool(1, 5):
                        cell = 5
                elif (clouds.cells[ri][ci] == 3):
                    print("🌧️ ", end="")
                    if cell == 5 and randbool(4, 6):
                        cell = 2
                elif (helico.x == ri and helico.y == ci):
                    print("🚁", end="")
                elif cell >= 0 and cell <= len(CELL_TYPES):
                    print(CELL_TYPES[cell], end="") 
            print("🟦")
        print("🟦" * (self.w + 2))

    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if randbool(r, mxr):
                    self.cells[ri][ci] = 1

    def generate_river(self, l):
        rc = randcell(self.w, self.h)
        for i in range(len(self.cells)):                        # проверяю есть ли уже река на карте, чтобы новая река генерировалась не рядом с существующей
            for j in range(len(self.cells[i])):
                if self.cells[i][j] == 2:
                    if (i not in range(1, self.w - 1)) or (j not in range(1, self.h - 1)):
                        rc = new_river(i, j, self.w, self.h)
        av = [self.w - 1, 0, self.h - 1]        
        if (rc[0] in av[0:2]) and (rc[1] not in av[1:3]):       # проверяю чтобы река начиналась у края карты
            rx, ry = rc[0], rc[1]
            self.cells[rx][ry] = 2
        elif (rc[0] not in av[0:2]) and (rc[1] in av[1:3]):
            rx, ry = rc[0], rc[1]
            self.cells[rx][ry] = 2
        else:
            return self.generate_river(l)
        rs=(rx, ry)                                             # координаты начала реки
        while l-1 > 0:
            rc2 = riverflow(rx, ry, self.w, self.h, rs)
            rx2, ry2 = rc2[0], rc2[1]
            if self.cells[rx2][ry2] != 2:                       # чтобы не вставала на местоб уже занятое рекой
                self.cells[rx2][ry2] = 2
                rx, ry = rx2, ry2
                l -= 1

    def grow_up_tree(self):
        c = randcell(self.w, self.h) 
        cx, cy = c[0], c[1]
        if (self.checkbounds(cx, cy)) and (self.cells[cx][cy] == 0):
            self.cells[cx][cy] = 1
        else:
            return self.grow_up_tree()

    def add_fire(self): 
        c = randcell(self.w, self.h) 
        cx, cy = c[0], c[1]
        if (self.checkbounds(cx, cy)) and (self.cells[cx][cy] == 1):
            self.cells[cx][cy] = 5
        else:
            return self.add_fire()

    def update_fires(self, helico, r = 5, mxr = 10): 
        for ri in range(self.h):
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if (cell == 5) and (randbool(4, 8)):          # огонь не обязательно затухает
                    self.cells[ri][ci] = 0
                    helico.score -= TREE_BONUS
                    if helico.score == -1000:
                        helico.game_over()
                    f1 = [(ri + 1, ci), (ri - 1, ci), (ri, ci + 1), (ri, ci - 1)]                         # координаты соседних клеток
                    for i in range(len(f1)):
                        if (self.checkbounds(f1[i][0], f1[i][1])) and (self.cells[f1[i][0]][f1[i][1]] == 1):  # проверяю чтобы клетка не выходила за дипазон и содержала лес
                            if randbool(3, 6):                                                                # вероятность распространения огня
                                self.cells[f1[i][0]][f1[i][1]] = 5                                            # поджигаю
        if randbool(5, 10):
            self.add_fire()
        if randbool(2, 10):
            self.add_fire()

    def generate_upgrade_shop(self):
        c = randcell(self.w, self.h) 
        cy, cx = c[0], c[1]
        if (self.cells[cx][cy] == 0) or (self.cells[cx][cy] == 1):     # чтобы вставал на место поля или леса
            self.cells[cx][cy] = 4
        else:
            return self.generate_upgrade_shop()

    def generate_workshop(self):
        c = randcell(self.w, self.h) 
        cy, cx = c[0], c[1]
        if (self.cells[cx][cy] == 0) or (self.cells[cx][cy] == 1):     # чтобы вставал на место поля или леса
            self.cells[cx][cy] = 3
        else:
            return self.generate_workshop()          

    def process_helicopter(self, helico, clouds):
        c = self.cells[helico.x][helico.y]
        d = clouds.cells[helico.x][helico.y]
        if c == 2:
            helico.tank = helico.mxtank
        if c == 5 and helico.tank > 0:
            helico.tank -= 1
            helico.score += TREE_BONUS
            self.cells[helico.x][helico.y] = 1
        if (c == 4) and (helico.score >= UPGRADE_COST) and (helico.mxtank < 5):
            helico.mxtank +=1
            helico.score -= UPGRADE_COST
        if (c == 3) and (helico.score >= LIFE_COST) and (helico.lives < helico.mxlives):
            helico.lives += 1000
            if helico.lives > helico.mxlives:
                helico.lives = helico.mxlives
            helico.score -= LIFE_COST
        if (d == 2):
            helico.lives -= 10
            if helico.lives == 0:
                helico.game_over()

    def export_data(self):
        return{"cells": self.cells}

    def import_data(self, data):
       self.cells = data["cells"] or [[0 for i in range(self.w)] for j in range(self.h)]