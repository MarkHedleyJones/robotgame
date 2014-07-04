import rg
import numpy as np
import math
import random
import itertools
import sys
import time

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
                if ref[1] & item[1]:
                    # Add this bot to he movement group and remove from
                    # the pool
                    group.append(item)
                    pool.remove(item)
            index += 1

        movement_groups.append(group)

    return movement_groups


def movelist_sorted(bot, moves, logicfield):
    moves = [(x,logicfield[x[0]][x[1]]) for x in moves]
    moves.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in moves]


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

def pick_optimal(possibility_array,logicfield):
    top_score = 0
    top_combo = None

    option_array = [[coord_to_cell(coord) for coord in options] for options in possibility_array]

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


class Robot:


    def level4_field(self, members):
        out = newfield()
        for distance in range(0,13):
            for x,y in squares_dist(rg.CENTER_POINT, distance):
                if within_bounds((x,y)):
                    out[x][y] = 12-distance
        return out


    def act(self, game):

        global game_turn, attack_damage, spawn, obstacle, centre, move_count
        global frontlinelogic
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
            movements = [(x,available_options(x)) for x in friendlies]
            movement_groups = group_by_interferrence(movements)

            final_movements = {}

            def num_combinations(possibility_array):
                num_combinations = 1
                for member in reduced:
                    num_combinations *= len(member)
                return num_combinations


            # The movements_group movement decisions have been split
            for movement_group in movement_groups:
                # Turn the moves into ordered lists
                group_movement_possibilities = [movelist_sorted(x[0], list(x[1]),frontlinelogic) for x in movement_group]

                # Settle on isolated best logic
                reduced = group_movement_possibilities

                # Go through each member truncating their list of options
                # to end at with the first option that no other robots
                # have available to them. Remember, options are sorted by benefit.
                for pos in range(5):
                    for i in range(len(group_movement_possibilities)):
                        if pos < len(group_movement_possibilities[i]):
                            test = group_movement_possibilities[i][pos]
                            contest = False
                            for j in range(len(group_movement_possibilities)):
                                if j != i:
                                    if test in group_movement_possibilities[j]:
                                        contest = True
                                        break
                            if not contest:
                                reduced[i] = reduced[i][:pos+1]


                num_options = num_combinations(reduced)

                def a(group, field):
                    sx, sy = group[0]
                    moves = group[1]
                    return [(field[ex][ey] - field[sx][sy]) for (ex,ey) in moves]

                if num_options == 1:
                    top_combo = reduced
                elif num_options < 800000:
                    top_combo = pick_optimal(reduced, frontlinelogic)
                    print('calc')
                else:
                    print('skipped')
                    # Take a shortcut here
                    # while num_combinations(reduced) > 50000:

                    # Recompile the movement group with reduced logic options
                    movement_group = [(x[0],y) for (x,y) in zip(movement_group,reduced)]
                    group_option_gains = [a(x,frontlinelogic) for x in movement_group]
                    group_option_moves = [x for x in movement_group]
                    data = [(x[0],x[1],y) for x,y in zip(group_option_moves,group_option_gains)]
                    while True:
                        # Identify which bot has the most to gain and grant that move
                        #
                        max_gain = 0
                        for member in data:
                            tmp = max(member[2])
                            if tmp > max_gain:
                                max_gain = tmp
                        print(max_gain)
                        print(data)
                        break

                for index, member in enumerate(movement_group):
                    final_movements[member[0]] = top_combo[index]


                for bot in final_movements:
                    print('bot ' + str(bot) + ' moves to ' + str(final_movements[bot]))




        move = best_option(self.location, frontlinelogic)

        if move == self.location:
            return ['guard', move]
        else:
            return ['move', move]



