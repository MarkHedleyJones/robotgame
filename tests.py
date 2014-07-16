#! /usr/bin/python2.7
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
        level += 1
        if len(element) > 1:
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

start = (12, 9)
end = (10, 10)
available = [
    (12, 8),
    (12, 9),
    (12, 10),
    (11, 8),
    (11, 9),
    (11, 10),
    (10, 7),
    (10, 8),
    (10, 9),
    (10, 10),
    (10, 11)]
print(find_paths(start, end, available))

start = (5, 9)
end = (9, 7)
available = [
    (6, 9),
    (7, 8),
    (7, 9),
    (7, 10),
    (8, 7),
    (8, 8),
    (8, 9),
    (8, 10),
    (8, 11),
    (9, 7),
    (9, 8),
    (9, 9),
    (9, 10),
    (9, 11),
    (12, 8),
    (12, 9),
    (12, 10),
    (11, 8),
    (11, 9),
    (11, 10),
    (10, 7),
    (10, 8),
    (10, 9),
    (10, 10),
    (10, 11)]

print(find_paths(start, end, available))