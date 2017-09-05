# {
#     object: id,
#     timestamp: iso8601 - 2016-06-10t21:42:24.760738,
#     tx: int    ±100.000  1/10 mm ~ 5m
#     ty: int
#     tz: int
#     temp: int 1/10 ˚c
#     hygro: int 0..100 %rh
# }

# simulate controller serial messages to datalogger

# from datasheet (see mail from Luca Poli) distance formula is:
# distance[cm] = pulse_width [µs] / 58
# if pulse_width ≥ 38 ms ==> no obstacle or over range.
# pulse_width may vary from 150µs to 25ms which means:
# Minimum distance ....... 150µs/58 = 2,59cm
# Maximum distance ....... 25000µs/58 = 431,03 cm --> 4,3 m !

import random
import time

#def Controller (min_dist_time = 150, max_dist_time = 250, tShift = 0, tPause = 0.025, moving = False):
min_dist_time = 150  # expressed in µs
max_dist_time = 25000  # expressed in µs
tShift = 0  # Time shift from start acquisition
tPause = 0.025  # Time to wait for simulating ultrasonic sensor acquiring process

moving = True  # Determines when we are simulating static object (False) or moving object (True)

random.seed()  # initialize random number generator

while True:

    tx = random.randint(min_dist_time, max_dist_time)
    ty = random.randint(min_dist_time, max_dist_time)
    tz = random.randint(min_dist_time, max_dist_time)

    print("%.5f\t%d\t%d\t%d" % (tShift, tx, ty, tz))
    #       yield (tShift, tx, ty, tz)
    if moving:
        tPause = random.uniform(0.00150, 0.025)
        time.sleep(tPause)
    else:
        time.sleep(tPause)

    tShift += tPause

# myController = Controller()
# myController.send(None)
#
# while True:
#     myCntrl = list(myController)
#     print (myController)
#     print(myCntrl)
#     for i in myCntrl:
#         print("%.5f\t%d\t%d\t%d" % myCntrl[0], myCntrl[1], myCntrl[2], myCntrl[3])
