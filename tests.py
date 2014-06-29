#! /usr/bin/python2.7
import numpy as np
import sys

def print_field(field):
    for row in field:
        for i, x in enumerate(row):
            print('{0:4d}'.format(int(x))),
            if i == len(row) - 1:
                print()

def squares_dist(position, distance):
    if distance == 0:
        return position
    else:
        out = []
        px = position[0]
        py = position[1]
        for x in range(distance):
            y = distance - x
            out += [(px+x,py+y), (px+y,py-x), (px-x,py-y), (px-y,py+x)]
        return out

def adjacent((x,y)):
    return set([(x + dx, y + dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0))])

def within_bounds((x,y)):
    return x > 0 and y > 0 and x < 18 and y < 18 and (x,y) not in obstacle


def normalise(field):
    return (field / np.max(field)) * 100.0

def safest_route(start, end):
    pass

field = [[100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100],
        [100,100,100,100,100,100,100,88,85,81,83,87,100,100,100,100,100,100,100],
        [100,100,100,100,100,94,88,58,51,43,62,68,92,93,100,100,100,100,100],
        [100,100,100,91,94,72,58,41,33,35,44,50,58,72,85,96,100,100,100],
        [100,100,100,89,79,63,51,43,38,35,43,47,55,50,67,95,100,100,100],
        [100,100,94,87,60,65,58,38,36,38,50,42,39,36,30,58,78,100,100],
        [100,100,100,61,65,59,47,35,25,25,36,33,29,28,26,37,75,100,100],
        [100,79,58,49,52,53,39,29,22,17,21,23,27,23,24,23,49,78,100],
        [100,86,53,31,44,49,35,24,17,8,12,16,20,22,21,20,38,77,100],
        [100,79,42,19,24,31,21,1,5,3,7,9,12,16,18,19,37,74,100],
        [100,79,33,21,24,25,23,15,9,5,11,12,14,18,22,25,40,77,100],
        [100,73,49,22,27,27,21,18,14,9,14,17,20,22,25,29,55,81,100],
        [100,100,0,46,28,28,25,22,19,15,19,21,24,27,29,44,81,100,100],
        [100,100,1,64,39,31,29,27,23,21,29,26,28,31,35,59,85,100,100],
        [100,100,100,91,59,42,37,38,33,32,42,36,34,36,61,86,100,100,100],
        [100,100,100,88,92,78,61,54,40,33,39,36,49,61,86,88,100,100,100],
        [100,100,100,100,100,94,90,69,49,44,47,60,83,86,100,100,100,100,100],
        [100,100,100,100,100,100,100,88,84,78,82,83,100,100,100,100,100,100,100],
        [100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100]]


def blur(field):
    out = np.zeros((19,19))
    for y, row in enumerate(field):
        for x, col in enumerate(row):
            out[x][y] = sum([field[x][y] for x,y in list(adjacent((x,y))) + [(x,y)] if (0 <= x <= 18 and 0 <= y <= 18)])
    return normalise(out)
    
def locate_min(field):
    min_element = np.argmin(field)
    return (min_element % len(field[0]), min_element / len(field[0]))
print('orig')
print_field(field)
x = blur(field)
print('blurred')
print_field(x)
x = blur(x)
print('blurred x2')
print_field(x)
x = blur(x)
print('blurred x3')
print_field(x)

print(locate_min(x))

sys.exit()




print_field(field)
min_element = np.argmin(field)
x = min_element % len(field[0])
y = min_element / len(field[0])
print(min_element)
print('x = ' + str(x))
print('y = ' + str(y))

print(locate_min(field))
