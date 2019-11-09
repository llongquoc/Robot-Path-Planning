import turtle
import random
from Draw import*
from AStarSearch import*
from Dijkstra import*
from GreedySearch import*
from AStarPickPoint import*
from HelpAnimation import*


def readData(f):
    with open(f, "r") as fp:
        line=fp.readline()
        cnt=1
        data=list()
        while line:
            k = line.strip().split(",")
            a = [int(x) for x in k]
            data.append((cnt, a))
            line = fp.readline()
            cnt += 1
    return data

data=readData("data.txt")


def drawBlockedUp(t, start_x, start_y, box_size, M,N):
    for u in range(0, M):
        for v in range(N, N+1):
            drawBox(t, start_x + u * box_size, start_y + v * box_size, box_size, "white")

def drawBlockedRight(t, start_x, start_y, box_size, M,N):
    for u in range(M, M+1):
        for v in range(0,N):
            drawBox(t, start_x + u * box_size, start_y + v * box_size, box_size, "white")

def colorBlockedUp(t, start_x, start_y,box_size,M,N):
    for u in range(0, M+1):
        for v in range(N,N + 1):
            color(t, start_x + u * box_size, start_y + v * box_size, box_size, "Dim Gray")

def colorBlockedRight(t, start_x, start_y,box_size,M,N):
    for u in range(M, M+1):
        for v in range(0,N + 1):
            color(t, start_x + u * box_size, start_y + v * box_size, box_size, "Dim Gray")

def colorBlockedLeft(t, start_x, start_y,box_size,M,N):
    for u in range(0, 1):
        for v in range(0,N + 1):
            color(t, start_x + u * box_size, start_y + v * box_size, box_size, "Dim Gray")


def colorBlockedDown(t, start_x, start_y,box_size,M,N):
    for u in range(0, M+1):
        for v in range(0,1):
            color(t, start_x + u * box_size, start_y + v * box_size, box_size, "Dim Gray")

def drawMatrixTableAnimation(board,start_x, start_y, box_size,square_color):

    b = [[0 for x in range(data[0][1][0])] for y in range(data[0][1][1])]

    with open('data.txt') as f:
        # read matrix size and create matrix
        r, c = [int(x) for x in next(f).split(',')]
        r += 1
        c += 1
        a = [[0 for x in range(c)] for y in range(r)]
        # read start, goal coordinates
        s, g = readEndpoint(f)
        # read number of polygons
        n = int(next(f))
        # read n polygons and draw
        i = 1
        for line in f:
            co = [int(x) for x in line.split(',')]
            drawPolygon(a, co, i)
            i += 1

            for x in range(r):
                for y in range(c):
                    if (x == 0 or y == 0 or x == r - 1 or y == c - 1):
                        a[x][y] = 'x'
        result = []
        checkWay = 1
        isFindWay = 0
        robot = Cell(s.x, s.y)
        source = Cell(s.x, s.y)
        colors = ["red", "green", "Cyan", "Medium Spring Green", "Rosy Brown", "Aquamarine", "Burlywood",
                  "Violet", "Deep Sky Blue", "Lawn Green", "Gold", "Salmon", "Deep Pink",
                  "orange", "purple", "pink", "yellow", "Light Sea Green", "Light Slate Gray",
                  "Dodger Blue", "Maroon", "Old Lace", "Lemon Chiffon"
            , "Chocolate"]
        col = [0 for x in range(i)]
        for x in range(i):
            col[x] = random.choice(colors)
            colors.remove(col[x])
        while (checkWay == 1 and isFindWay == 0):
            check, cost, way = aStartSearch2(a, source, g, r, c)
            if (check == 0):
                checkWay = 0
                continue
            for j in range(len(way)):
                tempCheck = 1
                if (a[way[j].x][way[j].y] == 0):
                    if (j >= 1):
                        disX = s.x - g.x
                        disY = s.y - g.y
                        if (disX == 1 and disY == 1 and a[way[j].x-1][way[j].y] != 0 and a[way[j].x][way[j].y-1] != 0):
                            tempCheck = 0
                        if (disX == -1 and disY == 1 and a[way[j].x+1][way[j].y] != 0 and a[way[j].x][way[j].y-1] != 0):
                            tempCheck = 0
                        if (disX == 1 and disY == -1 and a[way[j].x-1][way[j].y] != 0 and a[way[j].x][way[j].y+1] != 0):
                            tempCheck = 0
                        if (disX == -1 and disY == -1 and a[way[j].x+1][way[j].y] != 0 and a[way[j].x][way[j].y+1] != 0):
                            tempCheck = 0
                else:
                    tempCheck = 0
                if (tempCheck == 1):
                    robot = Cell(way[j].x, way[j].y)
                    result.append(robot)
                    move(a, r, c, robot, source, s, g, i)
                    a[s.x][s.y] = i
                    a[g.x][g.y] = i
                    a[robot.x][robot.y] = i
                    index = 1
                    while (index <= i):
                        for x in range(r):
                            for y in range(c):
                                if (a[x][y] == index):
                                    color(board, start_x + x * box_size, start_y + y * box_size, box_size, col[index-1].strip())
                        index += 1
                    a[s.x][s.y] = 0
                    a[g.x][g.y] = 0
                    a[robot.x][robot.y] = 0
                    if (robot.x == g.x and robot.y == g.y):
                        isFindWay = 1
                        break
                    else:
                        turtle.tracer(0, 0)
                        turtle.speed(0)
                        turtle.update()
                        turtle.speed(0)
                        for x in range(r):
                            for y in range(c):
                                drawBox(board, start_x + x * box_size, start_y + y * box_size, box_size, square_color)
                            square_color = 'white'
                        drawBlockedUp(board, start_x, start_y, box_size, r, c)
                        drawBlockedRight(board, start_x, start_y, box_size, r, c)
                        colorBlockedUp(board, start_x, start_y, box_size, r, c)
                        colorBlockedLeft(board, start_x, start_y, box_size, r, c)
                        colorBlockedRight(board, start_x, start_y, box_size, r, c)
                        colorBlockedDown(board, start_x, start_y, box_size, r, c)
                else:
                    source = Cell(robot.x, robot.y)
                    result.remove(robot)
                    break
        cost = 0
        for j in range(len(result) - 1):
            cost += calCost(result[j], result[j + 1])
        if (checkWay == 0):
            print("Can not find a way")
        else:
            print("Cost=", cost)


def drawMatrixTable(board,start_x, start_y, box_size,square_color):
    print(data)
    l=data[2][0]
    square_color = "white"
    colors = ["red", "green", "Cyan", "Medium Spring Green", "Rosy Brown", "Aquamarine", "Burlywood",
              "Violet" , "Deep Sky Blue","Lawn Green", "Gold", "Salmon", "Deep Pink",
              "orange", "purple", "pink", "yellow","Light Sea Green", "Light Slate Gray", "Dodger Blue","Maroon","Old Lace","Lemon Chiffon"
              , "Chocolate"                                     ]
    a = [[0 for x in range(data[0][1][1])] for y in range(data[0][1][0])]
    for i in range(0, data[0][1][0]):
        for j in range(0, data[0][1][1]):
            drawBox(board, start_x + i * box_size, start_y + j * box_size, box_size, square_color)
        square_color = 'white'
    index=3
    for i in range(3,len(data)):
        c=random.choice(colors)
        colors.remove(c)
        for j in range(0, len(data[i][1])-1, 2):
            color(board, start_x + data[i][1][j] * box_size, start_y + data[i][1][j + 1] * box_size, box_size,c.strip())
        drawPolygon(a,data[i][1],index)
        for m in range(0, data[0][1][0]):
            for n in range(0, data[0][1][1]):
                if(a[m][n]==index):
                 color(board,start_x+m*box_size, start_y+n*box_size, box_size, c.strip())
        index+=1



    for i in range(0, 3,2):
        co=random.choice(colors)
        color(board, start_x + data[1][1][i] * box_size, start_y + data[1][1][i + 1] * box_size, box_size, "blue")

    for u in range(0, data[0][1][0]):
        for v in range(data[0][1][1], data[0][1][1]+1):
            drawBox(board, start_x + u * box_size, start_y + v * box_size, box_size, "white")
    drawBlockedUp(board,start_x,start_y,box_size,data[0][1][0], data[0][1][1])
    drawBlockedRight(board, start_x, start_y, box_size, data[0][1][0], data[0][1][1])
    colorBlockedUp(board, start_x, start_y, box_size, data[0][1][0], data[0][1][1])
    colorBlockedLeft(board, start_x, start_y, box_size, data[0][1][0], data[0][1][1])
    colorBlockedRight(board, start_x, start_y, box_size, data[0][1][0], data[0][1][1])
    colorBlockedDown(board, start_x, start_y, box_size, data[0][1][0], data[0][1][1])



    b=[[0 for x in range(data[0][1][0])] for y in range(data[0][1][1])]
    if(len(data[1][1])>4):
        print("Tìm đường đi khi có điểm đón")
        c = [[0 for x in range(data[0][1][1])] for y in range(data[0][1][0])]
        adjusta(c, data[0][1][0], data[0][1][1])
        implementPickPoint(c, "data.txt")
        col = random.choice(colors)
        for i in range(data[0][1][0]):
            for j in range(data[0][1][1]):
                if (c[i][j] == data[2][1][0]+3):
                    color(board, start_x + i * box_size, start_y + j * box_size, box_size, col)
        colors.remove(col)
        co = random.choice(colors)
        for k in range(4, len(data[1][1]) - 1, 2):
            color(board, start_x + data[1][1][k] * box_size, start_y + data[1][1][k + 1] * box_size, box_size, co)
    else:
     print("---------------------------------------------")
     print("1. Tìm đường đi bằng giải thuật Dijkstra")
     print("2. Tìm đường đi bằng giải thuật A* Search")
     print("3. Tìm đường đi bằng giải thuật Greedy Search ")
     print("4. Tìm đường đi khi vật cản di chuyển")
     choose=int(input("Bạn chọn option: "))
     if (choose == 3):
         savePathGreedySearch(b)
         for i in range(0, data[0][1][0]):
             for j in range(0, data[0][1][1]):
                 if (b[data[0][1][1] - 1 - j][i] == 2):
                     color(board, start_x + i * box_size, start_y + j * box_size, box_size, "blue")
     elif (choose == 1):
         c = [[0 for x in range(data[0][1][1])] for y in range(data[0][1][0])]
         adjusta(c, data[0][1][0], data[0][1][1])
         save_path_ucs(c, "data.txt")
         for i in range(data[0][1][0]):
             for j in range(data[0][1][1]):
                 if (c[i][j] == data[2][1][0] + 1):
                     color(board, start_x + i * box_size, start_y + j * box_size, box_size, "blue")

     elif (choose == 2):
         savePathAStar(b)
         for i in range(0, data[0][1][0]):
             for j in range(0, data[0][1][1]):
                 if (b[data[0][1][1] - 1 - j][i] == 2):
                     color(board, start_x + i * box_size, start_y + j * box_size, box_size, "blue")
     elif (choose == 4):
         drawMatrixTableAnimation(board, start_x, start_y, box_size, square_color)



def readData(f):
    with open(f, "r") as fp:
        line=fp.readline()
        cnt=1
        data=list()
        while line:
            k = line.strip().split(",")
            a = [int(x) for x in k]
            print("Line {}: {}".format(cnt, a))
            data.append((cnt, a))
            line = fp.readline()
            cnt += 1
    return data


#Vẽ ô vuông
def drawBox(t, x, y, size, fill_color):
    t.penup()
    t.goto(x, y)
    t.pendown()

    t.fillcolor(fill_color)
    t.begin_fill()
    for i in range(0, 4):
        board.forward(size)
        board.right(90)
    t.end_fill()

#Tô màu ô vuông
def color(t, x, y, size, fill_color):
    t.penup()
    t.goto(x, y)

    t.fillcolor(fill_color)
    t.begin_fill()

    for i in range(0, 4):
        board.forward(size)
        board.right(90)
    t.end_fill()

board = turtle.Turtle()
turtle.speed(1)
turtle.tracer(3,4)
turtle.hideturtle()
turtle.ht()
drawMatrixTable(board,-300,-250,20,"white")
turtle.hideturtle()
turtle.ht()
turtle.update()
turtle.done()