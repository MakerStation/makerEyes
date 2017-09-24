# Application that will read data from serial port and push values to Socket.py's websocket
import logging
import math
import datetime

import operator
import itertools
from functools import partial
import MathUtility

from socketIO_client import SocketIO, LoggingNamespace
from Tracker import Tracker

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

# def distance (t, c):
#    # t --> tuple with the time from the sensors (s)
#    d = (c * t[0], c * t[1], c * t[2])
#    return d;

# def coordinate (l, d):
#     # l --> tuple with the distances between the sensors
#     # d --> tuple with the distance of the object from the three sensors
#     xc = (math.pow(l[0], 2) + math.pow(d[0], 2) - math.pow(d[2], 2)) / (2 * l[0])
#     zc = (math.pow(l[1], 2) + math.pow(d[0], 2) - math.pow(d[1], 2)) / (2 * l[1])
#     yc = math.sqrt(math.pow(d[0], 2) - math.pow(zc, 2) - math.pow(xc, 2))
#     coordinates = (round(xc, 3), round(yc, 3), round(zc, 3))
#     return coordinates;
#
#     # l[0] = distance of the first sensor from the middle one
#     # l[1] = distance of the second sensor form the middle one
#     # d[0] = distance of the object from the middle sensor
#     # d[1] = distance of the object from the second sensor (l2)
#     # d[2] = distance of the object from the first sensor (l1)

# ================================================================

def aPosition(alpha):
    speed = 1
    angle = alpha * speed
    x = 0.0 + 0.3 * math.sin(math.radians(angle))
    y = 0.0 - 0.3 * math.cos(math.radians(angle))
    z = 1.0

    return (x, y, z)

def bPosition(alpha):
    speed = 1
    angle = alpha * speed
    x = 0.0 + 0.3 * math.cos(math.radians(angle))
    y = 0.0
    z = 1.3 + 0.3 * math.sin(math.radians(angle))

    return (x, y, z)

def cPosition(alpha):
    speed = 1
    angle = alpha * speed
    x = 0.0
    y = 0.0 - 0.3 * math.cos(math.radians(angle))
    z = 1.3 + 0.3 * math.sin(math.radians(angle))

    return (x, y, z)

def computeControllerMessage(objectID, position, sensor, tick, soundSpeed):
    distances = tuple(map(partial(MathUtility.distance, position), sensor))
    responseTimes = tuple(map(partial(operator.mul, 1 / soundSpeed), distances))

    return (
        objectID,
        tick,
        responseTimes[0],
        responseTimes[1],
        responseTimes[2]
    )

if __name__ == '__main__':
    logging.getLogger('socketIO-client').setLevel(logging.WARN)
    logging.basicConfig()

    socketIO = SocketIO('localhost', 8085)
    chat = socketIO.define(LoggingNamespace, '/dataLogger')

    objectPathFunctions = {
        'A': aPosition,
        'B': bPosition,
        'C': cPosition
    }

    temperature = 20;
    pressure = 101000;
    relativeHumidity = 50;
    soundSpeed = sound_speed(temperature, pressure, relativeHumidity)

    sensorPositions = ((0.0, 0.0, 0.0), (0.4, 0.0, 0.0), (0.0, 0.4, 0.0))
    startTime = datetime.datetime.now();
    tracker = Tracker(sensorPositions, soundSpeed, startTime)

    for alpha in itertools.cycle(range(360)):
        for objectID, objectPathFunction in objectPathFunctions.items():
            print("--- ", objectID, " --------------------------")
            position = objectPathFunction(alpha)
            print("position", position)

            #================================================
            #   Controller scope
            #
            tick = (datetime.datetime.now() - startTime).microseconds
            controllerMessage = computeControllerMessage(objectID, position, sensorPositions, tick, soundSpeed)
#           print("controller message", controllerMessage)
            #================================================
            #   DataLogger scope
            #
            dataLoggerMessage = tracker.dataLoggerMessage(controllerMessage)
            trackedPosition = (dataLoggerMessage['x'], dataLoggerMessage['y'], dataLoggerMessage['z'])
            print("traked position", trackedPosition)
            print("delta", tuple(round(abs(x-y), 10) for x,y in zip(position, trackedPosition)))
            
            chat.emit("broadcast", dataLoggerMessage)
            socketIO.wait(seconds=1/200)
