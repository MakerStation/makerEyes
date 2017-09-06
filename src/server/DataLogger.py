# Application that will read data from serial port and push values to Socket.py's websocket
import logging
import math
import datetime
import random
import itertools

from socketIO_client import SocketIO, LoggingNamespace

def sound_speed (temp, p ,rh):

    # temp --> temperature (Degree Celsius)
    # p --> pressure (Pa)
    # rh --> relative humidity (%)

    ######################## Following code from: "http://www.sengpielaudio.com/calculator-airpressure.htm" ##############

    t_kel = 273.15 + temp; # Measure ambient temp (in Kelvin)

    # Molecular concentration of water vapour calculated from Rh using Giacomos method by Davis(1991) as implemented in DTU report 11b - 1997
    ENH = math.pi * math.pow(10,-8)* p + 1.00062 + math.pow(temp, 2) * 5.6 * math.pow(10, -7);

    # These commented lines correspond to values used in Cramer (Appendix)
    # PSV1 = sqr(T_kel)*1.2811805*Math.pow(10,-5)-1.9509874*Math.pow(10,-2)*T_kel
    # PSV2 = 34.04926034-6.3536311*Math.pow(10,3)/T_kel
    PSV1 = math.pow(t_kel, 2) * 1.2378847 * math.pow(10, -5) - 1.9121316 * math.pow(10, -2) * t_kel
    PSV2 = 33.93711047 - 6.3431645 * math.pow(10, 3) / t_kel
    PSV = math.pow(math.e, PSV1)* math.pow(math.e, PSV2)

    H = rh * ENH * PSV / p

    Xw = H/100.0

    # Xc = 314.0*Math.pow(10,-6)
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
    xc = (math.pow(l[0], 2) + d[0] - d[2]) / (2 * l[0])
    zc = (math.pow(l[1], 2) + d[0] - d[1]) / (2 * l[1])
    yc = math.sqrt(d[0] - math.pow(zc, 2) - math.pow(xc, 2))
    coordinates = (xc, yc, zc)
    return coordinates;

    # l[0] = distance of the first sensor from the middle one
    # l[1] = distance of the second sensor form the middle one
    # d[0] = distance of the object from the middle sensor ^ 2
    # d[1] = distance of the object from the second sensor (l2) ^ 2
    # d[2] = distance of the object from the first sensor (l1 ) ^ 2

if __name__ == '__main__':
    logging.getLogger('socketIO-client').setLevel(logging.WARN)
    logging.basicConfig()

    socketIO = SocketIO('localhost', 8085)
    chat = socketIO.define(LoggingNamespace, '/dataLogger')

    min_dist_time = 15000  # expressed in µs
    max_dist_time = 25000  # expressed in µs

    temperature = 20;
    pressure = 101000;
    relativeHumidity = 50;

    sensor = (0.4, 0.4)
    soundSpeed = sound_speed(temperature, pressure, relativeHumidity)
    print(soundSpeed)
    startTime = datetime.datetime.now();

    controllerObjectID = "A"

    objects = ["A", "B", "C"]
    for currentObject in itertools.cycle(objects):
        controllerMessage = (
            currentObject,
            datetime.datetime.now() - startTime,
            random.randint(min_dist_time, max_dist_time),
            random.randint(min_dist_time, max_dist_time),
            random.randint(min_dist_time, max_dist_time)
        )

        objectID = controllerMessage[0]
        deltaTime = controllerMessage[1]
        deltaTimes = (
            controllerMessage[2],
            controllerMessage[3],
            controllerMessage[4]
        )

#       print("deltaTimes", deltaTimes)
#       print("deltaDistances", distance(deltaTimes, soundSpeed))
        (x, y, z) = coordinate(sensor, distance(deltaTimes, soundSpeed))
#       print("position", (x, y, z))
        chat.emit("broadcast", {
            'object': objectID,
            'timestamp': str(startTime + deltaTime),
            'x': x,
            'y': y,
            'z': z
        })
        socketIO.wait(seconds=1)

