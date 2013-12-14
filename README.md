#Robot
Robot is a sensor plugin for [Scratch](http://scratch.mit.edu) it depends on Scratra https://github.com/scratra/scratra
There might be some other dependencies, I will update the docs later for the setup from a clean Raspberry Pi image

###Running it
You do need to run this as root to have hardware access to the robot
(you could mess about with udev to avoid this, or just run it with sudo)
put scratra.py and robot.py in the same directory then

sudo python robot.py

In scratch you need to enable remote sensors in your project, go to the Sensing blocks and right click
the sensor value block and enable remote sensors. This makes scratch broadcast stuff on port 42001 that
we can listen to.
