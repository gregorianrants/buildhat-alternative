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
