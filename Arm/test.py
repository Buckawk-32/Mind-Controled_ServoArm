import serial
import serial.tools
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

for index, value in enumerate(sorted(ports)):
    print(index)