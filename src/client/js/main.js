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

let namespace = '/dataLogger';
let socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
let positionRx = RxfromIO(socket, 'broadcast');
positionRx.subscribe(function(x) { console.log("position", x); });

//speedRx = positionRx.bufferCount(2, 1).subscribe( x => x );
//speedRx.subscribe(function(x) { console.log("speed", x); });


