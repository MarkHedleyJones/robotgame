import numpy as np
import sys
import random
import itertools
import operator
import copy
# import pudb

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


def adjacent(pos):
    x, y = pos
    adj = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    return set([(x + dx, y + dy) for dx, dy in adj])



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
        for item in element:
            out += flaten_pathnest(item, level+1)
        return out
    else:
        return [(element,level-1)]


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


def make_moves(system, move_paths):
    print('making moves ' + str(move_paths))
    print('system =')
    for a in system:
        print(str(a) + ' - ' + str(system[a]))
    for moves in move_paths:
        for start in range(len(moves)-1):
            end = start + 1
            grant_move(system, moves[start], moves[end])
    print('done')
    print('system is now =')
    for a in system:
        print(str(a) + ' - ' + str(system[a]))

def find_paths(start, end, available):
    """
    Return a list of the shortest possible paths between
    the given start and end points
    """
    print('')
    print("THIS IS FIND_PATHS")
    print('from ' + str(start) + ' to ' + str(end) + ' with ' + str(available))
    path_nest = shortest_paths(start, end, available)
    print(path_nest)
    flat_nest = flaten_pathnest(path_nest[0],0)
    print(flat_nest)
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
    print('')
    return paths

xs = [('a', 'b'), ('c', 'b'), ('g', 'b')]
ys = [(10, 10),(12, 9), (8,8), (9,1)]


def mixer(xs, ys):
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
            out.append([list(x) for x in combo])
    return out

def mix_lists(xs, ys):
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

    return out

system = {
    (5, 9): {'options': [(6, 9), (5, 9), (5, 10), (4, 9)], 'scores': [1, 0, -1, -1]},
    (6, 9): {'options': [(7, 9), (6, 9), (5, 9), (6, 10), (6, 8)], 'scores': [1, 0, -1, -1, -1]},
    (10, 11): {'options': [(9, 11), (10, 10), (10, 11), (11, 11), (10, 12)], 'scores': [1, 1, 0, -1, -1]},
    (9, 8): {'options': [(9, 9), (9, 8), (10, 8), (8, 8), (9, 7)], 'scores': [1, 0, -1, -1, -1]},
    (10, 6): {'options': [(10, 7), (9, 6), (10, 6), (10, 5), (11, 6)], 'scores': [1, 1, 0, -1, -1]},
    (7, 7): {'options': [(7, 8), (8, 7), (7, 7), (7, 6), (6, 7)], 'scores': [1, 1, 0, -1, -1]},
    (10, 12): {'options': [(10, 11), (9, 12), (10, 12), (11, 12)], 'scores': [1, 1, 0, -1]},
    (8, 9): {'options': [(9, 9), (8, 9), (8, 8), (8, 10), (7, 9)], 'scores': [1, 0, -1, -1, -1]},
    (7, 11): {'options': [(8, 11), (7, 10), (7, 11), (7, 12), (6, 11)], 'scores': [1, 1, 0, -1, -1]},
    (14, 9): {'options': [(13, 9)], 'scores': [1]},
    (12, 9): {'options': [(11, 9), (12, 9), (12, 10), (12, 8)], 'scores': [1, 0, -1, -1]},
    (10, 8): {'options': [(9, 8), (10, 9), (10, 8), (11, 8), (10, 7)], 'scores': [1, 1, 0, -1, -1]},
    (11, 10): {'options': [(11, 9), (10, 10), (11, 10), (12, 10), (11, 11)], 'scores': [1, 1, 0, -1, -1]},
    (10, 7): {'options': [(10, 8), (9, 7), (10, 7), (10, 6), (11, 7)], 'scores': [1, 1, 0, -1, -1]},
    (6, 10): {'options': [(6, 9), (7, 10), (6, 10), (6, 11), (5, 10)], 'scores': [1, 1, 0, -1, -1]},
    (8, 10): {'options': [(9, 10), (8, 9), (8, 10), (8, 11), (7, 10)], 'scores': [1, 1, 0, -1, -1]},
    (9, 11): {'options': [(9, 10), (9, 11), (8, 11), (10, 11), (9, 12)], 'scores': [1, 0, -1, -1, -1]},
    (7, 10): {'options': [(8, 10), (7, 9), (7, 10), (7, 11), (6, 10)], 'scores': [1, 1, 0, -1, -1]},
    (8, 6): {'options': [(9, 6), (8, 7), (8, 6), (7, 6), (8, 5)], 'scores': [1, 1, 0, -1, -1]},
    (10, 9): {'options': [(9, 9), (10, 9), (10, 8), (11, 9), (10, 10)], 'scores': [1, 0, -1, -1, -1]},
    (9, 7): {'options': [(9, 8), (9, 7), (10, 7), (9, 6), (8, 7)], 'scores': [1, 0, -1, -1, -1]},
    (9, 14): {'options': [(9, 13), (9, 14)], 'scores': [1, 0]},
    (11, 7): {'options': [(11, 8), (10, 7), (11, 7), (12, 7), (11, 6)], 'scores': [1, 1, 0, -1, -1]},
    (13, 9): {'options': [(12, 9), (13, 10), (13, 8)], 'scores': [1, -1, -1]},
    (8, 11): {'options': [(9, 11), (8, 10), (8, 11), (7, 11), (8, 12)], 'scores': [1, 1, 0, -1, -1]},
    (11, 9): {'options': [(10, 9), (11, 9), (11, 8), (11, 10), (12, 9)], 'scores': [1, 0, -1, -1, -1]},
    (10, 15): {'options': [(10, 14)], 'scores': [1]},
    (9, 10): {'options': [(9, 9), (9, 10), (9, 11), (8, 10), (10, 10)], 'scores': [1, 0, -1, -1, -1]},
    (15, 7): {'options': [(15, 8)], 'scores': [1]},
    (8, 7): {'options': [(8, 8), (9, 7), (8, 7), (8, 6), (7, 7)], 'scores': [1, 1, 0, -1, -1]},
    (12, 10): {'options': [(11, 10), (12, 9), (12, 10), (13, 10), (12, 11)], 'scores': [1, 1, 0, -1, -1]},
    (9, 6): {'options': [(9, 7), (9, 6), (8, 6), (10, 6), (9, 5)], 'scores': [1, 0, -1, -1, -1]},
    (7, 9): {'options': [(8, 9), (7, 9), (6, 9), (7, 8), (7, 10)], 'scores': [1, 0, -1, -1, -1]},
    (9, 13): {'options': [(9, 12), (9, 13), (9, 14), (10, 13), (8, 13)], 'scores': [1, 0, -1, -1, -1]},
    (6, 8): {'options': [(7, 8), (6, 9), (6, 8), (6, 7), (5, 8)], 'scores': [1, 1, 0, -1, -1]},
    (8, 12): {'options': [(8, 11), (9, 12), (8, 12), (7, 12), (8, 13)], 'scores': [1, 1, 0, -1, -1]},
    (11, 8): {'options': [(11, 9), (10, 8), (11, 8), (11, 7), (12, 8)], 'scores': [1, 1, 0, -1, -1]},
    (10, 10): {'options': [(9, 10), (10, 9), (10, 10), (11, 10), (10, 11)], 'scores': [1, 1, 0, -1, -1]},
    (9, 9): {'options': [(9, 9), (9, 10), (8, 9), (9, 8), (10, 9)], 'scores': [0, -1, -1, -1, -1]},
    (15, 6): {'options': [(15, 7)], 'scores': [1]},
    (8, 8): {'options': [(8, 9), (9, 8), (8, 8), (7, 8), (8, 7)], 'scores': [1, 1, 0, -1, -1]},
    (15, 9): {'options': [(14, 9)], 'scores': [1]},
    (9, 5): {'options': [(9, 6), (9, 5), (10, 5), (8, 5), (9, 4)], 'scores': [1, 0, -1, -1, -1]},
    (7, 8): {'options': [(8, 8), (7, 9), (7, 8), (6, 8), (7, 7)], 'scores': [1, 1, 0, -1, -1]},
    (9, 12): {'options': [(9, 11), (9, 12), (9, 13), (10, 12), (8, 12)], 'scores': [1, 0, -1, -1, -1]},
    (12, 8): {'options': [(11, 8), (12, 9), (12, 8), (12, 7), (13, 8)], 'scores': [1, 1, 0, -1, -1]}
}

def try_movement_sets(system, targets, candidates, squares):
    match_sets = mix_lists(candidates, targets)
    print('Match sets generated = ' + str(match_sets))
    available_coords = set(squares)
    for match_set in match_sets:
        print('')
        print('Looking at ' + str(match_set))
        set_paths = []
        skip = False
        taken_coords = set()
        for start, end in match_set:
            coords = available_coords
            coords.add(end)
            coords.difference(taken_coords)
            print('Find paths between ' + str(start) + ' and ' + str(end))
            paths = find_paths(start, end, list(coords))
            print(str(len(paths)) + ' paths = ' + str(paths))
            if paths == None:
                skip = True
                break
            else:
                set_paths.append(paths)

        print('Finished generating path sets')
        print(set_paths)
        print('')

        if skip == False:
            print('Checking match_set, ' + str(match_set))
            print('Which generated the set_paths ' + str(set_paths))

            for path_group in itertools.product(*set_paths):
                print('Checking ' + str(path_group))
                if check_moves(system, path_group):
                    print('Looking good, implementing set')
                    make_moves(system, path_group)
                    print('after returning, systemm is now =')
                    for a in system:
                        print(str(a) + ' - ' + str(system[a]))
                    return True
            print('Tried all moves but none worked')
        else:
            print('Skipped as no paths')

    print('Fell out of loop without a solution')
    return False

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
    valid = is_valid(tmp_sys)
    if valid:
        print('Works... ' + str(move_paths))
        return True
    else:
        print('The sistem is invalid')
        return False

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


outcome = {}
target_occupied_not_occupied = [(10, 10), (10,11)]
current_bots_in_optional_that_can_move_to_occupied = [(6, 9), (9,11)]
movable_bots_in_occupied_that_have_to_move = []

outcome['available_bots'] = [(10, 8), (6, 9), (11, 7), (9, 8), (11, 9), (9, 9), (8, 10), (9, 10), (8, 8), (9, 11), (8, 9), (7, 9), (10, 9), (9, 7)]

if try_movement_sets(system,
                     target_occupied_not_occupied,
                     current_bots_in_optional_that_can_move_to_occupied + movable_bots_in_occupied_that_have_to_move,
                     outcome['available_bots']):
    print('The movements were made')
else:
    print('The movements could not be made')

# -------------------------- running turn 28 ---------------------------


# => INITIAL
# BOT Positions:
# 14 participants
#      5   6   7   8   9  10  11  12
#  6                   -
#  7               -   X   -   X
#  8           -   X   X   X   -
#  9   -   X   X   X   X   X   X
# 10           -   X   X   -   -
# 11               -   X   -
# 12


# -------------------------------------
# => AFTER DANGLING GRANTS
# BOT Positions:
# 14 participants
#      5   6   7   8   9  10  11  12
#  6                   -
#  7               -   X   -   X
#  8           -   X   X   X   -
#  9   -   X   X   X   X   X   X
# 10           -   X   X   -   -
# 11               -   X   -
# 12

# determine_ideal_outcome called with [(10, 8), (6, 9), (11, 7), (9, 8), (11, 9), (9, 9), (8, 10), (9, 10), (8, 8), (9, 11), (8, 9), (7, 9), (10, 9), (9, 7)]
# outcome =
# num_optional - 1
# optional - [(6, 9), (10, 11), (11, 10), (10, 7), (7, 10), (8, 11), (8, 7), (9, 6), (11, 8), (7, 8)]
# occupied - [(9, 9), (9, 8), (8, 9), (10, 9), (9, 10), (10, 8), (8, 10), (9, 11), (9, 7), (11, 9), (7, 9), (10, 10), (8, 8)]
# available_bots - [(10, 8), (6, 9), (11, 7), (9, 8), (11, 9), (9, 9), (8, 10), (9, 10), (8, 8), (9, 11), (8, 9), (7, 9), (10, 9), (9, 7)]
# levels - {8: [(5, 9), (11, 7)], 9: [(6, 9), (10, 11), (11, 10), (10, 7), (7, 10), (8, 11), (8, 7), (9, 6), (11, 8), (7, 8)], 10: [(10, 8), (8, 10), (9, 11), (9, 7), (11, 9), (7, 9), (10, 10), (8, 8)], 11: [(9, 8), (8, 9), (10, 9), (9, 10)], 12: [(9, 9)]}
# max_score - 145

# -------------------------------------
# TARGET system:
# 14 participants
# ()
#      5   6   7   8   9  10  11  12
#  6                   1
#  7               1   X   1
#  8           1   X   X   X   1
#  9       1   X   X   X   X   X
# 10           1   X   X   X   1
# 11               1   X   1
# 12


# -------------------------------------
# => SYSTEM PUSHED TOWARDS IDEAL
# BOT Positions:
# 14 participants
#      5   6   7   8   9  10  11  12
#  6                   -
#  7               -   0   -   X
#  8           -   0   0   0   -
#  9       ?   0   0   0   0   0
# 10           -   0   0   =   -
# 11               -   0   -
# 12

# Cell Scores:
#      5   6   7   8   9  10  11  12
#  6                   9
#  7               9  10   9   8
#  8           9  10  11  10   9
#  9       9  10  11  12  11  10
# 10           9  10  11  10   9
# 11               9  10   9
# 12

# The system now has a total of 500000000 options
# The initial system score was 143
# The maximum obtainable for the system is 145
# The score gain were looking for is 2
# The system_score_gain_required = 2

# bots_in_optional = [(6, 9)]
# bots_in_optional_moving_to_occupied = []
# bots_outside_system = [(11, 7)]
# bots_outside_system_moving_to_optional  = [(11, 7)]
# bots_in_occupied = [(10, 8), (9, 8), (11, 9), (9, 9), (8, 10), (9, 10), (8, 8), (9, 11), (8, 9), (7, 9), (10, 9), (9, 7)]
# bots_in_occupied_moving_to_optional = []
# movable_bots_in_occupied_that_have_to_move = []
# num_target_bots_in_optional = 1
# num_target_bots_in_occupied = 13
# current_bots_in_optional = [(6, 9), (11, 7)]
# current_bots_in_optional_that_can_move_to_occupied = [(6, 9)]
# current_bots_in_occupied = [(10, 8), (9, 8), (11, 9), (9, 9), (8, 10), (9, 10), (8, 8), (9, 11), (8, 9), (7, 9), (10, 9), (9, 7)]
# current_bots_in_occupied_that_can_move_to_optional = [(10, 8), (11, 9), (8, 10), (8, 8), (9, 11), (7, 9), (9, 7)]
# current_bots_outside = []
# target_occupied_not_occupied = [(10, 10)]
# target_occupied_with_bot_now_or_definite_bot_next = [(10, 8), (9, 8), (11, 9), (9, 9), (8, 10), (9, 10), (8, 8), (9, 11), (8, 9), (7, 9), (10, 9), (9, 7)]

# Optional squares exist
# 1 bots need to move out of optional
# And 1 bots need to move into occupied
# len(current_bots_in_optional_that_can_move_to_occupied) = 1
# Deficit = 0
# It should be possible to make this happen
# Like by doing one from 1 of the following solutions
# Match sets generated = [[((6, 9), (10, 10))]]
# Looking at [((6, 9), (10, 10))]

# Find paths between (6, 9) and (10, 10)
# Using only [(10, 8), (6, 9), (11, 7), (9, 8), (11, 9), (9, 9), (8, 10), (9, 10), (8, 8), (9, 11), (8, 9), (9, 7), (10, 10), (10, 9), (7, 9)]
# Checking match_set, [((6, 9), (10, 10))]
# Which generated the set_paths [[[(6, 9), (7, 9), (8, 9), (8, 8), (9, 9), (9, 10), (10, 10)], [(6, 9), (7, 9), (8, 9), (8, 8), (10, 9), (10, 10)], [(6, 9), (7, 9), (8, 9), (8, 10), (9, 10), (10, 10)]]]
# Checking [[(6, 9), (7, 9), (8, 9), (8, 8), (9, 9), (9, 10), (10, 10)], [(6, 9), (7, 9), (8, 9), (8, 8), (10, 9), (10, 10)], [(6, 9), (7, 9), (8, 9), (8, 10), (9, 10), (10, 10)]]
# Move ((6, 9), (7, 9))
# Move ((7, 9), (8, 9))
# Move ((8, 9), (8, 8))
# Move ((8, 8), (9, 9))
# Referenced non-available move ((8, 8), (9, 9))
# Tried all moves but none worked
# Fell out of loop without a solution
# The movements could not be made
# unoccupied squares exist ... [(10, 10)]
# We need to find paths between those and 1 bots
# There are 1 bots that can be used... [(6, 9)]
# Match sets generated = [[((6, 9), (10, 10))]]
# Looking at [((6, 9), (10, 10))]

# Find paths between (6, 9) and (10, 10)
# Using only [(10, 8), (6, 9), (11, 7), (9, 8), (11, 9), (9, 9), (8, 10), (9, 10), (8, 8), (9, 11), (8, 9), (9, 7), (10, 10), (10, 9), (7, 9)]
# Checking match_set, [((6, 9), (10, 10))]
# Which generated the set_paths [[[(6, 9), (7, 9), (8, 9), (8, 8), (9, 9), (9, 10), (10, 10)], [(6, 9), (7, 9), (8, 9), (8, 8), (10, 9), (10, 10)], [(6, 9), (7, 9), (8, 9), (8, 10), (9, 10), (10, 10)]]]
# Checking [[(6, 9), (7, 9), (8, 9), (8, 8), (9, 9), (9, 10), (10, 10)], [(6, 9), (7, 9), (8, 9), (8, 8), (10, 9), (10, 10)], [(6, 9), (7, 9), (8, 9), (8, 10), (9, 10), (10, 10)]]
# Move ((6, 9), (7, 9))
# Move ((7, 9), (8, 9))
# Move ((8, 9), (8, 8))
# Move ((8, 8), (9, 9))
# Referenced non-available move ((8, 8), (9, 9))
# Tried all moves but none worked
# Fell out of loop without a solution
# It failed