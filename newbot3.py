import rg
import math
import random
import itertools
import time
import operator
import heapq
import copy

times = []
labels = {}
game_turn = -1
attack_damage = 10
feasable_size = 100000

spawn = {(7,1),(8,1),(9,1),(10,1),(11,1),(5,2),(6,2),(12,2),(13,2),(3,3),(4,3),(14,3),(15,3),(3,4),(15,4),(2,5),(16,5),(2,6),(16,6),(1,7),(17,7),(1,8),(17,8),(1,9),(17,9),(1,10),(17,10),(1,11),(17,11),(2,12),(16,12),(2,13),(16,13),(3,14),(15,14),(3,15),(4,15),(14,15),(15,15),(5,16),(6,16),(12,16),(13,16),(7,17),(8,17),(9,17),(10,17),(11,17)}
deepspawn = {(3,3),(15,3),(15,15),(3,15)}
obstacle = {(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),(15,0),(16,0),(17,0),(18,0),(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(0,2),(1,2),(2,2),(3,2),(4,2),(14,2),(15,2),(16,2),(17,2),(18,2),(0,3),(1,3),(2,3),(16,3),(17,3),(18,3),(0,4),(1,4),(2,4),(16,4),(17,4),(18,4),(0,5),(1,5),(17,5),(18,5),(0,6),(1,6),(17,6),(18,6),(0,7),(18,7),(0,8),(18,8),(0,9),(18,9),(0,10),(18,10),(0,11),(18,11),(0,12),(1,12),(17,12),(18,12),(0,13),(1,13),(17,13),(18,13),(0,14),(1,14),(2,14),(16,14),(17,14),(18,14),(0,15),(1,15),(2,15),(16,15),(17,15),(18,15),(0,16),(1,16),(2,16),(3,16),(4,16),(14,16),(15,16),(16,16),(17,16),(18,16),(0,17),(1,17),(2,17),(3,17),(4,17),(5,17),(6,17),(12,17),(13,17),(14,17),(15,17),(16,17),(17,17),(18,17),(0,18),(1,18),(2,18),(3,18),(4,18),(5,18),(6,18),(7,18),(8,18),(9,18),(10,18),(11,18),(12,18),(13,18),(14,18),(15,18),(16,18),(17,18),(18,18)}
centre = rg.CENTER_POINT
move_count = 0


def adjacent((x, y)):
    return set([(x + dx, y + dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0))])


def surrounding((x, y)):
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

    print('   '),
    for x, ax in enumerate(range(19)):
        print('{0:2d}'.format(ax) + ' '),
    print('')
    for y, ay in enumerate(range(19)):
        print('{0:2d} '.format(ay)),
        for x, ax in enumerate(range(19)):
            if (ax, ay) in obstacle:
                print('   '),
            else:
                print('{0:2d} '.format(int(field[ay][ax]))),
        print('')


def fieldval((x, y), field):
    return int(field[y][x])


def newfield():
    return [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]
    ]


# Will choose the most logical move and if two of equal logic value exist
# then it will randomly select one
def best_option(pos, logicfield):
    moves = [(x, fieldval(x, logicfield)) for x in available_options(pos)]
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


def movelist_sorted(bot, options, gains):
    moves = [(x[0], x[1]) for x in zip(options, gains)]
    moves.sort(key=lambda x: x[1], reverse=True)
    return [bot, [x[0] for x in moves], [x[1] for x in moves]]
#
#
#def product(*args):
#    pools = map(tuple, args)
#    result = [[]]
#    for pool in pools:
#        result = [x+[y] for x in result for y in pool if y not in x]
#    for prod in result:
#        yield tuple(prod)
#
#
#def movement_gains(bot_action, field):
#    coord_from = bot_action[0]
#    moves = bot_action[1]
#    return [(fieldval(coord_to, field) - fieldval(coord_from, field)) for coord_to in moves]


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

    for pos, bot in system.items():
        start = coord_to_cell(pos)
        moves = [(start, coord_to_cell(end)) for end in bot['options']]
        for index, move in enumerate(moves):
            scores[move] = bot['scores'][index]
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


def grant_move(system, winner, target, return_system=False):
    set_option(system, winner, target)
    consolodate(system)
    if return_system:
        return system



def deny_move(system, winner, target, return_system=False):
    remove_option(system, winner, target)
    consolodate(system)
    if return_system:
        return system



def get_print_dimensions(system):
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
    return (x_min, x_max, y_min, y_max)

def show_system(system,
                 optionals=False,
                 occupieds=False,
                 sym_occupied='O',
                 sym_option='.',
                 sym_occupied_occupied='0',
                 sym_occupied_optional='?',
                 sym_unoccupied_occupied='=',
                 sym_unoccupied_optional='-'):

    x_min, x_max, y_min, y_max = get_print_dimensions(system)

    if optionals == False:
        optionals = []
    if occupieds == False:
        occupieds = []

    squares = {}
    # Fill options
    for bot in system:
        for option in system[bot]['options']:
            squares[option] = sym_option
    # Fill bot positions
    for bot in system:
        squares[bot] = sym_occupied

    # Amend for optionals
    for square in optionals:
        if square in squares:
            if squares[square] == sym_occupied:
                squares[square] = sym_occupied_optional
            else:
                squares[square] = sym_unoccupied_optional
        else:
            squares[square] = sym_unoccupied_occupied

    # Amend for occupieds
    for square in occupieds:
        if square in squares:
            if squares[square] == sym_occupied:
                squares[square] = sym_occupied_occupied
            else:
                squares[square] = sym_unoccupied_occupied
        else:
            squares[square] = sym_unoccupied_occupied


    print('BOT Positions:')
    print(str(len(system)) + ' participants')
    print('   '),
    for x, ax in enumerate(range(x_min, x_max)):
        print('{0:2d}'.format(ax) + ' '),
    print('')
    for y, ay in enumerate(range(y_min, y_max)):
        print('{0:2d}'.format(ay)),
        for x, ax in enumerate(range(x_min, x_max)):
            if (ax, ay) in squares:
                print('  ' + squares[(ax, ay)]),
            else:
                print('   '),
        print('')


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
                try:
                    relevant_cells.remove(system[member]['options'][0])
                except:
                    pass
                    # Who cares its only printing
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
                    print(' {0:2d}'.format(int(fieldval((ay, ax), field)))),
                elif (ax, ay) in relevant_cells:
                    print(' {0:2d}'.format(int(fieldval((ay, ax), field)))),
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
                grant_move(system, bot, gain_move)
                changed = True
                print('Awarded move for ' + str(bot)),
                print(' to ' + str(gain_move))
    return changed


def split_sys(input_system):

    system = copy.deepcopy(input_system)

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

    for movement_group in groups:
        sub_system = {}
        for member in movement_group:
            sub_system[member[0]] = {
                'options': member[1],
                'scores': member[2]
            }
        systems.append(sub_system)

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
        score = fieldval((x, y), field)
        # score = int(field[y][x])
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


# def path_walk(path):
#     """
#     Return a nested list of possible paths that could be taken
#     by a bot in an attempt to move from the start to the end of
#     the given path list
#     """
#     if path == []:
#         return []
#     elif len(path) == 1:
#         options = path[0]
#         return [option for option in options]
#     else:
#         options = copy.deepcopy(path[0])
#         next_squares = copy.deepcopy(path[1])
#         remainder = None
#         if len(path) > 2:
#             remainder = copy.deepcopy(path[2:])
#         bang = []
#         for option in options:
#             # print(option)
#             rem_options = [list(adjacent(option) & set(next_squares))]
#             if remainder:
#                 rem_options = rem_options + remainder
#             bang.append((option, rem_options))
#         return [[here] + path_walk(there) for here, there in copy.deepcopy(bang)]


# def shortest_paths(start, end, available_squares):
#     """
#     Find the shortest paths between two coordinates
#     using only the array of squares passed
#     """
#     squares_by_dist = [[start]]
#     available_squares = set(available_squares)
#     distance = 0
#     at_radius = False
#     while at_radius == False:
#         distance += 1
#         squares = squares_dist(start, distance)
#         tmp = list(set(squares) & available_squares)
#         if tmp == []:
#             return None
#         elif end in tmp:
#             squares_by_dist.append([end])
#             at_radius = True
#         else:
#             squares_by_dist.append(tmp)
#         if distance > 19:
#             break

#     return path_walk(squares_by_dist)


# def flaten_pathnest(element, level=-1):
#     """
#     Take a nested array from shortest_paths and
#     flatten it while removing paths that dont lead
#     to the end square
#     """
#     out = []
#     if type(element) == list:
#         for item in element:
#             if type(item) == list:
#                 out += flaten_pathnest(item, level)
#             else:
#                 level += 1
#                 out.append((item, level))
#         return out
#     else:
#         # level -= 1
#         return [(element,level)]


# def find_paths(start, end, available):
#     """
#     Return a list of the shortest possible paths between
#     the given start and end points
#     """
#     path_nest = shortest_paths(start, end, available)
#     flat_nest = flaten_pathnest(path_nest)
#     paths = []
#     tmp = []
#     last_level = -1
#     for node, level in flat_nest:
#         try:
#             tmp[level] = node
#         except:
#             tmp.append(node)

#         if node == end:
#             paths.append(tmp)
#             tmp = tmp[:level]
#         last_level = level
#     return paths

class Cell(object):
    def __init__(self, x, y):
        """
        Initialize new cell

        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        """
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

class AStar(object):

    def __init__(self, available_coords):
        self.op = []
        heapq.heapify(self.op)
        self.cl = set()
        self.cells = []
        self.gridHeight = 19
        self.gridWidth = 19
        self.available_coords = available_coords


    def find_path(self, start, end):
        path = []
        self.cells = []
        for x, y in self.available_coords:
            self.cells.append(Cell(x, y))
        self.cells.append(Cell(start[0], start[1]))
        self.cells.append(Cell(end[0], end[1]))
        self.end = self.get_cell(start[0], start[1])
        self.start = self.get_cell(end[0], end[1])

        # add starting cell to open heap queue
        heapq.heappush(self.op, (self.start.f, self.start))
        while len(self.op):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.op)
            # add cell to closed list so we don't process it twice
            self.cl.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                return self.return_path()

            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for c in adj_cells:
                if (c.x, c.y) in self.available_coords and c not in self.cl:
                    if (c.f, c) in self.op:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found for this adj
                        # cell.
                        if c.g > cell.g + 10:
                            self.update_cell(c, cell)
                    else:
                        self.update_cell(c, cell)
                        # add adj cell to open list
                        heapq.heappush(self.op, (c.f, c))


    def get_heuristic(self, cell):
        """
        Compute the heuristic value H for a cell: distance between
        this cell and the ending cell multiply by 10.

        @param cell
        @returns heuristic value H
        """
        return (abs(cell.x - self.end.x) + abs(cell.y - self.end.y)) * 10

    def get_cell(self, x, y):
        """
        Returns a cell from the cells list

        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        # return self.cells[x * self.gridHeight + y]
        return [cell for cell in self.cells if cell.x == x and cell.y == y][0]

    def get_adjacent_cells(self, cell):
        return [self.get_cell(x, y) for x, y in adjacent((cell.x, cell.y)) if (x, y) in self.available_coords]

    def return_path(self):
        path = []
        cell = self.end
        while cell.parent is not self.start:
            path.append((cell.x, cell.y))
            cell = cell.parent
        path.append((cell.x, cell.y))
        path.append((self.start.x, self.start.y))
        return path


    def update_cell(self, adj, cell):
        """
        Update adjacent cell

        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g


def find_path(start, end, available):
    a = AStar(available + [start] + [end])
    path = a.find_path(start, end)
    if path is None:
        return None
    out = []
    i, length = 0, len(path) - 1
    while i < length:
        out.append((path[i], path[i+1]))
        i += 1
    return out



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
                print('Move ' + str((moves[start], moves[end])))
                grant_move(tmp_sys, moves[start], moves[end])
            except ValueError:
                print('Referenced non-available move ' + str((moves[start], moves[end])))
                return False
            except KeyError:
                print('Attempted to move non-existant bot ' + str((moves[start], moves[end])))
                return False
    valid = is_valid(tmp_sys)
    if valid:
        print('Works... ' + str(move_paths))
        return True
    else:
        print('The system is invalid')
        return False


def make_moves(system, move_paths):
    for moves in move_paths:
        for start in range(len(moves)-1):
            end = start + 1
            grant_move(system, moves[start], moves[end])
    for a in system:
        print(str(a) + ' - ' + str(system[a]))


def mixer(xs, ys):
    tc('start')
    """
    Take two lists of equal size and return their combinations where no
    elements are repeated
    """
    out = []
    length = len(xs)
    a = [(a,b) for a in xs for b in ys]
    z = []
    for start in [x * length for x in range(length)]:
        z.append(a[start:start+length])
    for combo in itertools.product(*z):
        used = [x[1] for x in combo]
        if len(set(used)) == len(used):
            out.append([x for x in combo])
    tc('mixer')
    return out

def mix_lists(xs, ys):
    tc('start')
    """
    Take two lists, each of any length, and return their combinations where
    no elements are repeated
    """
    out = []
    if len(xs) < len(ys):
        for _ys_ in itertools.combinations(ys, len(xs)):
            out += mixer(xs, _ys_)
    elif len(xs) > len(ys):
        for _xs_ in itertools.combinations(xs, len(ys)):
            out += mixer(_xs_, ys)
    else:
        out = mixer(xs, ys)
    tc('mix_lists')
    return out



def solve_microsystems(system):
        print('Identify identical contest sets and grant')
        copies = [[a,b] for a in system for b in system if a != b and (set(system[a]['options']) - set([a])) == (set(system[b]['options']) - set([b])) and (set(system[a]['options']) - set([a]) != set()) and ((set(system[a]['options']) - set([a])) & set(system.keys()) == set())]
        micro_systems_pairs = []
        for pair in copies[:]:
            if pair not in micro_systems_pairs and [pair[1], pair[0]] not in micro_systems_pairs:
                micro_systems_pairs.append(pair)

        if micro_systems_pairs != []:
            print('Found micro-systems-pairs')

        for i, (botA, botB) in enumerate(micro_systems_pairs):
            micro_system = {
                botA: system[botA],
                botB: system[botB]
            }
            print('Micro-system #' + str(i) + ' = ' + str(micro_system))
            best = pick_best(micro_system)
            make_moves(system, best)

        return micro_systems_pairs != []


def pick_best_with_bots(system, bots):
    micro_system = {}
    for bot in bots:
        micro_system[bot] = system[bot]
    best = pick_best(micro_system)
    make_moves(system, best)


def try_movement_sets(system, targets, candidates, squares):
    global feasable_size
    print('')
    print('')
    print('')
    print('TRY MOVEMENT SETS')

    while solve_microsystems(system):
        print('solve_microsystems reduction made, repeating')
    else:
        print('no solve_microsystems reductions made')


    while grant_dangling_move(system):
        print('simplification made, repeating')
    else:
        print('No simplifications made')

    if len(targets) == 1 and len(candidates) == 1:
        path = find_path(candidates[0], targets[0], squares)
        if path is not None:
            make_moves(system, path)
            return True
        else:
            return False


    tc('start')
    print('try_movement_sets dimensions')
    print(str(len(targets)) + ' targets')
    print(str(len(candidates)) + ' candidates')
    match_sets = mix_lists(candidates, targets)

    # precheck for bad links
    print('Precheck FOR BAD LINKS')
    bad_links = []
    for end in targets:
        for start in candidates:
            path = find_path(start, end, squares)
            print(str(start) + ' -> ' + str(end) + ' = ' + str(path))
            if path is None:
                print('bad')
                bad_links.append((start, end))
            else:
                print('okay')

    print('bad links = ' + str(bad_links))

    available_coords = set(squares)
    for match_set in match_sets:
        print('')
        print('Looking at ' + str(match_set))
        set_paths = []
        skip = False
        taken_coords = set()
        for start, end in match_set:
            if (start, end) not in bad_links:
                tmp = copy.deepcopy(available_coords)
                coords = tmp.difference(taken_coords)
                print('Find a path between ' + str(start) + ' and ' + str(end))
                print('Using coords ' + str(list(coords)))
                path = find_path(start, end, list(coords))
                if path is None:
                    print('couldnt path ' + str(start) + ' to ' + str(end))
                    skip = True
                    break
                else:
                    print('pathed as ' + str(path))
                    coords = [end for start, end in path]
                    coords.append(path[0][0])
                    print('used coords = ' + str(coords))
                    taken_coords = set(list(taken_coords) + coords)
                    set_paths.append(path)

        print('Finished generating path sets')
        print(set_paths)
        print('')

        if skip:
            continue
        else:
            for path in set_paths:
                make_moves(system, path)
            tc('try_movement_sets')
            return True






        # if skip == False:
        #     # print('Checking match_set, ' + str(match_set))
        #     # print('Which generated the set_paths ' + str(set_paths))

        #     for path_group in itertools.product(*set_paths):
        #         # print('Checking ' + str(path_group))
        #         if check_moves(system, path_group):
        #             # print('Looking good, implementing set')
        #             make_moves(system, path_group)
        #             # tc('try_movement_sets')
        #             return True
        #     # print('Tried all moves but none worked')
        # # else:
        #     # print('Skipped as no paths')

    # print('Fell out of loop without a solution')
    tc('try_movement_sets')
    return False


def make_obvious_moves(system, detail, debug=False):
    changed = False
    if debug:
        print('Precheck for obvious moves')
    for target in detail['target_occupied_not_occupied'][:]:
        adjacent_bots = adjacent(target)
        adjacent_bots_movable = list(set(adjacent_bots) & set(detail['current_bots_in_optional_that_can_move_to_occupied'] + detail['movable_bots_in_occupied_that_have_to_move']))
        if len(adjacent_bots_movable) == 1:
            bot_to_move = adjacent_bots_movable[0]
            if debug:
                print('Forced ' + str(bot_to_move) + ' to move into ' + str(target) + ' as only bot for this target')
            detail['target_occupied_not_occupied'].remove(target)
            grant_move(system, adjacent_bots_movable[0], target)
            changed = True
            if bot_to_move in detail['current_bots_in_optional_that_can_move_to_occupied']:
                detail['current_bots_in_optional_that_can_move_to_occupied'].remove(bot_to_move)
            else:
                detail['movable_bots_in_occupied_that_have_to_move'].remove(bot_to_move)
            if bot_to_move in detail['movable_bots_in_occupied']:
                detail['movable_bots_in_occupied'].remove(bot_to_move)
    for source in detail['current_bots_in_optional_that_can_move_to_occupied']:
        adjacent_coords = adjacent(source)
        adjacent_targets_reachable = list(set(adjacent_coords) & set(detail['target_occupied_not_occupied']))
        if len(adjacent_targets_reachable) == 1:
            bot_to_move = source
            target = adjacent_targets_reachable[0]
            if debug:
                print('Forced ' + str(bot_to_move) + ' to move into ' + str(target) + ' as only target for this bot')
            detail['target_occupied_not_occupied'].remove(target)
            if target in system[bot_to_move]['options']:
                grant_move(system, bot_to_move, target)
                changed = True
                if bot_to_move in detail['current_bots_in_optional_that_can_move_to_occupied']:
                    detail['current_bots_in_optional_that_can_move_to_occupied'].remove(bot_to_move)
                if bot_to_move in detail['movable_bots_in_occupied_that_have_to_move']:
                    detail['movable_bots_in_occupied_that_have_to_move'].remove(bot_to_move)
                if bot_to_move in detail['movable_bots_in_occupied']:
                    detail['movable_bots_in_occupied'].remove(bot_to_move)


    if changed:
        print('simplification made, will repeat')
        make_obvious_moves(system, detail, debug)


def system_details(system, outcome, field):

    score_absolute_initial = 0
    for bot in system:
        score_absolute_initial += fieldval(bot, field)
    # Bots that didn't partake in the grand simplification
    outcome['available_bots'] = set(outcome['available_bots']) - set([bot for bot in outcome['available_bots'] if len(system[bot]['options']) == 1])
    unavailable_bots = list(set(system.keys()) - outcome['available_bots'])

    free_unavailable = [bot for bot in unavailable_bots if len(system[bot]['options']) > 1]
    if len(free_unavailable) != 0:
        print('ERROR: THE FOLLOWING BOTS WERENT FROZEN - MANUALLY freezing')
        print([bot for bot in free_unavailable if len(system[bot]['options']) > 1])
        pick_best_with_bots(system, free_unavailable)
        # raise UserWarning('Some unavailable_bots are not frozen')

    # Calculate the score contribution from the non-sub_system bots
    remaining_score = 0
    for bot in unavailable_bots:
        x,y = system[bot]['options'][0]
        # remaining_score += int(field[y][x])
        remaining_score += fieldval((x, y), field)

    score_absolute_max = remaining_score + outcome['max_score']
    score_gain_required = score_absolute_max - score_absolute_initial
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
    current_bots_in_optional_that_can_move_to_other_optional = [bot for bot in current_bots_in_optional if set(system[bot]['options']) & set(outcome['optional'])]
    current_bots_in_optional = filter(lambda x: x not in bots_in_optional_moving_to_occupied, current_bots_in_optional)
    current_bots_in_optional_that_can_move_to_occupied = [bot for bot in current_bots_in_optional if set(system[bot]['options']) & set(outcome['occupied'])]
    current_bots_in_occupied = bots_in_occupied + bots_in_optional_moving_to_occupied + bots_outside_system_moving_to_occupied
    movable_bots_in_occupied = [bot for bot in current_bots_in_occupied if len(system[bot]['options']) > 1]
    current_bots_in_occupied = filter(lambda x: x not in bots_in_occupied_moving_to_optional, current_bots_in_occupied)
    current_bots_in_occupied_that_can_move_to_optional = [bot for bot in current_bots_in_occupied if set(system[bot]['options']) & set(outcome['optional'])]
    squares_that_will_be_occupied = [system[bot]['options'][0] for bot in system.keys() if len(system[bot]['options']) == 1]
    target_occupied_with_bot_now_or_definite_bot_next = list(set(squares_that_will_be_occupied) & set(outcome['occupied']))
    target_occupied_with_bot_now_or_definite_bot_next += current_bots_in_occupied
    target_occupied_not_occupied = list(set(outcome['occupied']) - set(target_occupied_with_bot_now_or_definite_bot_next))
    current_bots_outside = filter(lambda x: x not in bots_outside_system_moving_to_optional and x not in bots_outside_system_moving_to_occupied, bots_outside_system)
    min_possible_num_bots_in_optional = len(set(current_bots_in_optional) - set(current_bots_in_optional_that_can_move_to_occupied))
    movable_bots_in_occupied_that_have_to_move = [bot for bot in movable_bots_in_occupied if bot not in system[bot]['options']]


    details = {
       'score_absolute_initial': score_absolute_initial,
       'score_absolute_max': score_absolute_max,
       'score_gain_required': score_gain_required,
       'bots_in_optional': bots_in_optional,
       'bots_in_optional_moving_to_occupied': bots_in_optional_moving_to_occupied,
       'bots_outside_system': bots_outside_system,
       'bots_outside_system_moving_to_optional': bots_outside_system_moving_to_optional,
       'bots_outside_system_moving_to_occupied': bots_outside_system_moving_to_occupied,
       'bots_in_occupied': bots_in_occupied,
       'bots_in_occupied_moving_to_optional': bots_in_occupied_moving_to_optional,
       'num_target_bots_in_optional': num_target_bots_in_optional,
       'num_target_bots_in_occupied': num_target_bots_in_occupied,
       'current_bots_in_optional': current_bots_in_optional,
       'current_bots_in_optional': current_bots_in_optional,
       'current_bots_in_optional_that_can_move_to_other_optional' : current_bots_in_optional_that_can_move_to_other_optional,
       'current_bots_in_optional_that_can_move_to_occupied': current_bots_in_optional_that_can_move_to_occupied,
       'current_bots_in_occupied': current_bots_in_occupied,
       'movable_bots_in_occupied': movable_bots_in_occupied,
       'current_bots_in_occupied': current_bots_in_occupied,
       'current_bots_in_occupied_that_can_move_to_optional': current_bots_in_occupied_that_can_move_to_optional,
       'squares_that_will_be_occupied': squares_that_will_be_occupied,
       'target_occupied_with_bot_now_or_definite_bot_next': target_occupied_with_bot_now_or_definite_bot_next,
       'target_occupied_not_occupied': target_occupied_not_occupied,
       'current_bots_outside': current_bots_outside,
       'min_possible_num_bots_in_optional': min_possible_num_bots_in_optional,
       'movable_bots_in_occupied_that_have_to_move': movable_bots_in_occupied_that_have_to_move
    }
    return details




def reduce_sys(system):
    reduced = False
    for index in range(5):
        for bot in system.keys():
            if index < len(system[bot]['options']) - 1:
                test_move = system[bot]['options'][index]
                contest = False
                for contestant in [x for x in system.keys() if x != bot]:
                    if test_move in system[contestant]['options']:
                        contest = True
                        break
                if contest == False:
                    system[bot]['options'] = system[bot]['options'][:index+1]
                    system[bot]['scores'] = system[bot]['scores'][:index+1]
                    reduced = True
    consolodate(system)
    return reduced


def simplify_sys(system, field, debug=False):
    complexity_entry = total_combinations(system)

    while reduce_sys(system):
        print('System has been reduced')

    global feasable_size

    if debug:
        print('')
        print('')
        print('=> INITIAL')
        print_system(system)

    # Any unoccupied cell with 2 adjacent bots should be evaluated for
    # this simplification
    while grant_dangling_move(system):
        if debug:
            print('simplification made, repeating')

    if debug:
        print('')
        print('-------------------------------------')
        print('=> AFTER DANGLING GRANTS')
        print_system(system)


    systems = split_sys(system)

    if len(systems) > 1:
        if debug:
            print('System can be split into ' + str(len(systems)) + ' systems')
        for i, subsys in enumerate(systems):
            if debug:
                print('Solving system # ' + str(i))
                for a in subsys:
                    print(str(a) + ' - ' + str(subsys[a]))
            num_outcomes = total_combinations(subsys)
            if num_outcomes < int(feasable_size / 10):
                if num_outcomes == 1:
                    if debug:
                        print('This system has 1 move so it already solved!')
                    continue
                else:
                    if debug:
                        print('This subsystem has less than ' + str(int(feasable_size / 10)) + ' options, solving')
                    best = pick_best(subsys)
                    if best is not None:
                        make_moves(system, best)
                    else:
                        print('BEST MO')
            else:
                if debug:
                    print('A subsystem...')
                    print('has ' + str(len(subsys)) + ' members')
                    print(str(total_combinations(subsys)) + ' combinations')
                simplify_sys(subsys, field)
                if debug:
                    print('simplified...')
                    print(str(total_combinations(subsys)) + ' combinations')
                print('')
                for bot in subsys:
                    if subsys[bot]['options'] != system[bot]['options']:
                        removed_moves = list(set(system[bot]['options']) - set(subsys[bot]['options']))
                        if debug:
                            print('Subsystem differs with bot ' + str(bot) + ' by')
                            print('system = ' + str(bot) + ': ' + str(system[bot]))
                            print('subsys = ' + str(bot) + ': ' + str(subsys[bot]))
                        if removed_moves != []:
                            for move in removed_moves:
                                deny_move(system, bot, move)
                        else:
                            raise UserWarning('No moves to remove but options changed!!!')
        print('Leaving THE SYSTEM SPLIT AREA AND SYSTEM IS ')
        for a in system:
            print(str(a) + ': ' + str(system[a]))

    outcome = determine_ideal_outcome(system)

    if debug:
        print('outcome = ')
        for a in outcome:
            print(str(a) + ' - ' + str(outcome[a]))

        print_target_system(system,
                            outcome['occupied'],
                            outcome['optional'],
                            outcome['num_optional'])





    d = system_details(system, outcome, field)

    if debug:
        print('')
        print('The initial system score was ' + str(d['score_absolute_initial']))
        print('The maximum obtainable for the system is ' + str(d['score_absolute_max']))
        print('The score gain were looking for is ' + str(d['score_gain_required']))
        print('bots_in_optional = ' + str(d['bots_in_optional']))
        print('bots_in_optional_moving_to_occupied = ' + str(d['bots_in_optional_moving_to_occupied']))
        print('bots_outside_system = ' + str(d['bots_outside_system']))
        print('bots_outside_system_moving_to_optional  = ' + str(d['bots_outside_system_moving_to_optional']))
        print('bots_in_occupied = ' + str(d['bots_in_occupied']))
        print('bots_in_occupied_moving_to_optional = ' + str(d['bots_in_occupied_moving_to_optional']))

        print('movable_bots_in_occupied_that_have_to_move = ' + str(d['movable_bots_in_occupied_that_have_to_move']))
        print('num_target_bots_in_optional = ' + str(d['num_target_bots_in_optional']))
        print('num_target_bots_in_occupied = ' + str(d['num_target_bots_in_occupied']))
        print('current_bots_in_optional = ' + str(d['current_bots_in_optional']))
        print('current_bots_in_optional_that_can_move_to_occupied = ' + str(d['current_bots_in_optional_that_can_move_to_occupied']))
        print('current_bots_in_occupied = ' + str(d['current_bots_in_occupied']))
        print('current_bots_in_occupied_that_can_move_to_optional = ' + str(d['current_bots_in_occupied_that_can_move_to_optional']))
        print('current_bots_outside = ' + str(d['current_bots_outside']))
        print('target_occupied_not_occupied = ' + str(d['target_occupied_not_occupied']))
        print('target_occupied_with_bot_now_or_definite_bot_next = ' + str(d['target_occupied_with_bot_now_or_definite_bot_next']))

        print('')




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
        sub_systems = split_sys(sub_system)
        for sub_system in sub_systems:
            tmp = pick_best(sub_system)
            for start, end in tmp:
                grant_move(system, start, end)


    # Make the simplifications that push the current available bots
    # into the ideal system
    bots_to_figure_out = []
    for bot in outcome['available_bots']:
        if set(system[bot]['options']) & ideal_system:
            move_removals = list(set(system[bot]['options']) - ideal_system)
            for move_removal in move_removals:
                deny_move(system, bot, move_removal)
        else:
            bots_to_figure_out.append(bot)
            # raise UserWarning('Bot ' + str(bot) + ' cant make it to the sub_system')
    if bots_to_figure_out != []:
        sub_system = {}
        for bot in bots_to_figure_out:
            sub_system[bot] = system[bot]
        print('Bots who cant make it to the subsystem are ' + str(bots_to_figure_out))
        best = pick_best(system)
        print('Picking best for these bots')
        print('pick_best = ' + str(best))
        for coord_from, coord_to in best:
            print('Granting ' + str(coord_from) + ' -> ' + str(coord_to))
            grant_move(system,
                       coord_from,
                       coord_to)

        d = system_details(system, outcome, field)
        # print('ERROR: The following bots could not make it to the ideal system')
        # print(bots_to_figure_out)

    if debug:
        print('')
        print('-------------------------------------')
        print('=> SYSTEM PUSHED TOWARDS IDEAL')
        print_system(system,
                     justbots=outcome['available_bots'],
                     occupied=outcome['occupied'],
                     optional=outcome['optional'],
                     scores=True)

        print('The system now has a total of ' + str(total_combinations(system)) + ' options')





        if d['min_possible_num_bots_in_optional'] > outcome['num_optional']:
            diff = outcome['num_optional'] - d['min_possible_num_bots_in_optional']
            if debug:
                print('ALERT! - There ' + str(diff) + ' bots too many that will have to stay in optional squares')
                print('Occupied squares that need someone assigned are')
                print(d['target_occupied_not_occupied'])


    if len(d['current_bots_outside']) > 0:
        for bot in d['current_bots_outside']:
            if bot in system[bot]['options']:
                raise UserWarning('Bots need to come in but ' + str(bot) + ' outside staying still!')

    if d['num_target_bots_in_optional'] == 0:
        if debug:
            print('No optional squares exist so bots should just be packing into occupied squares')
            if len(d['target_occupied_not_occupied']) > 0:
                print('Will try packing in')
                print('try_movement_sets being called with parameters')
                print('system = ' + str(system))
                print('targets = ' + str(d['target_occupied_not_occupied']))
                print('candidates = ' + str(d['movable_bots_in_occupied_that_have_to_move']))
                print('squares = ' + str(d['movable_bots_in_occupied']))
                if try_movement_sets(system,
                                     d['target_occupied_not_occupied'],
                                     d['movable_bots_in_occupied_that_have_to_move'],
                                     d['movable_bots_in_occupied']):
                    if debug:
                        print('The movements were made')
                        print_system(system)
                else:
                    if debug:
                        print('The movements could not be made')
            else:
                print('target_occupied_not_occupied had a length < 1')


    else:
        if debug:
            print('Optional squares exist')

        num_bots_to_move_into_optional = d['num_target_bots_in_optional'] - len(d['current_bots_in_optional'])
        num_bots_to_move_into_occupied = d['num_target_bots_in_occupied'] - len(d['current_bots_in_occupied'])

        if num_bots_to_move_into_optional > 0:
            if debug:
                print(str(num_bots_to_move_into_optional) + ' bots need to move into optional')

            if num_bots_to_move_into_occupied > 0:
                if debug:
                    print('And ' + str(num_bots_to_move_into_occupied) + ' bots need to move into occupied')
            elif num_bots_to_move_into_occupied < 0:
                if debug:
                    print('And ' + str(-num_bots_to_move_into_occupied) + ' bots need to move out of occupied')
                    print('LOGIC NEEDS ATTENTION ON MOVE')
                    print('bots_in_optional_moving_to_occupied = ' + str(d['bots_in_optional_moving_to_occupied']))
                    print('So lets move one of ' + str(d['current_bots_in_occupied_that_can_move_to_optional']))
                    print('Who is near the entering bot (above), into the nearest available optional square')


            else:
                if debug:
                    print('But no bots need to move into occupied')

        elif num_bots_to_move_into_optional < 0:
            if debug:
                print(str(-num_bots_to_move_into_optional) + ' bots need to move out of optional')
            if num_bots_to_move_into_occupied > 0:
                deficit = num_bots_to_move_into_occupied - len(d['current_bots_in_optional_that_can_move_to_occupied'])
                if debug:
                    print('Deficit = ' + str(deficit))
                    print('And ' + str(num_bots_to_move_into_occupied) + ' bots need to move into occupied')
                    print('len(current_bots_in_optional_that_can_move_to_occupied) = ' + str(len(d['current_bots_in_optional_that_can_move_to_occupied'])))
                if deficit > 0:
                    failed_occupied_coord_scores = sorted([fieldval(coord, field) for coord in d['target_occupied_not_occupied']])
                    optsqr = outcome['optional'][0]
                    optional_square_score = fieldval(optsqr, field)
                    score_reduction = 0
                    for index in range(deficit):
                        score_reduction -= failed_occupied_coord_scores[index] - optional_square_score
                    d['score_absolute_max'] += score_reduction
                    d['score_gain_required'] += score_reduction
                    if debug:
                        print('failed_occupied_coord_scores = ' + str(failed_occupied_coord_scores))
                        print('optional_square_score = ' + str(optional_square_score))
                        print('The max gain should now be reduced by ' + str(score_reduction))
                        print('score_gain_required now = ' + str(d['score_gain_required']))
                        print('score_absolute_max now = ' + str(d['score_absolute_max']))

                    if deficit < num_bots_to_move_into_occupied:
                        make_obvious_moves(system, d, True)
                        if debug:
                            print('With remaining bots lets try to path their way')
                            print('A - Like by doing one from ' + str(len(d['current_bots_in_optional_that_can_move_to_occupied'])) + ' of the following solutions')
                        print_system(system,
                                     justbots=outcome['available_bots'],
                                     occupied=outcome['occupied'],
                                     optional=outcome['optional'])
                        if try_movement_sets(system,
                                             d['target_occupied_not_occupied'],
                                             d['current_bots_in_optional_that_can_move_to_occupied'] + d['movable_bots_in_occupied_that_have_to_move'],
                                             d['movable_bots_in_occupied']):
                            if debug:
                                print('The movements were made')
                                print_system(system)
                        else:
                            if debug:
                                print('The movements could not be made')
                else:
                    # Find nont_occupied squares who only have one candidate
                    # bot and make that happen
                    make_obvious_moves(system, d, True)
                    num_to_implement = len(d['target_occupied_not_occupied'])
                    if debug:
                        print('It should be possible to make this happen')
                        print('B - Like by doing one from ' + str(num_to_implement) + ' of the following solutions')
                    print('try_movement_sets being called with parameters')
                    print('system = ' + str(system))
                    print('targets = ' + str(d['target_occupied_not_occupied']))
                    print('candidates = ' + str(d['current_bots_in_optional_that_can_move_to_occupied'] + d['movable_bots_in_occupied_that_have_to_move']))
                    print('squares = ' + str(d['movable_bots_in_occupied']))
                    # print_system(system,
                    #              justbots=outcome['available_bots'],
                    #              occupied=outcome['occupied'],
                    #              optional=outcome['optional'])

                    if try_movement_sets(system,
                                         d['target_occupied_not_occupied'],
                                         d['current_bots_in_optional_that_can_move_to_occupied'] + d['movable_bots_in_occupied_that_have_to_move'],
                                         d['movable_bots_in_occupied']):
                        if debug:
                            print('The movements were made')
                            print_system(system)
                    else:
                        if debug:
                            print('The movements could not be made')


            elif num_bots_to_move_into_occupied < 0:
                if debug:
                    print('And ' + str(-num_bots_to_move_into_occupied) + ' bots need to move out of occupied')
            else:
                if debug:
                    print('But no bots need to move into occupied')

        elif len(d['target_occupied_not_occupied']) > 0:
            print('system has unoccupied occupied squares and the occupied squares are correct')
            print('ASSUMING WE USE current_bots_outside TO FILL THE unoccupied Occupied')
            print('try_movement_sets being called with parameters')
            print('system = ' + str(system))
            print('targets = ' + str(d['target_occupied_not_occupied']))
            print('candidates = ' + str(d['current_bots_outside']))
            squares = list(set(d['current_bots_in_optional_that_can_move_to_occupied'] + d['current_bots_in_optional_that_can_move_to_other_optional'] + d['movable_bots_in_occupied']))
            print('squares = ' + str(squares))
            if try_movement_sets(system,
                                 d['target_occupied_not_occupied'],
                                 d['current_bots_outside'],
                                 squares):
                if debug:
                    print('The movements were made')
                    print_system(system)
            else:
                if debug:
                    print('The movements could not be made')

    if debug:
        print('')
        print('System result = ...')
        print('The system has a total of ' + str(total_combinations(system)) + ' options')
        for pos, bot in system.items():
            print(str(pos) + ' - ' + str(bot))
        print('')

        print('')

    outcome['score_absolute_max'] = d['score_absolute_max']
    outcome['score_gain_required'] = d['score_gain_required']

    complexity_exit = total_combinations(system)
    if complexity_exit < complexity_entry:
        if debug:
            print('The system became simpler while in simplyfy, run again')
        return simplify_sys(system, field, True)
    else:
        if debug:
            print('The system did not get simpler in simplify system, returning')
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




def is_valid(system):
    consolodate(system)

    if len([b for b in system if system[b]['options'] == []]) > 0:
        # print('System failed because a bot has no moves')
        return False

    taken_moves = [system[bot]['options'][0] for bot in system if len(system[bot]['options']) == 1]
    if len(taken_moves) != len(set(taken_moves)):
        # print('System failed because two bots take the same coordinate')
        return False

    return True


def is_settled(system):
    return len([b for b in system if len(system[b]['options']) == 1]) == len(system.keys())


def bot_to_move(system, outcome):
    boi = [bot for bot in system if len(system[bot]['options']) > 1]
    boi = filter(lambda x: x not in system[x]['options'], boi)
    if boi == []:
        return None
    else:
        return random.choice(boi)


def system_walk(system, outcome):
    tc('start')

    if is_settled(system) == False:
        btm = bot_to_move(system, outcome)
        if btm:
            subsys = [grant_move(copy.deepcopy(system), btm, move, True) for move in system[btm]['options']]
            pre_num = len(subsys)
            subsys = filter(is_valid, subsys)

            out = []
            for sys in subsys:
                # print(sys)
                if is_settled(sys):
                    # print('(SETTLED)')
                    if 'score_gain_required' in outcome and system_score_relative(sys) == outcome['score_gain_required']:
                        print('And is max gain - returning this system')
                        tc('system_walk')
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
                                tc('system_walk')
                                return [tmp_sys]
                    else:
                        out += test
            tc('system_walk')
            return out
        else:
            if is_valid(system):
                # print('No bots to move - attempt a freeze')
                if attempt_freeze(system) == False:
                    print('attempt_freeze faield')
                    best = pick_best(system,max_gain)
                    for move_from, move_to in best:
                        print('granting move ' + str(move))
                        grant_move(system, move_from, move_to)
                    return [system]
                else:
                    if 'score_gain_required' in outcome:
                        if system_score_relative(system) == outcome['score_gain_required']:
                            print('A system with max gain has been found!')
                            tc('system_walk')
                            return [system]
                        else:
                            print('The found system has a score of ' + str(system_score_relative(system)) + ' but we needed ' + str(outcome['score_gain_required']))
                            print('Returning - ' + str(system))
                            tc('system_walk')
                            return [system]
            else:
                print('system_walk: The system is invalid, returning None')
                tc('system_walk')
                return None
    else:
        print('system_walk - system is settled, returning')
        tc('system_walk')
        return [system]


def tc(label):
    global times, labels
    times.append(time.clock())
    if len(times) > 1:
        diff = (times[-1] - times[-2]) * 1000
        if label != 'start':
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


def system_score_relative(system):
    return sum([system[b]['scores'][0] for b in system])


def calculate_relative_score(system, moves):
    out = 0
    for start, end in moves:
        out += system[start]['scores'][system[start]['options'].index(end)]
    return out


def solve_sys(system, details):
    possibilities = system_walk(system, details)
    print('solve_sys: Entered')
    if 'score_gain_required' in details:
        print('solve_sys: Looking for a system score gain of ' + str(details['score_gain_required']))
    if possibilities != []:
        top_score = -9999
        result = None
        for possibility in possibilities:
            print('solve_sys: assessing a possibility')
            if is_valid(possibility):
                score = system_score_relative(possibility)
                print('solve_sys: is valid and has a score of ' + str(score))
                if system_score_relative(possibility) == details['score_gain_required']:
                    print('solve_sys: top possiblilty found, returning it')
                    return possibility
                elif this_score > top_score:
                    print('solve_sys: this is a new high-score')
                    result = possibility
                    top_score = score
            else:
                print('solve_sys: the possibility was invalid')
        if result is not None:
            print('solve_sys: returning the highest scoring possiblilty')
            return result
        else:
            print('solve_sys: no valid possibilities, returning None')
            return None
    else:
        print('solve_sys: possibilities = [], that was returned by system_walk, returning None')
        return None


def settle_sys(system, field):
    for subsystem in split_sys(system):
        if total_combinations(subsystem) < 1000:
            print('settle_sys: Subsystem combinations < 1000 so brute forcing')
            make_moves(subsystem, pick_best(subsystem))
        else:
            details = simplify_sys(subsystem, field)
            combinations = total_combinations(subsystem)
            print('settle_sys: this subsystem has ' + str(combinations) + ' combinations')
            if 1 < combinations <= feasable_size:
                make_moves(subsystem, pick_best(subsystem, details))
            elif combinations > feasable_size:

                tmp_system = solve_sys(subsystem, details)
                if tmp_system is None:
                    print('settle_sys: No solved system - ABORTING !!!!!!')
                    raise UserWarning('no solution found')
                else:
                    print('settle_sys: Solved')
                    subsystem = tmp_system

        # Implement subsystem outcome into system
        for bot in subsystem:
            system[bot] = subsystem[bot]

    return system


decided_options = None


def level4_field(radius, max_points=13, step=1, width=2):
    out = newfield()
    from_rad = 0
    for distance in range(0, 13):
        score = 0
        if distance > radius:
            from_rad = distance - radius
            score = max_points - (from_rad * step)
        else:
            if distance > (radius - width):
                score = max_points
            else:
                score = max_points - (radius - width + 1 - distance) * step
        # print('radius = ' + str(radius) + ' distance = ' + str(distance) + ', from_rad = ' + str(from_rad))
        for x, y in squares_dist((9, 9), distance):
            if within_bounds((x, y)):
                out[y][x] = score
    return out


def find_frontline_radius(system, width=2):
    for radius in [13 - x for x in range(0, 14)]:
        frontline_coords = []
        for layer in range(width):
            frontline_coords += squares_dist((9, 9), radius-layer)
        num_coords_in_frontline = len(frontline_coords)
        num_bots_in_frontline = len([bot for bot in system if bot in frontline_coords])
        if num_coords_in_frontline == num_bots_in_frontline:
            # print('returning ' + str(radius))
            return radius

    return 0


def create_system(bots, field):
    system = {}
    for bot in bots:
        options = available_options(bot)
        current_score = fieldval(bot, field)
        scores = [fieldval(coord_to, field) - current_score for coord_to in options]
        moves = [(x[0], x[1]) for x in zip(options, scores)]
        moves.sort(key=lambda x: x[1], reverse=True)
        system[bot] = {
            'options': [x[0] for x in moves],
            'scores':  [x[1] for x in moves]
        }
    return system


def cluster(friendlies, enemies):
    # lookup = {}
    groups = []
    for friends, foes in [(friendlies, enemies)]:
        output = []
        for robot in friends:
            # lookup[robot] = {
            #         'ratio': [],
            #         'members': []
            #     }
            ratio = []
            members = []
            within = []
            for distance in range(1, 24):
                squares = set(squares_dist(robot, distance))
                within += list(squares & friends)
                if squares & foes:
                    ratio.append(len(within) / float(distance))
                    members.append(copy.copy(within))
                    break
            else:
                ratio.append(len(within) / float(distance))
                members.append(copy.copy(within))
            max_ratio = max(ratio)
            grp_dist = ratio.index(max_ratio)
            output.append((robot, max_ratio, members[grp_dist]))
        output = filter(lambda x: x[1] > 0.0, output)
        output.sort(key=lambda x: x[1])
        print(output)
        out = []
        taken = []
        for member in output[:]:
            if member[0] not in taken and set(member[2]) & set(taken) == set():
                result = [member[0]]
                result += member[2]
                for tmp in output:
                    if tmp[0] in result:
                        result += tmp[2]
                    elif set(tmp[2]) & set(result):
                        result += [tmp[0]]

                group = list(set(result))
                out.append(group)
                taken += group

        return out



class Robot:

    def act(self, game):
        global game_turn, attack_damage, spawn, obstacle, centre
        global move_count, decided_options, frontlinelogic
        global vulnerability, health_diffs, attack_ratio

        robots = game.robots

        friendlies = set([bot for bot in robots if robots[bot].player_id == self.player_id])
        enemies = set(robots)-friendlies

        if game.turn != game_turn:

            game_turn = game.turn
            turn = game_turn - 1


            groups = cluster(friendlies, enemies)
            print('There are ' + str(len(groups)) + ' groups')
            for group in groups:
                print(group)


            ## Level 4 logic
            available_members = [x for x in friendlies]
            frontline_radius = find_frontline_radius(friendlies, 1)
            print('frontline_radius = ' + str(frontline_radius))
            frontlinelogic = level4_field(frontline_radius, max_points=40, width=1, step=1)

            health_diffs = {}
            attack_ratio = {}
            vulnerability = {}


            for team, opponents in [(friendlies, enemies), (enemies, friendlies)]:
                for robot in team:
                    coords_around = surrounding(robot)
                    opponents_around = [bot for bot in list(coords_around) if bot in list(opponents)]
                    relevant_cells = []
                    for opponent in opponents_around:
                        relevant_cells += list(surrounding(opponent) & coords_around)
                    support = [bot for bot in team if bot in relevant_cells]
                    opponent_health = sum([robots[bot].hp for bot in opponents_around])
                    health_diff = robots[robot].hp - opponent_health
                    strength = 1 - len(opponents_around) + len(support)
                    health_diffs[robot] = health_diff
                    attack_ratio[robot] = strength

                    # Calculate vunerability
                    for distance in range(1, 24):
                        if set(squares_dist(robot, distance)) & set(team):
                            vulnerability[robot] = distance
                            break

            for bot in robots:
                print('({0:2d},{1:2d})'.format(*bot)),
                if bot in enemies:
                    print('(enemy)    '),
                else:
                    print('(friendly) '),
                print('vulnerability = {0:2d}'.format(vulnerability[bot])),
                print('attack_ratio = {0:2d}'.format(attack_ratio[bot])),
                print('health_diffs = {0:2d}'.format(health_diffs[bot]))




            if turn % 10 == 9:
                for x, y in spawn:
                   frontlinelogic[y][x] = 10
                for x, y in deepspawn:
                   frontlinelogic[y][x] = 0

            for enemy in enemies:
                for distance, danger in [(1, 2), (2, 1)]:
                    for x, y in squares_dist(enemy, distance):
                        if within_bounds((x, y)):
                            frontlinelogic[y][x] -= danger

            print_field(frontlinelogic)
            system = create_system(friendlies, frontlinelogic)

            decided_options = settle_sys(system, frontlinelogic)
            print('settle_sys returned with ' + str(decided_options))

        try:
            move = decided_options[self.location]['options'][0]

            enemies_adjacent = set(adjacent(self.location)) & enemies
            if enemies_adjacent and attack_ratio[self.location] > -1 and robots[self.location].hp > 9:
                weakest = min([robots[bot].hp for bot in enemies_adjacent])
                enemies_adjacent = list(enemies_adjacent)
                if len(enemies_adjacent) == 4:
                    return ['suicide', (9, 9)]
                elif len(enemies_adjacent) > 1 and robots[self.location].hp < len(enemies_adjacent) * 8:
                    return ['suicide', (9, 9)]
                weakest_adjacent = [bot for bot in enemies_adjacent if robots[bot].hp == weakest]
                to_attack = random.choice(weakest_adjacent)
                return ['attack', to_attack]
            elif enemies_adjacent and move == self.location and robots[self.location].hp < 10:
                return ['suicide', (9, 9)]
            else:
                if move == self.location:
                    return ['guard', move]
                else:
                    return ['move', move]

        except KeyError:
            return ['suicide', (9, 9)]
