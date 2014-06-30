import rg
import numpy as np
import math

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

def move_options( (x,y) ):
    return list(adjacent((x,y)) - obstacle) + [(x,y)]


def squares_dist(position, distance):
    if distance == 0:
        return position
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


staticfield = {
    'spawn': np.zeros((19,19)),
    'inner': np.zeros((19,19)),
    'mask':  np.zeros((19,19))
}

history = []

########################################################################
# Create the static fields
########################################################################

# Map out the spawn field
for x,y in spawn:
    for a,b in adjacent((x,y)):
        if within_bounds((a,b)):
            staticfield['spawn'][a][b] += 25

for x,y in spawn:
    staticfield['spawn'][x][y] = 100

staticfield['spawn'] = normalise(staticfield['spawn'])

# Map out the innerfield
for distance in range(1,13):
    for x,y in squares_dist(centre, distance):
        if within_bounds((x,y)):
            staticfield['inner'][x][y] = distance

staticfield['inner'] = normalise(staticfield['inner'])

# Map out the mask
for x,y in obstacle:
    staticfield['mask'][x][y] = 100

def newfield():
    return np.zeros((19,19))


class Robot:

    def act(self, game):

        global game_turn, attack_damage, spawn, obstacle, centre, move_count, staticfield, history
        robots = game.robots

        if game.turn != game_turn:
            game_turn = game.turn
            turn = game_turn - 1

            friendlies = set([bot for bot in robots if robots[bot].player_id==self.player_id])
            enemies = set(robots)-friendlies


            history.append({
                'them_now':  newfield(),
                'us_now':   newfield(),
                'us_next':  newfield(),
            })

            for friend in friendlies:
                x,y = robots[friend].location
                history[turn]['us_now'][x][y] = robots[friend].robot_id


            # Map out the danger field from the enemies
            dangerfield = newfield()
            for enemy in enemies:
                x,y = robots[enemy].location
                history[turn]['them_now'][x][y] = robots[enemy].hp
                dangerfield[x][y] += robots[enemy].hp * 2
                for distance in [ x+1 for x in range(int(math.ceil(robots[enemy].hp/attack_damage)))]:
                    for pos in squares_dist(enemy, distance):
                        if within_bounds(pos):
                            dangerfield[pos[0]][pos[1]] += int(math.ceil(robots[enemy].hp / distance))

            dangerfield = normalise(dangerfield)

            fields = [dangerfield, staticfield['spawn'], staticfield['inner']]
            weight = [0.26, 0.1 * (turn % 10), 0.6]

            logicfield_move = newfield()
            for weight, field in zip(weight,fields):
                logicfield_move += field * weight

            # Normalise logicfield
            logicfield_move = normalise(logicfield_move)
            logicfield_move += staticfield['mask']

            possibilities = []
            for friend in friendlies:
                possibilities.append([(pos,logicfield_move[pos[0]][pos[1]]) for pos in move_options(friend)])

            print(possibilities)

            # Write a recursive function to find ways of choosing 1 from each subarray to minimise x


            # Implement
            # * Movement logic
            # * Attack logic
            # * Guard logic
            # * Suicide logic
            # Assess every option and act accordingly


        return ['guard', centre]


