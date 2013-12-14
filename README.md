#Robot
Robot is a sensor plugin for [Scratch](http://scratch.mit.edu) it depends on (but includes) Scratra https://github.com/scratra/scratra and it also depends on python-usb version 1 or above - this is *not* currently included in Debian or Ubuntu

###Installation
grab the code:

    git clone https://github.com/ALanBell/robopi.git
    git clone https://github.com/walac/pyusb.git

install python-usb

    cd pyusb
    sudo python setup.py install
and finally go back out of the pyusb directory

    cd ..


###Running
In scratch you need to enable remote sensors in your project, go to the Sensing blocks and right click
the sensor value block and enable remote sensors. This makes scratch broadcast stuff on port 42001 that
we can listen to.
Now that you have scratch running and listening, (and the robot arm plugged in) open a terminal and start the program to communicate with the arm. You do need to run this as root to have hardware access to the robot (you could mess about with udev to avoid this, or just run it with sudo)

    cd robopy
    sudo python robot.py

Sometimes Scratch doesn't seem to get hold of port 42001 on tcp, just udp. If it isn't working try "netstat -ln |grep 42" to see if both ports are working. If only udp is working try restarting scratch.

