## Background

This is a stand alone package for control of motors using the raspberry pi Buildhat.  It loads the firmware onto the Buildhat and doesn't rely on the official raspberry pi Buildhat library for anything.

currently it has functionality to control the speed of motors.  more functionality may be added in the future.

I created this library because the official library has some issues that make it not suitable for wheeled robots.
The main problem is that when controlling the speed of 2 motors there is a lag in updating there speeds.  this results in a robot that turns quickly when trying to go straight.  this problem is documented at the following locations:

https://forums.raspberrypi.com/viewtopic.php?t=337816#p2022632

https://github.com/RaspberryPiFoundation/python-build-hat/issues/152

## A Note about how the buidlhat works for any library

whether using this library or the official library there are 2 pieces of software that are involved in using he buildhat. 

1. firmware that runs on the buildhat
2. software that runs on the pi and speaks to the firmware over serial

this library replaces the official buildhat library that runs on the pi, but uses the same firmware.  you can find info on the firmware and the commands that can be sent over serial here.

https://datasheets.raspberrypi.com/build-hat/build-hat-serial-protocol.pdf

important to note is that the firmware was updated and there are some new commands, if you use the help command documented in the firmware you will see the commands.

of particular note is the command 

selrate <rate>        : set reporting period (use after 'select') 

this changes the rate that sensor readings are outputed at.

i have used - selrate 10 - with motors and get a reading every 10ms

i have not tried this command with other sensors as i use non lego sensors on my robots.

I plan on writing more at some point about how the serial protocol for the firmware works.



## How this library differs from the official one

first a note about how the official library works and then how this library is different.

The official library relies on a pid algorithm that runs on the Buildhat, all the official library does is put the buildhat into pid mode then send it a speed which will then be regulated on the Buildhat.

This library puts the buidlhat into pwm mode as opposed to pid mode. this allows controling the power of the motors.  it also selects a data output mode that outputs the encoder readings 100 times per second.