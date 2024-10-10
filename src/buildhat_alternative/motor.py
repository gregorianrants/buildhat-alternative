import math
from .pid_controller import PIDController
import time


class DataEmitter:
    def __init__(self, in_rate, out_rate, formatter):
        if out_rate > in_rate:
            raise ValueError("output rate can not be greater than input rate")
        if in_rate % out_rate != 0:
            raise ValueError(
                f"input rate :{in_rate}, divided by output rate: {out_rate} must result in whole number"
            )
        if type(in_rate) != int or type(out_rate) != int:
            raise ValueError("in_rate and out rate must be integers")
        self.in_rate = in_rate
        self.out_rate = out_rate
        self.count_to_handle_data_on = self.in_rate / self.out_rate
        self.counter = 0
        self.handler = None
        self.formatter = formatter
        self.unique_id = 0
        self.ids = []
        self.handlers = []

    def add_handler(self, handler):
        handler_id = self.unique_id
        self.unique_id += 1
        self.ids.append(handler_id)
        self.handlers.append(handler)
        return handler_id

    def remove_listener(self, id):
        i = self.ids.index(id)
        self.ids = [item for idx, item in enumerate(self.ids) if idx != id]
        self.handlers = [item for idx, item in enumerate(self.handlers) if idx != id]

    def handleData(self, speed, pos, apos):
        if self.counter == 0:
            data = self.formatter(speed, pos, apos)
            self.call_handlers(data)
        self.counter = (self.counter + 1) % self.count_to_handle_data_on

    def call_handlers(self, data):
        [listener(data) for listener in self.handlers]


class Motor:
    PORTS = ["A", "B", "C", "D"]

    def __init__(self, port, ser, direction=1, output_data_rate=1):
        self.port_letter = port
        self.port_index = self.PORTS.index(port)
        self.mode = 0
        self.ser = ser
        self.listeners = []
        self.count = 0
        self.direction = direction
        self.wheel_diameter = 276  # mm
        # self.PIDcontroller = PIDController(0.001,0,0.02)
        self.PIDcontroller = PIDController(0.00076, 0.003, 0.0153)
        self.speed = 0
        self.selrate = 10  # number of milliseconds between data emissions by the buildhat over serial.
        self.ser.add_motor(self)
        self.set_combi_mode()
        self.set_plimit()

        self.received_data_rate = 1000 // self.selrate  # convert to Hz
        self.data_emitter = DataEmitter(
            in_rate=self.received_data_rate,
            out_rate=output_data_rate,
            formatter=self.format_data,
        )
        # for some reason if i dont put a delay here the buildhat outputs zero speed
        # for a about 3 seconds even if wheels are moving.  this causes large measured error
        # in pid which sets max pwm and wheels go to fast.
        # thought it was an error being raised on buildhat when i was setting bias with deprecated command
        # the problem still remains though.
        # time.sleep(3)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        print("exiting motor")
        self.clean_up()

    """
    methods which send messages to the buildhat
    """

    def write(self, message):
        full_message = f"port {self.port_index}; {message}"
        self.ser.write(full_message)

    def set_combi_mode(self):
        pass
        self.write(f"select")
        self.write(f"combi 0 1 0 2 0 3 0")
        self.write(f"select 0; selrate 10")

    def set_plimit(self):
        self.write(f"plimit 1")

    def pwm(self, pwm):
        pwm = (pwm * self.direction) / 100
        if pwm > 1 or pwm < -1:
            # print("pwm must be between -1 and 1")
            pwm = math.copysign(1, pwm) * 1
        data = f"set {pwm};"
        self.write(data)

    """methods which handles messages received from the build hat"""

    def format_data(self, speed, pos, apos):
        data = {
            "port": self.port_letter,
            "target_speed_deg/sec": self.PIDcontroller.set_point,
            "speed_deg/sec": speed * 10,
            "speed_mm/s": speed * (1 / 36) * 276.401,
            "pos": pos,
            "apos": apos,
            "time": time.time(),
        }
        return data

    def handle_data(self, speed, pos, apos):
        # we are converting the speed output by the build hat which is in 10 degrees per second
        # yes you read that right i said "10"
        # to degrees per second.
        self.data_emitter.handleData(
            speed * self.direction, pos * self.direction, apos * self.direction
        )
        speed = self.direction * speed * 10
        self.update(speed)

    def update(self, speed):
        updated_pwm = self.PIDcontroller.update(speed)
        self.pwm(updated_pwm)

    """utility methods"""

    def getSpeed(self, aSpeed):
        speed = (aSpeed / 36) * self.wheel_diameter
        return speed

    def getDistance(self, pos):
        distance = pos / 360 * self.wheel_diameter
        return distance

    """interface"""

    def clean_up(self):
        self.pwm(0)
        self.write(f"select")
        time.sleep(0.2)
        self.pwm(0)
        time.sleep(0.5)

    def add_listener(self, listener):
        """not fully implemented here as an idea only"""
        return self.data_emitter.add_handler(listener)

    def remove_listener(self, id):
        """not fully implemented here as an idea only"""
        self.data_emitter.remove_listener(id)

    def dc(self, duty=0.2):
        """using this method will switch to controlling power via pwm directly
        calling run again will switch to a speed control mode.
        """
        pass

    # we have changed the speed entered here from mm_per_second to degrees per second.
    def run(self, degrees_per_second):
        self.speed = degrees_per_second
        self.PIDcontroller.set_point = self.speed

    def __str__(self):
        return f"Motor PortIndex:{self.port_index}, Port: {self.port_letter}"
