import sys
from Draw import*
from utilities import *

FLT_MAX = sys.maxsize


def tracePath(cellDetails, dest,R,save):
    r = dest.x
    c = dest.y
    Path = list()
    while (not (cellDetails[r][c].x == r and cellDetails[r][c].y == c)):
        Path.append((Cell(r, c)))
        temp_row = cellDetails[r][c].x
        temp_col = cellDetails[r][c].y
        r = temp_row
        c = temp_col

    Path.append(Cell(r, c))
    while (not (len(Path) == 0)):
        p = Path.pop()
        save.append((Cell(p.y,R-p.x-1)))
        print("->({},{})".format(p.x, p.y),end=" ")


def printPath(cellDetails, dest, matrix):
    r = dest.x
    c = dest.y
    while (not (cellDetails[r][c].x == r and cellDetails[r][c].y == c)):
        matrix[r][c] = 'x'
        temp_row = cellDetails[r][c].x
        temp_col = cellDetails[r][c].y
        r = temp_row
        c = temp_col

    matrix[r][c] = 'x'



def greedySearch(matrix, src, dest, R, C,save_path):
    if (not isValidInput(matrix, src, dest, R, C)):
        return False, 0

    dx = [0, 0, 1, 1, 1, -1, -1, -1]
    dy = [-1, 1, -1, 0, 1, -1, 0, 1]

    curCell = src
    cost = 0

    closedList = [[False for i in range(C)] for j in range(R)]
    closedList[curCell.x][curCell.y] = True

    trace = [[Cell(-1, -1) for x in range(C)] for y in range(R)]
    trace[curCell.x][curCell.y] = curCell

    while True:
        nextCell = None
        nextH = FLT_MAX
        for i in range(8):
            cell = Cell(curCell.x + dx[i], curCell.y + dy[i])
            if isValid(cell, R, C) and not closedList[cell.x][cell.y] and canMove(matrix, curCell, cell):
                h = calculateHValue(cell, dest)
                if (h < nextH):
                    nextH = h
                    nextCell = cell

        if (nextCell is None):
            return False, 0  # can not find path using greedy search

        cost += 1.0 if (nextCell.x - curCell.x == 0 or nextCell.y - curCell.y == 0) else 1.5
        trace[nextCell.x][nextCell.y] = curCell

        if (isDestination(nextCell, dest)):
            tracePath(trace, dest,R,save_path)
            #printPath(trace, dest, matrix)
            return save_path, cost

        curCell = nextCell
        closedList[curCell.x][curCell.y] = True

def savePathGreedySearch(b):
    a, m, n,s,g = implementInput("data.txt")
    for i in range(n):
        for j in range(m):
            if (a[j][n - i - 1] != 0):
                b[i][j] = 1
    for i in range(m):
        for j in range(0,1):
            b[n-j-1][i]=1
    for i in range(0,1):
        for j in range(n):
            b[n-j-1][i]=1
    src = Cell(n-s.y-1, s.x)
    dest = Cell(n-g.y-1, g.x)
    a=[]
    s,cost=greedySearch(b,src,dest,n,m,a)
    print("\n")
    print("Greedy Search Cost: {} ".format(cost))
    print("\n")
    if(s==False):
        print("No path!")
    else:
     for id in range(len(s)):
        for j in range(m):
            for k in range(n):
                if(j==s[id].x and k==s[id].y):
                    b[n-k-1][j]=2

