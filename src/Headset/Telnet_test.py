from collections import deque
import serial
from Headset import Parser

x = Parser.NeruoskyParser(None, 115200)

x.start_telnet()


