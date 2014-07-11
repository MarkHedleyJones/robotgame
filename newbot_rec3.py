import rg
import numpy as np
import math
import random
import itertools
import sys
import time
import operator
import sys
import copy
import pudb

game_turn = -1
attack_damage = 10
feasable_size = 100

spawn = {(7,1),(8,1),(9,1),(10,1),(11,1),(5,2),(6,2),(12,2),(13,2),(3,3),(4,3),(14,3),(15,3),(3,4),(15,4),(2,5),(16,5),(2,6),(16,6),(1,7),(17,7),(1,8),(17,8),(1,9),(17,9),(1,10),(17,10),(1,11),(17,11),(2,12),(16,12),(2,13),(16,13),(3,14),(15,14),(3,15),(4,15),(14,15),(15,15),(5,16),(6,16),(12,16),(13,16),(7,17),(8,17),(9,17),(10,17),(11,17)}
obstacle = {(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),(15,0),(16,0),(17,0),(18,0),(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(0,2),(1,2),(2,2),(3,2),(4,2),(14,2),(15,2),(16,2),(17,2),(18,2),(0,3),(1,3),(2,3),(16,3),(17,3),(18,3),(0,4),(1,4),(2,4),(16,4),(17,4),(18,4),(0,5),(1,5),(17,5),(18,5),(0,6),(1,6),(17,6),(18,6),(0,7),(18,7),(0,8),(18,8),(0,9),(18,9),(0,10),(18,10),(0,11),(18,11),(0,12),(1,12),(17,12),(18,12),(0,13),(1,13),(17,13),(18,13),(0,14),(1,14),(2,14),(16,14),(17,14),(18,14),(0,15),(1,15),(2,15),(16,15),(17,15),(18,15),(0,16),(1,16),(2,16),(3,16),(4,16),(14,16),(15,16),(16,16),(17,16),(18,16),(0,17),(1,17),(2,17),(3,17),(4,17),(5,17),(6,17),(12,17),(13,17),(14,17),(15,17),(16,17),(17,17),(18,17),(0,18),(1,18),(2,18),(3,18),(4,18),(5,18),(6,18),(7,18),(8,18),(9,18),(10,18),(11,18),(12,18),(13,18),(14,18),(15,18),(16,18),(17,18),(18,18)}
centre = rg.CENTER_POINT
move_count = 0

def adjacent( (x,y) ):
    return set([(x + dx, y + dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0))])

def sourrounding( (x,y) ):
    return set([(x + dx, y + dy) for dx, dy in ((1, -1), (-1, 1), (-1, -1), (1, 1), (0, 1), (1, 0), (0, -1), (-1, 0))])

def within_bounds((x,y)):
    return x > 0 and y > 0 and x < 18 and y < 18 and (x,y) not in obstacle

def normalise(field):
    return (field / np.max(field)) * 100.0

def blur(field):
    out = np.zeros((19,19))
    for y, row in enumerate(field):
        for x, col in enumerate(row):
            out[x][y] = sum([field[x][y] for x,y in list(adjacent((x,y))) + [(x,y)] if (0 <= x <= 18 and 0 <= y <= 18)])
    return normalise(out)


def squares_dist(position, distance):
    if distance == 0:
        return [position]
    else:
        out = []
        px = position[0]
        py = position[1]
        for x in range(distance):
            y = distance - x
            out += [(px+x,py+y), (px+y,py-x), (px-x,py-y), (px-y,py+x)]
        return out

def print_field(field):
    for j, row in enumerate(field):
        for i, x in enumerate(row):
            if (i,j) in obstacle:
                print('    '),
            else:
                print('{0:4d}'.format(int(x))),
            if i == len(row) - 1:
                print('')

def fieldval((x,y), field):
    return field[x][y]

def locate_min(field):
    min_element = np.argmin(field)
    return (min_element % len(field[0]), min_element / len(field[0]))

def newfield():
    return np.zeros((19,19))

# Will choose the most logical move and if two of equal logic value exist
# then it will randomly select one
def best_option(pos, logicfield):
    moves = [(x,logicfield[x[0]][x[1]]) for x in available_options(pos)]
    higest_score = max(moves, key=lambda x: x[1])[1]
    if higest_score:
        return random.choice([x[0] for x in moves if x[1] == higest_score])
    else:
        # No moves exist
        return None


# def available_moves(pos):
#     return adjacent(pos) - obstacle

def available_options((x,y)):
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
    moves = [(x[0],x[1]) for x in zip(moves,gains)]
    moves.sort(key=lambda x: x[1], reverse=True)
    return [bot,[x[0] for x in moves],[x[1] for x in moves]]


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
    return [(field[ex][ey] - field[sx][sy]) for (ex,ey) in moves]


def total_combinations(system):
    total_combinations = 1
    if type(system) == dict:
        for pos, bot in system.items():
            total_combinations *= len(bot['options'])
    else:
        for bot in system:
            total_combinations *= len(bot[1])
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

        bots = [pos for pos,bot in system.items() if len(bot['options']) == max_opts]
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


def print_system(system):
    global frontlinelogic
    field = frontlinelogic
    x_min = 18
    y_min = 18

    x_max = 0
    y_max = 0

    for x,y in system:
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
    # relevant_cells = list(set(flatten([adjacent(bot) for bot in system])))
    relevant_cells = []
    for member in system:
        relevant_cells += system[member]['options']
    relevant_cells = list(set(relevant_cells))
    for member in system:
        if len(system[member]['options']) == 1:
            relevant_cells.remove(system[member]['options'][0])
    print('BOT Positions:')
    print('   '),
    for x, ax in enumerate(range(x_min,x_max)):
        print('{0:2d}'.format(ax) + ' '),
    print('')
    for y, ay in enumerate(range(y_min,y_max)):
        print('{0:2d}'.format(ay)),
        for x, ax in enumerate(range(x_min,x_max)):
            if (ax,ay) in system and len(system[(ax,ay)]['options']) > 1:
                print('  X'),
            elif (ax,ay) in relevant_cells:
                print('  -'),
            else:
                print('   '),
        print('')
    print('')
    print('Cell Scores:')
    print('   '),
    for x, ax in enumerate(range(x_min,x_max)):
        print('{0:2d}'.format(ax) + ' '),
    print('')
    for y, ay in enumerate(range(y_min,y_max)):
        print('{0:2d}'.format(ay)),
        for x, ax in enumerate(range(x_min,x_max)):
            if (ax,ay) in system and len(system[(ax,ay)]['options']) > 1:
                print(' {0:2d}'.format(int(field[ay][ax]))),
            elif (ax,ay) in relevant_cells:
                print(' {0:2d}'.format(int(field[ay][ax]))),
            else:
                print('   '),
        print('')


def is_beneficial_move(system, (start, end)):
    return system[start]['scores'][system[start]['options'].index(end)] > 0


def cells_in_direction(start,direction):
    if start[0] == direction[0]:
        if start[1] == direction[1]:
            raise ValueError('Start and direction are the same location')
        # Vertical
        if start[1] > direction[1]:
            # Going up
            return [start] + [(start[0], direction[1]-y) for y in range(0,direction[1])]
        else:
            # Going down
            return [start] + [(start[0], y) for y in range(direction[1],18)]
    elif start[1] == direction[1]:
        if start[0] == direction[0]:
            raise ValueError('Start and direction are the same location')
        # Horizontal
        if start[0] > direction[0]:
            # Going left
            return [start] + [(direction[0]-x, start[1]) for x in range(0, direction[0])]
        else:
            # Going right
            return [start] + [(x, start[1]) for x in range(direction[0],18)]
    else:
        raise ValueError('Start and direction cells are not adjacent')



def print_target_system(system, occupied, optional):
    x_min = 18
    y_min = 18

    x_max = 0
    y_max = 0

    for x,y in system:
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
    print('Target system:')
    print('   '),
    for x, ax in enumerate(range(x_min,x_max)):
        print('{0:2d}'.format(ax) + ' '),
    print('')
    for y, ay in enumerate(range(y_min,y_max)):
        print('{0:2d}'.format(ay)),
        for x, ax in enumerate(range(x_min,x_max)):
            if (ax,ay) in occupied:
                print('  X'),
            elif (ax,ay) in optional:
                print('  0'),
            else:
                print('   '),
        print('')
    print('')


def simplify_system(system):
    global frontlinelogic
    field = frontlinelogic
    # Detect a bot sourrounded by friends and whos maximum move yields 0 gain
    # and fix his position
    bot_positions = set(system.keys())
    print('')
    print('')
    print('=> BEFORE')
    print_system(system)

    # for bot in system:
    #     if system[bot]['scores'][0] == 0:
    #         if len(list(adjacent(bot) & bot_positions)) == 4:
    #             make_reduction(system, (bot, bot))
    #             print('Will hold ' + str(bot) + ' where he is...')
    #     if len(list(sourrounding(bot) & bot_positions)) == 8:
    #             make_reduction(system, (bot, bot))
    #             print('Will hold ' + str(bot) + ' where he is...')


    # Any unoccupied cell with 2 adjacent bots should be evaluated for
    # this simplification
    changed = False
    while changed:
        print('Running simplification')
        changed = False
        for bot in system.keys():
            if len(system[bot]['options']) > 1:
                gain_cell = [system[bot]['options'][system[bot]['scores'].index(score)] for score in system[bot]['scores'] if score > 0]
                if len(gain_cell) == 1:
                    gain_cell = gain_cell[0]
                    if gain_cell not in bot_positions:
                        contest = cells_in_direction(bot, gain_cell)[2]
                        if contest in bot_positions:
                            if len(bot_positions & adjacent(gain_cell)) == 2:
                                print('Awarded move from ' + str(bot) + ' to ' + str(gain_cell))
                                make_reduction(system, (bot, gain_cell))
                                changed = True
                    elif gain_cell not in system[gain_cell]['options']:
                        # Occupant moving out of this cell so it's available
                        # Contestants?
                        contestants = [coord for coord in adjacent(gain_cell) if coord in bot_positions and coord != bot]
                        print('contestants for cell ' + str(gain_cell) + ' = ' + str(contestants))







    # If a bot, not surrounded by any friends, has only one direction that
    # causes a gain and the square he wishes to move into is in contest with
    # only one other bot and that bot would loose then grant to the gaining bot
    # for bot in system.keys()[:]:
    #     if bot_positions & sourrounding(bot) == set():
    #         # print(str(bot) + ' - ' + str(system[bot]))
    #         gain_cell = [system[bot]['options'][system[bot]['scores'].index(score)] for score in system[bot]['scores'] if score > 0]

    #         if (len(gain_cell)) == 1 and gain_cell[0] not in bot_positions:
    #             # Has only one beneficail move
    #             contest = cells_in_direction(bot, gain_cell[0])[2]
    #             if contest in bot_positions:
    #                 if gain_cell[0] in system[contest]['options']:
    #                     if is_beneficial_move(system, (contest, gain_cell[0]) ) == False:
    #                         print('Joinee ' + str(bot) + ' was granted ' + str(gain_cell[0]))
    #                         print('He had ' + str(len(system[bot]['options'])) + 'available moves')
    #                         make_reduction(system, (bot, gain_cell[0]))

    print('')
    print('-------------------------------------')
    print('=> AFTER')
    print_system(system)

    free_system_bots = []
    free_system_scores = []
    free_system_coords = []
    for bot in system.keys():
        if len(system[bot]['options']) > 1:
            free_system_bots.append(bot)
            free_system_coords += system[bot]['options']

    free_system_coords = list(set(free_system_coords))
    coords_by_score = {}
    for (x,y) in free_system_coords:
        score = int(field[y][x])
        free_system_scores.append(score)
        if score in coords_by_score:
            coords_by_score[score].append((x,y))
        else:
            coords_by_score[score] = [(x,y)]

    free_system_scores = list(set(free_system_scores))
    free_system_scores.sort(reverse=True)

    targets_occupied = []
    targets_optional = []

    available_bots = len(free_system_bots)
    for score in free_system_scores:
        if available_bots > 0:
            coords = coords_by_score[score]
            if len(coords) <= available_bots:
                targets_occupied += coords
            else:
                targets_optional += coords
            available_bots -= len(coords)

    print_target_system(system, targets_occupied, targets_optional)

    # Perform translation to target system
    if len(targets_optional) == 0:
        good = True
        for target in targets_occupied:
            if target not in system.keys():
                good = False
                break
        if good:
            for bot in system:
                make_reduction(system, (bot, bot))



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

def choose_moves(system):
    global feasable_size
    top_score = -9999
    result = None

    simplify_system(system)

    for system in reduced_systems(system, feasable_size):

        best = pick_best(system)
        if best is None:
            continue

        score = calculate_score(system, best)
        if score > top_score:
            result = best
            top_score = score
    return result

def calculate_score(system, moves):
    out = 0.0
    for start,end in moves:
        out += system[start]['scores'][system[start]['options'].index(end)]
    return out

def decide_actions(movements,recursed=False):
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
                system[member[0]] = {'options':member[1], 'scores': member[2]}

            breakdown = choose_moves(system)

            for bot, move in breakdown:
                final_movements[bot] = move


    return final_movements

decided_movements = None

class Robot:


    def level4_field(self, members):
        out = newfield()
        for distance in range(0,13):
            for x,y in squares_dist(rg.CENTER_POINT, distance):
                if within_bounds((x,y)):
                    out[x][y] = 12-distance
        return out


    def act(self, game):

        global game_turn, attack_damage, spawn, obstacle, centre, move_count, decided_movements, frontlinelogic
        robots = game.robots

        if game.turn != game_turn:

            game_turn = game.turn
            turn = game_turn - 1

            friendlies = set([bot for bot in robots if robots[bot].player_id==self.player_id])
            enemies = set(robots)-friendlies


            ## Level 4 logic
            available_members = [x for x in friendlies]
            frontlinelogic = self.level4_field(available_members)

            # All the movement possibilities
            bots = [x for x in friendlies]
            moves = [available_options(x) for x in bots]
            gains = [movement_gains(action,frontlinelogic) for action in zip(bots,moves)]

            name_me = zip(bots,moves,gains)
            # Turn the moves into ordered lists
            group_sorted_movements = [movelist_sorted(x[0], list(x[1]),x[2]) for x in name_me]


            decided_movements = decide_actions(group_sorted_movements)


            # for bot in decided_movements:
            #     print('bot ' + str(bot) + ' moves to ' + str(decided_movements[bot]))


        # print('allocating movment for ' + str(self.location))
        move = decided_movements[self.location]

        if move == self.location:
            return ['guard', move]
        else:
            return ['move', move]



