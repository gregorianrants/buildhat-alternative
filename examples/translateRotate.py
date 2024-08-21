from buildhat_alternative.buildhat import BuildHat
from buildhat_alternative.motor import Motor
from buildhat_alternative.robot import Robot
import time
import signal
import sys
from sshkeyboard import listen_keyboard
import math

print('dont press anything yet we will let you know when we are ready to rock.....')

with (
    BuildHat() as buildhat,
    Motor("C", buildhat, -1) as left_motor,
    Motor("D", buildhat, 1) as right_motor,
):
    try:
        robot = Robot(left_motor, right_motor)
        
        #make a left turn
        robot.set_velocities(translational=300,rotational=math.pi/4)
        time.sleep(10)
        robot.pause()
        
    except KeyboardInterrupt:
        print("you pressed control c")

