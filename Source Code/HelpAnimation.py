import heapq
import random
import time
from utilities import *
from Draw import*

FLT_MAX = 1000000

from collections import namedtuple

Cell = namedtuple('Cell', 'x y')

def tracePath(cellDetails, dest):
    r = dest.x
    c = dest.y
    Path = list()
    while not(cellDetails[r][c].parent_x == r and cellDetails[r][c].parent_y == c):
        Path.append((Cell(r, c)))
        temp_row = cellDetails[r][c].parent_x
        temp_col = cellDetails[r][c].parent_y
        r = temp_row
        c = temp_col

    Path.append(Cell(r, c))
    while not len(Path) == 0:
        p = Path.pop()
        print("->({},{})".format(p.x, p.y))


def printPath(cellDetails, dest, matrix, i):
    r = dest.x
    c = dest.y
    while(not(cellDetails[r][c].parent_x == r and cellDetails[r][c].parent_y == c)):
        matrix[r][c] = i
        temp_row = cellDetails[r][c].parent_x
        temp_col = cellDetails[r][c].parent_y
        r = temp_row
        c = temp_col
    matrix[r][c] = i


def aStartSearch(matrix, src, dest, R, C, i):
    if (not isValidInput(matrix, src, dest, R, C)):
        return False, 0

    dx = [0, 0, 1, 1, 1, -1, -1, -1]
    dy = [-1, 1, -1, 0, 1, -1, 0, 1]

    cellDetails = [[CellDetails(-1,-1,FLT_MAX,FLT_MAX,FLT_MAX) for x in range(C)] for y in range(R)]

    curCell = src
    hNew = calculateHValue(curCell, dest)
    cellDetails[curCell.x][curCell.y] = CellDetails(curCell.x, curCell.y, hNew, 0.0, hNew)

    closedList=[[False for x in range(C)] for y in range(R)]

    openList = []
    heapq.heappush(openList, (0.0, curCell))

    while(len(openList) != 0):
        p = heapq.heappop(openList)
        curCell = p[1]
        if (closedList[curCell.x][curCell.y] == True):
            continue
        closedList[curCell.x][curCell.y] = True

        for d in range(8):
            nextCell = Cell(curCell.x + dx[d], curCell.y + dy[d])
            if isValid(nextCell, R, C):
                if isDestination(nextCell, dest):
                    gNew = cellDetails[curCell.x][curCell.y].g + (1.0 if (dx[d] == 0 or dy[d] == 0) else 1.5)
                    cellDetails[nextCell.x][nextCell.y] = CellDetails(curCell.x, curCell.y, gNew, gNew, 0.0)
                    # tracePath(cellDetails, dest)
                    printPath(cellDetails, dest, matrix, i)
                    return True, gNew
                elif not closedList[nextCell.x][nextCell.y] and canMove(matrix, curCell, nextCell):
                    gNew = cellDetails[curCell.x][curCell.y].g + (1.0 if (dx[d] == 0 or dy[d] == 0) else 1.5)
                    hNew = calculateHValue(nextCell, dest)
                    fNew = gNew + hNew

                    if cellDetails[nextCell.x][nextCell.y].f == FLT_MAX or cellDetails[nextCell.x][nextCell.y].f > fNew:
                        heapq.heappush(openList, (fNew, nextCell))
                        cellDetails[nextCell.x][nextCell.y] = CellDetails(curCell.x, curCell.y, fNew, gNew, hNew)
    return False, 0


def printPath2(cellDetails, dest):
    result = []
    r = dest.x
    c = dest.y
    while(not(cellDetails[r][c].parent_x == r and cellDetails[r][c].parent_y == c)):
        result.insert(0, Cell(r, c))
        temp_row = cellDetails[r][c].parent_x
        temp_col = cellDetails[r][c].parent_y
        r = temp_row
        c = temp_col
    result.insert(0, Cell(r, c))
    return result


def aStartSearch2(matrix, src, dest, R, C):
    if (not isValidInput(matrix, src, dest, R, C)):
        return False, 0, []

    dx = [0, 0, 1, 1, 1, -1, -1, -1]
    dy = [-1, 1, -1, 0, 1, -1, 0, 1]

    cellDetails = [[CellDetails(-1,-1,FLT_MAX,FLT_MAX,FLT_MAX) for x in range(C)] for y in range(R)]

    curCell = src
    hNew = calculateHValue(curCell, dest)
    cellDetails[curCell.x][curCell.y] = CellDetails(curCell.x, curCell.y, hNew, 0.0, hNew)

    closedList=[[False for x in range(C)] for y in range(R)]

    openList = []
    heapq.heappush(openList, (0.0, curCell))

    while(len(openList) != 0):
        p = heapq.heappop(openList)
        curCell = p[1]
        if (closedList[curCell.x][curCell.y] == True):
            continue
        closedList[curCell.x][curCell.y] = True

        for d in range(8):
            nextCell = Cell(curCell.x + dx[d], curCell.y + dy[d])
            if isValid(nextCell, R, C):
                if isDestination(nextCell, dest):
                    gNew = cellDetails[curCell.x][curCell.y].g + (1.0 if (dx[d] == 0 or dy[d] == 0) else 1.5)
                    cellDetails[nextCell.x][nextCell.y] = CellDetails(curCell.x, curCell.y, gNew, gNew, 0.0)
                    # tracePath(cellDetails, dest)
                    result = printPath2(cellDetails, dest)
                    return True, gNew, result
                elif not closedList[nextCell.x][nextCell.y] and canMove(matrix, curCell, nextCell):
                    gNew = cellDetails[curCell.x][curCell.y].g + (1.0 if (dx[d] == 0 or dy[d] == 0) else 1.5)
                    hNew = calculateHValue(nextCell, dest)
                    fNew = gNew + hNew

                    if cellDetails[nextCell.x][nextCell.y].f == FLT_MAX or cellDetails[nextCell.x][nextCell.y].f > fNew:
                        heapq.heappush(openList, (fNew, nextCell))
                        cellDetails[nextCell.x][nextCell.y] = CellDetails(curCell.x, curCell.y, fNew, gNew, hNew)
    return False, 0, []


def checkRule(m, n, robot, source, s, g, r, c):
    check = 1
    if (m < 1 or m >= r-1 or n < 1 or n >= c-1):
        check = 0
    if ((m == robot.x and n == robot.y) or (m == source.x and n == source.y) or (m == s.x and n == s.y) or (m == g.x and n == g.y)):
        check = 0
    return check


def move(a, m, n, robot, source, s, g, i):
    b = [[0 for x in range(n)] for y in range(m)]
    for x in range(m):
        for y in range(n):
            b[x][y] = 0
    for j in range(1, i+1):
        count = 0
        bool = 0
        rand = random.randint(0, 7)
        used = []
        used.append(rand)
        while (count < 8 and bool == 0):
            checkCase = 1
            if (rand == 0):
                for x in range(m):
                    for y in range(n):
                        if (a[x][y] == j):
                            check = checkRule(x-1, y, robot, source, s, g, m, n)
                            if (check == 1):
                                for k in range(1, i+1):
                                    if (k != j and a[x-1][y] == k):
                                        check = 0
                                        break
                            if (check == 0):
                                checkCase = check
                if (checkCase == 1):
                    for x in range(m):
                        for y in range(n):
                            if (a[x][y] == j):
                                b[x-1][y] = j
                                a[x][y] = 0
                    for x in range(m):
                        for y in range(n):
                            if (b[x][y] == j):
                                a[x][y] = j
                                b[x][y] = 0
                    bool = 1
                else:
                    if (count < 7):
                        while (1):
                            temp = random.randint(0, 7)
                            checkUsed = 1
                            for p in range(len(used)):
                                if (temp == used[p]):
                                    checkUsed = 0
                            if (checkUsed == 1):
                                rand = temp
                                used.append(rand)
                                break
                    count += 1
            if (rand == 1):
                for x in range(m):
                    for y in range(n):
                        if (a[x][y] == j):
                            check = checkRule(x+1, y, robot, source, s, g, m, n)
                            if (check == 1):
                                for k in range(1, i+1):
                                    if (k != j and a[x+1][y] == k):
                                        check = 0
                                        break
                            if (check == 0):
                                checkCase = check
                if (checkCase == 1):
                    for x in range(m):
                        for y in range(n):
                            if (a[x][y] == j):
                                b[x+1][y] = j
                                a[x][y] = 0
                    for x in range(m):
                        for y in range(n):
                            if (b[x][y] == j):
                                a[x][y] = j
                                b[x][y] = 0
                    bool = 1
                else:
                    if (count < 7):
                        while (1):
                            temp = random.randint(0, 7)
                            checkUsed = 1
                            for p in range(len(used)):
                                if (temp == used[p]):
                                    checkUsed = 0
                            if (checkUsed == 1):
                                rand = temp
                                used.append(rand)
                                break
                    count += 1
            if (rand == 2):
                for x in range(m):
                    for y in range(n):
                        if (a[x][y] == j):
                            check = checkRule(x, y-1, robot, source, s, g, m, n)
                            if (check == 1):
                                for k in range(1, i+1):
                                    if (k != j and a[x][y-1] == k):
                                        check = 0
                                        break
                            if (check == 0):
                                checkCase = check
                if (checkCase == 1):
                    for x in range(m):
                        for y in range(n):
                            if (a[x][y] == j):
                                b[x][y-1] = j
                                a[x][y] = 0
                    for x in range(m):
                        for y in range(n):
                            if (b[x][y] == j):
                                a[x][y] = j
                                b[x][y] = 0
                    bool = 1
                else:
                    if (count < 7):
                        while (1):
                            temp = random.randint(0, 7)
                            checkUsed = 1
                            for p in range(len(used)):
                                if (temp == used[p]):
                                    checkUsed = 0
                            if (checkUsed == 1):
                                rand = temp
                                used.append(rand)
                                break
                    count += 1
            if (rand == 3):
                for x in range(m):
                    for y in range(n):
                        if (a[x][y] == j):
                            check = checkRule(x, y+1, robot, source, s, g, m, n)
                            if (check == 1):
                                for k in range(1, i+1):
                                    if (k != j and a[x][y+1] == k):
                                        check = 0
                                        break
                            if (check == 0):
                                checkCase = check
                if (checkCase == 1):
                    for x in range(m):
                        for y in range(n):
                            if (a[x][y] == j):
                                b[x][y+1] = j
                                a[x][y] = 0
                    for x in range(m):
                        for y in range(n):
                            if (b[x][y] == j):
                                a[x][y] = j
                                b[x][y] = 0
                    bool = 1
                else:
                    if (count < 7):
                        while (1):
                            temp = random.randint(0, 7)
                            checkUsed = 1
                            for p in range(len(used)):
                                if (temp == used[p]):
                                    checkUsed = 0
                            if (checkUsed == 1):
                                rand = temp
                                used.append(rand)
                                break
                    count += 1
            if (rand == 4):
                for x in range(m):
                    for y in range(n):
                        if (a[x][y] == j):
                            check = checkRule(x-1, y-1, robot, source, s, g, m, n)
                            if (check == 1):
                                for k in range(1, i+1):
                                    if (k != j and a[x-1][y-1] == k):
                                        check = 0
                                        break
                                if (x - 1 == robot.x and y == robot.y):
                                    for xx in range(m):
                                        for yy in range(n):
                                            if (a[xx][yy] == j and xx == robot.x and yy - 1 == robot.y):
                                                check = 0
                                if (x == robot.x and y - 1 == robot.y):
                                    for xx in range(m):
                                        for yy in range(n):
                                            if (a[xx][yy] == j and xx - 1 == robot.x and yy == robot.y):
                                                check = 0
                            if (check == 0):
                                checkCase = check
                if (checkCase == 1):
                    for x in range(m):
                        for y in range(n):
                            if (a[x][y] == j):
                                b[x-1][y-1] = j
                                a[x][y] = 0
                    for x in range(m):
                        for y in range(n):
                            if (b[x][y] == j):
                                a[x][y] = j
                                b[x][y] = 0
                    bool = 1
                else:
                    if (count < 7):
                        while (1):
                            temp = random.randint(0, 7)
                            checkUsed = 1
                            for p in range(len(used)):
                                if (temp == used[p]):
                                    checkUsed = 0
                            if (checkUsed == 1):
                                rand = temp
                                used.append(rand)
                                break
                    count += 1
            if (rand == 5):
                for x in range(m):
                    for y in range(n):
                        if (a[x][y] == j):
                            check = checkRule(x-1, y+1, robot, source, s, g, m, n)
                            if (check == 1):
                                for k in range(1, i+1):
                                    if (k != j and a[x-1][y+1] == k):
                                        check = 0
                                        break
                                if (x - 1 == robot.x and y == robot.y):
                                    for xx in range(m):
                                        for yy in range(n):
                                            if (a[xx][yy] == j and xx == robot.x and yy + 1 == robot.y):
                                                check = 0
                                if (x == robot.x and y + 1 == robot.y):
                                    for xx in range(m):
                                        for yy in range(n):
                                            if (a[xx][yy] == j and xx - 1 == robot.x and yy == robot.y):
                                                check = 0
                            if (check == 0):
                                checkCase = check
                if (checkCase == 1):
                    for x in range(m):
                        for y in range(n):
                            if (a[x][y] == j):
                                b[x-1][y+1] = j
                                a[x][y] = 0
                    for x in range(m):
                        for y in range(n):
                            if (b[x][y] == j):
                                a[x][y] = j
                                b[x][y] = 0
                    bool = 1
                else:
                    if (count < 7):
                        while (1):
                            temp = random.randint(0, 7)
                            checkUsed = 1
                            for p in range(len(used)):
                                if (temp == used[p]):
                                    checkUsed = 0
                            if (checkUsed == 1):
                                rand = temp
                                used.append(rand)
                                break
                    count += 1
            if (rand == 6):
                for x in range(m):
                    for y in range(n):
                        if (a[x][y] == j):
                            check = checkRule(x+1, y+1, robot, source, s, g, m, n)
                            if (check == 1):
                                for k in range(1, i + 1):
                                    if (k != j and a[x+1][y+1] == k):
                                        check = 0
                                        break
                                if (x + 1 == robot.x and y == robot.y):
                                    for xx in range(m):
                                        for yy in range(n):
                                            if (a[xx][yy] == j and xx == robot.x and yy + 1 == robot.y):
                                                check = 0
                                if (x == robot.x and y + 1 == robot.y):
                                    for xx in range(m):
                                        for yy in range(n):
                                            if (a[xx][yy] == j and xx + 1 == robot.x and yy == robot.y):
                                                check = 0
                            if (check == 0):
                                checkCase = check
                if (checkCase == 1):
                    for x in range(m):
                        for y in range(n):
                            if (a[x][y] == j):
                                b[x+1][y+1] = j
                                a[x][y] = 0
                    for x in range(m):
                        for y in range(n):
                            if (b[x][y] == j):
                                a[x][y] = j
                                b[x][y] = 0
                    bool = 1
                else:
                    if (count < 7):
                        while (1):
                            temp = random.randint(0, 7)
                            checkUsed = 1
                            for p in range(len(used)):
                                if (temp == used[p]):
                                    checkUsed = 0
                            if (checkUsed == 1):
                                rand = temp
                                used.append(rand)
                                break
                    count += 1
            if (rand == 7):
                for x in range(m):
                    for y in range(n):
                        if (a[x][y] == j):
                            check = checkRule(x+1, y-1, robot, source, s, g, m, n)
                            if (check == 1):
                                for k in range(1, i + 1):
                                    if (k != j and a[x+1][y-1] == k):
                                        check = 0
                                        break
                                if (x + 1 == robot.x and y == robot.y):
                                    for xx in range(m):
                                        for yy in range(n):
                                            if (a[xx][yy] == j and xx == robot.x and yy - 1 == robot.y):
                                                check = 0
                                if (x == robot.x and y - 1 == robot.y):
                                    for xx in range(m):
                                        for yy in range(n):
                                            if (a[xx][yy] == j and xx + 1 == robot.x and yy == robot.y):
                                                check = 0
                            if (check == 0):
                                checkCase = check
                if (checkCase == 1):
                    for x in range(m):
                        for y in range(n):
                            if (a[x][y] == j):
                                b[x+1][y-1] = j
                                a[x][y] = 0
                    for x in range(m):
                        for y in range(n):
                            if (b[x][y] == j):
                                a[x][y] = j
                                b[x][y] = 0
                    bool = 1
                else:
                    if (count < 7):
                        while (1):
                            temp = random.randint(0, 7)
                            checkUsed = 1
                            for p in range(len(used)):
                                if (temp == used[p]):
                                    checkUsed = 0
                            if (checkUsed == 1):
                                rand = temp
                                used.append(rand)
                                break
                    count += 1


def calCost(s, g):
    disX = abs(s.x - g.x)
    disY = abs(s.y - g.y)
    if (disX == 0 or disY == 0):
        return 1
    return 1.5

def findWay(a, r, c, s, g, i):
    result = []
    checkWay = 1
    isFindWay = 0
    robot = Cell(s.x, s.y)
    source = Cell(s.x, s.y)
    count = 0
    while (checkWay == 1 and isFindWay == 0):
        check, cost, way = aStartSearch2(a, source, g, r, c)
        if (check == 0):
            if (count < r*c):
                count += 1
                move(a, r, c, robot, source, s, g, i)
            else:
                checkWay = 0
            continue
        else:
            count = 0
        for j in range(len(way)):
            if (a[way[j].x][way[j].y] == 0):
                robot = Cell(way[j].x, way[j].y)
                result.append(robot)
                a[robot.x][robot.y] = i
                move(a, r, c, robot, source, g, i)
                myPrint(a)
                print("\n")
                a[robot.x][robot.y] = 0
                if (robot.x == g.x and robot.y == g.y):
                    isFindWay = 1
                    break
            else:
                source = Cell(robot.x, robot.y)
                result.remove(robot)
                break
    cost = 0
    for j in range(len(result)-1):
        cost += calCost(result[j], result[j+1])
    if (checkWay == 0):
        print("Can not find a way")
    else:
        print("Cost=", cost)


def main():
    # read numbers
    with open('data.txt') as f:
        # read matrix size and create matrix
        r, c = [int(x) for x in next(f).split(',')]
        r += 1
        c += 1
        a = [[0 for x in range(c)] for y in range(r)]
        # read start, goal coordinates
        s, g, pickPoints = readEndpointforPickPoint(f)
        # read number of polygons
        n = int(next(f))
        # read n polygons and draw
        i = 1
        for line in f:
            co = [int(x) for x in line.split(',')]
            drawPolygon(a, co, i)
            i += 1

        if (len(pickPoints) == 0):
            for x in range(r):
                for y in range(c):
                    if (x == 0 or y == 0 or x == r - 1 or y == c - 1):
                        a[x][y] = 'x'
            findWay(a, r, c, s, g, i)


if __name__ == '__main__':
    main()