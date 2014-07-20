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
    coord_from = bot_action[0]
    moves = bot_action[1]
    return [(fieldval(coord_to, field) - fieldval(coord_from, field)) for coord_to in moves]


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


def system_split(input_system):

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
    if path_nest is None:
        return []
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
    for a in system:
        print(str(a) + ' - ' + str(system[a]))
    for moves in move_paths:
        for start in range(len(moves)-1):
            end = start + 1
            grant_move(system, moves[start], moves[end])


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
        copies = [[a,b] for a in system for b in system if a != b and (set(system[a]['options']) - set([a])) == (set(system[b]['options']) - set([b])) and (set(system[a]['options']) - set([a]) != set())]
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

    tmp_system = {}
    for candidate in candidates:
        tmp_system[candidate] = system[candidate]

    show_system(tmp_system)

    for a in tmp_system:
        print(str(a) + ' - ' + str(tmp_system[a]))

    if total_combinations(tmp_system) < (feasable_size / 1000):
        print('The tmp_system has under ' + str((feasable_size / 1000)) + ' moves, solving NOW')
        best = pick_best(system)
        for coord_from, coord_to in best:
            grant_move(system, coord_from, coord_to)
            return True

    print('The temp system has TOO MAYNY combinations to solve straight')
    print(total_combinations(tmp_system))

    subsystems = system_split(tmp_system)
    print('Can be split into ' + str(len(subsystems)) + ' subsystems')

    # TODO: This is being split so that we can separate target-candidate
    # systems and solve separately.

    # NEEDS TO HAPPEN:
    # Pluck targets and candidates out of each split system and solve
    # for each subsystem

    # print('SPLIT ATTEMPT...')
    # print('There are ' + str(len(subsystems)) + ' subsystems')
    # for subsystem in subsystems:

    # if len(subsystems) == 1:
    #     print('here it is')
    #     for a in subsystems:
    #         print(str(a) + ' - ' + str(subsystems[a]))

    tc('start')
    print('try_movement_sets dimensions')
    print(str(len(targets)) + ' targets')
    print(str(len(candidates)) + ' candidates')
    match_sets = mix_lists(candidates, targets)

    # precheck for bad links
    bad_links = []
    for end in targets:
        for start in candidates:
            if find_paths(start, end, squares + [end]) == []:
                bad_links.append((start, end))

    available_coords = set(squares)
    for match_set in match_sets:
        print('')
        print('Looking at ' + str(match_set))
        set_paths = []
        skip = False
        taken_coords = set()
        for start, end in match_set:
            if (start, end) not in bad_links:
                coords = copy.deepcopy(available_coords)
                coords.add(end)
                coords.difference(taken_coords)
                print('Find paths between ' + str(start) + ' and ' + str(end))
                paths = find_paths(start, end, list(coords))
                print(str(len(paths)) + ' paths = ' + str(paths))
                if paths == []:
                    skip = True
                    break
                else:
                    set_paths.append(paths)

        print('Finished generating path sets')
        print(set_paths)
        print('')

        if skip == False:
            # print('Checking match_set, ' + str(match_set))
            # print('Which generated the set_paths ' + str(set_paths))

            for path_group in itertools.product(*set_paths):
                # print('Checking ' + str(path_group))
                if check_moves(system, path_group):
                    # print('Looking good, implementing set')
                    make_moves(system, path_group)
                    # tc('try_movement_sets')
                    return True
            # print('Tried all moves but none worked')
        # else:
            # print('Skipped as no paths')

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


def system_details(system, outcome, score_absolute_initial, field):
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






def simplify_system(system, debug=False):
    changed = False

    global feasable_size
    global frontlinelogic

    field = frontlinelogic
    score_absolute_initial = 0
    for x, y in system:
        score_absolute_initial += fieldval((x, y), field)

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
        changed = True

    if debug:
        print('')
        print('-------------------------------------')
        print('=> AFTER DANGLING GRANTS')
        print_system(system)


    systems = system_split(system)

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
                    make_moves(system, best)
                    changed = True
            else:
                if debug:
                    print('A subsystem...')
                    print('has ' + str(len(subsys)) + ' members')
                    print(str(total_combinations(subsys)) + ' combinations')
                simplify_system(subsys)
                if debug:
                    print('simplified...')
                    print(str(total_combinations(subsys)) + ' combinations')
                print('')
                for bot in subsys:
                    if subsys[bot]['options'] != system[bot]['options']:
                        changed = True
                        removed_moves = list(set(system[bot]['options']) - set(subsys[bot]['options']))
                        if debug:
                            print('Subsystem differs with bot ' + str(bot) + ' by')
                            print('system = ' + str(bot) + ': ' + str(system[bot]))
                            print('subsys = ' + str(bot) + ': ' + str(subsys[bot]))
                        if removed_moves != []:
                            for move in removed_moves:
                                deny_move(system, bot, move)
                                changed = True
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





    d = system_details(system, outcome, score_absolute_initial, field)

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
        sub_systems = system_split(sub_system)
        for sub_system in sub_systems:
            tmp = pick_best(sub_system)
            for start, end in tmp:
                grant_move(system, start, end)
                changed = True


    # Make the simplifications that push the current available bots
    # into the ideal system
    bots_to_figure_out = []
    for bot in outcome['available_bots']:
        if set(system[bot]['options']) & ideal_system:
            move_removals = list(set(system[bot]['options']) - ideal_system)
            for move_removal in move_removals:
                deny_move(system, bot, move_removal)
                changed = True
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

        d = system_details(system, outcome, score_absolute_initial, field)
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
                        print('score_gain_required now = ' + str(score_gain_required))
                        print('score_absolute_max now = ' + str(score_absolute_max))

                    if deficit < len(d['current_bots_in_optional_that_can_move_to_occupied']):
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
                            changed = True
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
                        changed = True
                    else:
                        if debug:
                            print('The movements could not be made')


            elif num_bots_to_move_into_occupied < 0:
                if debug:
                    print('And ' + str(-num_bots_to_move_into_occupied) + ' bots need to move out of occupied')
            else:
                if debug:
                    print('But no bots need to move into occupied')

        # # This may need to be in the else statement but it might be good
        # # to have it as a catch all.
        # if len(d['target_occupied_not_occupied']) > 0:
        #     make_obvious_moves(system, d)
        #     source_bots = d['movable_bots_in_occupied_that_have_to_move'] + d['current_bots_in_optional_that_can_move_to_occupied']
        #     if debug:
        #         print('unoccupied squares exist ... ' + str(d['target_occupied_not_occupied']))
        #         print('We need to find paths between those and ' + str(len(d['target_occupied_not_occupied'])) + ' bots')
        #         print('There are ' + str(len(source_bots)) + ' bots that can be used... ' + str(source_bots))
        #     if try_movement_sets(system,
        #                          d['target_occupied_not_occupied'],
        #                          source_bots,
        #                          d['movable_bots_in_occupied']):
        #         if debug:
        #             print('It worked')
        #         changed = True
        #     else:
        #         if debug:
        #             print('It failed')

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

    if changed:
        if debug:
            print('The system changed while in simplyfy, running system through simplyfy_system again')
        return simplify_system(system, True)
    else:
        if debug:
            print('The system did not change in simplify system, returning')
        return outcome





# def simplify_system(system, debug=False):
#     changed = False

#     global feasable_size
#     global frontlinelogic

#     field = frontlinelogic
#     score_absolute_initial = 0
#     for x, y in system:
#         score_absolute_initial += fieldval((x, y), field)

#     if debug:
#         print('')
#         print('')
#         print('=> INITIAL')
#         print_system(system)

#     # Any unoccupied cell with 2 adjacent bots should be evaluated for
#     # this simplification
#     while grant_dangling_move(system):
#         if debug:
#             print('simplification made, repeating')
#         changed = True

#     if debug:
#         print('')
#         print('-------------------------------------')
#         print('=> AFTER DANGLING GRANTS')
#         print_system(system)


#     systems = system_split(system)
#     if len(systems) > 1:
#         if debug:
#             print('System can be split')
#         for subsys in systems:
#             print(subsys)
#             if total_combinations(subsys) < int(feasable_size / 10):
#                 if debug:
#                     print('This subsystem has less than ' + str(int(feasable_size / 10)) + ' options, solving')
#                 pick_best(subsys)
#                 print('')
#                 for bot in subsys:
#                     if subsys[bot]['options'] != system[bot]['options']:
#                         if debug:
#                             print('Subsystem differs with bot ' + str(bot) + ' by')
#                             print('system = ' + str(bot) + ': ' + str(system[bot]))
#                             print('subsys = ' + str(bot) + ': ' + str(subsys[bot]))
#                         system[bot] = subsys[bot]
#                         if debug:
#                             print('merging, to confirm it worked ..')
#                             print('system = ' + str(bot) + ': ' + str(system[bot]))
#                             print('subsys = ' + str(bot) + ': ' + str(subsys[bot]))
#             if debug:
#                 print('A subsystem...')
#                 print('has ' + str(len(subsys)) + ' members')
#                 print(str(total_combinations(subsys)) + ' combinations')
#             simplify_system(subsys)
#             if debug:
#                 print('simplified...')
#                 print(str(total_combinations(subsys)) + ' combinations')
#             print('')
#             for bot in subsys:
#                 if subsys[bot]['options'] != system[bot]['options']:
#                     if debug:
#                         print('Subsystem differs with bot ' + str(bot) + ' by')
#                         print('system = ' + str(bot) + ': ' + str(system[bot]))
#                         print('subsys = ' + str(bot) + ': ' + str(subsys[bot]))
#                     system[bot] = subsys[bot]
#                     if debug:
#                         print('merging, to confirm it worked ..')
#                         print('system = ' + str(bot) + ': ' + str(system[bot]))
#                         print('subsys = ' + str(bot) + ': ' + str(subsys[bot]))

#     outcome = determine_ideal_outcome(system)
#     if debug:
#         print('outcome = ')
#         for a in outcome:
#             print(str(a) + ' - ' + str(outcome[a]))

#         print_target_system(system,
#                             outcome['occupied'],
#                             outcome['optional'],
#                             outcome['num_optional'])

#     ideal_system = set(outcome['occupied'] + outcome['optional'])
#     detached_bots = list(set(movable_bots(system)) - set(outcome['available_bots']))

#     # Take the bots that couldnt make it to the system and calculate their moves
#     # separately
#     if len(detached_bots) > 0:
#         sub_system = {}
#         for bot in detached_bots:
#             sub_system[bot] = {
#                 'options': system[bot]['options'],
#                 'scores': system[bot]['scores']
#             }
#         sub_systems = system_split(sub_system)
#         for sub_system in sub_systems:
#             tmp = pick_best(sub_system)
#             for start, end in tmp:
#                 grant_move(system, start, end)
#                 changed = True


#     # Make the simplifications that push the current available bots
#     # into the ideal system
#     for bot in outcome['available_bots']:
#         if set(system[bot]['options']) & ideal_system:
#             move_removals = list(set(system[bot]['options']) - ideal_system)
#             for move_removal in move_removals:
#                 deny_move(system, (bot, move_removal))
#                 changed = True
#         else:
#             raise UserWarning('Bot ' + str(bot) + ' cant make it to the sub_system')

#     if debug:
#         print('')
#         print('-------------------------------------')
#         print('=> SYSTEM PUSHED TOWARDS IDEAL')
#         print_system(system,
#                      justbots=outcome['available_bots'],
#                      occupied=outcome['occupied'],
#                      optional=outcome['optional'],
#                      scores=True)

#         print('The system now has a total of ' + str(total_combinations(system)) + ' options')


#     # Bots that didn't partake in the grand simplification
#     unavailable_bots = list(set(system.keys()) - set(outcome['available_bots']))
#     free_unavailable = [bot for bot in unavailable_bots if len(system[bot]['options']) > 1]

#     if len(free_unavailable) != 0:
#         raise UserWarning('Some unavailable_bots arent frozen')

#     # Calculate the score contribution from the non-sub_system bots
#     remaining_score = 0
#     for bot in unavailable_bots:
#         x,y = system[bot]['options'][0]
#         # remaining_score += int(field[y][x])
#         remaining_score += fieldval((x, y), field)
#     score_absolute_max = remaining_score + outcome['max_score']
#     score_gain_required = score_absolute_max - score_absolute_initial
#     system_score_gain_required = score_gain_required - sum(system[bot]['scores'][0] for bot in unavailable_bots)
#     bots_in_optional = [bot for bot in outcome['available_bots'] if bot in outcome['optional']]
#     bots_in_optional_moving_to_occupied = [bot for bot in bots_in_optional if len(system[bot]['options']) == 1 and system[bot]['options'][0] in outcome['occupied']]
#     bots_outside_system = [bot for bot in outcome['available_bots'] if bot not in outcome['optional'] and bot not in outcome['occupied']]
#     bots_outside_system_moving_to_optional = [bot for bot in bots_outside_system if len(set(system[bot]['options']) & set(outcome['optional'])) == len(system[bot]['options'])]
#     bots_outside_system_moving_to_occupied = [bot for bot in bots_outside_system if len(set(system[bot]['options']) & set(outcome['occupied'])) == len(system[bot]['options'])]
#     bots_in_occupied = [bot for bot in outcome['available_bots'] if bot in outcome['occupied']]
#     bots_in_occupied_moving_to_optional = [bot for bot in bots_in_occupied if len(system[bot]['options']) == 1 and system[bot]['options'][0] in outcome['optional']]
#     num_target_bots_in_optional = outcome['num_optional']
#     num_target_bots_in_occupied = len(outcome['occupied'])
#     current_bots_in_optional = bots_in_optional + bots_outside_system_moving_to_optional + bots_in_occupied_moving_to_optional
#     current_bots_in_optional = filter(lambda x: x not in bots_in_optional_moving_to_occupied, current_bots_in_optional)
#     current_bots_in_optional_that_can_move_to_occupied = [bot for bot in current_bots_in_optional if set(system[bot]['options']) & set(outcome['occupied'])]
#     current_bots_in_occupied = bots_in_occupied + bots_in_optional_moving_to_occupied + bots_outside_system_moving_to_occupied
#     movable_bots_in_occupied = [bot for bot in current_bots_in_occupied if len(system[bot]['options']) > 1]
#     current_bots_in_occupied = filter(lambda x: x not in bots_in_occupied_moving_to_optional, current_bots_in_occupied)
#     current_bots_in_occupied_that_can_move_to_optional = [bot for bot in current_bots_in_occupied if set(system[bot]['options']) & set(outcome['optional'])]
#     squares_that_will_be_occupied = [system[bot]['options'][0] for bot in system.keys() if len(system[bot]['options']) == 1]
#     target_occupied_with_bot_now_or_definite_bot_next = list(set(squares_that_will_be_occupied) & set(outcome['occupied']))
#     target_occupied_with_bot_now_or_definite_bot_next += current_bots_in_occupied
#     target_occupied_not_occupied = list(set(outcome['occupied']) - set(target_occupied_with_bot_now_or_definite_bot_next))
#     current_bots_outside = filter(lambda x: x not in bots_outside_system_moving_to_optional and x not in bots_outside_system_moving_to_occupied, bots_outside_system)
#     min_possible_num_bots_in_optional = len(set(current_bots_in_optional) - set(current_bots_in_optional_that_can_move_to_occupied))
#     movable_bots_in_occupied_that_have_to_move = [bot for bot in movable_bots_in_occupied if bot not in system[bot]['options']]

#     if debug:
#         print('')
#         print('The initial system score was ' + str(score_absolute_initial))
#         print('The maximum obtainable for the system is ' + str(score_absolute_max))
#         print('The score gain were looking for is ' + str(score_gain_required))
#         print('The system_score_gain_required = ' + str(system_score_gain_required))
#         print('bots_in_optional = ' + str(bots_in_optional))
#         print('bots_in_optional_moving_to_occupied = ' + str(bots_in_optional_moving_to_occupied))
#         print('bots_outside_system = ' + str(bots_outside_system))
#         print('bots_outside_system_moving_to_optional  = ' + str(bots_outside_system_moving_to_optional))
#         print('bots_in_occupied = ' + str(bots_in_occupied))
#         print('bots_in_occupied_moving_to_optional = ' + str(bots_in_occupied_moving_to_optional))

#         print('movable_bots_in_occupied_that_have_to_move = ' + str(movable_bots_in_occupied_that_have_to_move))
#         print('num_target_bots_in_optional = ' + str(num_target_bots_in_optional))
#         print('num_target_bots_in_occupied = ' + str(num_target_bots_in_occupied))
#         print('current_bots_in_optional = ' + str(current_bots_in_optional))
#         print('current_bots_in_optional_that_can_move_to_occupied = ' + str(current_bots_in_optional_that_can_move_to_occupied))
#         print('current_bots_in_occupied = ' + str(current_bots_in_occupied))
#         print('current_bots_in_occupied_that_can_move_to_optional = ' + str(current_bots_in_occupied_that_can_move_to_optional))
#         print('current_bots_outside = ' + str(current_bots_outside))
#         print('target_occupied_not_occupied = ' + str(target_occupied_not_occupied))
#         print('target_occupied_with_bot_now_or_definite_bot_next = ' + str(target_occupied_with_bot_now_or_definite_bot_next))

#         print('')


#         if min_possible_num_bots_in_optional > outcome['num_optional']:
#             diff = outcome['num_optional'] - min_possible_num_bots_in_optional
#             if debug:
#                 print('ALERT! - There ' + str(diff) + ' bots too many that will have to stay in optional squares')
#                 print('Occupied squares that need someone assigned are')
#                 print(target_occupied_not_occupied)


#     if len(current_bots_outside) > 0:
#         for bot in current_bots_outside:
#             if bot in system[bot]['options']:
#                 raise UserWarning('Bots need to come in but ' + str(bot) + ' outside staying still!')

#     if num_target_bots_in_optional == 0:
#         if debug:
#             print('No optional squares exist so bots should just be packing into occupied squares')
#     else:
#         if debug:
#             print('Optional squares exist')

#         num_bots_to_move_into_optional = num_target_bots_in_optional - len(current_bots_in_optional)
#         num_bots_to_move_into_occupied = num_target_bots_in_occupied - len(current_bots_in_occupied)

#         if num_bots_to_move_into_optional > 0:
#             if debug:
#                 print(str(num_bots_to_move_into_optional) + ' bots need to move into optional')

#             if num_bots_to_move_into_occupied > 0:
#                 if debug:
#                     print('And ' + str(num_bots_to_move_into_occupied) + ' bots need to move into occupied')
#             elif num_bots_to_move_into_occupied < 0:
#                 if debug:
#                     print('And ' + str(-num_bots_to_move_into_occupied) + ' bots need to move out of occupied')
#                     print('LOGIC NEEDS ATTENTION ON MOVE')
#                     print('bots_in_optional_moving_to_occupied = ' + str(bots_in_optional_moving_to_occupied))
#                     print('So lets move one of ' + str(current_bots_in_occupied_that_can_move_to_optional))
#                     print('Who is near the entering bot (above), into the nearest available optional square')


#             else:
#                 if debug:
#                     print('But no bots need to move into occupied')

#         elif num_bots_to_move_into_optional < 0:
#             if debug:
#                 print(str(-num_bots_to_move_into_optional) + ' bots need to move out of optional')
#             if num_bots_to_move_into_occupied > 0:
#                 deficit = num_bots_to_move_into_occupied - len(current_bots_in_optional_that_can_move_to_occupied)
#                 if debug:
#                     print('Deficit = ' + str(deficit))
#                     print('And ' + str(num_bots_to_move_into_occupied) + ' bots need to move into occupied')
#                     print('len(current_bots_in_optional_that_can_move_to_occupied) = ' + str(len(current_bots_in_optional_that_can_move_to_occupied)))
#                 if deficit > 0:
#                     failed_occupied_coord_scores = sorted([fieldval(coord, field) for coord in target_occupied_not_occupied])
#                     optsqr = outcome['optional'][0]
#                     optional_square_score = fieldval(optsqr, field)
#                     score_reduction = 0
#                     for index in range(deficit):
#                         score_reduction -= failed_occupied_coord_scores[index] - optional_square_score
#                     score_absolute_max += score_reduction
#                     score_gain_required += score_reduction
#                     if debug:
#                         print('failed_occupied_coord_scores = ' + str(failed_occupied_coord_scores))
#                         print('optional_square_score = ' + str(optional_square_score))
#                         print('The max gain should now be reduced by ' + str(score_reduction))
#                         print('score_gain_required now = ' + str(score_gain_required))
#                         print('score_absolute_max now = ' + str(score_absolute_max))

#                     if deficit < len(current_bots_in_optional_that_can_move_to_occupied):
#                         make_obvious_moves(system, d)
#                         if debug:
#                             print('With remaining bots lets try to path their way')
#                             print('A - Like by doing one from ' + str(len(current_bots_in_optional_that_can_move_to_occupied)) + ' of the following solutions')
#                         print_system(system,
#                                      justbots=outcome['available_bots'],
#                                      occupied=outcome['occupied'],
#                                      optional=outcome['optional'])
#                         if try_movement_sets(system,
#                                              target_occupied_not_occupied,
#                                              current_bots_in_optional_that_can_move_to_occupied + movable_bots_in_occupied_that_have_to_move,
#                                              movable_bots_in_occupied):
#                             if debug:
#                                 print('The movements were made')
#                             changed = True
#                         else:
#                             if debug:
#                                 print('The movements could not be made')
#                 else:
#                     # Find nont_occupied squares who only have one candidate
#                     # bot and make that happen
#                     make_obvious_moves(system, d)
#                     num_to_implement = len(target_occupied_not_occupied)
#                     if debug:
#                         print('It should be possible to make this happen')
#                         print('B - Like by doing one from ' + str(num_to_implement) + ' of the following solutions')
#                     print_system(system,
#                                  justbots=outcome['available_bots'],
#                                  occupied=outcome['occupied'],
#                                  optional=outcome['optional'])

#                     if try_movement_sets(system,
#                                          target_occupied_not_occupied,
#                                          current_bots_in_optional_that_can_move_to_occupied + movable_bots_in_occupied_that_have_to_move,
#                                          movable_bots_in_occupied):
#                         if debug:
#                             print('The movements were made')
#                         changed = True
#                     else:
#                         if debug:
#                             print('The movements could not be made')


#             elif num_bots_to_move_into_occupied < 0:
#                 if debug:
#                     print('And ' + str(-num_bots_to_move_into_occupied) + ' bots need to move out of occupied')
#             else:
#                 if debug:
#                     print('But no bots need to move into occupied')

#         # # This may need to be in the else statement but it might be good
#         # # to have it as a catch all.
#         # if len(target_occupied_not_occupied) > 0:
#         #     source_bots = movable_bots_in_occupied_that_have_to_move + current_bots_in_optional_that_can_move_to_occupied
#         #     if debug:
#         #         print('unoccupied squares exist ... ' + str(target_occupied_not_occupied))
#         #         print('We need to find paths between those and ' + str(len(target_occupied_not_occupied)) + ' bots')
#         #         print('There are ' + str(len(source_bots)) + ' bots that can be used... ' + str(source_bots))
#         #     if try_movement_sets(system,
#         #                          target_occupied_not_occupied,
#         #                          source_bots,
#         #                          movable_bots_in_occupied):
#         #         if debug:
#         #             print('It worked')
#         #         changed = True
#         #     else:
#         #         if debug:
#         #             print('It failed')

#     if debug:
#         print('')
#         print('System result = ...')
#         print('The system has a total of ' + str(total_combinations(system)) + ' options')
#         for pos, bot in system.items():
#             print(str(pos) + ' - ' + str(bot))
#         print('')

#         print('')

#     outcome['score_absolute_max'] = score_absolute_max
#     outcome['score_gain_required'] = score_gain_required

#     if changed and total_combinations(system) > feasable_size:
#         if debug:
#             print('The system changed while in simplyfy, running system through simplyfy_system again')
#         return simplify_system(system, True)
#     else:
#         if debug:
#             print('The system did not change in simplify system, returning')
#         return outcome


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



def freeze(system, score_absolute_initial, score_absolute_max):
    # If we fixed everyones position that has options, how close do we get?
    print('Testing a bot freeze situation')
    test_sys = copy.deepcopy(system)
    for bot in test_sys:
        if len(test_sys[bot]['options']) > 1 and bot in test_sys[bot]['options']:
            grant_move(test_sys, bot, bot)
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
                    grant_move(system, bot, bot)




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
                        # print('And is max gain - returning this system')
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
                                # print('Top solution detected - avalanching down')
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
                else:
                    if 'score_gain_required' in outcome:
                        if system_score_relative(system) == outcome['score_gain_required']:
                            print('A system with max gain has been found!')
                        else:
                            print('The found system has a score of ' + str(system_score_relative(system)) + ' but we needed ' + str(outcome['score_gain_required']))
                            print('Returning - ' + str(system))
                            tc('system_walk')
                            return [system]
            else:
                print('The system is invalid')
                tc('system_walk')
                return None
            tc('system_walk')
            return [system]
    else:
        print('system_walk - system is settled, returning')
        tc('system_walk')
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



def choose_moves(system):
    global feasable_size
    tc('start')
    sys_backup = copy.deepcopy(system)
    outcome = simplify_system(system, True)
    tc('simplify_system')
    if total_combinations(system) == 1:
        print('The system only has one possibility so returning early')
        return system
    else:
        print('Will try freezing the system')
        attempt_freeze(system)
        out = solve_system(system, outcome)
        if out != None:
            print('solve_system returned - choose moves will return')
            try:
                for a in out:
                    print(str(a[0]) +  ' -> ' + str(a[1]))
            except TypeError:
                print('ERROR: TypeError')
                print(out)
            return out
        else:
            print('solve_system returned NONE')



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

def num_cells_at_radius_from_centre(radius):
    num = radius * 4
    if num > 0:
        return num
    else:
        return 1

# def num_cells_inside_radius_from_centre(radius):
#     return sum([1] + [x*4 for x in range(radius+1)])

def max_front_radius(members):
    max_radius = 0
    for radius in range(13):
        cells_at_radius = squares_dist((9, 9), radius)
        cells_inner_layer = []
        if radius > 0:
            cells_inner_layer = squares_dist((9, 9), radius - 1)
        cells_outer_layer = squares_dist((9, 9), radius + 1)
        num_cells_at_radius = num_cells_at_radius_from_centre(radius)
        participant_cells = cells_at_radius + cells_inner_layer + cells_outer_layer
        participant_bots = [bot for bot in participant_cells if bot in members]
        if len(participant_bots) >= num_cells_at_radius:
            max_radius = radius
    return max_radius

class Robot:

    # def level4_field(self, members):
    #     out = newfield()
    #     for distance in range(0, 13):
    #         for x, y in squares_dist(rg.CENTER_POINT, distance):
    #             if within_bounds((x, y)):
    #                 out[y][x] = 18-distance
    #     for coord in [(9,9), (8, 8), (8, 10), (10, 8), (10, 10)]:
    #         for x, y in adjacent(coord):
    #             out[y][x] -= 1
    #     return out

    def level4_field(self, members):
        print(members)
        target_radius = max_front_radius(members)
        out = newfield()
        # target_radius = 3
        max_points = 50
        for distance in range(0, 13):
            for x, y in squares_dist(rg.CENTER_POINT, distance):
                if within_bounds((x, y)):
                    if distance < target_radius:
                        out[y][x] = max_points - (target_radius - distance)
                    elif distance > target_radius:
                        out[y][x] = max_points - (distance - target_radius)
                    else:
                        out[y][x] = max_points
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
            bad_coords = []
            for enemy in enemies:
                enemy_adj = adjacent(enemy)
                min_score = min([frontlinelogic[y][x] for x,y in enemy_adj]) - 1
                if min_score < 0:
                    min_score = 0
                for x, y in enemy_adj:
                    frontlinelogic[y][x] = min_score
                frontlinelogic[enemy[1]][enemy[0]] = min_score
            print_field(frontlinelogic)

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
