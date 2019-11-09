import heapq
from Draw import*
from utilities import *

FLT_MAX = 1000000
def printPath(cellDetails, dest, matrix):
    r = dest.x
    c = dest.y
    while(not(cellDetails[r][c].parent_x == r and cellDetails[r][c].parent_y == c)):
        matrix[r][c] = 'x'
        temp_row = cellDetails[r][c].parent_x
        temp_col = cellDetails[r][c].parent_y
        r = temp_row
        c = temp_col
    matrix[r][c] = 'x'


def tracePath(cellDetails, dest, save, R):
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
        save.append(Cell(p.y,R-p.x-1))
        print("->({},{})".format(p.y, R-p.x-1))


def aStartSearch(matrix, src, dest, R, C,save_path):
    if (not isValidInput(matrix, src, dest, R, C)):
        return False,0

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
                    tracePath(cellDetails, dest,save_path,R)
                    #printPath(cellDetails, dest, matrix)
                    return save_path,gNew
                elif (not (closedList[nextCell.x][nextCell.y])) and canMove(matrix, curCell, nextCell):
                    gNew = cellDetails[curCell.x][curCell.y].g + (1.0 if (dx[d] == 0 or dy[d] == 0) else 1.5)
                    hNew = calculateHValue(nextCell, dest)
                    fNew = gNew + hNew

                    if cellDetails[nextCell.x][nextCell.y].f == FLT_MAX or cellDetails[nextCell.x][nextCell.y].f > fNew:
                        heapq.heappush(openList, (fNew, nextCell))
                        cellDetails[nextCell.x][nextCell.y] = CellDetails(curCell.x, curCell.y, fNew, gNew, hNew)
    return False,0


def savePathAStar(b):
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
    s,f=aStartSearch(b, src, dest, n, m,a)
    print("A* Search Cost: {} ".format(f))
    print("\n")
    if(s==False):
        print("No path!")
    else:
        for id in range(len(s)):
         for j in range(m):
            for k in range(n):
                if(j==s[id].x and k==s[id].y):
                    b[n-k-1][j]=2

