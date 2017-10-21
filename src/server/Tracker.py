import operator
from functools import partial
import datetime
import numpy
import MathUtility
import pprint

def createTrackerContext(sensorPositions):
    #   https://en.wikipedia.org/wiki/Trilateration#Preliminary_and_final_computations

    P1 = numpy.asarray(sensorPositions[0])
    P2 = numpy.asarray(sensorPositions[1])
    P3 = numpy.asarray(sensorPositions[2])

    d = MathUtility.vectorMagnitude(P2 - P1)

    ex = MathUtility.normalizeVector(P2 - P1)
    i = numpy.dot(ex, (P3 - P1))

    ey = MathUtility.normalizeVector(P3 - P1 - i * ex)
    j = numpy.dot(ey, P3 - P1)

    ez = numpy.cross(ex, ey)

    context = {
        'P1': P1,
        'P2': P2,
        'P3': P3,

        'ex': ex,
        'ey': ey,
        'ez': ez,

        'd':  d,
        'i':  i,
        'j':  j
    }
#   print("tracker context", pprint.pprint(context, indent=4))

    return context

class Tracker:

    def __init__(self, sensorPositions, soundSpeed, startTime):
        self.sensorPositions = sensorPositions
        self.soundSpeed = soundSpeed
        self.startTime = startTime

        self.context = createTrackerContext(sensorPositions)

    def dataLoggerMessage(self, controllerMessage):
        deltaTimes = (controllerMessage[2], controllerMessage[3], controllerMessage[4])
        distances = tuple(map(partial(operator.mul, self.soundSpeed), deltaTimes))
        normalizedPosition = MathUtility.normalizedTrilateration(self.context['d'], self.context['i'], self.context['j'], distances)
        position = tuple(self.context['P1'] + normalizedPosition[0] * self.context['ex'] + normalizedPosition[1] * self.context['ey'] + normalizedPosition[2] * self.context['ez'])

        return {
            'object': controllerMessage[0],
            'timestamp': str(self.startTime + datetime.timedelta(microseconds=controllerMessage[1])),
            'x': position[0],
            'y': position[1],
            'z': position[2]
        }
