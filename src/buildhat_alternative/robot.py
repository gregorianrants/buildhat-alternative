import time

DISTANCE_BETWEEN_WHEELS= 176

class Robot():
    def __init__(self,left_motor,right_motor):
        self.left_motor = left_motor
        self.right_motor = right_motor
        
    def get_velocities(self,translational, rotational):
        v_right = translational + (DISTANCE_BETWEEN_WHEELS / 2) * rotational
        v_left = translational - (DISTANCE_BETWEEN_WHEELS / 2) * rotational
        return (v_left,v_right)
    
    def set_velocities(self,translational,rotational):
        v_left,v_right = self.get_velocities(translational,rotational) 
        self.left_motor.run(v_left)
        self.right_motor.run(v_right)
  
    def forward(self,speed=500):
        self.pause()
        time.sleep(0.5)
        print('going forward')
        self.left_motor.run(speed)
        self.right_motor.run(speed)
        
    def back(self,speed=500):
        self.pause()
        time.sleep(0.5)
        self.forward(-speed)
        
    def left(self,speed=350):
        self.pause()
        time.sleep(0.5)
        self.left_motor.run(-speed)
        self.right_motor.run(speed)
        
    def right(self,speed=350):
        self.pause()
        time.sleep(0.5)
        self.left_motor.run(speed)
        self.right_motor.run(-speed)
        
    def pause(self):
        self.left_motor.run(0)
        self.right_motor.run(0)