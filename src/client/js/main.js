
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

deltaT = function (x1, x0, dt) {
    return (x1 - x0) / dt;
}

xyzDeltaT = function (xyz1, xyz0, dt) {
    return {
        x: deltaT(xyz1['x'], xyz0['x'], dt),
        y: deltaT(xyz1['y'], xyz0['y'], dt),
        z: deltaT(xyz1['z'], xyz0['z'], dt)
    }
}

vectorMagnitude = function (vector) {
    return Math.sqrt(Math.pow(vector['x'], 2) + Math.pow(vector['y'], 2) + Math.pow(vector['z'], 2));
}
/*
collectLatestResults = function (accumulator, currentValue) {
    var values;

    let key = currentValue['object'];
    if (key in accumulator) {
        values = accumulator[key].concat([currentValue]);
    } else {
        values = [currentValue]
    }

    if (values.length > 10) {
        values = values.slice(1);
    } else {
        values = values;
    }

    accumulator[key] = values;

    return accumulator;
}
*/

collectResults = function (accumulator, currentValue) {
    var newValue = {};
    let key = currentValue['object'];
    newValue[key] = [currentValue].concat(accumulator[key]);
    return Object.assign({}, accumulator, newValue);
}

//=================================================================

function initRx() {
    let namespace = '/dataLogger';
    let socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    let rawEventsRx = RxfromIO(socket, 'broadcast');
    let eventsRx = rawEventsRx.map(function (e) {
        return {
            object:e['object'],
            timestamp:(new Date(e['timestamp']).getTime()),
            position: {
                x:e['x'],
                y:e['y'],
                z:e['z']
            }
        };
    });

    //.................................................................

    let objects = ["A", "B", "C"];

    let positionsRx = objects.map(x => eventsRx.filter(filterObjects(x)));

    let velocitiesRx = positionsRx.map(p => p.bufferCount(count=2, skip=1).map(function ([p0, p1]) {
        let dt = p1['timestamp'] - p0['timestamp'];
        speedVector = xyzDeltaT(p1['position'], p0['position'], dt);
        return {
            object:         p1['object'],
            timestamp:      p1['timestamp'],
            position:       p1['position'],
            speed:          vectorMagnitude(speedVector),
            speedVector:    speedVector
        }
    }));

    let accellerationsRx = velocitiesRx.map(p => p.bufferCount(count=2, skip=1).map(function ([v0, v1]) {
        let dt = v1['timestamp'] - v0['timestamp'];
        accellerationVector = xyzDeltaT(v1['speedVector'], v0['speedVector'], dt);
        return {
            object:                 v1['object'],
            timestamp:              v1['timestamp'],
            position:               v1['position'],
            speed:                  v1['speed'],
            speedVector:            v1['speedVector'],
            accelleration:          vectorMagnitude(accellerationVector),
            accellerationVector:    accellerationVector
        }
    }));

    let initialValues = objects.reduce(function (accumulator, value) {
        var newValue = {};
        newValue[value] = [];
        return Object.assign({}, accumulator, newValue);
    }, {});

    let mergeAllLatestEventsRs = Rx.Observable.merge.apply(this, accellerationsRx);
    let collectedEventsRx = mergeAllLatestEventsRs.scan(collectResults, initialValues);

    collectedEventsRx.subscribe(x => console.log("collected events ", x));
    collectedEventsRx.subscribe(data => ReactDOM.render(View3D({'data':data}), document.getElementById('view3D')));
    collectedEventsRx.subscribe(data => ReactDOM.render(TabularData({'data':data}), document.getElementById('tabularData')));
}
/*
function initReact() {
    ReactDOM.render(
      MainComponent({height:100, width:100}),
      document.getElementById('main')
    );
}
*/
document.addEventListener("DOMContentLoaded", function() {
//  initReact();
  initRx();
});