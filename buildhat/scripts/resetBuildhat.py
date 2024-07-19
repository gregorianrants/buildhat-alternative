from gpiozero import Device,DigitalOutputDevice
#from gpiozero.pins.rpigpio import RPiGPIOFactory
import time

from gpiozero.pins.lgpio import LGPIOFactory


#PAY ATTENTION IT IS DEVICE WE NEED TO SET PIN FACTORY ON
#Device.pin_factory  = RPiGPIOFactory()
Device.pin_factory  = LGPIOFactory()

#EVEN THOUGH WE USE DigitalOutputDevice which has a pin factory property
#DigitalOutputDevice.pin_factory = RPiGPIOFactory()
#will not work

RESET_GPIO_NUMBER = 4
BOOT0_GPIO_NUMBER = 22

print(DigitalOutputDevice.pin_factory)

def reset_hat():
        """Reset the HAT"""
        print('resetting hat')
        reset = DigitalOutputDevice(RESET_GPIO_NUMBER)
        boot0 = DigitalOutputDevice(BOOT0_GPIO_NUMBER)
        boot0.off()
        reset.off()
        time.sleep(0.01)
        reset.on()
        time.sleep(0.01)
        boot0.close()
        reset.close()
        time.sleep(0.5)
        print('should be reset')
        
        
if __name__ =='__main__':
    reset_hat()