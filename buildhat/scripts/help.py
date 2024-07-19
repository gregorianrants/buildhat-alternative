import serial
import time

ser = serial.Serial("/dev/serial0",115200,timeout=1)

ser.write(f'help \r'.encode())

for i in range(100):
    line = ser.readline()
    line = line.strip()
    print(line.decode())

