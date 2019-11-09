from Draw import*


def dijkstra(a, s, g, count):
    oo = 10000

    m = len(a)
    if (m == 0):
        return
    n = len(a[0])


    distance = [[0 for x in range(m*n)] for y in range(m*n)]

    for i in range(m*n):
        for j in range(m*n):
            if ((i//n == 0 and j//n == m-1) or (i//n == m-1 and j//n == 0) or (i%n == 0 and j%n == n-1) or (i%n == n-1 and j%n == 0)):
                distance[i][j] = oo
            else:
                if (i == j):
                    distance[i][j] = 0
                else:
                    if (a[j//n][j%n] != 0 and a[j//n][j%n] != count):
                        distance[i][j] = oo
                    else:
                        if (i == j-1 or i == j+1 or i == j+n or i == j-n):
                            distance[i][j] = 1
                        else:
                            if (i == j - n + 1):
                                if (i-1 >= 0 and i+n < m*n):
                                    if ((a[(i-1)//n][(i-1)%n] == 0 and a[(i+n)//n][(i+n)%n] == 0) or
                                            a[(i-1)//n][(i-1)%n] != a[(i+n)//n][(i+n)%n]):
                                        distance[i][j] = 1.5
                            else:
                                if (i == j - n - 1):
                                    if (i + 1 < m * n and i + n < m * n):
                                        if ((a[(i + 1) // n][(i + 1) % n] == 0 and a[(i + n) // n][(i + n) % n] == 0) or
                                                a[(i + 1) // n][(i + 1) % n] != a[(i + n) // n][(i + n) % n]):
                                            distance[i][j] = 1.5
                                else:
                                    if (i == j + n + 1):
                                        if (i - 1 >= 0 and i - n >= 0):
                                            if ((a[(i - 1) // n][(i - 1) % n] == 0 and a[(i - n) // n][(i - n) % n] == 0) or
                                                    a[(i - 1) // n][(i - 1) % n] != a[(i - n) // n][(i - n) % n]):
                                                distance[i][j] = 1.5
                                    else:
                                        if (i == j + n - 1):
                                            if (i + 1 < m * n and i - n >= 0):
                                                if ((a[(i + 1) // n][(i + 1) % n] == 0 and a[(i - n) // n][(i - n) % n] == 0) or
                                                        a[(i + 1) // n][(i + 1) % n] != a[(i - n) // n][(i - n) % n]):
                                                    distance[i][j] = 1.5
                                        else:
                                            distance[i][j] = oo

    isTravel = [[0 for x in range(m*n)] for y in range(m*n)]
    previousPoint = [[0 for x in range(m * n)] for y in range(m * n)]
    cost = [[0 for x in range(m * n)] for y in range(m * n)]
    for i in range(m*n):
        isTravel[i] = 0
        previousPoint[i] = s.x * n + s.y
        cost[i] = oo
    cost[s.x*n + s.y] = 0
    check = 1
    while (isTravel[g.x*n + g.y] == 0):
        i = 0
        for i in range(m * n):
            if (isTravel[i] == 0 and cost[i] < oo):
                break
            else:
                if (i == m*n-1):
                    check = 0
        if (check == 0):
            break
        for j in range(m * n):
            if (isTravel[j] == 0 and cost[j] < cost[i]):
                i = j
        isTravel[i] = 1
        for j in range(m * n):
            if (isTravel[j] == 0 and distance[i][j] != 0 and cost[i] + distance[i][j] < cost[j]):
                cost[j] = cost[i] + distance[i][j]
                previousPoint[j] = i

    if (check == 1):
        i = g.x*n + g.y
        while (i != s.x*n + s.y):
            i = previousPoint[i]
            a[i//n][i%n] = count
    return check, cost[g.x*n + g.y]

def save_path_ucs(a,file):
    # read numbers
    with open(file) as f:
        # read matrix size and create matrix
        m, n = [int(x) for x in next(f).split(',')]
        #a = [[0 for x in range(n)] for y in range(m)]
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
        a[s.x][s.y] = i
        a[g.x][g.y] = i
        check, cost = dijkstra(a, s, g, i)
        if (check == 0):
            print("Can't find a way")
        else:
            print("Cost = ", cost)
