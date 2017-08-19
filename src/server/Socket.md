#Socket.py

*What follows is a brief explanation of Socket.py structure and detail*

> #####This document should be replaced with correct documentation written using `Docstring` and `Sphinx`

In this case we want to have a application that serves web pages to client so we have to:
* define server object which will handle socket communication
* define web server object which handle user interface

so we have to import some modules...

* `aiohttp` to use Asyncronous http

* `socketio` to use socket for communication

Async method is necessary because we have 2 object running the same time:
* socket server
* web application

In this situation we can't serve both simultaneously, so we have to do asynced.

> In this moment we don't need the full `aiohttp` module, we need only web part so we have to "specialize" the import of the module with  `from aiohttp import web`


---

`sio = socketio.AsyncServer()`

Defines the socket server object `sio` and create it as an Asynchronous server (`.AsyncServer()`).

---

`app = web.Application()`

Defines the web application `app`
We called it simply without parameters because we specify them more over. 

---

`sio.attach(app)`
Now we tell to the socket server to attach itself to an app to run (in this case `app` which is our web app).


---

Never forget rule: if you have to deal with Async objects, functions and methods call related to them should use `async` and `await`

```
async def message(sid, data)

await sio.disconnect(sid, namespace='/chat')

```

###Event definition
With `socketio` you can define as many _custom events_ as you want.

> The event names `connect`, `message` and `disconnect` are reserved and should not be used.

Prepend them with _`@<server_object_var>.on("event_name", eventually_namespace_to_restrict)`_

Example: `@sio.on('msg_to_server', namespace='/chat')` define event `msg_to_server` related to namespace `/chat`.

It's important that in web pages delivered to client you recall correctly the event name in you code _(see ../client/index.html)_.

