# Application that will read data from serial port and push values to Socket.py's websocket
import random
import string
import logging

from socketIO_client import SocketIO, LoggingNamespace

if __name__ == '__main__':
    logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
    logging.basicConfig()

    socketIO = SocketIO('homer.local', 8085)
    chat = socketIO.define(LoggingNamespace, '/chat')

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

