# io-touchpad
## Description
    
     touchpadlib and app.py was implemented and linked.
     
     touchpadlib is library that contains functions responsible for taking the
       coordinates (and few other values of interest that will be used in later processing) of a touched point. It is
       modified evtest.
    
     app.py is basic application that uses touchpadlib - it is partitioned into two threads:
       one is continuously taking new event (info about touch) from touchpadlib and adds it to the queue (python structure
        used to synchronize threads)
        
       second is taking the oldest event from the queue and analyzes it, that means he either adds it to a collection of
        points representing symbol currently being drawn, or it determines that the symbol was finished. It       
        does by checking if difference between signals is higher then 0.3s (we're planning to change the way it
        recognizes to a special "stop" signal (type of event)) it also cuts the stream of points if it is too  
        long (in time) and sends what he has to symbol_interpreter, this is implemented so that if someone randomly draws
        shapes on touchpad without intention to send symbol, then he won't overflow memory. Currently symbol_interpreter
        can only count the number of events and write coordinates (it is used as a touchpadlib test).
    
    
### Usage

    make
    sudo python3 ./app.py

