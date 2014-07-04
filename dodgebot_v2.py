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
import numpy as np
import math
import pdb
#import matplotlib.pyplot as plt

turn_number = -1
attack_damage = 10

filenames = [] # For plotting

# set of all spawn locations
spawn = {(7,1),(8,1),(9,1),(10,1),(11,1),(5,2),(6,2),(12,2),(13,2),(3,3),(4,3),(14,3),(15,3),(3,4),(15,4),(2,5),(16,5),(2,6),(16,6),(1,7),(17,7),(1,8),(17,8),(1,9),(17,9),(1,10),(17,10),(1,11),(17,11),(2,12),(16,12),(2,13),(16,13),(3,14),(15,14),(3,15),(4,15),(14,15),(15,15),(5,16),(6,16),(12,16),(13,16),(7,17),(8,17),(9,17),(10,17),(11,17)}
# set of all obstacle locations
obstacle = {(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),(15,0),(16,0),(17,0),(18,0),(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(0,2),(1,2),(2,2),(3,2),(4,2),(14,2),(15,2),(16,2),(17,2),(18,2),(0,3),(1,3),(2,3),(16,3),(17,3),(18,3),(0,4),(1,4),(2,4),(16,4),(17,4),(18,4),(0,5),(1,5),(17,5),(18,5),(0,6),(1,6),(17,6),(18,6),(0,7),(18,7),(0,8),(18,8),(0,9),(18,9),(0,10),(18,10),(0,11),(18,11),(0,12),(1,12),(17,12),(18,12),(0,13),(1,13),(17,13),(18,13),(0,14),(1,14),(2,14),(16,14),(17,14),(18,14),(0,15),(1,15),(2,15),(16,15),(17,15),(18,15),(0,16),(1,16),(2,16),(3,16),(4,16),(14,16),(15,16),(16,16),(17,16),(18,16),(0,17),(1,17),(2,17),(3,17),(4,17),(5,17),(6,17),(12,17),(13,17),(14,17),(15,17),(16,17),(17,17),(18,17),(0,18),(1,18),(2,18),(3,18),(4,18),(5,18),(6,18),(7,18),(8,18),(9,18),(10,18),(11,18),(12,18),(13,18),(14,18),(15,18),(16,18),(17,18),(18,18)}
center = rg.CENTER_POINT
move_count = 0

movements = np.zeros((19,19))
logicfield = np.zeros((19,19))

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


def adjacent((x,y)):
    return set([(x + dx, y + dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0))])

# function to find the locations around a spot
# removes obstacle locations from output
def around((x,y)):
    return adjacent((x,y))-obstacle

# Function to find the closest bot to a specific location by diagonal distance
# Also used to pick the direction closest to the movement goal
def mindist (bots, loc):
    return min(bots,key=lambda x:rg.dist(x, loc))

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


def move_options( (x,y), logicfield, movements):
    available = around( (x,y) )
    free = []
    for option in available:
        status = movements[option[0]][option[1]]
        if status <= 1:
            free.append({
                'pos': option,
                'logic': logicfield[option[0]][option[1]],
                'status': 'free' if status == 0 else 'pending'
            })

    return free

def safest_adjacent((x,y), logicfield, movements):
    options = around( (x,y) )
    free = []
    for option in options:
        status = movements[option[0]][option[1]]
        if status == 0:
            free.append(option)
        elif status == 2:
            pass
    options = free
    if options:
        return min(options, key=lambda (x,y): logicfield[x][y])
    else:
        return None
#    return min(around((x,y)),key=lambda x:danger_at(x,dangerfield))

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

#def plot_field(field,filename):
#    plt.clf()
#    plt.imshow(field,interpolation='nearest')
#    plt.savefig(filename,format='pdf')


def combine_pdfs(filenames, outputFilename):
    from pyPdf import PdfFileWriter, PdfFileReader
    """
    Combines multiple pdf files into a single document
    """
    print "Starting pdf export"
    print filenames
    output = PdfFileWriter()
    files = []
    inputStreams = []
    for filename in filenames:
        files.append(file(filename, "rb"))
        num = len(files) - 1
        inputStreams.append(PdfFileReader(files[num]))
        output.addPage(inputStreams[num].getPage(0))
    outputStream = file(outputFilename, "wb")
    output.write(outputStream)
    outputStream.close()
    for filename in files:
        filename.close()

def fieldval((x,y), field):
    return field[x][y]

def locate_min(field):
    min_element = np.argmin(field)
    return (min_element % len(field[0]), min_element / len(field[0]))




class Robot:
    def act(self, game):



        # Used to make the code a little more readable
        robots = game.robots

        # Use turn_number to tell if this is the first robot called this turn
        # If so, then clear the list of taken moves
        # The list of taken moves is used to prevent bots from running into each other
        global turn_number, taken_moves, move_count, center, logicfield, movements

        if game.turn != turn_number:
            turn_number = game.turn
            taken_moves = set()

        # If moving save the location we are moving to
        def moving(me,to):
            taken_moves.add(to)
            movements[me[0]][me[1]] = 0
            movements[to[0]][to[1]] = 2
            return ['move', to]

        # If staying save the location that we are at
        def staying(act,loc=center):
            movements[bot[0]][bot[1]] = 2
            taken_moves.add(bot)
            return [act, loc]

        # Function to find bot with the least health
        def minhp (bots):
            return min(bots,key=lambda x:robots[x].hp)


        # Setup basic sets of robots
        me = self.location
        friendlies = set([bot for bot in robots if robots[bot].player_id==self.player_id])
        enemies = set(robots)-friendlies

        move = []

        if taken_moves == set():

            for friend in friendlies:
                movements[friend[0]][friend[1]] = 1

            dangerfield = np.zeros((19,19))      # Where the danger is
            supportfield = np.zeros((19,19))     # Where my friends are
            penaltyfield = np.zeros((19,19))     # Where it would be stupid to move
            spawnfield = np.zeros((19,19))       # Where the spawns happen
            innerfield = np.zeros((19,19))       # Slope toward the center
            logicfield = np.zeros((19,19))       # Result of combining the others
            mask = np.zeros((19,19))             # Where the obsticles are


            # Map out the danger field from the enemies
            for y,x in enemies:
                dangerfield[x][y] = 100
                for pos in squares_dist((x,y),1):
                    if within_bounds(pos):
                        dangerfield[pos[1]][pos[0]] = 100
                for pos in squares_dist((x,y),2):
                    if within_bounds(pos):
                        dangerfield[pos[1]][pos[0]] = 50
                # for x,y in adjacent(enemy):
                #     dangerfield[x][y] = 100
                # for x,y in squares_dist(enemy,2):
                #     if within_bounds((x,y)):
                #         dangerfield[x][y] = 50

            # Map out the spawn field
            for x,y in spawn:
                for a,b in around((x,y)):
                    if within_bounds((a,b)):
                        spawnfield[a][b] += 25
            for x,y in spawn:
                spawnfield[x][y] = 100

            # Map out the innerfield
            for distance in range(1,13):
                for x,y in squares_dist(center, distance):
                    if within_bounds((x,y)):
                        innerfield[x][y] = distance

            # Map out the mask
            for x,y in obstacle:
                mask[x][y] = 100


            fields = [dangerfield, spawnfield, innerfield]
            weight = [1.0, 0.333, 0.8]

            # Normalise fields
            for field in fields:
                field = normalise(field)

            if turn_number == 1:
                print_field(dangerfield + (0.01*mask))

            for i, field in enumerate(fields):
                logicfield += field * weight[i]

            # Normalise logicfield
            logicfield = normalise(logicfield)
            logicfield += mask

            #logicfield = blur(logicfield)
            #logicfield += mask
#            filename = 'plot' + str(turn_number) + '.pdf'
#            filenames.append(filename)
#            plot_field(logicfield,filename)


        move = []

        options = move_options(me, logicfield, movements)
        options = sorted(options, key=lambda x: x['logic'])
        for option in options:
            if option['status'] == 'free':
                move = moving(me, option['pos'])
                break;

        if move == []:
            return ['guard', center]


#        print(options)

#        safest_move = safest_adjacent(me, logicfield, movements)
#        move_gain = 0
#        if safest_move is None:
#            move_gain = 0.0
#            instinct = 'stay'
#        else:
#            move_gain = fieldval(me, logicfield)-fieldval(safest_move, logicfield)
#            instinct = 'move'
#
#        if instinct == 'move':
#            move = moving(me,safest_move)
#        else:
#            move = staying('guard')
#
#        print_field(movements)

#        if safest_move is None:
#            safest_move = list(around(me))[0]
#
#        move = moving(safest_move)
#
#        gain_move = fieldval(me, logicfield)-fieldval(safest_move, logicfield)
#
#        if gain_move <= 0:
#            move = staying('guard')
#        else:
#            move = moving(safest_move)
#
#        next_pos = move[1]
#        next_adj = set(around(next_pos)) - set(me)
#        if next_adj & enemies:
#            move = staying('attack', next_pos)

#        imminent_danger = set(around(me)) & enemies

#        if imminent_danger:
#            move_danger = set(around(next_pos)) & enemies
#            if move_danger:
#                move = staying('attack', imminent_danger.pop())

#        move_count += 1
#        if move_count == (len(friendlies)):
#            #print('Danger')
#            #print_field(dangerfield)
#            #print('Support')
#            #print_field(supportfield)
#            #print('Penalty')
#            #print_field(penaltyfield)
#            #print('Spawn')
#            #print_field(spawnfield)
#            #print('Inner')
#            #print_field(innerfield)
#            #print('Mask')
#            #print_field(mask)
#            #print('The output field')
#            #print_field(logicfield)
#            #filename = 'plot' + str(turn_number) + '.pdf'
#            #filenames.append(filename)
#            #plot_field(logicfield, filename)
#            #move_count = 0
#            #np.savetxt('field.txt', logicfield, fmt='%0.0d',delimiter=',')
#            #print(logicfield)
#            pass
#        if turn_number == 99:
#            combine_pdfs(filenames,'out.pdf')

        return move


