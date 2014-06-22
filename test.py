import os
import subprocess
import numpy

out = subprocess.check_output(["rgrun", "gypsy.py", "simplebot.py", "-H", "-c", "50"]).decode()

runs = []
lines = out.split("\n")
for line in list(lines):
    if str(line).find('] - seed:') != -1:
        parts = line.split()
        myscore = int(parts[0][1:-1])
        total = myscore + int(parts[1][:-1])
        frac = float(myscore) / float(total)
        runs.append(frac)
a = numpy.array(runs)

print("Mean kills: " + str(int(a.mean() * 100)) + "%")
print("Variance:   " + str(int(a.var()) * 100) + "%")
