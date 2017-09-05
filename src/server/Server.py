# Web Application that will handle websocket, with write received by Main.py calls, and values pushed to all web clients

from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    """Serve the client-side application."""
    with open('../client/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

# -------------------------------------------------------------------

@sio.on('connect', namespace='/dataLogger')
def connect(sid, environ):
    """On connection event from client print to stdout the connect event and sid of client."""
    print("connect ", sid)

@sio.on('broadcast', namespace='/dataLogger')
async def message(sid, data):
    """Get message from client and reply with same message to it."""
    print("broadcast", data, sid)
    await sio.emit('broadcast', data=data, skip_sid=True, namespace='/dataLogger')

@sio.on('disconnect request', namespace='/dataLogger')
async def disconnect(sid):
    """Close socket connection for client with specified sid."""
    print('disconnect ', sid)
    await sio.disconnect(sid, namespace='/dataLogger')

@sio.on('command', namespace='/dataLogger')
def my_event(sid, data):
    """Get message from client and print to stdout."""
    print("command", sid, data)

# -------------------------------------------------------------------

app.router.add_get('/', index)
app.router.add_static('/js', '../client/js')

if __name__ == '__main__':
    web.run_app(app, port=8085)
