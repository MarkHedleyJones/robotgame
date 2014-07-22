import numpy as np
import sys
import random
import itertools
import operator
import copy
import heapq
# import pudb

spawn = {(7,1),(8,1),(9,1),(10,1),(11,1),(5,2),(6,2),(12,2),(13,2),(3,3),(4,3),(14,3),(15,3),(3,4),(15,4),(2,5),(16,5),(2,6),(16,6),(1,7),(17,7),(1,8),(17,8),(1,9),(17,9),(1,10),(17,10),(1,11),(17,11),(2,12),(16,12),(2,13),(16,13),(3,14),(15,14),(3,15),(4,15),(14,15),(15,15),(5,16),(6,16),(12,16),(13,16),(7,17),(8,17),(9,17),(10,17),(11,17)}
obstacle = {(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),(15,0),(16,0),(17,0),(18,0),(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(0,2),(1,2),(2,2),(3,2),(4,2),(14,2),(15,2),(16,2),(17,2),(18,2),(0,3),(1,3),(2,3),(16,3),(17,3),(18,3),(0,4),(1,4),(2,4),(16,4),(17,4),(18,4),(0,5),(1,5),(17,5),(18,5),(0,6),(1,6),(17,6),(18,6),(0,7),(18,7),(0,8),(18,8),(0,9),(18,9),(0,10),(18,10),(0,11),(18,11),(0,12),(1,12),(17,12),(18,12),(0,13),(1,13),(17,13),(18,13),(0,14),(1,14),(2,14),(16,14),(17,14),(18,14),(0,15),(1,15),(2,15),(16,15),(17,15),(18,15),(0,16),(1,16),(2,16),(3,16),(4,16),(14,16),(15,16),(16,16),(17,16),(18,16),(0,17),(1,17),(2,17),(3,17),(4,17),(5,17),(6,17),(12,17),(13,17),(14,17),(15,17),(16,17),(17,17),(18,17),(0,18),(1,18),(2,18),(3,18),(4,18),(5,18),(6,18),(7,18),(8,18),(9,18),(10,18),(11,18),(12,18),(13,18),(14,18),(15,18),(16,18),(17,18),(18,18)}
move_count = 0


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



def adjacent(pos):
    x, y = pos
    adj = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    return set([(x + dx, y + dy) for dx, dy in adj])




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
            for path_group in paths:
                if check_moves(system, [path_group]) == False:
                    print('ERROR: GENERATED INVALID PATH')
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
                # print('Move ' + str((moves[start], moves[end])))
                grant_move(tmp_sys, moves[start], moves[end])
            except ValueError:
                print('Referenced non-available move ' + str((moves[start], moves[end])))
                return False
    valid = is_valid(tmp_sys)
    if valid:
        # print('Works... ' + str(move_paths))
        return True
    else:
        # print('The sistem is invalid')
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


def cells_inside_radius_from_centre(radius):
    if radius == 0:
        return []
    else:
        out = []
        for rad in range(radius):
            out += squares_dist((9, 9), rad)
        return out


def num_cells_inside_radius_from_centre(radius):
    return sum([1] + [x*4 for x in range(radius+1)])


def num_cells_at_radius_from_centre(radius):
    num = radius * 4
    if num > 0:
        return num
    else:
        return 1




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


def within_bounds(coord):
    x, y = coord
    return x > 0 and y > 0 and x < 18 and y < 18 and (x, y) not in obstacle


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
        print('radius = ' + str(radius) + ' distance = ' + str(distance) + ', from_rad = ' + str(from_rad))
        for x, y in squares_dist((9, 9), distance):
            if within_bounds((x, y)):
                out[y][x] = score
    return out





def flaten_pathnest(element, level=-1):
    """
    Take a nested array from shortest_paths and
    flatten it while removing paths that dont lead
    to the end square
    """
    out = []
    if type(element) == list:
        for item in element:
            if type(item) == list:
                out += flaten_pathnest(item, level)
            else:
                level += 1
                out.append((item, level))
        return out
    else:
        # level -= 1
        return [(element,level)]









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

def movable_bots(system):
    return [bot for bot in system if len(system[bot]['options']) > 1]


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

def pt(it, lv):
    for i in range(lv):
        print('\t'),
    print(it)

def ppn(pn, lv):
    if type(pn) == list:
        for p in pn:
            if type(p) == list:
                ppn(p, lv+1)
            else:
                pt(p, lv)
    else:
        pt(pn, lv)



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

############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
#
#
# class Cell(object):
#     def __init__(self, x, y, reachable):
#         """
#         Initialize new cell

#         @param x cell x coordinate
#         @param y cell y coordinate
#         @param reachable is cell reachable? not a wall?
#         """
#         self.reachable = reachable
#         self.x = x
#         self.y = y
#         self.parent = None
#         self.g = 0
#         self.h = 0
#         self.f = 0

# class AStar(object):

#     def __init__(self):
#         self.op = []
#         heapq.heapify(self.op)
#         self.cl = set()
#         self.cells = []
#         self.gridHeight = 19
#         self.gridWidth = 19

#     def init_grid(self):
#         # walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),
#         #          (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))

#         available = ((6, 9), (10, 11), (9, 8), (8, 9), (12, 9), (10, 8),
#                      (11, 10), (10, 7), (8, 10), (9, 11), (7, 10),
#                      (10, 9), (9, 7), (8, 11), (11, 9), (9, 10), (8, 7),
#                      (9, 6), (7, 9), (10, 10), (11, 8), (8, 8), (7, 8),
#                      (9, 12), (9, 5))

#         for x in range(self.gridWidth):
#             for y in range(self.gridHeight):
#                 if (x, y) in available:
#                     reachable = True
#                 else:
#                     reachable = False
#                 self.cells.append(Cell(x, y, reachable))

#         self.start = self.get_cell(9, 5)
#         self.end = self.get_cell(9, 12)

#     def get_heuristic(self, cell):
#         """
#         Compute the heuristic value H for a cell: distance between
#         this cell and the ending cell multiply by 10.

#         @param cell
#         @returns heuristic value H
#         """
#         return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

#     def get_cell(self, x, y):
#         """
#         Returns a cell from the cells list

#         @param x cell x coordinate
#         @param y cell y coordinate
#         @returns cell
#         """
#         return self.cells[x * self.gridHeight + y]

#     def get_adjacent_cells(self, cell):
#         """
#         Returns adjacent cells to a cell. Clockwise starting
#         from the one on the right.

#         @param cell get adjacent cells for this cell
#         @returns adjacent cells list
#         """
#         cells = []
#         if cell.x < self.gridWidth-1:
#             cells.append(self.get_cell(cell.x+1, cell.y))
#         if cell.y > 0:
#             cells.append(self.get_cell(cell.x, cell.y-1))
#         if cell.x > 0:
#             cells.append(self.get_cell(cell.x-1, cell.y))
#         if cell.y < self.gridHeight-1:
#             cells.append(self.get_cell(cell.x, cell.y+1))
#         return cells

#     def display_path(self):
#         cell = self.end
#         while cell.parent is not self.start:
#             cell = cell.parent
#             print 'path: cell: %d,%d' % (cell.x, cell.y)


#     def update_cell(self, adj, cell):
#         """
#         Update adjacent cell

#         @param adj adjacent cell to current cell
#         @param cell current cell being processed
#         """
#         adj.g = cell.g + 10
#         adj.h = self.get_heuristic(adj)
#         adj.parent = cell
#         adj.f = adj.h + adj.g

#     def process(self):
#         # add starting cell to open heap queue
#         heapq.heappush(self.op, (self.start.f, self.start))
#         while len(self.op):
#             # pop cell from heap queue
#             f, cell = heapq.heappop(self.op)
#             # add cell to closed list so we don't process it twice
#             self.cl.add(cell)
#             # if ending cell, display found path
#             if cell is self.end:
#                 self.display_path()
#                 break
#             # get adjacent cells for cell
#             adj_cells = self.get_adjacent_cells(cell)
#             for c in adj_cells:
#                 if c.reachable and c not in self.cl:
#                     if (c.f, c) in self.op:
#                         # if adj cell in open list, check if current path is
#                         # better than the one previously found for this adj
#                         # cell.
#                         if c.g > cell.g + 10:
#                             self.update_cell(c, cell)
#                     else:
#                         self.update_cell(c, cell)
#                         # add adj cell to open list
#                         heapq.heappush(self.op, (c.f, c))





# a = AStar()
# a.process()





def shortest_paths(start, end, available_squares):
    """
    Find the shortest paths between two coordinates
    using only the array of squares passed
    """
    squares_by_dist = [[start]]
    available_squares = set(available_squares)
    distance = 0
    while True:
        distance += 1
        squares = squares_dist(start, distance)
        tmp = list(set(squares) & available_squares)
        if tmp == []:
            break
        elif end in tmp:
            squares_by_dist.append([end])
            break
        else:
            squares_by_dist.append(tmp)
    for dist, squares in enumerate(squares_by_dist):
        print(str(dist) + ' - ' + str(squares))

    return path_walk(squares_by_dist)


def find_paths(start, end, available):
    """
    Return a list of the shortest possible paths between
    the given start and end points
    """
    print('')
    print('find_paths called with')
    print('start = ' + str(start))
    print('end = ' + str(end))
    print('available = ' + str(available))
    path_nest = shortest_paths(start, end, available)
    print('PRINGING PATH NEST!!!')
    ppn(path_nest, 0)


    print('path_nest = ' + str(path_nest))
    flat_nest = flaten_pathnest(path_nest)
    print('flat_nest = ' + str(flat_nest))
    paths = []
    tmp = []
    last_level = -1
    for node, level in flat_nest:
        for i in range(level):
            print('\t'),
        print(node)
        try:
            tmp[level] = node
        except:
            tmp.append(node)

        if node == end:
            print('TMP = ' + str(tmp))
            paths.append(tmp)
            tmp = tmp[:level]
        last_level = level
    sys.exit()
    return paths


def try_movement_sets(system, targets, candidates, squares):
    for a in system:
        print(str(a) + ': ' + str(system[a]))
    show_system(system)
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


    print('try_movement_sets dimensions')
    print(str(len(targets)) + ' targets')
    print(str(len(candidates)) + ' candidates')
    match_sets = mix_lists(candidates, targets)

    # precheck for bad links
    bad_links = []
    for end in targets:
        for start in candidates:
            print('precheck for moves between ' + str(start) + ' and ' + str(end))
            these_squares = squares + [end] + [start]
            print(these_squares)
            print(find_paths(start, end, these_squares))
            if find_paths(start, end, squares + [end]) == []:
                bad_links.append((start, end))

    print('bad_links = '  + str(bad_links))

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
    return False




system = {(6, 9): {'options': [(7, 9), (6, 9), (5, 9)], 'scores': [2, 0, -2]}, (10, 11): {'options': [(9, 11), (10, 10), (10, 11), (11, 11), (10, 12)], 'scores': [2, 2, 0, -2, -2]}, (9, 8): {'options': [(10, 8), (8, 8), (9, 7), (9, 8), (9, 9)], 'scores': [2, 2, 2, 0, -2]}, (8, 9): {'options': [(8, 8), (8, 10), (7, 9), (8, 9), (9, 9)], 'scores': [2, 2, 2, 0, -2]}, (12, 9): {'options': [(11, 9), (12, 9), (12, 10), (12, 8)], 'scores': [2, 0, -2, -2]}, (10, 8): {'options': [(10, 8), (11, 8), (10, 7), (9, 8), (10, 9)], 'scores': [0, -2, -2, -2, -2]}, (11, 10): {'options': [(11, 9), (10, 10), (11, 10), (12, 10), (11, 11)], 'scores': [2, 2, 0, -2, -2]}, (10, 7): {'options': [(10, 8), (9, 7), (10, 7), (10, 6), (11, 7)], 'scores': [2, 2, 0, -2, -2]}, (11, 12): {'options': [(10, 12), (11, 11)], 'scores': [2, 2]}, (8, 10): {'options': [(8, 10), (9, 10), (8, 9), (8, 11), (7, 10)], 'scores': [0, -2, -2, -2, -2]}, (9, 11): {'options': [(9, 11), (9, 10), (8, 11), (10, 11), (9, 12)], 'scores': [0, -2, -2, -2, -2]}, (7, 10): {'options': [(8, 10), (7, 9), (7, 10), (7, 11), (6, 10)], 'scores': [2, 2, 0, -2, -2]}, (10, 9): {'options': [(10, 8), (11, 9), (10, 10), (10, 9), (9, 9)], 'scores': [2, 2, 2, 0, -2]}, (9, 7): {'options': [(9, 7), (10, 7), (9, 8), (9, 6), (8, 7)], 'scores': [0, -2, -2, -2, -2]}, (8, 11): {'options': [(9, 11), (8, 10), (8, 11), (7, 11), (8, 12)], 'scores': [2, 2, 0, -2, -2]}, (11, 9): {'options': [(11, 9), (11, 8), (11, 10), (12, 9), (10, 9)], 'scores': [0, -2, -2, -2, -2]}, (9, 10): {'options': [(9, 11), (8, 10), (10, 10), (9, 10), (9, 9)], 'scores': [2, 2, 2, 0, -2]}, (8, 7): {'options': [(8, 8), (9, 7), (8, 7), (8, 6), (7, 7)], 'scores': [2, 2, 0, -2, -2]}, (9, 6): {'options': [(9, 7), (9, 6), (8, 6), (10, 6), (9, 5)], 'scores': [2, 0, -2, -2, -2]}, (7, 9): {'options': [(7, 9), (8, 9), (6, 9), (7, 8), (7, 10)], 'scores': [0, -2, -2, -2, -2]}, (10, 10): {'options': [(10, 10), (9, 10), (11, 10), (10, 11), (10, 9)], 'scores': [0, -2, -2, -2, -2]}, (11, 8): {'options': [(11, 9), (10, 8), (11, 8), (11, 7), (12, 8)], 'scores': [2, 2, 0, -2, -2]}, (8, 8): {'options': [(8, 8), (8, 9), (9, 8), (7, 8), (8, 7)], 'scores': [0, -2, -2, -2, -2]}, (9, 5): {'options': [(9, 6), (9, 5)], 'scores': [2, 0]}, (7, 8): {'options': [(8, 8), (7, 9), (7, 8), (6, 8)], 'scores': [2, 2, 0, -2]}}
targets = [(9, 12)]
candidates = [(9, 5)]
squares = [(6, 9), (10, 11), (9, 8), (8, 9), (12, 9), (10, 8), (11, 10), (10, 7), (8, 10), (9, 11), (7, 10), (10, 9), (9, 7), (8, 11), (11, 9), (9, 10), (8, 7), (9, 6), (7, 9), (10, 10), (11, 8), (8, 8), (7, 8)]

try_movement_sets(system, targets, candidates, squares)