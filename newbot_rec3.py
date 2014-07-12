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
        if int(score) >= max_score:
            print('PICK BEST FOUND A SOLUTION EARLY - quitting')
            return [(cell_to_coord(x), cell_to_coord(y)) for x, y in possibility]
        elif score > top_score:
            result, top_score = possibility, score

    if result is None:
        return None
    else:
        return [(cell_to_coord(x), cell_to_coord(y)) for x, y in result]


def coord_to_cell(coord):
    return coord[0] + coord[1] * 19


def cell_to_coord(cell):
    x = cell % 19
    y = int(cell / 19)
    return (x, y)


def test_system(system):
    for pos, bot in system.items():
        num_opts = len(bot['options'])
        if num_opts == 0:
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

        best_candidates = [pos for pos in system if pos in candidates and len(system[pos]['options']) == 1]

        # If not best candidate at this point, find the most deserving
        if best_candidates == []:

            best_candidates = []
            for candidate in candidates.iteritems():
                best_candidates.append(candidate[0])

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

        bots = [pos for pos, bot in system.items() if len(bot['options']) == max_opts]
        winner = random.choice(bots)
        out_options = []
        for index, score in enumerate(system[winner]['scores']):
            if score >= 0:
                out_options.append(system[winner]['options'][index])
        return (out_options, winner)


def make_reduction(system, (winner, target)):

    for pos, bot in system.items():
        if pos == winner:
            # Make this move the only option for the winner
            bot['scores'] = [bot['scores'][bot['options'].index(target)]]
            bot['options'] = [target]
        else:
            if pos == target:
                # Remove bot swap as an option for target square
                try:
                    swap_index = bot['options'].index(winner)
                except:
                    swap_index = None

                if swap_index:
                    del bot['options'][swap_index]
                    del bot['scores'][swap_index]
            if target in bot['options']:
                # Remove this option from other bots move options
                bot['scores'].remove(bot['scores'][bot['options'].index(target)])
                bot['options'].remove(target)

    return system


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
                make_reduction(system, (bot, gain_move))
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
        'occupied': targets_occupied,
        'optional': targets_optional,
        'num_optional': num_optional,
        'available_bots': available_bots,
        'max_score': max_score
    }

    return result


def determine_ideal_outcome(system, available_bots):

    available_bots = movable_bots(system)
    outcome = find_ideal_system(system, available_bots)

    ideal_system = set(outcome['occupied'] + outcome['optional'])

    valid_available_bots = []
    for bot in available_bots:
        if set(system[bot]['options']) & ideal_system:
            valid_available_bots.append(bot)

    # Repeat, but this time only including the bots that can make it
    # into the ideal system
    return find_ideal_system(system, valid_available_bots)


def simplify_system(system, max_options):

    global frontlinelogic
    field = frontlinelogic
    absolute_score = 0
    for x, y in system:
        absolute_score += field[y][x]

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
    #         print_system(subsys)
    available_bots_nieve = movable_bots(copy.deepcopy(system))
    outcome = determine_ideal_outcome(system, available_bots_nieve)


    print(available_bots_nieve)
    print(outcome['available_bots'])
    print_target_system(system,
                        outcome['occupied'],
                        outcome['optional'],
                        outcome['num_optional'])
    ideal_system = set(outcome['occupied'] + outcome['optional'])
    unavailable_bots = list(set(available_bots_nieve) - set(outcome['available_bots']))

    if len(list(unavailable_bots)) > 0:
        print('Removing unavailable_bots from the problem')
        sub_system = {}
        for bot in unavailable_bots:
            sub_system[bot] = {
                'options': system[bot]['options'],
                'scores': system[bot]['scores']
            }
        print('The system of unavailable_bots is')
        for pos, bot in sub_system.items():
            print(str(pos) + ' - ' + str(bot))
        sub_systems = system_split(sub_system)
        print('')
        print('This splits into ' + str(len(sub_systems)) + ' smaller systems')
        for sub_system in sub_systems:
            tmp = pick_best(sub_system)
            print('The optimum outcome here is')
            print(tmp)
            for move in tmp:
                make_reduction(system,move)
                print('The system was reduced')

        print('')
        print('-------------------------------------')
        print('=> SYSTEM SPLIT REDUCTION')
        print_system(system)


    # Make the simplifications that push the current available bots
    # into the ideal system
    for bot in outcome['available_bots']:
        to_remove = []
        for index, option in enumerate(system[bot]['options']):
            if option not in ideal_system:
                to_remove.append(option)
        for removal in to_remove:
            print('Removing move ' + str(bot) + ' -> ' + str(removal)),
            print(' because it moves away from the ideal')

            index = system[bot]['options'].index(removal)
            del system[bot]['scores'][index]
            del system[bot]['options'][index]

    # Make sure any bots with only one move aren't contesed by others
    for bot in outcome['available_bots']:
        if len(system[bot]['options']) == 1:
            move = system[bot]['options'][0]
            for b in outcome['available_bots']:
                if b != bot and move in system[b]['options']:
                    index = system[b]['options'].index(move)
                    del system[b]['scores'][index]
                    del system[b]['options'][index]

    print('')
    print('-------------------------------------')
    print('=> SYSTEM PUSHED TOWARDS IDEAL')
    print_system(system,
                 justbots=outcome['available_bots'],
                 occupied=outcome['occupied'],
                 optional=outcome['optional'])


    # Bots that didn't partake in the grand simplification
    unavailable_bots = list(set(system.keys()) - set(outcome['available_bots']))
    free_unavailable = [bot for bot in unavailable_bots if len(system[bot]['options']) > 1]

    for a,b in system.items():
        print(str(a) + ' - ' + str(b))

    if len(free_unavailable) == 0:
        print('All remaining bots are frozen')

        remaining_score = 0
        for bot in unavailable_bots:
            x,y = system[bot]['options'][0]
            remaining_score += field[y][x]
        print('The outcome_max_score = ' + str(outcome['max_score']))
        absolute_maximum_score = remaining_score + outcome['max_score']
        outcome['absolute_maximum_score'] = absolute_maximum_score

        # If we fixed everyones position that has options, how close do we get?
        print('Testing a bot freeze situation')
        test_sys = copy.deepcopy(system)
        for bot in test_sys:
            if len(test_sys[bot]['options']) > 1 and bot in test_sys[bot]['options']:
                make_reduction(test_sys, (bot, bot))
        print('Did this generate a solution?')

        moves = []
        for bot in test_sys:
            if len(test_sys[bot]['options']) == 1:
                moves.append((bot, test_sys[bot]['options'][0]))
            else:
                moves = False
                break

        if moves == False:
            print('No, it didnt')
        else:
            print('Yes it did')
            print('The initial system score was ' + str(absolute_score))
            score_diff = calculate_score(test_sys, moves)
            print('Freezing the system as-is will change it by ' + str(score_diff))
            print('The maximum obtainable for the system is ' + str(absolute_maximum_score))
            frozen_score = absolute_score + score_diff
            print('The frozen system now has a score of ' + str(frozen_score))
            if frozen_score == absolute_maximum_score:
                system = test_sys






    # while total_combinations(system) > max_options:
    #     print('This system has ' + str(total_combinations(system)) + ' possible solutions')
    #     print('Making a simplification as options greater than ' + str(max_options))
    #     print('Current system is:')
    #     for a,b in system.items():
    #         print(str(a) + ' - ' + str(b))
    #     print('')


    #     # Find a bot not in the optional area and move him into it

    #     # Are there more bots in the optional coordinates than the minimum?
    #     num_in_optionals = 0
    #     for bot in outcome['available_bots']:
    #         if bot in outcome['optional']:
    #             num_in_optionals += 1
    #     if num_in_optionals > outcome['num_optional']:
    #         # Yes
    #         # Move the bot with the least options out of the optional
    #         option_count = []
    #         for bot in outcome['available_bots']:
    #             count = len(system[bot]['options'])
    #             if count > 1:
    #                 option_count.append(count)
    #         min_count = min(option_count)
    #         constrained_bots = []
    #         for bot in outcome['available_bots']:
    #             if len(system[bot]['options']) == min_count:
    #                 constrained_bots.append(bot)
    #         bot_to_move = random.choice(constrained_bots)
    #         max_score = max(system[bot_to_move]['scores'])
    #         best_moves = []
    #         for index, score in enumerate(system[bot_to_move]['scores']):
    #             if score == max_score:
    #                 best_moves.append(system[bot_to_move]['options'][index])
    #         best_move = random.choice(best_moves)
    #         print('Moving ' + str(bot_to_move) + ' to ' + str(best_move))

    #         make_reduction(system, (bot_to_move, best_move))
    #     else:
    #         # Fix a random bot's positon
    #         bots_in_place = [bot for bot in outcome['available_bots'] if bot in outcome['occupied'] and len(system[bot]['options']) > 1]
    #         bot_to_fix = random.choice(bots_in_place)
    #         print('Fixing ' + str(bot_to_fix) + '\'s position')
    #         make_reduction(system, (bot_to_fix, bot_to_fix))

    return outcome



def reduced_systems(system, size):

    if total_combinations(system) > size:

        cells, candidates = find_possible_simplifications(system)

        if type(candidates) == list:
            new_systems = [make_reduction(copy.deepcopy(system), (candidate, cells)) for candidate in candidates]
        elif type(cells) == list:
            new_systems = [make_reduction(copy.deepcopy(system), (candidates, cell)) for cell in cells]

        filter(test_system, new_systems)

        out_systems = []
        for tmp_sys in new_systems:
            if total_combinations(tmp_sys) > size:
                new_red = reduced_systems(tmp_sys, size)
                for r in new_red:
                    out_systems.append(r)
            else:
                out_systems.append(tmp_sys)
        return out_systems
    else:
        return [system]


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

    if 'absolute_maximum_score' in outcome:
        print('Picking best move - looking for score of ' + str(outcome['absolute_maximum_score']))
        best = pick_best(system, outcome['absolute_maximum_score'])
    else:
        print('Picking best move blindly')
        best = pick_best(system)
    tc('pick_best')
    if best == None:
        print('FUCK - THIS WENT BAD')
        for a,b in system.items():
            print(str(a) + ' - ' + str(b))

        print('')
        print('AND WE STARTED WITH ')
        print('')
        for a,b in sys_backup.items():
            print(str(a) + ' - ' + str(b))



    return best

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

#         score = calculate_score(system, best)
#         if score > top_score:
#             result = best
#             top_score = score
#     return result


def calculate_score(system, moves):
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
            for bot, move in breakdown:
                final_movements[bot] = move

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

        move = decided_movements[self.location]

        if move == self.location:
            return ['guard', move]
        else:
            return ['move', move]
