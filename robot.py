#first.py
from scratra import *
#ROBOT ARM CONTROL PROGRAM
#import the USB and Time librarys into Python
import usb.core, usb.util, time
#Allocate the name 'RoboArm' to the USB device
RoboArm = usb.core.find(idVendor=0x1267, idProduct=0x000)
#Check if the arm is detected and warn if not
if RoboArm is None:
    raise ValueError("Arm not found")
#Create a variable for duration
Duration=1.0
#Define a procedure to execute each movement
def MoveArm(Duration, ArmCmd):
    #Start the movement
    try:
        RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,3)
    except:
        #if it fails then stop moving stuff, don't leave it in a moving state.
        time.sleep(0.1)
        ArmCmd=[0,0,0]
        RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,3)
        
    #Stop the movement after waiting a specified duration
    #we do want to sleep here, not do an async callback because we don't want other motions starting
    time.sleep(Duration)
    ArmCmd=[0,0,0]
    try:
        RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,3)
    except:
        #if it fails then stop moving stuff, don't leave it in a moving state.
        time.sleep(0.1)
        ArmCmd=[0,0,0]
        RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,3)

    time.sleep(0.2)#pausing for a tiny bit after the motion stops feels right

@start
def whenstart(scratch):
    #on startup lets jiggle all the motors a bit
    MoveArm(.1,[0,1,0]) #Rotate base anti-clockwise
    MoveArm(.1,[0,2,0]) #Rotate base clockwise
    MoveArm(.1,[64,0,0]) #Shoulder up
    MoveArm(.1,[128,0,0]) #Shoulder down
    MoveArm(.1,[16,0,0]) #Elbow up
    MoveArm(.1,[32,0,0]) #Elbow down
    MoveArm(.1,[4,0,0]) #Wrist up
    MoveArm(.1,[8,0,0]) # Wrist down
    MoveArm(.1,[2,0,0]) #Grip open
    MoveArm(.1,[1,0,0]) #Grip close
    MoveArm(.1,[0,0,1]) #Light on

@broadcast('Base right')
def baseright(scratch):
    print 'Base right'
    MoveArm(Duration/10.0,[0,1,0])

@broadcast('Base left')
def baseleft(scratch):
    print 'Base left'
    MoveArm(Duration/10.0,[0,2,0])

@broadcast('Shoulder up')
def shoulderup(scratch):
    print 'Shoulder up'
    MoveArm(Duration/10.0,[64,0,0])

@broadcast('Shoulder down')
def shoulderdown(scratch):
    print 'Shoulder down'
    MoveArm(Duration/10.0,[128,0,0])


@broadcast('Elbow down')
def elbowdown(scratch):
    print 'Elbow down'
    MoveArm(Duration/10.0,[32,0,0])


@broadcast('Elbow up')
def elbowout(scratch):
    print 'Elbow up'
    MoveArm(Duration/10.0,[16,0,0])

@broadcast('Wrist up')
def elbowdown(scratch):
    print 'Wrist up'
    MoveArm(Duration/10.0,[4,0,0])

@broadcast('Wrist down')
def elbowdown(scratch):
    print 'Wrist down'
    MoveArm(Duration/10.0,[8,0,0])

@broadcast('Grip open')
def elbowdown(scratch):
    print 'Grip open'
    MoveArm(Duration/10.0,[2,0,0])

@broadcast('Grip close')
def elbowdown(scratch):
    print 'Grip close'
    MoveArm(Duration/10.0,[1,0,0])

@broadcast('Light on')
def elbowdown(scratch):
    print 'Light on'
    MoveArm(Duration/10.0,[0,0,1])

@update('MoveDuration')
def updateDuration(scratch,value):
    global Duration
    Duration=value
    print value
run()
