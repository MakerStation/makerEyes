# Application that will read data from serial port and push values to Socket.py's websocket
import logging
import math
import datetime
import random
import itertools
import time

from socketIO_client import SocketIO, LoggingNamespace

# ================================================================

def sound_speed (temp, p ,rh):

    # temp --> temperature (Degree Celsius)
    # p --> pressure (Pa)
    # rh --> relative humidity (%)

    ######################## Following code from: "http://www.sengpielaudio.com/calculator-airpressure.htm" ##############

    t_kel = 273.15 + temp # Measure ambient temp (in Kelvin)

    # Molecular concentration of water vapour calculated from Rh using Giacomos method by Davis(1991) as implemented in DTU report 11b - 1997
    ENH = math.pi * math.pow(10,-8) * p + 1.00062 + math.pow(temp, 2) * 5.6 * math.pow(10, -7)

    # These commented lines correspond to values used in Cramer (Appendix)
    PSV1 = math.pow(t_kel, 2) * 1.2378847 * math.pow(10, -5) - 1.9121316 * math.pow(10, -2) * t_kel
    PSV2 = 33.93711047 - 6.3431645 * math.pow(10, 3) / t_kel
    PSV = math.pow(math.e, PSV1) * math.pow(math.e, PSV2)

    H = rh * ENH * PSV / p

    Xw = H/100.0

    Xc = 400.0 * math.pow(10, -6)

    # Speed calculated using the method of Cramer from JASA vol 93 p. 2510
    C1 = 0.603055 * temp + 331.5024 - math.pow(temp, 2) * 5.28 * math.pow(10, -4) + (0.1495874 * temp + 51.471935 - math.pow(temp, 2) * 7.82 * math.pow(10, -4)) * Xw
    C2 = (-1.82 * math.pow(10, -7) + 3.73 * math.pow(10, -8) * temp - math.pow(temp, 2) * 2.93 * math.pow(10, -10)) * p + (-85.20931 - 0.228525 * temp + math.pow(temp, 2) * 5.91 * math.pow(10, -5)) * Xc
    C3 = math.pow(Xw, 2) * 2.835149 - math.pow(p, 2) * 2.15 * math.pow(10, -13) + math.pow(Xc, 2) * 29.179762 + 4.86 * math.pow(10, -4) * Xw * p * Xc
    c = round(C1 + C2 - C3, 2)

    ####################################################################################################################

    return (c / 10e6); # (m/µs)

def distance (t, c):

    # t --> tuple with the time from the sensors (s)

    d = (c * t[0], c * t[1], c * t[2])
    return d;

def coordinate (l, d):
    # l --> tuple with the distances between the sensors
    # d --> tuple with the distance of the object from the three sensors
    xc = (math.pow(l[0], 2) + math.pow(d[0], 2) - math.pow(d[2], 2)) / (2 * l[0])
    zc = (math.pow(l[1], 2) + math.pow(d[0], 2) - math.pow(d[1], 2)) / (2 * l[1])
    yc = math.sqrt(math.pow(d[0], 2) - math.pow(zc, 2) - math.pow(xc, 2))
    coordinates = (round(xc, 3), round(yc, 3), round(zc, 3))
    return coordinates;

    # l[0] = distance of the first sensor from the middle one
    # l[1] = distance of the second sensor form the middle one
    # d[0] = distance of the object from the middle sensor
    # d[1] = distance of the object from the second sensor (l2)
    # d[2] = distance of the object from the first sensor (l1)

# ================================================================

def aDistances (t):
    speed = 1
    angle = t * speed
    x = 0 + 0.3 * math.sin(angle / 180 * math.pi)
    y = 1.3 - 0.3 * math.cos(angle / 180 * math.pi)
    z = 0
    dist0 = math.sqrt(math.pow((0 - x), 2) + math.pow((0 - y), 2) + math.pow((0 - z), 2))
    dist1 = math.sqrt(math.pow((0.4 - x), 2) +math.pow((0 - y), 2) + math.pow((0 - z), 2) )
    dist2 = math.sqrt(math.pow((0 - x), 2)  + math.pow((0.4 - y), 2) + math.pow((0 - z), 2) )
    return (dist0, dist1, dist2);

def bDistances (t):
    speed = 1
    angle = t * speed
    x = 0 + 0.3 * math.cos(angle / 180 * math.pi)
    y = 1.3
    z = 0 + 0.3 * math.sin(angle / 180 * math.pi)
    dist0 = math.sqrt(math.pow((0 - x), 2) + math.pow((0 - y), 2) + math.pow((0 - z), 2))
    dist1 = math.sqrt(math.pow((0.4 - x), 2) + math.pow((0 - y), 2) + math.pow((0 - z), 2))
    dist2 = math.sqrt(math.pow((0 - x), 2) + math.pow((0.4 - y), 2) + math.pow((0 - z), 2))
    return (dist0, dist1, dist2);

def cDistances (t):
    speed = 1
    angle = t * speed
    x = 0
    y = 1.3 - 0.3 * math.cos(angle / 180 * math.pi)
    z = 0 + 0.3 * math.sin(angle / 180 * math.pi)
    dist0 = math.sqrt(math.pow((0 - x), 2) + math.pow((0 - y), 2) + math.pow((0 - z), 2))
    dist1 = math.sqrt(math.pow((0.4 - x), 2) + math.pow((0 - y), 2) + math.pow((0 - z), 2))
    dist2 = math.sqrt(math.pow((0 - x), 2) + math.pow((0.4 - y), 2) + math.pow((0 - z), 2))
    return (dist0, dist1, dist2);


def aPosition (t, soundSpeed):
    d = aDistances(t)
    return (d[0]/soundSpeed, d[1]/soundSpeed, d[2]/soundSpeed);

def bPosition (t, soundSpeed):
    d = bDistances(t)
    return (d[0] / soundSpeed, d[1] / soundSpeed, d[2] / soundSpeed);

def cPosition (t, soundSpeed):
    d = cDistances(t)
    return (d[0] / soundSpeed, d[1] / soundSpeed, d[2] / soundSpeed);

if __name__ == '__main__':
    logging.getLogger('socketIO-client').setLevel(logging.WARN)
    logging.basicConfig()
    #
    socketIO = SocketIO('localhost', 8085)
    chat = socketIO.define(LoggingNamespace, '/dataLogger')
    #
    # min_dist_time = 15000  # expressed in µs
    # max_dist_time = 25000  # expressed in µs
    #

    #
    # sensor = (0.4, 0.4)
    # print(soundSpeed)
    # startTime = datetime.datetime.now();

#     objects = ["A", "B", "C"]
#     for currentObject in itertools.cycle(objects):
#         controllerMessage = (
#             currentObject,
#             datetime.datetime.now() - startTime,
#             random.randint(min_dist_time, max_dist_time),
#             random.randint(min_dist_time, max_dist_time),
#             random.randint(min_dist_time, max_dist_time)
#         )
#
#         objectID = controllerMessage[0]
#         deltaTime = controllerMessage[1]
#         deltaTimes = (
#             controllerMessage[2],
#             controllerMessage[3],
#             controllerMessage[4]
#         )
#
# #       print("deltaTimes", deltaTimes)
# #       print("deltaDistances", distance(deltaTimes, soundSpeed))
#         (x, y, z) = coordinate(sensor, distance(deltaTimes, soundSpeed))
# #       print("position", (x, y, z))
#         chat.emit("broadcast", {
#             'object': objectID,
#             'timestamp': str(startTime + deltaTime),
#             'x': x,
#             'y': y,
#             'z': z
#         })
#         socketIO.wait(seconds=1)

    objectPathFunctions = {
        'A': aPosition,
        'B': bPosition,
        'C': cPosition
    }

    temperature = 20;
    pressure = 101000;
    relativeHumidity = 50;

    soundSpeed = sound_speed(temperature, pressure, relativeHumidity)
    startTime = datetime.datetime.now();

    for i in itertools.cycle(range(360)):
        for objectID, objectPathFunction in objectPathFunctions.items():
            position = objectPathFunction(i, soundSpeed)
            message = (
                objectID,
                datetime.datetime.now() - startTime,
                position[0],
                position[1],
                position[2]
            )
            chat.emit("broadcast", {
                'object': message[0],
                'timestamp': message[1],
                'x': ,
                'y': ,
                'z':
            })
            socketIO.wait(seconds=1)
            time.sleep(1/200)
