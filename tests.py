#! /usr/bin/python2.7
import numpy as np
import sys
import random

# def print_field(field):
#     for row in field:
#         for i, x in enumerate(row):
#             print('{0:4d}'.format(int(x))),
#             if i == len(row) - 1:
#                 print()

# def squares_dist(position, distance):
#     if distance == 0:
#         return position
#     else:
#         out = []
#         px = position[0]
#         py = position[1]
#         for x in range(distance):
#             y = distance - x
#             out += [(px+x,py+y), (px+y,py-x), (px-x,py-y), (px-y,py+x)]
#         return out

# def adjacent((x,y)):
#     return set([(x + dx, y + dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0))])

# def within_bounds((x,y)):
#     return x > 0 and y > 0 and x < 18 and y < 18 and (x,y) not in obstacle


# def normalise(field):
#     return (field / np.max(field)) * 100.0

# def safest_route(start, end):
#     pass

# field = [[100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100],
#         [100,100,100,100,100,100,100,88,85,81,83,87,100,100,100,100,100,100,100],
#         [100,100,100,100,100,94,88,58,51,43,62,68,92,93,100,100,100,100,100],
#         [100,100,100,91,94,72,58,41,33,35,44,50,58,72,85,96,100,100,100],
#         [100,100,100,89,79,63,51,43,38,35,43,47,55,50,67,95,100,100,100],
#         [100,100,94,87,60,65,58,38,36,38,50,42,39,36,30,58,78,100,100],
#         [100,100,100,61,65,59,47,35,25,25,36,33,29,28,26,37,75,100,100],
#         [100,79,58,49,52,53,39,29,22,17,21,23,27,23,24,23,49,78,100],
#         [100,86,53,31,44,49,35,24,17,8,12,16,20,22,21,20,38,77,100],
#         [100,79,42,19,24,31,21,1,5,3,7,9,12,16,18,19,37,74,100],
#         [100,79,33,21,24,25,23,15,9,5,11,12,14,18,22,25,40,77,100],
#         [100,73,49,22,27,27,21,18,14,9,14,17,20,22,25,29,55,81,100],
#         [100,100,0,46,28,28,25,22,19,15,19,21,24,27,29,44,81,100,100],
#         [100,100,1,64,39,31,29,27,23,21,29,26,28,31,35,59,85,100,100],
#         [100,100,100,91,59,42,37,38,33,32,42,36,34,36,61,86,100,100,100],
#         [100,100,100,88,92,78,61,54,40,33,39,36,49,61,86,88,100,100,100],
#         [100,100,100,100,100,94,90,69,49,44,47,60,83,86,100,100,100,100,100],
#         [100,100,100,100,100,100,100,88,84,78,82,83,100,100,100,100,100,100,100],
#         [100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100]]


# def blur(field):
#     out = np.zeros((19,19))
#     for y, row in enumerate(field):
#         for x, col in enumerate(row):
#             out[x][y] = sum([field[x][y] for x,y in list(adjacent((x,y))) + [(x,y)] if (0 <= x <= 18 and 0 <= y <= 18)])
#     return normalise(out)

# def locate_min(field):
#     min_element = np.argmin(field)
#     return (min_element % len(field[0]), min_element / len(field[0]))



# def minset(pos):
#     print('pos[0]')
#     print([pos[0]])
#     print('pos[1:]')
#     print(pos[1:])
#     print('')
#     if len(pos) == 1:
#         print('fired')
#         return [x for x in pos[0]]
#     else:
#         return [x + minset(pos[1:]) for x in pos[0]]
#        return sel + [minset(poss[1:],store[:].extend(poss[0][x])) for x in range(len(poss[0]))]


# pos = [
#     [((1, 11), 90.588500818145917), ((1, 9), 85.665519381594535)],
#     [((17, 10), 89.61236810923657), ((16, 9), 51.850702477007282)],
#     [((9, 2), 50.347006714438869), ((8, 1), 89.392315070811961)],
#     [((3, 4), 100.0), ((4, 3), 99.339840884726073)]
# ]
# print(pos)
# print('')
# import itertools
# a = list(itertools.product(*pos))
# for b in a:
#     print(b)

#com = minset(pos)
#for c in com:
#    print(c)

# nums = [abs(int(random.normalvariate(0,2))) for x in range(1000)]
# print(nums)
# a = np.array(nums)
# print(a.mean())

logicfield = [
 [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
 [  0,   0,   0,   0,   0,   0,   0,   2,   3,   4,   3,   2,   0,   0,  0,   0,   0,   0,   0,],
 [  0,   0,   0,   0,   0,   1,   2,   3,   4,   5,   4,   3,   2,   1,  0,   0,   0,   0,   0,],
 [  0,   0,   0,   0,   1,   2,   3,   4,   5,   6,   5,   4,   3,   2,  1,   0,   0,   0,   0,],
 [  0,   0,   0,   1,   2,   3,   4,   5,   6,   7,   6,   5,   4,   3,  2,   1,   0,   0,   0,],
 [  0,   0,   1,   2,   3,   4,   5,   6,   7,   8,   7,   6,   5,   4,  3,   2,   1,   0,   0,],
 [  0,   0,   2,   3,   4,   5,   6,   7,   8,   9,   8,   7,   6,   5,  4,   3,   2,   0,   0,],
 [  0,   2,   3,   4,   5,   6,   7,   8,   9,  10,   9,   8,   7,   6,  5,   4,   3,   2,   0,],
 [  0,   3,   4,   5,   6,   7,   8,   9,  10,  11,  10,   9,   8,   7,  6,   5,   4,   3,   0,],
 [  0,   4,   5,   6,   7,   8,   9,  10,  11,  12,  11,  10,   9,   8,  7,   6,   5,   4,   0,],
 [  0,   3,   4,   5,   6,   7,   8,   9,  10,  11,  10,   9,   8,   7,  6,   5,   4,   3,   0,],
 [  0,   2,   3,   4,   5,   6,   7,   8,   9,  10,   9,   8,   7,   6,  5,   4,   3,   2,   0,],
 [  0,   0,   2,   3,   4,   5,   6,   7,   8,   9,   8,   7,   6,   5,  4,   3,   2,   0,   0,],
 [  0,   0,   1,   2,   3,   4,   5,   6,   7,   8,   7,   6,   5,   4,  3,   2,   1,   0,   0,],
 [  0,   0,   0,   1,   2,   3,   4,   5,   6,   7,   6,   5,   4,   3,  2,   1,   0,   0,   0,],
 [  0,   0,   0,   0,   1,   2,   3,   4,   5,   6,   5,   4,   3,   2,  1,   0,   0,   0,   0,],
 [  0,   0,   0,   0,   0,   1,   2,   3,   4,   5,   4,   3,   2,   1,  0,   0,   0,   0,   0,],
 [  0,   0,   0,   0,   0,   0,   0,   2,   3,   4,   3,   2,   0,   0,  0,   0,   0,   0,   0,],
 [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,]
]
possibility_array = [[(1,0),(7, 9), (6, 9)],
    [(9, 9), (8, 9), (8, 8)],
    [(9, 9), (9, 10), (8, 9), (9, 8)],
    [(9, 9), (9, 10), (9, 11)],
    [(9, 10), (10, 9), (10, 10)],
    [(10, 9), (11, 9)]
]

def product(*args):
    pools = map(tuple, args)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool if y not in x]
    for prod in result:
        yield tuple(prod)

def pick_optimal(possibility_array,logicfield):
    top_score = 0
    top_combo = None
    num_members = len(possibility_array)
    for combo in product(*possibility_array):
        score = sum([logicfield[x][y] for x,y in combo])
        if score > top_score:
            top_combo = combo
            top_score = score
    return top_combo

def coord_to_cell( coord ):
    return coord[0] + coord[1] * 19

def cell_to_coord( cell ):
    x = cell % 19
    y = int(cell / 19)
    return (x,y)

def pick_optimal2(possibility_array,logicfield):
    top_score = 0
    top_combo = None
    #convert coordinates to square number

    option_array = []
    for options in possibility_array:
        option_array.append([coord_to_cell(coord) for coord in options])

    score_array = []
    for y in range(19):
        for x in range(19):
            score_array.append(logicfield[x][y])

    for combo in product(*option_array):
        score = sum([score_array[pos] for pos in combo])
        if score > top_score:
            top_combo = [cell_to_coord(cell) for cell in combo]
            top_score = score
    return top_combo

print(pick_optimal(possibility_array, logicfield))
print(pick_optimal2(possibility_array, logicfield))