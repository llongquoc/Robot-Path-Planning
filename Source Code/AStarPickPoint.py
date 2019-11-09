import heapq
from Draw import*
from utilities import *
from HelpAnimation import*

FLT_MAX = 1000000


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


def createCheckAndCost(a, s, g, pickPoints, check, cost, m, n):
    for x in range(len(pickPoints)):
        check[x][len(pickPoints)], cost[x][len(pickPoints)], result = aStartSearch2(a, s, pickPoints[x], m, n)
        check[x][len(pickPoints)+1], cost[x][len(pickPoints)+1], result = aStartSearch2(a, pickPoints[x], g, m, n)
    for x in range(len(pickPoints) - 1):
        for y in range(len(pickPoints)):
            if (x != y):
                check[x][y], cost[x][y], result = aStartSearch2(a, pickPoints[x], pickPoints[y], m, n)


def process(a, s, g, pickPoints, result, optimalCase, check, cost):
    costInCase = 0
    checkCase = 1
    temp1 = check[result[0]][len(result)]
    temp2 = cost[result[0]][len(result)]
    if (temp1 == 0):
        checkCase = temp1
    costInCase += temp2
    for i in range(len(result)):
        if (i != len(result) - 1):
            if (result[i] > result[i+1]):
                temp1 = check[result[i+1]][result[i]]
                temp2 = cost[result[i+1]][result[i]]
            else:
                temp1 = check[result[i]][result[i+1]]
                temp2 = cost[result[i]][result[i+1]]
            if (temp1 == 0):
                checkCase = temp1
            costInCase += temp2
        else:
            if (i == len(result) - 1):
                temp1 = check[result[i]][len(result)+1]
                temp2 = cost[result[i]][len(result)+1]
                if (temp1 == 0):
                    checkCase = temp1
                costInCase += temp2
    if (checkCase == 1 and costInCase < optimalCase[len(result)]):
        for i in range(len(result)):
            optimalCase[i] = result[i]
        optimalCase[len(result)] = costInCase


def backtrack(a, s, g, pickPoints, isTravel, result, i, optimalCase, check, cost):
    if (i > len(pickPoints) - 1):
        process(a, s, g, pickPoints, result, optimalCase, check, cost)
    else:
        for j in range(len(pickPoints)):
            if (isTravel[j] == 0):
                isTravel[j] = 1
                result[i] = j
                backtrack(a, s, g, pickPoints, isTravel, result, i+1, optimalCase, check, cost)
                isTravel[j] = 0


def drawWay(a, s, g, pickPoints, optimalCase, m, n, i):
    costInOptimalCase = 0
    temp1, temp2, result = aStartSearch2(a, s, pickPoints[optimalCase[0]], m, n)
    costInOptimalCase += temp2
    for j in range(len(optimalCase) - 1):
        if (j != len(optimalCase) - 2):
            temp1, temp2, tempResult = aStartSearch2(a, pickPoints[optimalCase[j]], pickPoints[optimalCase[j+1]], m, n)
            for x in range(len(tempResult)):
                result.append(tempResult[x])
            costInOptimalCase += temp2
        else:
            if (j == len(optimalCase) - 2):
                temp1, temp2, tempResult = aStartSearch2(a, pickPoints[optimalCase[j]], g, m, n)
                for x in range(len(tempResult)):
                    result.append(tempResult[x])
                costInOptimalCase += temp2
    for x in range(len(result)):
        a[result[x].x][result[x].y] = i
    return costInOptimalCase

def implementPickPoint(a,file):
    with open(file) as f:
        # read matrix size and create matrix
        r, c = [int(x) for x in next(f).split(',')]
        #a = [[0 for x in range(n)] for y in range(m)]
        # read start, goal coordinates
        s, g,pickPoints = readEndpointforPickPoint(f)
        # read number of polygons
        n = int(next(f))
        # read n polygons and draw
        i = 1
        for line in f:
            co = [int(x) for x in line.split(',')]
            drawPolygon(a, co, i)
            i += 1
        isTravel = [0 for x in range(len(pickPoints))]
        result = [0 for x in range(len(pickPoints))]
        optimalCase = [0 for x in range(len(pickPoints) + 1)]
        for x in range(len(pickPoints)):
            isTravel[x] = 0
            result[x] = 0
            optimalCase[x] = 0
        optimalCase[len(pickPoints)] = 10**9
        check = [[0 for x in range(len(pickPoints)+2)] for y in range(len(pickPoints))]
        cost = [[0 for x in range(len(pickPoints)+2)] for y in range(len(pickPoints))]
        createCheckAndCost(a, s, g, pickPoints, check, cost, r, c)
        backtrack(a, s, g, pickPoints, isTravel, result, 0, optimalCase, check, cost)
        bool = 0
        for x in range(len(optimalCase) - 1):
            if (optimalCase[x] != 0 or (len(optimalCase) == 2 and optimalCase[len(optimalCase) - 1] != 10**9)):
                bool = 1
        if (bool == 0):
            print("Can't find a way")
        else:
            costInOptimalCase = drawWay(a, s, g, pickPoints, optimalCase, r, c, i+2)
            a[s.x][s.y] = i
            a[g.x][g.y] = i
            for j in range(len(pickPoints)):
                a[pickPoints[j].x][pickPoints[j].y] = i+1
            myPrint(a)
            print("Cost = ", costInOptimalCase)

