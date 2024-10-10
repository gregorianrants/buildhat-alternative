## Background

This is a stand alone package for control of motors using the raspberry pi Buildhat. It loads the firmware onto the Buildhat and doesn't rely on the official raspberry pi Buildhat library for anything.

currently it has functionality to control the speed of motors. more functionality may be added in the future.

I created this library because the official library has some issues that make it not suitable for wheeled robots.
The main problem is that when controlling the speed of 2 motors there is a lag in updating there speeds. this results in a robot that turns quickly when trying to go straight. this problem is documented at the following locations:

https://forums.raspberrypi.com/viewtopic.php?t=337816#p2022632

https://github.com/RaspberryPiFoundation/python-build-hat/issues/152

## A Note about how the buidlhat works for any library

whether using this library or the official library there are 2 pieces of software that are involved in using the buildhat.

1. firmware that runs on the buildhat
2. software that runs on the pi and speaks to the firmware over serial

this library replaces the official buildhat library that runs on the pi, but uses the same firmware. you can find info on the firmware and the commands that can be sent over serial here.

https://datasheets.raspberrypi.com/build-hat/build-hat-serial-protocol.pdf

important to note is that the firmware was updated and there are some new commands, if you use the help command documented in the firmware you will see the commands.

of particular note is the command

selrate <rate> : set reporting period (use after 'select')

this changes the rate that sensor readings are outputed at.

i have used - selrate 10 - with motors and get a reading every 10ms

i have not tried this command with other sensors as i use non lego sensors on my robots.

I plan on writing more at some point about how the serial protocol for the firmware works.

## How this library differs from the official one

first a note about how the official library works and then how this library is different.

The official library relies on a pid algorithm that runs on the Buildhat, all the official library does is put the buildhat into pid mode then send it a speed which will then be regulated on the Buildhat.

The alternative library in this repo, puts the buidlhat into pwm mode as opposed to pid mode. this allows controling the power of the motors. it also selects a data output mode that outputs the encoder readings 100 times per second.

## performance

Here is the speed reading for encoders running for 6 seconds with a speed of 500 degrees per second. these readings are made on one of the wheels of a robot driving on carpet.

![plot of encoder readings](/Figure_1.png)

I could probably imporove the tuning as i got the pid working just good enough then went onto develop more features on my robot, i will work on this some more soon.

## Examples

you can find these examples in the examples folder also

# The most useful way to use the library

I find the most useful way to control a robot is giving it a translational and rotational velocity. This functionality is available on the Robot class. the example of using it is listed last as the simpler components it builds in are listed first.

# basic motor use

```python
from buildhat_alternative.buildhat import BuildHat
from buildhat_alternative.motor import Motor
from buildhat_alternative.robot import Robot
import time
import signal
import sys
from sshkeyboard import listen_keyboard
import math

from queue import Queue


print("dont press anything yet we will let you know when we are ready to rock.....")


q = Queue()

with (
    BuildHat() as buildhat,
    Motor(port="C", ser=buildhat, direction=-1, output_data_rate=1) as left_motor,
):
    try:

        # you can add a callback function that will be passed the data that is output from the motor i.e.
        # the encoder readings,
        # the motor outputs data pretty quick. note the output_data_rate (its in Hz) parameter above when setting up
        # output data rate must be 100hz or bellow.

        left_motor.add_listener(print)
        left_motor.add_listener(q.put)

        counter = 0
        start_time = time.time()
        #it is important that we wait till the motor as started emitting data before we start setting its 
        # #speed otherwise it causes the pid to ramp up to quickly
        while True:
            msg = q.get()
            print(msg)
            if counter == 5:
                left_motor.run(degrees_per_second=200)
            if time.time() - start_time > 10000:
                break
            counter += 1

        left_motor.run(0)

    except KeyboardInterrupt:
        print("you pressed control c")


```

# Keyboard control of a robot

```python
from buildhat_alternative.buildhat import BuildHat
from buildhat_alternative.motor import Motor
from buildhat_alternative.robot import Robot
import time
import signal
import sys
from sshkeyboard import listen_keyboard
import math

from queue import Queue

print("dont press anything yet we will let you know when we are ready to rock.....")

q = Queue()
counter = 0


with (
    BuildHat() as buildhat,
    Motor("C", buildhat, -1) as left_motor,
    Motor("D", buildhat, 1) as right_motor,
):
    try:
        left_motor.add_listener(q.put)
        left_motor.add_listener(print)
        # prints something like:
        # {'port': 'C', 'target_speed_deg/sec': 0, 'speed_deg/sec': 0, 'speed_mm/s': 0.0, 'pos': 2721, 'apos': 172, 'time': 1728570811.8964775}

        robot = Robot(left_motor, right_motor)

        def press(key):
            print(f"'{key}' pressed")
            if key == "k":
                robot.forward()
            if key == "m":
                robot.back()
            if key == "z":
                robot.left()
            if key == "x":
                robot.right()
            if key == "a":
                robot.set_velocities(300, math.pi / 4)
            if key == "s":
                robot.set_velocities(300, -math.pi / 4)
            if key == "space":
                robot.pause()

        def release(key):
            print(f"'{key}' released")

        # data event loop
        # listen for 5 data events before continuing this is to make sure everything is initialized
        while True:
            msg = q.get()
            # this message just has the same data that we are printing.
            if counter == 5:
                break

            counter += 1

        # because listen keyboard blocks we break out the loop before initializing, if we needed to do more stuff in the loop above
        # we could start listen keyboard in a thread, since this is just a demo i haven't overcomplicated it.

        print("ready to rock")
        print("keys are:")
        print("k=forward m=back z=left x=right")
        print("press SPACE TO STOP")

        listen_keyboard(
            on_press=press,
            on_release=release,
        )

    except KeyboardInterrupt:
        print("you pressed control c")



```

# Controlling with translational and rotational velocities

```python
from buildhat_alternative.buildhat import BuildHat
from buildhat_alternative.motor import Motor
from buildhat_alternative.robot import Robot
import time
import math

from queue import Queue

q = Queue()

print("dont press anything yet we will let you know when we are ready to rock.....")

with (
    BuildHat() as buildhat,
    Motor("C", buildhat, -1) as left_motor,
    Motor("D", buildhat, 1) as right_motor,
):
    try:
        robot = Robot(left_motor, right_motor)

        left_motor.add_listener(q.put)
        counter = 0
        start_time = None
        #it is important that we wait till the motor as started emitting data before we start setting its 
        # #speed otherwise it causes the pid to ramp up to quickly
        while True:
            msg = q.get()
            print(msg)
            if counter == 5:
                robot.set_velocities(translational=300, rotational=math.pi / 4)
                start_time = time.time()
            counter += 1
            if start_time and time.time() - start_time < 5000:
                break

        # make a left turn

        time.sleep(10)
        robot.pause()

    except KeyboardInterrupt:
        print("you pressed control c")


```

## Where i use this

I Use this library in composed-robot

https://github.com/gregorianrants/composed-robot?tab=readme-ov-file

this is a repo that composes a bunch of other repos to give a physical lego robot i have built, behaviors.

## where i am going with this

I will certainly add position control and stall detection. I don't have any sensors so not sure about that, i would certainly help anyone that wants to add sensors. i think sensors would be fairly easy as you are just reading data.
