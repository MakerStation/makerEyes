#makerEyes
###A spatial measuring system for physics experiment and whatever you want...(maybe)

*With this project we want to build a wirelss measuring system for physics experiment that would be able to identify, locate, measure and track objects into a pre-determinated area without having to introduce canonical measuring systems like meters, compass and others, wich can interferee with the experiment*

*Data acquired by the system needs to be converted to something human readable. For this reason the system is built with a small pc (i.e. Raspberry Pi) to acquire raw data from the sensor controller and dispatch them to any other pc which connetcs to its webserver building also a 3D and its prospectical views to represent the object in teh experiment.*

**Simple schema of the whole system**

```
                                   +-----+
                                   |  S1 |
     +-----------------------------+     |
     |                             +-----+
     |
     |
     |
     |                                                                                           +-----------+
     |                                                                                           |           |
     |                                         +-+ Obj1                                +---------+ Student   |
     |                                         +-+                                     |         | PC 1      |        +---------------+
     |                +-+ Obj3                                                         |         |           |        |               |
     |                +-+                                                              |         +-----------+        |               |
     |                                                                                 |                              |   Student     |
     |                                                                                 |                              |   PC 3        |
     |                                                                                 |        +------------+        |               |
     |                                +-+ Obj2                                         |        |            |        |               |
     |                                +-+                                              |        |  Student   |        +------+--------+
     |                                                                                 |  +-----+  Pc 2      |               |
     |                                                                                 |  |     |            |               |
     |                                                                                 |  |     +------------+               |   +-----------+
     |       +-----+                                                +-----+            |  |                                  |   |           |
     |       |     |                                                |     |            |  |                                  |   |  Student  |
     |  +----+ S3  |              +---------------------------------+ S2  |            |  |                                  |   |  PC n     |
     |  |    +-----+              |                                 +-----+            |  |                                  |   |           |
     |  |                         |                                                    |  |       +---------------+          |   +-----+-----+
     |  |   +---------------------+                                                    |  |       |               |          |         |
     |  |   |                                                                          |  |    +--+ Teacher PC    |          |         |
     |  |   |                                                                          |  |    |  |               |          |         |
   +-v--v---v---+           +------------+                                             |  |    |  |               |          |         |
   |            |           |            |                                             |  |    |  +---------------+          |         |
   | Sensor     |   RS232   | Web        |                                             |  |    |                             |         |
   | Controller <-----------> Server /   |                                             |  |    |                             |         |
   |            |           | Dispatcher |                                             |  |    |                             |         |
   +------------+           |            |                                             |  |    |                             |         |
                            +------+-----+                                             |  |    |                             |         |
                                   |                                                   |  |    |                             |         |
                                   |                               Ethernet LAN        |  |    |                             |         |
+------------------------------------------------------------------------------------------------------------------------------------------------------------+
+------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

##Legend and explanation
- S1..3: these are the sensors that receive the acoustic signal from the objects 
- Obj1..3: these are the object into the experiment; they emit an acoustic signal to tell their position in space
- Sensor controller: this is the heart of measuring system. It acquires signal from sensor and translates them into a positional coordinates which send to Web Server/Dispatcher for rappresentation and diffusion
- Web Server/Dispatcher: this is a PC (big or small doesn't matter). With the appropriate software on it, will make availlable datas through web interface to all the connected clients
- Studend PC1..PCn: these are the clients. In this situation the experiment is in a school, so they are the student PCs. In other situation they will be the clients of a research laboratory, for example.  

##Specifications:

* Sensor controller will communicate with "Web Server/Dispatcher" using a serial line with RS232 specification.
* For this version we assume that where will be only three sensors and only one controller. In future versions could be expanded to create a complex detection network. In that case RS232 is non the best serial interface to use...
* Web Server/Dispatcher must be run in Python exposing only the neccessary interface
* Web Server/dispatcher must have a Teacher reserved page to setup experiment, start & stop it, and other administration utilities that will be necessary.
* Client side of Web Server/Dispatcher must be developed in JavaScript
* All the softare **must** be written and developed using `Python virtualenv` to have a *virtual bubble* to preserve developer PC from mixing various software and libraries with the existing ones and let every developer have the same development enviroment.
* Data packet transmitted by Sensor controller will be 8 byte structured as follow:

```
2 byte for ObjectID
2 byte for Δt of X Coordinate
2 byte for Δt of Y Coordinate
2 byte for Δt of Z Coordinate
```


