# ToDo

## Rooms and messages
- room "????" - change "room" name for 'broadcast' messages from 'chat' to something more meaningfull;
  - Browser -> Server
    - setup
    - command
  - Server -> Browser
    - broadcast

- room "?????" - create a new "room" to handle DataLogger <-> Server communications
  - Server -> DataLogger (-> Controller):
    - setup
    - command
  - DataLogger -> Server
    - event



## Data Message format

### Controller -> DataLogger
- object ID
- time offset: at least 1/10 milliseconds (max value 1.000.000 1/10 milliseconds ~ 1min)
- tx, ty, tz: response time in µsec (max value ~ 25.000 (µsec) ~ 5m )


### for DataLogger -> Server communication

Payload "event"
{
    object: ID,
    timestamp: ISO8601 - 2016-06-10T21:42:24.760738,
    x: int    ±100.000  1/10 mm ~ 5m
    y: int
    z: int
}

# Sensors

L shaped, with two size (l1, l2) and a third sensor in the "origin"
temperature: 1/10 centigrades
%RH: unit

# Homeworks
- trigonometry
-