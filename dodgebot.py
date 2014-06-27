# Simplebot by ramk13
# Open source bot with really simple rules
# Feel free to use this as the starting point for a bot
# Please give credit if you do though...

# Moves out of spawn, attacks adjacent enemies
# Chases dying enemies, Attacks towards enemies two steps away
# Flees if in danger, and only moves to safe spots
# No two teammates should move into the same square
# Some teammates may move into stationary teammates

# Uses sets instead of lists for bot data structures
# This makes union/intersection a lot easier (credit to WALL-E for this idea)

# Ways to improve:
#   Instead of using pop() to attack in an arbitrary direction, pick intelligently
#   Instead of just moving to the closest enemies move to the closest weak enemies
#   In some cases it's worth moving into an enemies attack to be aggressive
#   Try to trap enemies bots in spawn
#   Allow bots in trouble to move first and push other bots
#       (requires all moves to be decided on the first act call)
#   When fleeing look for the safest direction

import rg
import numpy
import math

turn_number = -1
attack_damage = 10

# set of all spawn locations
spawn = {(7,1),(8,1),(9,1),(10,1),(11,1),(5,2),(6,2),(12,2),(13,2),(3,3),(4,3),(14,3),(15,3),(3,4),(15,4),(2,5),(16,5),(2,6),(16,6),(1,7),(17,7),(1,8),(17,8),(1,9),(17,9),(1,10),(17,10),(1,11),(17,11),(2,12),(16,12),(2,13),(16,13),(3,14),(15,14),(3,15),(4,15),(14,15),(15,15),(5,16),(6,16),(12,16),(13,16),(7,17),(8,17),(9,17),(10,17),(11,17)}
# set of all obstacle locations
obstacle = {(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),(15,0),(16,0),(17,0),(18,0),(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(0,2),(1,2),(2,2),(3,2),(4,2),(14,2),(15,2),(16,2),(17,2),(18,2),(0,3),(1,3),(2,3),(16,3),(17,3),(18,3),(0,4),(1,4),(2,4),(16,4),(17,4),(18,4),(0,5),(1,5),(17,5),(18,5),(0,6),(1,6),(17,6),(18,6),(0,7),(18,7),(0,8),(18,8),(0,9),(18,9),(0,10),(18,10),(0,11),(18,11),(0,12),(1,12),(17,12),(18,12),(0,13),(1,13),(17,13),(18,13),(0,14),(1,14),(2,14),(16,14),(17,14),(18,14),(0,15),(1,15),(2,15),(16,15),(17,15),(18,15),(0,16),(1,16),(2,16),(3,16),(4,16),(14,16),(15,16),(16,16),(17,16),(18,16),(0,17),(1,17),(2,17),(3,17),(4,17),(5,17),(6,17),(12,17),(13,17),(14,17),(15,17),(16,17),(17,17),(18,17),(0,18),(1,18),(2,18),(3,18),(4,18),(5,18),(6,18),(7,18),(8,18),(9,18),(10,18),(11,18),(12,18),(13,18),(14,18),(15,18),(16,18),(17,18),(18,18)}
center = rg.CENTER_POINT
move_count = 0
# danger = [
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]


# function to find the locations around a spot
# removes obstacle locations from output
def around((x,y)):
    offsets = ((0, 1), (1, 0), (0, -1), (-1, 0))
    return set([(x + dx, y + dy) for dx, dy in offsets])-obstacle

# Function to find the closest bot to a specific location by diagonal distance
# Also used to pick the direction closest to the movement goal
def mindist (bots, loc):
    return min(bots,key=lambda x:rg.dist(x, loc))

def within_bounds((x,y)):
    return x > 0 and y > 0 and x < 18 and y < 18 and (x,y) not in obstacle


def danger_at((x,y), dangerfield):
    return dangerfield[x][y]

def safest_adjacent((x,y), dangerfield):
    return min(around((x,y)),key=lambda x:danger_at(x,dangerfield))

# Returns an array of positions that are the given distance away
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
                print()


class Robot:
    def act(self, game):

        dangerfield = numpy.zeros((19,19))      # Where the danger is
        supportfield = numpy.zeros((19,19))     # Where my friends are
        penaltyfield = numpy.zeros((19,19))     # Where it would be stupid to move
        spawnfield = numpy.zeros((19,19))       # Where the spawns happen
        innerfield = numpy.zeros((19,19))       # Slope toward the center
        logicfield = numpy.zeros((19,19))       # Result of combining the others
        mask = numpy.zeros((19,19))             # Where the obsticles are


        # Used to make the code a little more readable
        robots = game.robots

        # Use turn_number to tell if this is the first robot called this turn
        # If so, then clear the list of taken moves
        # The list of taken moves is used to prevent bots from running into each other
        global turn_number, taken_moves, move_count, center
        if game.turn != turn_number:
            turn_number = game.turn
            taken_moves = set()

        # If moving save the location we are moving to
        def moving(loc):
            taken_moves.add(loc)
            return ['move', loc]

        # If staying save the location that we are at
        def staying(act,loc=center):
            taken_moves.add(bot)
            return [act, loc]

        # Function to find bot with the least health
        def minhp (bots):
            return min(bots,key=lambda x:robots[x].hp)


        # Setup basic sets of robots
        me = self.location
        friendlies = set([bot for bot in robots if robots[bot].player_id==self.player_id])

        enemies = set(robots)-friendlies
        adjacent = around(me)


        # adjacent squares with an enemies (enemies is one step away)
        adjacent_enemies = adjacent & enemies

        # adjacent squares with an enemies next to that square
        # excludes square if a teammate is in the square
        # (enemies is two steps away)
        adjacent_enemies2 = set(filter(lambda k:around(k) & enemies, adjacent)) - friendlies

        # set of squares that are safe to move to
        # spawn is bad, and moving into an enemies is bad
        # if an enemies is two steps away it might be attacking towards us
        # excludes teammates to prevent collisions
        safemove = adjacent-adjacent_enemies-adjacent_enemies2-spawn-friendlies-taken_moves
        semisafemove = adjacent-adjacent_enemies-spawn-friendlies-taken_moves
        safemove_withspawn = adjacent-adjacent_enemies-adjacent_enemies2-friendlies-taken_moves

        # Move towards the closest enemies unless leaving spawn or fleeing
        if enemies:
            closest_enemy = mindist(enemies,me)
        else:
            closest_enemy = center


        move = []

        # Map out the danger field from the enemies
        for enemy in enemies:
            enemy_health = robots[enemy].hp
            dangerfield[enemy[0]][enemy[1]] += enemy_health * 2
            for distance in [ x+1 for x in range(int(math.ceil(enemy_health/attack_damage)))]:
                for x,y in squares_dist(enemy, distance):
                    if within_bounds((x,y)):
                        dangerfield[x][y] += int(math.ceil(enemy_health / distance))

        # Map out the support field from friendlies
        for friend in friendlies:
            friend_health = robots[friend].hp
            supportfield[friend[0]][friend[1]] += friend_health * 2
            for distance in [ x+1 for x in range(int(math.ceil(friend_health/attack_damage)))]:
                for x,y in squares_dist(friend, distance):
                    if within_bounds((x,y)):
                        supportfield[x][y] += int(math.ceil(friend_health / distance))

        # Map out the penalty field
        for friend in friendlies:
            penaltyfield[friend[0]][friend[1]] += 100
            for x,y in around(friend):
                penaltyfield[x][y] += 50

        # Map out the spawn field
        for x,y in spawn:
            for a,b in around((x,y)):
                if within_bounds((a,b)):
                    spawnfield[a][b] += 25
        for x,y in spawn:
            spawnfield[x][y] = 100

        # Map out the innerfield
        for distance in range(1,12):
            for x,y in squares_dist(center, distance):
                if within_bounds((x,y)):
                    innerfield[x][y] = distance

        # Map out the mask
        for x,y in obstacle:
            mask[x][y] = 100


        fields = [dangerfield, supportfield, penaltyfield, spawnfield, innerfield]
        weight = [1.0, -1.0, 1.0, 1.0, 1.0]

        # Normalise fields
        for field in fields:
            field /= numpy.max(field)
            field *= 100.0


        for i, field in enumerate(fields):
            logicfield += field * weight[i]
        logicfield += mask

        # Find safest location on the map
        print(numpy.argmin(dangerfield))

        move = moving(safest_adjacent(me, dangerfield))
        
        move_count += 1
        if move_count == (len(friendlies)):
            print('Danger')
            print_field(dangerfield)
            print('Support')
            print_field(supportfield)
            print('Penalty')
            print_field(penaltyfield)
            print('Spawn')
            print_field(spawnfield)
            print('Inner')
            print_field(innerfield)
            print('Mask')
            print_field(mask)
            print()
#            print_field(penaltyfield)
            print('The output field')
            print_field(logicfield)
            move_count = 0



        return move


