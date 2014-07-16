import rg
import math
import random
import itertools
import time
import operator
import sys
import copy

times = []
labels = {}
game_turn = -1
attack_damage = 10
feasable_size = 100000

spawn = {(7,1),(8,1),(9,1),(10,1),(11,1),(5,2),(6,2),(12,2),(13,2),(3,3),(4,3),(14,3),(15,3),(3,4),(15,4),(2,5),(16,5),(2,6),(16,6),(1,7),(17,7),(1,8),(17,8),(1,9),(17,9),(1,10),(17,10),(1,11),(17,11),(2,12),(16,12),(2,13),(16,13),(3,14),(15,14),(3,15),(4,15),(14,15),(15,15),(5,16),(6,16),(12,16),(13,16),(7,17),(8,17),(9,17),(10,17),(11,17)}
obstacle = {(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),(15,0),(16,0),(17,0),(18,0),(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(0,2),(1,2),(2,2),(3,2),(4,2),(14,2),(15,2),(16,2),(17,2),(18,2),(0,3),(1,3),(2,3),(16,3),(17,3),(18,3),(0,4),(1,4),(2,4),(16,4),(17,4),(18,4),(0,5),(1,5),(17,5),(18,5),(0,6),(1,6),(17,6),(18,6),(0,7),(18,7),(0,8),(18,8),(0,9),(18,9),(0,10),(18,10),(0,11),(18,11),(0,12),(1,12),(17,12),(18,12),(0,13),(1,13),(17,13),(18,13),(0,14),(1,14),(2,14),(16,14),(17,14),(18,14),(0,15),(1,15),(2,15),(16,15),(17,15),(18,15),(0,16),(1,16),(2,16),(3,16),(4,16),(14,16),(15,16),(16,16),(17,16),(18,16),(0,17),(1,17),(2,17),(3,17),(4,17),(5,17),(6,17),(12,17),(13,17),(14,17),(15,17),(16,17),(17,17),(18,17),(0,18),(1,18),(2,18),(3,18),(4,18),(5,18),(6,18),(7,18),(8,18),(9,18),(10,18),(11,18),(12,18),(13,18),(14,18),(15,18),(16,18),(17,18),(18,18)}
centre = rg.CENTER_POINT
move_count = 0


def adjacent((x, y)):
    return set([(x + dx, y + dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0))])


def sourrounding((x, y)):
    return set([(x + dx, y + dy) for dx, dy in ((1, -1), (-1, 1), (-1, -1), (1, 1), (0, 1), (1, 0), (0, -1), (-1, 0))])


def within_bounds((x, y)):
    return x > 0 and y > 0 and x < 18 and y < 18 and (x, y) not in obstacle


def squares_dist(position, distance):
    if distance == 0:
        return [position]
    else:
        out = []
        px = position[0]
        py = position[1]
        for x in range(distance):
            y = distance - x
            out += [(px+x, py+y), (px+y, py-x), (px-x, py-y), (px-y, py+x)]
        return out


def print_field(field):
    for j, row in enumerate(field):
        for i, x in enumerate(row):
            if (i, j) in obstacle:
                print('    '),
            else:
                print('{0:4d}'.format(int(x))),
            if i == len(row) - 1:
                print('')


def fieldval((x, y), field):
    return field[x][y]


def newfield():
    return [
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,],
     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,]]


# Will choose the most logical move and if two of equal logic value exist
# then it will randomly select one
def best_option(pos, logicfield):
    moves = [(x, logicfield[x[0]][x[1]]) for x in available_options(pos)]
    higest_score = max(moves, key=lambda x: x[1])[1]
    if higest_score:
        return random.choice([x[0] for x in moves if x[1] == higest_score])
    else:
        # No moves exist
        return None


# def available_moves(pos):
#     return adjacent(pos) - obstacle

def available_options((x, y)):
    return set([(x + dx, y + dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0), (0, 0))]) - obstacle


def flatten(listOfLists):
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(listOfLists)


def group_by_interferrence(movements):

    # Separate conflicting movement groups
    movement_groups = []
    pool = movements[:]

    while pool != []:
        group = [pool[0]]
        pool.remove(group[0])
        index = 0

        while index < len(group):
            ref = group[index]
            for item in pool[:]:
                # If the two bots have a common move option or
                # one of the bots occupies a move option of the
                # other bot
                if set(ref[1]) & set(item[1]):
                    # Add this bot to he movement group and remove from
                    # the pool
                    group.append(item)
                    pool.remove(item)
            index += 1

        movement_groups.append(group)

    return movement_groups


def movelist_sorted(bot, moves, gains):
    moves = [(x[0], x[1]) for x in zip(moves, gains)]
    moves.sort(key=lambda x: x[1], reverse=True)
    return [bot, [x[0] for x in moves], [x[1] for x in moves]]


def product(*args):
    pools = map(tuple, args)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool if y not in x]
    for prod in result:
        yield tuple(prod)


def movement_gains(bot_action, field):
    sx, sy = bot_action[0]
    moves = bot_action[1]
    return [(field[ex][ey] - field[sx][sy]) for (ex, ey) in moves]


def total_combinations(system):
    total_combinations = 1
    if type(system) == dict:
        for pos, bot in system.items():
            total_combinations *= len(bot['options'])
    else:
        for bot in system:
            total_combinations *= len(bot[1])
    return total_combinations


def pick_best(system, max_score=False):
    if max_score == False:
        max_score = 9999
    top_score = -9999
    scores = {}
    num_system = len(system)
    options = []
    result = None

    if type(system) == dict:
        for pos, bot in system.items():
            start = coord_to_cell(pos)
            moves = [(start, coord_to_cell(end)) for end in bot['options']]
            for index, move in enumerate(moves):
                scores[move] = bot['scores'][index]
            options.append(moves)
    else:
        for member in system:
            start = coord_to_cell(member[0])
            moves = [(start, coord_to_cell(end)) for end in member[1]]
            for index, move in enumerate(moves):
                scores[move] = member[2][index]
            options.append(moves)

    for possibility in itertools.product(*options):
        ends = [y for x, y in possibility]
        if len(set([y for x, y in possibility])) != num_system:
            continue
        if set(possibility) & set([(y, x) for x, y in possibility if x != y]):
            continue

        score = sum([scores[move] for move in possibility])
        if score == max_score:
            print('PICK BEST FOUND A SOLUTION EARLY - quitting')
            return [(cell_to_coord(x), cell_to_coord(y)) for x, y in possibility]
        elif score > top_score:
            result, top_score = possibility, score

    if result is None:
        return None
    else:
        if max_score != 9999:
            print('Ran full set of options and didnt find top result')
            print('Score is ' + str(sum([scores[move] for move in result])))
        return [(cell_to_coord(x), cell_to_coord(y)) for x, y in result]


def coord_to_cell(coord):
    return coord[0] + coord[1] * 19


def cell_to_coord(cell):
    x = cell % 19
    y = int(cell / 19)
    return (x, y)



def remove_option(system, bot, option):
    index = system[bot]['options'].index(option)
    del system[bot]['options'][index]
    del system[bot]['scores'][index]


def set_option(system, bot, option):
    index = system[bot]['options'].index(option)
    system[bot]['options'] = [system[bot]['options'][index]]
    system[bot]['scores'] = [system[bot]['scores'][index]]


def consolodate(system):
    repeat = False
    single_option_bots = [bot for bot in system.keys() if len(system[bot]['options']) == 1]
    taken_coords = [system[bot]['options'][0] for bot in single_option_bots]
    swap_moves = [(system[bot]['options'][0],bot) for bot in single_option_bots if system[bot]['options'][0] != bot]
    movable_bots = filter(lambda x: x not in single_option_bots, system.keys())
    for bot in movable_bots:
        for move in system[bot]['options'][:]:
            if move in taken_coords:
                remove_option(system, bot, move)
            elif (bot,move) in swap_moves:
                remove_option(system, bot, move)
            if len(system[bot]['options']) == 1:
                repeat = True
                # We have effectively just granted this bot a move
                # So lets repeat
    if repeat:
        consolodate(system)


def grant_move(system, (winner, target), return_system=False):
    set_option(system, winner, target)
    consolodate(system)
    if return_system:
        return system



def deny_move(system, (winner, target), return_system=False):
    remove_option(system, winner, target)
    consolodate(system)
    if return_system:
        return system


# def grant_move(system, (winner, target)):

#     for pos, bot in system.items():
#         if pos == winner:
#             # Make this move the only option for the winner
#             bot['scores'] = [bot['scores'][bot['options'].index(target)]]
#             bot['options'] = [target]
#         else:
#             if pos == target:
#                 # Remove bot swap as an option for target square
#                 try:
#                     swap_index = bot['options'].index(winner)
#                 except:
#                     swap_index = None

#                 if swap_index:
#                     print('swap found')
#                     del bot['options'][swap_index]
#                     del bot['scores'][swap_index]
#             if target in bot['options']:
#                 print('collision')
#                 # Remove this option from other bots move options
#                 bot['scores'].remove(bot['scores'][bot['options'].index(target)])
#                 bot['options'].remove(target)

#     return system



def print_system(system, scores=False,justbots=False,occupied=False,optional=False):
    global frontlinelogic
    field = frontlinelogic
    x_min = 18
    y_min = 18

    x_max = 0
    y_max = 0

    for x, y in system:
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x

        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y

    x_min -= 1
    x_max += 2
    y_min -= 1
    y_max += 2

    if occupied == False:
        occupied = []
    if optional == False:
        optional = []

    # relevant_cells = list(set(flatten([adjacent(bot) for bot in system])))
    relevant_cells = []
    num_participants = 0
    if justbots == False:
        justbots = []
        for member in system:
            relevant_cells += system[member]['options']
            relevant_cells += member
            if len(system[member]['options']) > 1:
                num_participants += 1
        relevant_cells = list(set(relevant_cells))
        for member in system:
            if len(system[member]['options']) == 1:
                relevant_cells.remove(system[member]['options'][0])
    else:
        for member in justbots:
            num_participants += 1
            relevant_cells += system[member]['options']
        relevant_cells = list(set(relevant_cells))

    print('BOT Positions:')
    print(str(num_participants) + ' participants')
    print('   '),
    for x, ax in enumerate(range(x_min, x_max)):
        print('{0:2d}'.format(ax) + ' '),
    print('')
    for y, ay in enumerate(range(y_min, y_max)):
        print('{0:2d}'.format(ay)),
        for x, ax in enumerate(range(x_min, x_max)):
            if ((ax, ay) in system and len(system[(ax, ay)]['options']) > 1) or (ax, ay) in justbots:
                if (ax, ay) in occupied:
                    print('  0'),
                elif (ax, ay) in optional:
                    print('  ?'),
                else:
                    print('  X'),
            elif (ax, ay) in relevant_cells or (ax,ay) in optional:
                if (ax, ay) in occupied:
                    print('  ='),
                else:
                    print('  -'),
            else:
                print('   '),
        print('')
    if scores:
        print('')
        print('Cell Scores:')
        print('   '),
        for x, ax in enumerate(range(x_min, x_max)):
            print('{0:2d}'.format(ax) + ' '),
        print('')
        for y, ay in enumerate(range(y_min, y_max)):
            print('{0:2d}'.format(ay)),
            for x, ax in enumerate(range(x_min, x_max)):
                if ((ax, ay) in system and len(system[(ax, ay)]['options']) > 1) or (ax, ay) in justbots:
                    print(' {0:2d}'.format(int(field[ay][ax]))),
                elif (ax, ay) in relevant_cells:
                    print(' {0:2d}'.format(int(field[ay][ax]))),
                else:
                    print('   '),
            print('')
    print('')


def cells_in_direction(start, direction):
    if start[0] == direction[0]:
        if start[1] == direction[1]:
            raise ValueError('Start and direction are the same location')
        # Vertical
        if start[1] > direction[1]:
            # Going up
            return [start] + [(start[0], direction[1]-y) for y in range(0, direction[1])]
        else:
            # Going down
            return [start] + [(start[0], y) for y in range(direction[1], 18)]
    elif start[1] == direction[1]:
        if start[0] == direction[0]:
            raise ValueError('Start and direction are the same location')
        # Horizontal
        if start[0] > direction[0]:
            # Going left
            return [start] + [(direction[0]-x, start[1]) for x in range(0, direction[0])]
        else:
            # Going right
            return [start] + [(x, start[1]) for x in range(direction[0], 18)]
    else:
        raise ValueError('Start and direction cells are not adjacent')


def print_target_system(system, occupied, optional, num_optional):
    x_min = 18
    y_min = 18

    x_max = 0
    y_max = 0

    for x, y in system:
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x

        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y

    x_min -= 1
    x_max += 2
    y_min -= 1
    y_max += 2
    print('')
    print('-------------------------------------')
    print('TARGET system:')
    print(str(len(occupied) + num_optional) + ' participants')
    print()
    print('   '),
    for x, ax in enumerate(range(x_min, x_max)):
        print('{0:2d}'.format(ax) + ' '),
    print('')
    for y, ay in enumerate(range(y_min, y_max)):
        print('{0:2d}'.format(ay)),
        for x, ax in enumerate(range(x_min, x_max)):
            if (ax, ay) in occupied:
                print('  X'),
            elif (ax, ay) in optional:
                print(' {0:2d}'.format(num_optional)),
            else:
                print('   '),
        print('')
    print('')


def is_beneficial_move(system, (start, end)):
    return system[start]['scores'][system[start]['options'].index(end)] > 0


def movable_bots(system):
    return [bot for bot in system if len(system[bot]['options']) > 1]


def coord_contestees(system, coord):
    return [bot for bot in adjacent(coord) if bot in system.keys()]


def single_gain_move(system, bot):
    gain_cells = []
    for index, score in enumerate(system[bot]['scores']):
        if score > 0:
            gain_cells.append(system[bot]['options'][index])

    if len(gain_cells) == 1:
        return gain_cells[0]
    else:
        return None


def available_for_move_by(system, bot, coord):
    # Check for a bot at this coordinate who could stay
    if coord in system.keys() and coord in system[coord]['options']:
        return False

    # No other bots can have this as a move option
    for contestant in coord_contestees(system, coord):
        if contestant != bot:
            if coord in system[contestant]['options']:
                if is_beneficial_move(system, (contestant, coord)):
                    return False
    return True


def grant_dangling_move(system):
    changed = False
    for bot in movable_bots(system):
        gain_move = single_gain_move(system, bot)
        if gain_move:
            if available_for_move_by(system, bot, gain_move):
                grant_move(system, (bot, gain_move))
                changed = True
                print('Awarded move for ' + str(bot)),
                print(' to ' + str(gain_move))
    return changed


def system_split(system):

    # All the movement possibilities
    bots = system.keys()
    moves = [system[bot]['options'] for bot in bots]
    gains = [system[bot]['scores'] for bot in bots]
    name_me = zip(bots, moves, gains)
    # Turn the moves into ordered lists
    movement_groups = [movelist_sorted(x[0], list(x[1]), x[2]) for x in name_me]

    # Separate conflicting movement groups
    groups = []
    pool = movement_groups[:]

    while pool != []:
        group = [pool[0]]
        pool.remove(group[0])
        index = 0

        while index < len(group):
            ref = group[index]
            for item in pool[:]:
                # If the two bots have a common move option or
                # one of the bots occupies a move option of the
                # other bot
                if set(ref[1]) & set(item[1]):
                    # Add this bot to he movement group and remove from
                    # the pool
                    group.append(item)
                    pool.remove(item)
            index += 1

        groups.append(group)

    systems = []

    for movement_group in groups:

        for pos in range(5):
            for i in range(len(movement_group)):
                if pos < len(movement_group[i][1]):
                    test = movement_group[i][1][pos]
                    contest = False
                    for j in range(len(movement_group)):
                        if j != i:
                            if test in movement_group[j][1]:
                                contest = True
                                break
                    if not contest:
                        movement_group[i] = [movement_group[i][0], movement_group[i][1][:pos+1], movement_group[i][2][:pos+1]]

    print('This is system split, groups are...')
    for i, g in enumerate(groups):
        print(i)
        for a in g:
            print('  ' + str(a))
        print('')
        print('')


    for movement_group in groups:
        system = {}
        for member in movement_group:
            system[member[0]] = {
                'options': member[1],
                'scores': member[2]
            }
        systems.append(system)

    return systems


def find_ideal_system(system, available_bots):
    global frontlinelogic
    field = frontlinelogic
    available_coords = []
    for bot in available_bots:
        available_coords += system[bot]['options']
    available_coords = list(set(available_coords))

    available_scores = []
    coords_by_score = {}
    for (x, y) in available_coords:
        score = int(field[y][x])
        available_scores.append(score)
        if score in coords_by_score:
            coords_by_score[score].append((x, y))
        else:
            coords_by_score[score] = [(x, y)]

    available_scores = list(set(available_scores))
    available_scores.sort(reverse=True)

    targets_occupied = []
    targets_optional = []
    num_optional = 0
    max_score = 0

    num_available_bots = len(available_bots)
    for score in available_scores:
        if num_available_bots > 0:
            coords = coords_by_score[score]
            num_coords = len(coords)
            if num_coords <= num_available_bots:
                targets_occupied += coords
                max_score += score * num_coords
            else:
                targets_optional += coords
                num_optional += num_available_bots
                max_score += score * num_available_bots
            num_available_bots -= num_coords

    result = {
        'levels': coords_by_score,
        'occupied': targets_occupied,
        'optional': targets_optional,
        'num_optional': num_optional,
        'available_bots': available_bots,
        'max_score': max_score
    }

    return result


def path_walk(path):
    """
    Return a nested list of possible paths that could be taken
    by a bot in an attempt to move from the start to the end of
    the given path list
    """
    if path == []:
        return []
    elif len(path) == 1:
        options = path[0]
        return [option for option in options]
    else:
        options = copy.deepcopy(path[0])
        next_squares = copy.deepcopy(path[1])
        remainder = None
        if len(path) > 2:
            remainder = copy.deepcopy(path[2:])
        bang = []
        for option in options:
            # print(option)
            rem_options = [list(adjacent(option) & set(next_squares))]
            if remainder:
                rem_options = rem_options + remainder
            bang.append((option, rem_options))
        return [[here] + path_walk(there) for here, there in copy.deepcopy(bang)]


def shortest_paths(start, end, available_squares):
    """
    Find the shortest paths between two coordinates
    using only the array of squares passed
    """
    squares_by_dist = [[start]]
    available_squares = set(available_squares)
    distance = 0
    at_radius = False
    while at_radius == False:
        distance += 1
        squares = squares_dist(start, distance)
        tmp = list(set(squares) & available_squares)
        if tmp == []:
            return None
        elif end in tmp:
            squares_by_dist.append([end])
            at_radius = True
        else:
            squares_by_dist.append(tmp)
        if distance > 19:
            break

    return path_walk(squares_by_dist)


def flaten_pathnest(element, level):
    """
    Take a nested array from shortest_paths and
    flatten it while removing paths that dont lead
    to the end square
    """
    out = []
    if type(element) == list:
        level += 1
        if len(element) > 1:
            for item in element:
                out += flaten_pathnest(item, level)
        return out
    else:
        level -= 1
        return [(element,level)]


def find_paths(start, end, available):
    """
    Return a list of the shortest possible paths between
    the given start and end points
    """
    path_nest = shortest_paths(start, end, available)
    flat_nest = flaten_pathnest(path_nest[0],0)
    paths = []
    tmp = []
    last_level = 0
    for node, level in flat_nest:
        if level < last_level:
            tmp = tmp[:level]
        tmp += [node]
        if node == end:
            paths.append(tmp)
            tmp = tmp[:level]
        last_level = level
    return paths




def determine_ideal_outcome(system):

    available_bots = movable_bots(system)
    print('determine_ideal_outcome called with ' + str(available_bots))
    last_available_bots = available_bots
    settled = False
    while settled == False:
        outcome = find_ideal_system(system, last_available_bots)

        ideal_system = set(outcome['occupied'] + outcome['optional'])

        valid_available_bots = []
        for bot in outcome['available_bots']:
            if set(system[bot]['options']) & ideal_system:
                valid_available_bots.append(bot)

        if valid_available_bots == last_available_bots:
            settled = True
        else:
            print('Determining ideal outcome again as the result changed')
            last_available_bots = valid_available_bots

    return outcome

    # Repeat, but this time only including the bots that can make it
    # into the ideal system
    # return find_ideal_system(system, valid_available_bots)


def check_moves(system, move_paths):
    tmp_sys = copy.deepcopy(system)

    for moves in move_paths:
        for start in range(len(moves)-1):
            end = start + 1
            try:
                grant_move(tmp_sys, (moves[start], moves[end]))
            except ValueError:
                print('Referenced non-available move')
                return False
    valid = is_valid(tmp_sys)
    if valid:
        print('Works... ' + str(move_paths))
        return True
    else:
        print('The sistem is invalid')
        return False

def make_moves(system, move_paths):
    for moves in move_paths:
        for start in range(len(moves)-1):
            end = start + 1
            grant_move(system, (moves[start], moves[end]))


def simplify_system(system, max_options):
    global feasable_size
    global frontlinelogic

    field = frontlinelogic
    score_absolute_initial = 0
    for x, y in system:
        score_absolute_initial += field[y][x]

    print('')
    print('')
    print('=> INITIAL')
    print_system(system)

    # Any unoccupied cell with 2 adjacent bots should be evaluated for
    # this simplification
    while grant_dangling_move(system):
        print('simplification made, repeating')

    print('')
    print('-------------------------------------')
    print('=> AFTER DANGLING GRANTS')
    print_system(system)

    # systems = system_split(system)
    # if len(systems) > 1:
    #     print('System can be split')
    #     for subsys in systems:
    #         simplify_system(subsys, feasable_size)
    #         for bot in system.keys():
    #             if subsys[bot]['options'] != system[bot]['options']:
    #                 print('Subsystem differs with bot ' + str(bot) + ' by')
    #                 print(system[bot])
    #                 print(subsys[bot])

    outcome = determine_ideal_outcome(system)
    print('outcome = ')
    for a in outcome:
        print(str(a) + ' - ' + str(outcome[a]))

    print_target_system(system,
                        outcome['occupied'],
                        outcome['optional'],
                        outcome['num_optional'])

    ideal_system = set(outcome['occupied'] + outcome['optional'])
    detached_bots = list(set(movable_bots(system)) - set(outcome['available_bots']))

    # Take the bots that couldnt make it to the system and calculate their moves
    # separately
    if len(detached_bots) > 0:
        sub_system = {}
        for bot in detached_bots:
            sub_system[bot] = {
                'options': system[bot]['options'],
                'scores': system[bot]['scores']
            }
        sub_systems = system_split(sub_system)
        for sub_system in sub_systems:
            tmp = pick_best(sub_system)
            for move in tmp:
                grant_move(system,move)


    # Make the simplifications that push the current available bots
    # into the ideal system
    for bot in outcome['available_bots']:
        if set(system[bot]['options']) & ideal_system:
            move_removals = list(set(system[bot]['options']) - ideal_system)
            for move_removal in move_removals:
                deny_move(system, (bot, move_removal))
        else:
            raise UserWarning('Bot ' + str(bot) + ' cant make it to the sub_system')


    print('')
    print('-------------------------------------')
    print('=> SYSTEM PUSHED TOWARDS IDEAL')
    print_system(system,
                 justbots=outcome['available_bots'],
                 occupied=outcome['occupied'],
                 optional=outcome['optional'],
                 scores=True)

    print('The system now has a total of ' + str(total_combinations(system)) + ' optins')

    # Bots that didn't partake in the grand simplification
    unavailable_bots = list(set(system.keys()) - set(outcome['available_bots']))
    free_unavailable = [bot for bot in unavailable_bots if len(system[bot]['options']) > 1]

    if len(free_unavailable) != 0:
        raise UserWarning('Some unavailable_bots arent frozen')

    # Calculate the score contribution from the non-sub_system bots
    remaining_score = 0
    for bot in unavailable_bots:
        x,y = system[bot]['options'][0]
        remaining_score += int(field[y][x])
    score_absolute_max = remaining_score + outcome['max_score']


    print('The initial system score was ' + str(score_absolute_initial))
    print('The maximum obtainable for the system is ' + str(score_absolute_max))
    score_gain_required = score_absolute_max - score_absolute_initial
    print('The score gain were looking for is ' + str(score_gain_required))
    system_score_gain_required = score_gain_required - sum(system[bot]['scores'][0] for bot in unavailable_bots)
    print('The system_score_gain_required = ' + str(system_score_gain_required))



    bots_in_optional = [bot for bot in outcome['available_bots'] if bot in outcome['optional']]
    bots_in_optional_moving_to_occupied = [bot for bot in bots_in_optional if len(system[bot]['options']) == 1 and system[bot]['options'][0] in outcome['occupied']]

    bots_outside_system = [bot for bot in outcome['available_bots'] if bot not in outcome['optional'] and bot not in outcome['occupied']]
    bots_outside_system_moving_to_optional = [bot for bot in bots_outside_system if len(set(system[bot]['options']) & set(outcome['optional'])) == len(system[bot]['options'])]
    bots_outside_system_moving_to_occupied = [bot for bot in bots_outside_system if len(set(system[bot]['options']) & set(outcome['occupied'])) == len(system[bot]['options'])]

    bots_in_occupied = [bot for bot in outcome['available_bots'] if bot in outcome['occupied']]
    bots_in_occupied_moving_to_optional = [bot for bot in bots_in_occupied if len(system[bot]['options']) == 1 and system[bot]['options'][0] in outcome['optional']]

    num_target_bots_in_optional = outcome['num_optional']
    num_target_bots_in_occupied = len(outcome['occupied'])

    current_bots_in_optional = bots_in_optional + bots_outside_system_moving_to_optional + bots_in_occupied_moving_to_optional
    current_bots_in_optional = filter(lambda x: x not in bots_in_optional_moving_to_occupied, current_bots_in_optional)
    current_bots_in_optional_that_can_move_to_occupied = [bot for bot in current_bots_in_optional if set(system[bot]['options']) & set(outcome['occupied'])]


    current_bots_in_occupied = bots_in_occupied + bots_in_optional_moving_to_occupied + bots_outside_system_moving_to_occupied
    current_bots_in_occupied = filter(lambda x: x not in bots_in_occupied_moving_to_optional, current_bots_in_occupied)
    current_bots_in_occupied_that_can_move_to_optional = [bot for bot in current_bots_in_occupied if set(system[bot]['options']) & set(outcome['optional'])]

    squares_that_will_be_occupied = [system[bot]['options'][0] for bot in system.keys() if len(system[bot]['options']) == 1]
    target_occupied_with_bot_now_or_definite_bot_next = list(set(squares_that_will_be_occupied) & set(outcome['occupied']))
    target_occupied_with_bot_now_or_definite_bot_next += current_bots_in_occupied
    target_occupied_not_occupied = list(set(outcome['occupied']) - set(target_occupied_with_bot_now_or_definite_bot_next))

    current_bots_outside = filter(lambda x: x not in bots_outside_system_moving_to_optional and x not in bots_outside_system_moving_to_occupied, bots_outside_system)

    min_possible_num_bots_in_optional = len(set(current_bots_in_optional) - set(current_bots_in_optional_that_can_move_to_occupied))

    movable_bots_in_occupied_that_have_to_move = [bot for bot in current_bots_in_occupied if bot not in system[bot]['options']]
    # Is this one even a thing?
    # max_num_bots_in_optional = set(current_bots_in_optional) + set(current_bots_in_occupied_that_can_move_to_optional)

    print('')

    consolodate(system)

    print('bots_in_optional = ' + str(bots_in_optional))
    print('bots_in_optional_moving_to_occupied = ' + str(bots_in_optional_moving_to_occupied))
    print('bots_outside_system = ' + str(bots_outside_system))
    print('bots_outside_system_moving_to_optional  = ' + str(bots_outside_system_moving_to_optional))
    print('bots_in_occupied = ' + str(bots_in_occupied))
    print('bots_in_occupied_moving_to_optional = ' + str(bots_in_occupied_moving_to_optional))

    print('movable_bots_in_occupied_that_have_to_move = ' + str(movable_bots_in_occupied_that_have_to_move))
    print('num_target_bots_in_optional = ' + str(num_target_bots_in_optional))
    print('num_target_bots_in_occupied = ' + str(num_target_bots_in_occupied))
    print('current_bots_in_optional = ' + str(current_bots_in_optional))
    print('current_bots_in_optional_that_can_move_to_occupied = ' + str(current_bots_in_optional_that_can_move_to_occupied))
    print('current_bots_in_occupied = ' + str(current_bots_in_occupied))
    print('current_bots_in_occupied_that_can_move_to_optional = ' + str(current_bots_in_occupied_that_can_move_to_optional))
    print('current_bots_outside = ' + str(current_bots_outside))
    print('target_occupied_not_occupied = ' + str(target_occupied_not_occupied))
    print('target_occupied_with_bot_now_or_definite_bot_next = ' + str(target_occupied_with_bot_now_or_definite_bot_next))

    print('')


    if min_possible_num_bots_in_optional > outcome['num_optional']:
        diff = outcome['num_optional'] - min_possible_num_bots_in_optional
        print('ALERT! - There ' + str(diff) + ' bots too many that will have to stay in optional squares')
        print('Occupied squares that need someone assigned are')
        print(target_occupied_not_occupied)

    try_freeze = False

    if len(current_bots_outside) > 0:
        for bot in current_bots_outside:
            if bot in system[bot]['options']:
                raise UserWarning('Bots need to come in but ' + str(bot) + ' outside staying still!')

    if num_target_bots_in_optional == 0:
        print('No optional squares exist so bots should just be packing into occupied squares')
    else:
        print('Optional squares exist')

        num_bots_to_move_into_optional = num_target_bots_in_optional - len(current_bots_in_optional)
        num_bots_to_move_into_occupied = num_target_bots_in_occupied - len(current_bots_in_occupied)

        if num_bots_to_move_into_optional > 0:
            print(str(num_bots_to_move_into_optional) + ' bots need to move into optional')

            if num_bots_to_move_into_occupied > 0:
                print('And ' + str(num_bots_to_move_into_occupied) + ' bots need to move into occupied')
            elif num_bots_to_move_into_occupied < 0:
                print('And ' + str(-num_bots_to_move_into_occupied) + ' bots need to move out of occupied')
                print('LOGIC NEEDS ATTENTION ON MOVE')
                print('bots_in_optional_moving_to_occupied = ' + str(bots_in_optional_moving_to_occupied))
                print('So lets move one of ' + str(current_bots_in_occupied_that_can_move_to_optional))
                print('Who is near the entering bot (above), into the nearest available optional square')


            else:
                print('But no bots need to move into occupied')

        elif num_bots_to_move_into_optional < 0:
            print(str(-num_bots_to_move_into_optional) + ' bots need to move out of optional')

            if num_bots_to_move_into_occupied > 0:
                print('And ' + str(num_bots_to_move_into_occupied) + ' bots need to move into occupied')
                print('len(current_bots_in_optional_that_can_move_to_occupied) = ' + str(len(current_bots_in_optional_that_can_move_to_occupied)))
                deficit = num_bots_to_move_into_occupied - len(current_bots_in_optional_that_can_move_to_occupied)
                print('Deficit = ' + str(deficit))
                if deficit > 0:
                    failed_occupied_coord_scores = sorted([field[y][x] for x,y in target_occupied_not_occupied])
                    print('failed_occupied_coord_scores = ' + str(failed_occupied_coord_scores))
                    optsqr = outcome['optional'][0]
                    optional_square_score = field[optsqr[1]][optsqr[0]]
                    score_reduction = 0
                    for index in range(deficit):
                        score_reduction -= failed_occupied_coord_scores[index] - optional_square_score
                    print('The max gain should now be reduced by ' + str(score_reduction))
                    score_absolute_max += score_reduction
                    score_gain_required += score_reduction
                    print('score_gain_required now = ' + str(score_gain_required))
                    print('score_absolute_max now = ' + str(score_absolute_max))
                else:
                    num_to_implement = len(target_occupied_not_occupied)
                    print('It should be possible to make this happen')
                    pot_outcomes = []
                    for to_coord in target_occupied_not_occupied:
                        tmp_outcomes = []
                        for from_coord in current_bots_in_optional_that_can_move_to_occupied:
                            out = find_paths(from_coord, to_coord, outcome['available_bots'] + [to_coord])
                            if out != []:
                                tmp_outcomes.append(out)
                        pot_outcomes.append(tmp_outcomes)

                    print('Like by doing one from ' + str(num_to_implement) + ' of the following solutions')
                    move_paths = []
                    for a in pot_outcomes:
                        move_paths.append(flatten(a))
                    combos = itertools.product(*move_paths)
                    invalids = []
                    found = False
                    for combo in combos:
                        flat_combo = list(flatten(combo))
                        if len(set(flat_combo)) == len(flat_combo):
                            found = True
                            print('Valid combo (checking) = ' + str(combo))
                            if check_moves(system, combo):
                                print('Found a way of moving the bots around...')
                                print(combo)
                                make_moves(system, combo)
                                break
                            else:
                                print(combo)
                        else:
                            invalids.append(combo)
                    if found == False:
                        print('No valid combos found, list follows')
                        for z in invalids:
                            print(z)



            elif num_bots_to_move_into_occupied < 0:
                print('And ' + str(-num_bots_to_move_into_occupied) + ' bots need to move out of occupied')
            else:
                print('But no bots need to move into occupied')

        else:
            print('No bots need to leave optional')
            print(num_target_bots_in_occupied)
            if num_bots_to_move_into_occupied > 0:
                print('And ' + str(num_bots_to_move_into_occupied) + ' bots need to move into occupied')
            elif num_bots_to_move_into_occupied < 0:
                print('And ' + str(-num_bots_to_move_into_occupied) + ' bots need to move out of occupied')
            else:
                unoccupied_occupied = [square for square in outcome['occupied'] if square not in current_bots_in_occupied]
                print('unoccupied_occupied')
                print(unoccupied_occupied)
                # TODO: Find a way to locate unoccupied (occupied) squares before attemping a freeze
                # Also, freeze is saying a valid solution is returned when freezing wouldnt generate a valid solution
                # -------------------------- running turn 29 ---------------------------
                print('And no bots need to move into occupied, will try to freeze')
                try_freeze = True

    print('')
    print('System result = ...')
    print('The system has a total of ' + str(total_combinations(system)) + ' options')
    for pos, bot in system.items():
        print(str(pos) + ' - ' + str(bot))
    print('')

    print('')

    outcome['score_absolute_max'] = score_absolute_max
    outcome['score_gain_required'] = score_gain_required

    return outcome


def attempt_freeze(system):
    free_bots = [bot for bot in system if len(system[bot]['options']) > 1]
    freeze_moves = [(bot, bot) for bot in free_bots if bot in system[bot]['options']]
    if len(freeze_moves) != len(free_bots):
        print('A movable bot cant stay where it is')
        return False
    can_freeze = check_moves(system, freeze_moves)
    if can_freeze:
        print('Can freeze, freezing system')
        make_moves(system, freeze_moves)
        return True
    else:
        print('Cant freeze system for some reason!')
        return False


    # # If we fixed everyones position that has options, how close do we get?
    # print('Testing a bot freeze situation')
    # test_sys = copy.deepcopy(system)
    # for bot in test_sys:
    #     if len(test_sys[bot]['options']) > 1 and bot in test_sys[bot]['options']:
    #         grant_move(test_sys, (bot, bot))

    # if is_valid(test_sys):
    #     print('Returning a valid solution')
    #     for bot in system:
    #         if len(system[bot]['options']) > 1 and bot in system[bot]['options']:
    #             grant_move(system, (bot, bot))
    #     return True
    # else:
    #     print('No valid solution')
    #     return False

def freeze(system, score_absolute_initial, score_absolute_max):
    # If we fixed everyones position that has options, how close do we get?
    print('Testing a bot freeze situation')
    test_sys = copy.deepcopy(system)
    for bot in test_sys:
        if len(test_sys[bot]['options']) > 1 and bot in test_sys[bot]['options']:
            grant_move(test_sys, (bot, bot))
    print('Did this generate a solution?')

    moves = []
    for bot in test_sys:
        if len(test_sys[bot]['options']) == 1:
            moves.append((bot, test_sys[bot]['options'][0]))
        else:
            moves = False
            break

    if moves == False:
        raise UserWarning('Invalid system on freeze')
    else:
        print('Yes it did')
        score_diff = calculate_relative_score(test_sys, moves)
        frozen_score = score_absolute_initial + score_diff
        print('The frozen system now has a score of ' + str(frozen_score))
        if frozen_score == score_absolute_max:
            print('Will apply this to the real system')
            for bot in system:
                if len(system[bot]['options']) > 1 and bot in system[bot]['options']:
                    grant_move(system, (bot, bot))



# def find_possible_simplifications(system):

#     best_candidates = None

#     # Find the cell involved with the most moves
#     cells = {}
#     for pos, bot in system.items():
#         for cell in bot['options']:
#             if cell in cells:
#                 cells[cell] += 1
#             else:
#                 cells[cell] = 1

#     # Exclude cells that no bot is occupying
#     valid_cells = system.keys()
#     hot_cell = None
#     for cell in cells.keys():
#         if cell not in valid_cells:
#             del cells[cell]

#     hot_cell = max(cells.iteritems(), key=operator.itemgetter(1))[0]

#     if cells[hot_cell] > 1:

#         candidates = {}
#         for pos, bot in system.items():
#             if hot_cell in bot['options']:
#                 score = bot['scores'][bot['options'].index(hot_cell)]
#                 candidates[pos] = score

#         best_candidates = [pos for pos in system if pos in candidates and len(system[pos]['options']) == 1]

#         # If not best candidate at this point, find the most deserving
#         if best_candidates == []:

#             best_candidates = []
#             for candidate in candidates.iteritems():
#                 best_candidates.append(candidate[0])

#             # Filter out candidates who would cause a bot to be left with no moves
#             for candidate in best_candidates[:]:
#                 for pos, bot in system.items():
#                     if pos == hot_cell:
#                         if set(bot['options']) - set([hot_cell, candidate]) == set():
#                             # print('detected and removed bad candidate' + str(candidate))
#                             best_candidates.remove(candidate)

#         return (hot_cell, best_candidates)

#     else:
#         bots = {}
#         max_opts = 0
#         for pos, bot in system.items():
#             opts = len(bot['options'])
#             bots[pos] = opts
#             if opts > max_opts:
#                 max_opts = opts

#         bots = [pos for pos, bot in system.items() if len(bot['options']) == max_opts]
#         winner = random.choice(bots)
#         out_options = []
#         for index, score in enumerate(system[winner]['scores']):
#             if score >= 0:
#                 out_options.append(system[winner]['options'][index])
#         return (out_options, winner)


# def test_system(system):
#     boi = [bot for bot in system if len(system[bot]['options']) < 2]
#     for bot in boi:
#         if system[bot]['options'] == []:
#             return False
#         else:
#             target = system[bot]['options'][0]
#             if target in system and len(system[target]['options']) < 3:
#                 if bot in system[target]['options']:
#                     if target in system[target]['options']:
#                         return False
#     return True

# def reduced_systems(system, size):

#     if total_combinations(system) > size:

#         cells, candidates = find_possible_simplifications(system)

#         if type(candidates) == list:
#             new_systems = [grant_move(copy.deepcopy(system), (candidate, cells)) for candidate in candidates]
#         elif type(cells) == list:
#             new_systems = [grant_move(copy.deepcopy(system), (candidates, cell)) for cell in cells]

#         filter(test_system, new_systems)

#         out_systems = []
#         for tmp_sys in new_systems:
#             if total_combinations(tmp_sys) > size:
#                 new_red = reduced_systems(tmp_sys, size)
#                 for r in new_red:
#                     out_systems.append(r)
#             else:
#                 out_systems.append(tmp_sys)
#         return out_systems
#     else:
#         return [system]


def is_valid(system):
    consolodate(system)

    if len([b for b in system if system[b]['options'] == []]) > 0:
        print('System failed because a bot has no moves')
        return False

    taken_moves = [system[bot]['options'][0] for bot in system if len(system[bot]['options']) == 1]
    if len(taken_moves) != len(set(taken_moves)):
        print('System failed because two bots take the same coordinate')
        return False


    return True


def is_settled(system):
    return len([b for b in system if len(system[b]['options']) == 1]) == len(system.keys())


# 'occupied': targets_occupied,
# 'optional': targets_optional,
# 'num_optional': num_optional,
# 'available_bots': available_bots,
# 'max_score': max_score
# outcome['current_bots_in_occupied'] = current_bots_in_occupied
# outcome['current_bots_outside'] = current_bots_outside
# outcome['current_bots_in_optional'] = current_bots_in_optional
def bot_to_move(system, outcome):
    # Are there bots that need to move?
    boi = [bot for bot in system if len(system[bot]['options']) > 1]
    print('possible bots to move = ' + str(boi))
    boi = filter(lambda x: x not in system[x]['options'], boi)
    print('filtered = ' + str(boi))

    if boi == []:
        # num_target_bots_in_optional = outcome['num_optional']
        # num_target_bots_in_occupied = len(outcome['occupied'])
        # if len(outcome['current_bots_outside']) > 0:
        #     for bot in outcome['current_bots_outside']:
        #         if bot in system[bot]['options']:
        #             raise UserWarning('Bots need to come in but ' + str(bot) + ' outside staying still!')

        # if num_target_bots_in_optional == 0:
        #     print('No optional squares exist so bots should just be packing into occupied squares')
        # else:
        #     print('Optional squares exist')

        #     num_bots_to_move_into_optional = num_target_bots_in_optional - len(outcome['current_bots_in_optional'])
        #     num_bots_to_move_into_occupied = num_target_bots_in_occupied - len(outcome['current_bots_in_occupied'])

        #     if num_bots_to_move_into_optional > 0:
        #         print(str(num_bots_to_move_into_optional) + ' bots need to move into optional')

        #         if num_bots_to_move_into_occupied > 0:
        #             print('And ' + str(num_bots_to_move_into_occupied) + ' bots need to move into occupied')
        #         elif num_bots_to_move_into_occupied < 0:
        #             print('And ' + str(-num_bots_to_move_into_occupied) + ' bots need to move out of occupied')
        #         else:
        #             print('But no bots need to move into occupied')

        #     elif num_bots_to_move_into_optional < 0:
        #         print(str(-num_bots_to_move_into_optional) + ' bots need to move out of optional')

        #         if num_bots_to_move_into_occupied > 0:
        #             print('And ' + str(num_bots_to_move_into_occupied) + ' bots need to move into occupied')
        #         elif num_bots_to_move_into_occupied < 0:
        #             print('And ' + str(-num_bots_to_move_into_occupied) + ' bots need to move out of occupied')
        #         else:
        #             print('But no bots need to move into occupied')

        #     else:
        #         print('No bots need to leave optional')
        #         print(num_target_bots_in_occupied)
        #         if num_bots_to_move_into_occupied > 0:
        #             print('And ' + str(num_bots_to_move_into_occupied) + ' bots need to move into occupied')
        #         elif num_bots_to_move_into_occupied < 0:
        #             print('And ' + str(-num_bots_to_move_into_occupied) + ' bots need to move out of occupied')
        #         else:
        #             unoccupied_occupied = [square for square in outcome['occupied'] if square not in outcome['current_bots_in_occupied']]
        #             print('unoccupied_occupied')
        #             print(unoccupied_occupied)
        #             # TODO: Find a way to locate unoccupied (occupied) squares before attemping a freeze
        #             # Also, freeze is saying a valid solution is returned when freezing wouldnt generate a valid solution
        #             # -------------------------- running turn 29 ---------------------------
        #             print('And no bots need to move into occupied, will try to freeze')
        print('No bots that need to move could be found')
        return None
    else:
        return random.choice(boi)


def system_walk(system, outcome):
    # print('Entered system walk with')
    # for a in system:
        # print(str(a) + ' - ' + str(system[a]))
    if is_settled(system) == False:
        btm = bot_to_move(system, outcome)
        if btm:
            print('Will move ' + str(btm))
            subsys = [grant_move(copy.deepcopy(system), (btm, move), True) for move in system[btm]['options']]
            pre_num = len(subsys)
            subsys = filter(is_valid, subsys)
            print(str(pre_num - len(subsys)) + ' systems were filtered as they were not valid')

            out = []
            for sys in subsys:
                # print(sys)
                if is_settled(sys):
                    # print('(SETTLED)')
                    if 'score_gain_required' in outcome and system_score_relative(sys) == outcome['score_gain_required']:
                        print('And is max gain - returning this system')
                        return [sys]
                    else:
                        out.append(sys)
                else:
                    # print('(RECURSING...)')
                    test = system_walk(sys, outcome)
                    if 'score_gain_required' in outcome:
                        for tmp_sys in test:
                            if system_score_relative(tmp_sys) == outcome['score_gain_required']:
                                print('Top solution detected - avalanching down')
                                return [tmp_sys]
                    else:
                        out += test

            return out
        else:
            if is_valid(system):
                # print('No bots to move - attempt a freeze')
                if attempt_freeze(system) == False:
                    print('attempt_freeze faield')
                    best = pick_best(system,max_gain)
                    for move in best:
                        print('granting move ' + str(move))
                        grant_move(system, move)
                else:
                    if 'score_gain_required' in outcome:
                        if system_score_relative(system) == outcome['score_gain_required']:
                            print('A system with max gain has been found!')
                        else:
                            print('The found system has a score of ' + str(system_score_relative(system)) + ' but we needed ' + str(outcome['score_gain_required']))
                            print('Returning - ' + str(system))
                            return [system]
            else:
                print('The system is invalid')
                return None

            return [system]
    else:
        print('system_walk - system is settled, returning')
        return [system]


def solve_system(system, outcome):
    top_score = -9999
    result = None
    possibilities = system_walk(system, outcome)
    if possibilities == []:
        print('SYSTEM WALK FAILED SO RUN A FULL SOULTION')
        return pick_best(system)
    if 'score_gain_required' not in outcome:
        for possibility in possibilities:
            print('Checking possibility')
            if system_score_relative(possibility) > top_score:
                print('New highest possibility = ')
                # for a in possibility:
                    # print(a)
                result = possibility
                top_score = system_score_relative(possibility)
            else:
                print('Stink solution')
    else:
        print('possibilities from system_walk are...')
        print(possibilities)
        for possibility in possibilities:
            if is_valid(possibility):
                print('checking possibility for score of ' + str(outcome['score_gain_required']))
                this_score = system_score_relative(possibility)
                print('this possibility has a score of ' + str(this_score))
                if system_score_relative(possibility) == outcome['score_gain_required']:
                    print('checking')
                    print(possibility)
                    print('Found a winner!!!!!!!!!!!!!!')
                    return possibility
                elif this_score > top_score:
                    result = possibility
                    top_score = this_score
            else:
                print('WTF THERE WAS AN INVALID RESULT')
        print('Got to the end of possibility checking without finding a top result')
        print('Will return the highest scoring result')
    if result == None:
        print('No possibilities')
        return None
    else:
        print('Maximum score found was ' + str(top_score))
        return result




def tc(label):
    global times, labels
    times.append(time.clock())
    if len(times) > 1:
        diff = (times[-1] - times[-2]) * 1000
        print('It took ' + ' {0:0.6f}'.format(diff) + 'ms for ' +  label + ' to complete')
        if label not in labels:
            labels[label] = diff
        else:
            labels[label] += diff

def ts():
    global times, labels
    for label in labels:
        print('It took a total of {0:0.2f} Ms for {1:s} to complete'.format(labels[label],label))
    times = []
    labels = {}



def choose_moves(system):
    global feasable_size
    tc('start')
    sys_backup = copy.deepcopy(system)
    outcome = simplify_system(system, feasable_size)
    tc('simplify_system')
    target_gain = False
    if 'score_gain_required' in outcome:
        target_gain = outcome['score_gain_required']
    if total_combinations(system) == 1:
        print('The system only has one possibility so returning early')
        return system
    else:
        out = solve_system(system, outcome)
        if out != None:
            print('solve_system returned - choose moves will return')
            for a in out:
                print(str(a) +  ' - ' + str(out[a]))
            return out
        else:
            print('solve_system returned NONE')


# def choose_moves(system):
#     global feasable_size
#     tc('start')
#     sys_backup = copy.deepcopy(system)
#     outcome = simplify_system(system, feasable_size)
#     tc('simplify_system')
#     if 'score_absolute_max' in outcome:
#         print('Picking best move - looking for score_gain of ' + str(outcome['score_gain_required']))
#         best = pick_best(system, outcome['score_gain_required'])
#     else:
#         print('Picking best move blindly')
#         best = pick_best(system)
#     tc('pick_best')
#     if best == None:
#         print('FUCK - THIS WENT BAD')
#         for a,b in system.items():
#             print(str(a) + ' - ' + str(b))

#         print('')
#         print('AND WE STARTED WITH ')
#         print('')
#         for a,b in sys_backup.items():
#             print(str(a) + ' - ' + str(b))

#     return best

# def choose_moves(system):
#     global feasable_size
#     top_score = -9999
#     result = None
#     tc('start')
#     ideal_system = simplify_system(system)
#     tc('simplify_system')
#     reduced_systems_set = reduced_systems(system, feasable_size)
#     tc('reduced_systems')
#     for system in reduced_systems_set:

#         best = pick_best(system)
#         tc('pick_best')

#         if best is None:
#             continue

#         score = calculate_relative_score(system, best)
#         if score > top_score:
#             result = best
#             top_score = score
#     return result


def system_score_relative(system):
    return sum([system[b]['scores'][0] for b in system])

def calculate_relative_score(system, moves):
    out = 0
    for start, end in moves:
        out += system[start]['scores'][system[start]['options'].index(end)]
    return out


def decide_actions(movements, recursed=False):
    global feasable_size

    final_movements = {}
    # The movements_group movement decisions have been split
    for movement_group in group_by_interferrence(movements[:]):

        # Go through each member truncating their list of options
        # to end at with the first option that no other robots
        # have available to them. Remember, options are sorted by benefit.

        reduced = movement_group[:]

        for pos in range(5):
            for i in range(len(movement_group)):
                if pos < len(movement_group[i][1]):
                    test = movement_group[i][1][pos]
                    contest = False
                    for j in range(len(movement_group)):
                        if j != i:
                            if test in movement_group[j][1]:
                                contest = True
                                break
                    if not contest:
                        reduced[i] = [reduced[i][0], reduced[i][1][:pos+1], reduced[i][2][:pos+1]]

        num_options = total_combinations(reduced)

        if num_options == 1:
            for index, member in enumerate(movement_group):
                final_movements[member[0]] = reduced[index][1][0]
        elif num_options < feasable_size:
            top_combo = pick_best(reduced)
            if top_combo is None:
                return None
            for index, member in enumerate(movement_group):
                final_movements[member[0]] = top_combo[index][1]
        else:
            system = {}
            for member in reduced:
                system[member[0]] = {
                    'options': member[1],
                    'scores': member[2]
                }
            breakdown = choose_moves(system)
            for bot in breakdown:
                final_movements[bot] = breakdown[bot]['options'][0]

    ts()
    return final_movements

decided_movements = None


class Robot:

    def level4_field(self, members):
        out = newfield()
        for distance in range(0, 13):
            for x, y in squares_dist(rg.CENTER_POINT, distance):
                if within_bounds((x, y)):
                    out[x][y] = 12-distance
        return out

    def act(self, game):
        global game_turn, attack_damage, spawn, obstacle, centre
        global move_count, decided_movements, frontlinelogic
        robots = game.robots

        if game.turn != game_turn:

            game_turn = game.turn
            turn = game_turn - 1

            friendlies = set([bot for bot in robots if robots[bot].player_id == self.player_id])
            enemies = set(robots)-friendlies

            ## Level 4 logic
            available_members = [x for x in friendlies]
            frontlinelogic = self.level4_field(available_members)

            # All the movement possibilities
            bots = [x for x in friendlies]
            moves = [available_options(x) for x in bots]
            gains = [movement_gains(action, frontlinelogic) for action in zip(bots, moves)]
            name_me = zip(bots, moves, gains)
            # Turn the moves into ordered lists
            group_sorted_movements = [movelist_sorted(x[0], list(x[1]), x[2]) for x in name_me]

            decided_movements = decide_actions(group_sorted_movements)

        try:
            move = decided_movements[self.location]

            if move == self.location:
                return ['guard', move]
            else:
                return ['move', move]
        except KeyError:
            return ['suicide', (9,9)]
