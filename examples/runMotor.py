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
