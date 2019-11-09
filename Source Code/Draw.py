from utilities import *

# def readEndpoint(f):
# 	x1, y1, x2, y2 = [int(x) for x in next(f).split(',')]
# 	s = Cell(x1, y1)
# 	g = Cell(x2, y2)
# 	return s, g
# def readEndpoint(f):
# 	vals = [int(x) for x in next(f).split(",")]
# 	s = Cell(vals[0], vals[1])
# 	g = Cell(vals[2], vals[3])
# 	pickPoints = []
#     if(len(vals)>4):
# 	  for i in range(4, len(vals), 2):
# 		pickPoints.append(Cell(vals[i], vals[i + 1]))
# 	  return s, g, pickPoints
#     else:
#      return s,g
def readEndpointforPickPoint(f):
    vals=[int(x) for x in next(f).split(",")]
    s=Cell(vals[0], vals[1])
    g=Cell(vals[2], vals[3])
    pickPoints=[]
    for i in range(4,len(vals),2):
        pickPoints.append(Cell(vals[i], vals[i + 1]))
    return s,g,pickPoints

def readEndpoint(f):
	x1, y1, x2, y2 = [int(x) for x in next(f).split(',')]
	s = Cell(x1, y1)
	g = Cell(x2, y2)
	return s, g

def divideCellsToLines(nCells, nLines):
    cellPerLine = [nCells // nLines] * nLines;
    remain = nCells % nLines
    i = 0
    while (remain > 0):
        cellPerLine[i] += 1
        remain -= 1
        if (remain > 0):
            cellPerLine[nLines - 1 - i] += 1
            remain -= 1
        i += 1
    return cellPerLine


def helpDrawLine(a, c1, c2, nCells, nLines, dx, dy, index):
    if (nLines == 0):
        return
    if (dx > dy):  # lines and Ox are parallel
        changeCell = Cell(1 if c2.x > c1.x else -1, 0)
        changeLine = Cell(0, 1 if c2.y > c1.y else -1)
    else:  # lines and Oy are parallel
        changeCell = Cell(0, 1 if c2.y > c1.y else -1)
        changeLine = Cell(1 if c2.x > c1.x else -1, 0)

    cellPerLine = divideCellsToLines(nCells, nLines)

    x = c1.x
    y = c1.y
    for i in range(nLines):
        for j in range(cellPerLine[i]):
            x += changeCell.x
            y += changeCell.y
            a[x][y] = index
        x += changeLine.x
        y += changeLine.y


def drawVertice(a, c1, index):
    a[c1.x][c1.y] = index


def drawLine(a, c1, c2, index):
    drawVertice(a, c1, index)
    dx = abs(c1.x - c2.x) - 1
    dy = abs(c1.y - c2.y) - 1
    less = min(dx, dy)
    more = max(dx, dy)
    if (less == more):  # diagonal case
        x1Move = 1 if c2.x > c1.x else -1
        nextToC1 = Cell(c1.x + x1Move, c1.y)
        nextToC2 = Cell(c2.x - x1Move, c2.y)
        helpDrawLine(a, nextToC1, nextToC2, more, less, dx, dy, index)
    else:
        if (more < less + 2):  # not enough cells to draw from c1 to c2
            if (dy == more):  # draw along Oy
                nextToC1 = Cell(c1.x + (1 if c2.x > c1.x else -1), c1.y)
            else:  # draw along Ox
                nextToC1 = Cell(c1.x, c1.y + (1 if c2.y > c1.y else -1))
            helpDrawLine(a, nextToC1, c2, more, less + 1, dx, dy, index)
        else:  # draw like normal
            helpDrawLine(a, c1, c2, more, less + 2, dx, dy, index)


def drawPolygon(a, co, index):
    n = len(co)
    for i in range(0, n, 2):
        c1 = Cell(co[i], co[i + 1])  # from point c1
        c2 = Cell(co[(i + 2) % n], co[(i + 3) % n])  # to point c2
        drawLine(a, c1, c2, index)  # draw


def myPrint(a):
    m = len(a)
    if (m == 0):
        return
    n = len(a[0])

    for i in range(n):
        for j in range(m):
            print(a[j][n - 1 - i],end=" ")
        print("\n")

def adjusta(a,m,n):
    for i in range(n-1,n):
        for j in range(m):
            a[j][n - 1 - i]=1
    for i in range(0,n):
        for j in range(0,1):
            a[j][n-1-i]=1

def implementInput(file):
    # read numbers
    with open(file) as f:
        # read matrix size and create matrix
        m, k = [int(x) for x in next(f).split(',')]
        a = [[0 for x in range(k)] for y in range(m)]
        # read start, goal coordinates
        s, g = readEndpoint(f)
        # read number of polygons
        n = int(next(f))
        # read n polygons and draw
        i = 3
        for line in f:
            co = [int(x) for x in line.split(',')]
            drawPolygon(a, co, i)
            i += 1
        adjusta(a,m,k)
    print(a)
    myPrint(a)
    return a,m,k,s,g




if __name__ == '__main__':
    implementInput("data.txt")