# Application that will read data from serial port and push values to Socket.py's websocket
import random
import string
import logging
import math

from socketIO_client import SocketIO, LoggingNamespace

#def distance ():

def coordinate (l1, l2, d1, d2, d3):
    xc = (math.pow(l1, 2) + d1 - d3) / (2 * l1)
    zc = (math.pow(l2, 2) + d1 - d2) / (2 * l2)
    yc = math.sqrt(d1 - math.pow(zc, 2) - math.pow(xc, 2))
    coordinates = (xc, yc, zc)
    return coordinates;


if __name__ == '__main__':
    logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
    logging.basicConfig()

    socketIO = SocketIO('localhost', 8085)
    chat = socketIO.define(LoggingNamespace, '/chat')

    #l1 = #distance of the first sensor from the middle one
    #l2 = #distance of the second sensor form the middle one
    #d1 = #distance of the object from the middle sensor ^ 2
    #d2 = #distance of the object from the second sensor (l2) ^ 2
    #d3 = #distance of the object from the first sensor (l1 ) ^ 2


    while True:
        print("read value from serial")
        message = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        print("write value to websocket: " + message)
        chat.emit("broadcast", {"data": message })
#         chat.emit("broadcast", {
#             'object': "A",
#             'timestamp': "2016-06-10T21:42:24.760738",
#             'x': 25233,
#             'y': 5232,
#             'z': 25233
#         })
        socketIO.wait(seconds=1)

