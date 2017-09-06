function RxfromIO (io, eventName) {
    return Rx.Observable.create(observer => {
        io.on (eventName, (data) => {
            observer.next(data)
        });
        return {
            dispose : io.close
        }
    });
}

filterObjects = function (anObject) {
    return function (event) {
        return event['object'] == anObject;
    }
}

deltat = function (xyz1, xyz0, dt) {
    return {
        x: (xyz1['x'] - xyz0['x']) / dt,
        y: (xyz1['y'] - xyz0['y']) / dt,
        z: (xyz1['z'] - xyz0['z']) / dt
    }
}

let namespace = '/dataLogger';
let socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
let rawEventsRx = RxfromIO(socket, 'broadcast');
let eventsRx = rawEventsRx.map(function (e) { return {object:e['object'], timestamp:(new Date(e['timestamp']).getTime()), position:{ x:e['x'], y:e['y'], z:e['z']}}; });
eventsRx.subscribe(function(x) { console.log("broadcast", x); });

let objects = ["A", "B", "C"];
let positionsRx = objects.map(x => eventsRx.filter(filterObjects(x)));
let velocitiesRx = positionsRx.map(p => p.bufferCount(2, 1).map(function ([p0, p1]) {
    let dt = p1['timestamp'] - p0['timestamp'];
    return {
        object:    p1['object'],
        timestamp: p1['timestamp'],
        position:  p1['position'],
        speed:     deltat(p1['position'], p0['position'], dt)
    }
}));
let accellerationsRx = velocitiesRx.map(p => p.bufferCount(2, 1).map(function ([v0, v1]) {
    let dt = v1['timestamp'] - v0['timestamp'];
    return {
        object:        v1['object'],
        timestamp:     v1['timestamp'],
        position:      v1['position'],
        accelleration: deltat(v1['speed'], v0['speed'], dt)
    }
}));

positionsRx.map(p => p.subscribe(x => console.log("position " + x['object'], x)));
velocitiesRx.map(v => v.subscribe(x => console.log("velocity " + x['object'], x['speed'])));
accellerationsRx.map(a => a.subscribe(x => console.log("accelleration " + x['object'], x['accelleration'])));
