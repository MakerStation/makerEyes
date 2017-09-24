import math
import numpy

def distance(p0, p1):
    dx = p0[0] - p1[0]
    dy = p0[1] - p1[1]
    dz = p0[2] - p1[2]

    return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2) + math.pow(dz, 2))


def normalizeVector(vector):
    return vector / numpy.sqrt(numpy.dot(vector, vector))

def vectorMagnitude(vector):
    return numpy.sqrt(numpy.dot(vector, vector))


def normalizedTrilateration(d, i, j, radii):
    #   https://en.wikipedia.org/wiki/Trilateration
    d2 = math.pow(d, 2)
    i2 = math.pow(i, 2)
    j2 = math.pow(j, 2)

    r1 = radii[0]
    r2 = radii[1]
    r3 = radii[2]

    r12 = math.pow(r1, 2)
    r22 = math.pow(r2, 2)
    r32 = math.pow(r3, 2)

    x = (r12 - r22 + d2) / (d * 2)
    y = (r12 -r32 + i2 + j2) / (2 * j) - (i / j) * x

#   print("sqrt of ", (r12 - math.pow(x, 2) - math.pow(y, 2)))
    z = math.sqrt(abs(r12 - math.pow(x, 2) - math.pow(y, 2)))

    return (x, y, z)
