import math
a = [[1, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [2, 0, 3, 0, 0],
     [2, 0, 2, 0, 0],
     [2, 0, 2, 0, 0]]

def move(a):
    r = 0
    pos = [0,0]
    vuture_pos = [0, 0]
    for i in range(len(a)):
        for j in range(len(a[0])):
            if a[i][j] == 3:
                pos[0] = i
                pos[1] = j
                break
    for i in range(len(a)):
        for j in range(len(a[0])):
            if (math.fabs(i - pos[0])**2 + math.fabs(j - pos[1])**2)**0.5 > r:
                r = (math.fabs(i - pos[0])**2 + math.fabs(j - pos[1])**2)**0.5
                vuture_pos[0] = i
                vuture_pos[1] = j

