import rg
import numpy as np
import math
import random
import itertools
import sys
import time
import operator
import sys
game_turn = -1
attack_damage = 10

spawn = {(7,1),(8,1),(9,1),(10,1),(11,1),(5,2),(6,2),(12,2),(13,2),(3,3),(4,3),(14,3),(15,3),(3,4),(15,4),(2,5),(16,5),(2,6),(16,6),(1,7),(17,7),(1,8),(17,8),(1,9),(17,9),(1,10),(17,10),(1,11),(17,11),(2,12),(16,12),(2,13),(16,13),(3,14),(15,14),(3,15),(4,15),(14,15),(15,15),(5,16),(6,16),(12,16),(13,16),(7,17),(8,17),(9,17),(10,17),(11,17)}
obstacle = {(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),(15,0),(16,0),(17,0),(18,0),(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(0,2),(1,2),(2,2),(3,2),(4,2),(14,2),(15,2),(16,2),(17,2),(18,2),(0,3),(1,3),(2,3),(16,3),(17,3),(18,3),(0,4),(1,4),(2,4),(16,4),(17,4),(18,4),(0,5),(1,5),(17,5),(18,5),(0,6),(1,6),(17,6),(18,6),(0,7),(18,7),(0,8),(18,8),(0,9),(18,9),(0,10),(18,10),(0,11),(18,11),(0,12),(1,12),(17,12),(18,12),(0,13),(1,13),(17,13),(18,13),(0,14),(1,14),(2,14),(16,14),(17,14),(18,14),(0,15),(1,15),(2,15),(16,15),(17,15),(18,15),(0,16),(1,16),(2,16),(3,16),(4,16),(14,16),(15,16),(16,16),(17,16),(18,16),(0,17),(1,17),(2,17),(3,17),(4,17),(5,17),(6,17),(12,17),(13,17),(14,17),(15,17),(16,17),(17,17),(18,17),(0,18),(1,18),(2,18),(3,18),(4,18),(5,18),(6,18),(7,18),(8,18),(9,18),(10,18),(11,18),(12,18),(13,18),(14,18),(15,18),(16,18),(17,18),(18,18)}
centre = rg.CENTER_POINT
move_count = 0

def adjacent( (x,y) ):
    return set([(x + dx, y + dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0))])

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
    for row in field:
        for i, x in enumerate(row):
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


def coord_to_cell( coord ):
    return coord[0] + coord[1] * 19

def cell_to_coord( cell ):
    x = cell % 19
    y = int(cell / 19)
    return (x,y)

def pick_optimal(members):

    # option_array = [[x for x in range(len(options))] for options in [x[1] for x in members]]
    option_array = [[coord_to_cell(coord) for coord in options] for options in [x[1] for x in members]]
    scores = []
    for member, cells in zip(members, option_array):
        lookup = {}
        for index, cell in enumerate(cells):
            lookup[cell] = member[2][index]
        scores.append(lookup)

    top_score = -100
    top_combo = None
    for combo in product(*option_array):
        score = sum([scores[member][cell] for member, cell in enumerate(combo)])
        if score > top_score:
            top_combo = combo
            top_score = score

    if top_combo:
        return [cell_to_coord(x) for x in top_combo]
    else:
        return None

def pick_best(members):
    top_score = -9999
    scores = {}
    num_members = len(members)
    options = []
    result = None

    for member in members:
        start = coord_to_cell(member[0])
        moves = [(start,coord_to_cell(end)) for end in member[1]]
        for index, move in enumerate(moves):
            scores[move] = member[2][index]
        options.append(moves)

    for possibility in itertools.product(*options):
    	ends = [y for x,y in possibility]
        if len(set([y for x,y in possibility])) != num_members:
            continue
        if set(possibility) & set([(y,x) for x,y in possibility if x != y]):
            continue

        score = sum([scores[move] for move in possibility])
        if score > top_score:
            result, top_score = possibility, score

    if result is None:
        print('')
        print('NO RESULT from picking best')
        print(members)
        print('')
        print(options)
        return None
    else:
        return [(cell_to_coord(y)) for x,y in result]





def num_combinations(possibility_array):
    num_combinations = 1
    for member in possibility_array:
        num_combinations *= len(member[1])
    return num_combinations


def movement_gains(bot_action, field):
    sx, sy = bot_action[0]
    moves = bot_action[1]
    return [(field[ex][ey] - field[sx][sy]) for (ex,ey) in moves]

def make_reduction(system, move_granted):
    # TO HERE!!!!!!!!


def reduce_system(reduced):
    # Find the square with the most heat
    cells = {}
    for member in reduced:
        for cell in member[1]:
            if cell in cells:
                cells[cell] += 1
            else:
                cells[cell] = 1

    print('cells')
    print(cells)

    hot_cell = max(cells.iteritems(), key=operator.itemgetter(1))[0]
    print('hot cell')
    print(hot_cell)

    candidates = {}
    for index, member in enumerate(reduced):
        if hot_cell in member[1]:
            score = member[2][member[1].index(hot_cell)]
            candidates[member[0]] = score

    print('candidates')
    print(candidates)

    # If this square is the only available move for a candidate,
    # grant it to that candidate
    best_candidate = [x[0] for x in reduced if x[0] in candidates and len(x[1]) == 1]
    print('candidate that NEEDS this move')
    print(best_candidate)

    # If not best candidate at this point, find the most deserving
    if best_candidate == []:
        print('no necessary candidate, selecting by value')

        # for purge in range(level):
        #     print('Removing default candidate as that caused bad')
        #     print('removing key ' + str(max(candidates.iteritems(), key=operator.itemgetter(1))[0]))
        #     del candidates[max(candidates.iteritems(), key=operator.itemgetter(1))[0]]
        #     print('candidates are now...')
        #     print(candidates)
        max_score = -9999
        for candidate in candidates.iteritems():
            if candidate[1] > max_score:
                max_score = candidate[1]
        print('max score = ' + str(max_score))

        best_candidates = []
        for candidate in candidates.iteritems():
            if candidate[1] == max_score:
                best_candidates.append(candidate[0])
        print('best candidates = ' + str(best_candidates))

        # Filter out candidates who would cause a bot to be left with no moves
        for candidate in best_candidates[:]:
            for member in reduced:
                if member[0] == hot_cell:
                    if set(member[1]) - set([hot_cell, candidate]) == set():
                        print('detected and removed bad candidate' + str(candidate))
                        best_candidates.remove(candidate)
                else:
                    # Test to see if bad outcomes occur


        best_candidate = random.choice(best_candidates)
        print('best_candidate (chosen at random)')
        print(best_candidate)
    elif len(best_candidate) > 1:
        print('SHIT')
        return None
    else:
        best_candidate = best_candidate[0]

    print('orig')
    for member in reduced:
        print(member)

    # MOVE FROM HERE!!!!!!!!
    reduced2 = reduced[:]
    for member in reduced2:
        if member[0] == best_candidate:
            # Make this move the only option for the winner
            member[1] = [hot_cell]
            member[2] = [candidates[member[0]]]
        else:
            if member[0] == hot_cell:
                print('The winner is moving into this bots place')
                print(member)
                # Remove bot swap as an option for target square
                try:
                    swap_index = member[1].index(best_candidate)
                    print('A swap condidion exists')
                except:
                    swap_index = None
                if swap_index:
                    del member[1][swap_index]
                    del member[2][swap_index]
            if hot_cell in member[1]:
                # Remove this options from other bots move options
                member[2].remove(member[2][member[1].index(hot_cell)])
                member[1].remove(hot_cell)



    print('')
    print('red')
    for member in reduced2:
        print(member)

    return reduced2



def decide_actions(movements,recursed=False):
    feasable_size = 1000
    print('')
    print('Entered decide actions')

    if recursed == True:
        print('Called from recursed with...')
        print('movements passed...')
        for movement in movements:
            print(movement)


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

        num_options = num_combinations(reduced)

        if num_options == 1:
            print('single opt')
            for index, member in enumerate(movement_group):
                final_movements[member[0]] = reduced[index][1][0]
        elif num_options < feasable_size:
            top_combo = pick_best(reduced)
            if top_combo is None:
                return None
            for index, member in enumerate(movement_group):
                final_movements[member[0]] = top_combo[index]
        else:
            print('large set')
            # Simplify and recurse
            reduced2 = reduce_system(reduced)
            while num_combinations(reduced2) > feasable_size:
                print('num combinations = ' + str(num_combinations(reduced2)))
                reduced2 = reduce_system(reduced2)
                print('reduced to = ' + str(num_combinations(reduced2)))
                print('')

            breakdown = decide_actions(reduced2,True)

            # Recurse with simplifed system
            # breakdown = decide_actions(reduced2,True)

            print('JOINED BACK')
            for item in breakdown:
                print('adding ' + str(breakdown[item]) + ' -> ' + str(item))
                final_movements[item] = breakdown[item]

    print('RETURNING')
    print('with...')
    for move in final_movements:
        print(str(move) + ' -> ' + str(final_movements[move]))
    print('')

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


            for bot in decided_movements:
                print('bot ' + str(bot) + ' moves to ' + str(decided_movements[bot]))


        print('allocating movment for ' + str(self.location))
        move = decided_movements[self.location]

        if move == self.location:
            return ['guard', move]
        else:
            return ['move', move]



