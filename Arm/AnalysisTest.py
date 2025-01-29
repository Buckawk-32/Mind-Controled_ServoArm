from Headset import Parser
from collections import deque
import time

headset = Parser.NeruoskyParser("COM6", 115200)

attention_data = deque(maxlen=100)

headset.start_serial()

time.sleep(7)

while len(attention_data) != 100:
    print(f"Attention: {headset.attention}")
    attention_data.append(headset.attention)


print(attention_data)

    

# def categorize(data):
#     for i in data:
#         print(i) 
#         if i >



def lerp(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    







