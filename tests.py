import math

def squares_dist(pos, dist):
    if dist == 0:
        return pos
    else:
        out = []
        px = pos[0]
        py = pos[1]
        for x in range(dist):
            y = dist - x
            out += [(px+x,py+y), (px+y,py-x), (px-x,py-y), (px-y,py+x)]
        return out

# for x in range(5):
#     print(squares_dist((1,1),x))

hp = 32
print(math.ceil(hp/10))
print(int(hp/10))