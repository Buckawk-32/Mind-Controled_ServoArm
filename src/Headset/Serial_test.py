from Headset import Parser
import time

parser = Parser.NeruoskyParser("COM6", 115200)

parser.start_serial()

while True:
    print( 
f"""
--------------------------------
Attention: {parser.attention}
Meditation: {parser.meditation}
--------------------------------
Delta: {parser.delta}
Theta: {parser.theta}
LowAplha: {parser.lowAlpha}
HighAplha: {parser.highAlpha}
LowBeta: {parser.lowBeta}
HighBeta: {parser.highBeta}
LowGamma: {parser.lowGamma}
MidGamma: {parser.midGamma}
--------------------------------
Raw Value: {parser.rawValue}
--------------------------------
""")
    time.sleep(1)


