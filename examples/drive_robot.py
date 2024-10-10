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
