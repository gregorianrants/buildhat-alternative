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
    Motor(port="C", ser=buildhat, direction=-1,output_data_rate=1) as left_motor,
):
    try:
        
        #you can add a callback function that will be passed the data that is output from the motor i.e. 
        # the encoder readings,  
        # the motor outputs data pretty quick note teh output_data_rate parameter above when setting up
        # motor this controls the interval callback is called at in seconds.
        
        left_motor.add_listener(print)
        
        left_motor.run(degrees_per_second=360)
        time.sleep(5)
        left_motor.run(0)
       
    except KeyboardInterrupt:
        print("you pressed control c")

