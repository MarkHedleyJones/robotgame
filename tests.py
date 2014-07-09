#! /usr/bin/python2.7
import numpy as np
import sys
import random
import itertools
import operator
import copy
import pudb

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

reduced = [
    [(9, 10), [(9, 9), (9, 10), (9, 11)],                   [1.0, 0.0, -1.0]],
    [(9, 8),  [(9, 9), (9, 8), (10, 8), (8, 8), (9, 7)],    [1.0, 0.0, -1.0, -1.0, -1.0]],
    [(9, 9),  [(9, 9), (9, 10), (8, 9), (9, 8), (10, 9)],   [0.0, -1.0, -1.0, -1.0, -1.0]],
    [(8, 9),  [(9, 9), (8, 9), (8, 8), (8, 10), (7, 9)],    [1.0, 0.0, -1.0, -1.0, -1.0]],
    [(10, 9), [(9, 9), (10, 9), (10, 8), (11, 9)],          [1.0, 0.0, -1.0, -1.0]]
]

system = {}
for member in reduced:
    system[member[0]] = {'options':member[1], 'scores': member[2]}

# Turn system into a dictionary
# print(system)

def total_combinations(system):
    total_combinations = 1
    for pos, bot in system.items():
        total_combinations *= len(bot['options'])
    return total_combinations

def pick_best(system):
    top_score = -9999
    scores = {}
    num_system = len(system)
    options = []
    result = None

    if type(system) == dict:
        for pos, bot in system.items():
            start = coord_to_cell(pos)
            moves = [(start,coord_to_cell(end)) for end in bot['options']]
            for index, move in enumerate(moves):
                scores[move] = bot['scores'][index]
            options.append(moves)
    else:
        for member in system:
            start = coord_to_cell(member[0])
            moves = [(start,coord_to_cell(end)) for end in member[1]]
            for index, move in enumerate(moves):
                scores[move] = member[2][index]
            options.append(moves)

    for possibility in itertools.product(*options):
        ends = [y for x,y in possibility]
        if len(set([y for x,y in possibility])) != num_system:
            continue
        if set(possibility) & set([(y,x) for x,y in possibility if x != y]):
            continue

        score = sum([scores[move] for move in possibility])
        if score > top_score:
            result, top_score = possibility, score

    if result is None:
        # print('')
        # print('NO RESULT from picking best')
        # print(system)
        # print('')
        # print(options)
        return None
    else:
        return [(cell_to_coord(x),cell_to_coord(y)) for x,y in result]


def coord_to_cell( coord ):
    return coord[0] + coord[1] * 19

def cell_to_coord( cell ):
    x = cell % 19
    y = int(cell / 19)
    return (x,y)

def test_system(system):
    for pos, bot in system.items():
        num_opts = len(bot['options'])
        if num_opts == 0:
            #pu.db
            return False
        elif num_opts == 1 and bot['options'][0] != pos:
            try:
                displaced_bot_options = system[bot['options'][0]]
                displaced_bot = bot['options'][0]
            except KeyError:
                displaced_bot = None

            if displaced_bot:
                if len(displaced_bot_options) <= 2:
                    if set(displaced_bot_options) - set([pos, displaced_bot]) == set():
                        #pu.db
                        return False

    return True


def find_possible_simplifications(system):

    best_candidates = None

    # Find the cell involved with the most moves
    cells = {}
    for pos, bot in system.items():
        for cell in bot['options']:
            if cell in cells:
                cells[cell] += 1
            else:
                cells[cell] = 1

    # print('cells')
    # print(cells)
    #
    #
    #
    #
    # TODO: Doing this means a non-occupied cell will always be assigned to neighbouring cells
    # at some point so in-turn that means that we can't consider the situation
    # where everyone stays where they are!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #
    #
    #
    #

    # Exclude cells that no bot is occupying
    valid_cells = system.keys()
    hot_cell = None
    for cell in cells.keys():
        if cell not in valid_cells:
            del cells[cell]

    hot_cell = max(cells.iteritems(), key=operator.itemgetter(1))[0]

    if cells[hot_cell] > 1:

        candidates = {}
        for pos, bot in system.items():
            if hot_cell in bot['options']:
                score = bot['scores'][bot['options'].index(hot_cell)]
                candidates[pos] = score

        # print('candidates')
        # print(candidates)

        # If this square is the only available move for a candidate,
        # grant it to that candidate
        best_candidates = [pos for pos in system if pos in candidates and len(system[pos]['options']) == 1]
        # print('candidates that NEED this move')
        # print(best_candidates)

        # If not best candidate at this point, find the most deserving
        if best_candidates == []:
            # print('no necessary candidates, selecting by value')
            # max_score = -9999
            # for candidate in candidates.iteritems():
            #     if candidate[1] > max_score:
            #         max_score = candidate[1]
            # # print('max score = ' + str(max_score))

            best_candidates = []
            for candidate in candidates.iteritems():
                best_candidates.append(candidate[0])
            # print('best candidates = ' + str(best_candidates))
            # print(best_candidates)
            # sys.exit()
            # Filter out candidates who would cause a bot to be left with no moves
            for candidate in best_candidates[:]:
                for pos, bot in system.items():
                    if pos == hot_cell:
                        if set(bot['options']) - set([hot_cell, candidate]) == set():
                            # print('detected and removed bad candidate' + str(candidate))
                            best_candidates.remove(candidate)

        return (hot_cell, best_candidates)
    else:
        bots = {}
        max_opts = 0
        for pos, bot in system.items():
            opts = len(bot['options'])
            bots[pos] = opts
            if opts > max_opts:
                max_opts = opts

        bots = [pos for pos,bot in system.items() if len(bot['options']) == max_opts]
        winner = random.choice(bots)
        return (system[winner]['options'], winner)





def make_reduction(input_system, (winner, target)):

    system = copy.deepcopy(input_system)

    print('')
    print('Making a reduction')
    print('The cell ' + str(target) + ' has been awarded to the bot in ' + str(winner))

    print('Original system')
    for member in input_system.iteritems():
        print(member)


    for pos, bot in system.items():
        if pos == winner:
            # Make this move the only option for the winner
            bot['scores'] = [bot['scores'][bot['options'].index(target)]]
            bot['options'] = [target]
        else:
            if pos == target:
                # print('The winner, '+str(winner)+', is moving into this bots place:')
                # print((pos,bot))

                # Remove bot swap as an option for target square
                try:
                    swap_index = bot['options'].index(winner)
                    # print('A swap condidion exists')
                except:
                    swap_index = None

                if swap_index:
                    del bot['options'][swap_index]
                    del bot['scores'][swap_index]
            if target in bot['options']:
                # Remove this option from other bots move options
                bot['scores'].remove(bot['scores'][bot['options'].index(target)])
                bot['options'].remove(target)

    print('Reduced system')
    for member in system.iteritems():
        print(member)

    return system

counter = 0

def debug_sys(systemz):
    # count stayings
    count = 0
    for p,b in systemz.items():
        if p in b['options']:
            count += 1
    if(count == 5):
        #pu.db
        pass

def reduced_systems(system, size):
    global counter
    counter += 1
    print(counter)

    if total_combinations(system) > size:
        debug_sys(system)
        # print('')
        # print('System has ' + str(total_combinations(system)) + ' total_combinations')
        # print('Breaking system down')
        if counter == 10:
            #pu.db
            pass
        cells, candidates = find_possible_simplifications(system)

        if type(candidates) == list:
            new_systems = [make_reduction(copy.deepcopy(system), (candidate, cells)) for candidate in candidates]
        elif type(cells) == list:
            new_systems = [make_reduction(copy.deepcopy(system), (candidates, cell)) for cell in cells]

        filter(test_system, new_systems)



        # print('After filtering there are only ' + str(len(new_systems)) + ' systems')
        # print('')
        # print('')
        # print('Made a new set of simplified systems')
        # for system in new_systems:
        #     print(system)
        #     print(total_combinations(system))

        out_systems = []
        for tmp_sys in new_systems:
            debug_sys(tmp_sys)
            if total_combinations(tmp_sys) > size:
                new_red = reduced_systems(tmp_sys, size)
                for r in new_red:
                    debug_sys(r)
                    out_systems.append(r)
                counter -= 1
            else:
                # print('adding')
                out_systems.append(tmp_sys)
        # print('returning')
        # print(out_systems)
        return out_systems
    else:
        # print('System is simple enough returning')
        # print([system])
        return [system]

def choose_moves(system):
    top_score = -9999
    result = None

    for system in reduced_systems(system, 100):
        o = []
        for key in system:
            o.append((key,system[key]['options'][0]))
        print('')
        print(o)
        best = pick_best(system)
        score = calculate_score(system, best)
        print(score)
        if score > top_score:
            result = best
            top_score = score
    return result

def calculate_score(system, moves):
    out = 0.0
    for start,end in moves:
        out += system[start]['scores'][system[start]['options'].index(end)]
    return out

# for bot, stuff in system.items():
#     print(bot)
#     print(stuff)
a = choose_moves(system)
print(a)
print(calculate_score(system, a))
print('')
b = pick_best(system)
print(b)
print(calculate_score(system, b))
