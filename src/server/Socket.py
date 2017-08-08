# Web Application that will handle websocket, with write received by Main.py calls, and values pushed to all web clients

from aiohttp import web
import socketio
import time
#import asyncio


#async def index(request):
#    """Serve the client-side application."""
#    with open('../client/index.html') as f:
#        return web.Response(text=f.read(), content_type='text/html')

@socket.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

@socket.on('write', namespace='/chat')
async def message(sid, data):
    print("message ", data)
    await socket.emit('push', room=sid)

@socket.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

app.router.add_static('/app', '../client')
#app.router.add_get('/', index)

async def main(loop):
    while True:
        print("push event")
        await socket.emit('data', info="pippo")
		await socket.
        time.sleep(5)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()

	app = web.Application(loop=loop)
	socket = socketio.AsyncServer()
	socket.attach(app)

    loop.run_until_complete(main(loop))

    web.run_app(app, loop=loop, host='localhost', port=8080)

