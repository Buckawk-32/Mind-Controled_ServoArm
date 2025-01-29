from telnetlib3 import TelnetClient
import threading
import time
import json

import serial
from Redo import HeadsetConnector

CONNECT = '\xc0'
DISCONNECT = '\xc1'
AUTOCONNECT = '\xc2'
SYNC = '\xaa'
EXCODE = '\x55'
POOR_SIGNAL = '\x02'
ATTENTION = '\x04'
MEDITATION = '\x05'
BLINK = '\x16'
HEADSET_CONNECTED = '\xd0'
HEADSET_NOT_FOUND = '\xd1'
HEADSET_DISCONNECTED = '\xd2'
REQUEST_DENIED = '\xd3'
STANDBY_SCAN = '\xd4'
RAW_VALUE = '\x80'


class NeruoskyParser(object): 

# data vairables

    attention = 0
    meditation = 0
    rawValue = 0
    delta = 0
    theta = 0
    lowAlpha = 0
    highAlpha = 0
    lowBeta = 0
    highBeta = 0
    lowGamma = 0
    midGamma = 0
    poorSignal = 0
    blinkStrength = 0

    eSenseDict = {'attention':0, 'meditation':0}
    waveDict = {
        'lowGamma': 0,
        'highGamma': 0, 
        'highAlpha': 0, 
        'delta': 0, 
        'highBeta': 0, 
        'lowAlpha': 0, 
        'lowBeta': 0, 
        'theta': 0
    }



    def __init__(self, port, baudrate):
        self.devID = "BTHENUM\Dev_C464E3E6E244"
        self.port = port
        self.srl = None
        self.telnet = None
        self.thread = None
        self.threadIsRunning = False
        self.baudrate = baudrate


        self.packetReceived = 0
        self.VerbosedpacketReceived = 0

    def __del__(self):
        if self.threadIsRunning == True:
            self.stop()


    def serial_connect(self):
        self.srl.write(CONNECT.encode("utf-8"))
    
    def serial_disconnect(self):
        self.srl.write(DISCONNECT.encode("utf-8"))


    def start_serial(self):
        if self.threadIsRunning == True:
            print("Mindwave is already Running...")
            return
        
        if self.srl == None:
            print("Building Serial Connection to Mindwave...")
            self.srl = serial.Serial(self.port, self.baudrate)
        else:
            self.srl.open()

        if self.devID:
            print("Sending Serial Connection message to Mindwave...")
            self.serial_connect()

        self.thread = threading.Thread(target=self.serial_parse)
        self.threadIsRunning = True

        print("Parsing Thread Made...")
        print("")

        self.thread.start()

# TODO: Rewrite the Telnet Parser
    def start_telnet(self):
        if self.threadIsRunning == True:
            print("Mindwave is already Running...")
            return
        
        if self.telnet == None:
            print("Building Telnet Connection to ThinkGear Connector...")
            self.telnet = Telnet("localhost", 13854)
        else:
            self.telnet.open("localhost", 13854)

        self.thread = threading.Thread(target=self.telnet_parse)
        self.threadIsRunning = True

        print("Parsing Thread Made...")
        print("")

        self.thread.start()
        print("Parser Thread Started...")

    def stop(self):
        if self.threadIsRunning == True:
            self.thread.join
            self.threadIsRunning = False

        if self.srl:
            self.srl.close()

        if self.telnet:
            self.telnet.close()


    def telnet_parse(self):
        data = self.telnet.read_until(bytes("\r", "utf-8"))
        data_dict = json.loads(data)
        print(data_dict)
        time.sleep(0.25)



    def serial_parse(self):
        "packetParser runs continously in a separate thread to parse packets from mindwave and update the corresponding variables"
        print("Parsing...")
        while self.threadIsRunning:
            p1 = self.srl.read(1).hex()  # read first 2 packets
            p2 = self.srl.read(1).hex()
            while (p1 != 'aa' or p2 != 'aa') and self.threadIsRunning:
                p1 = p2
                p2 = self.srl.read(1).hex()
            else:
                if self.threadIsRunning == False:
                    break
                # a valid packet is available
                self.packetReceived += 1
                payload = []
                checksum = 0
                payloadLength = int(self.srl.read(1).hex(), 16) #PLENGTH
                #print('payloadLength: ' + str(payloadLength))
                for i in range(payloadLength):
                    tempPacket = self.srl.read(1).hex()
                    payload.append(tempPacket)
                    checksum += int(tempPacket, 16) #sum every byte in the payload
                checksum = ~checksum & 0x000000ff #take the lowest 8 bits and invert them
                if checksum == int(self.srl.read(1).hex(), 16): #read the next byte of the package after the payload and check it with the checksum just calculated
                    i = 0
#                    print('payload ' + str(i) + ' = ' + str(payload[i]))
                    while i < payloadLength:

                        while payload[i] == '55': 
                                i = i+1

                        code = payload[i]
                        #print('packet ' + str(self.__packetsReceived) + ' code==' + str(code))
                        if (code == 'd0'):
                            print("Headset connected!")
                            self.__connected = True
                        elif (code == 'd1'):
                            print("Headset not found, reconnecting")
                            self.connect()
                        elif(code == 'd2'):
                            print("Disconnected!")
                            self.connect()
                        elif(code == 'd3'):
                            print("Headset denied operation!")
                        elif(code == 'd4'):
                            if payload[2] == 0 and not self.__connected:
                                print("Idle, trying to reconnect")
                                self.connect()
                        elif(code == '02'):  # poorSignal
                            i = i + 1
                            self.poorSignal = int(payload[i], 16)
                        elif(code == 'ba'):  # unknown
                            i = i + 1
                            self.unknown_ba = int(payload[i], 16)
#                            print('self.unknown_ba = ' + str(self.unknown_ba))
                        elif(code == 'bc'):  # unknown
                            i = i + 1
                            self.unknown_bc = int(payload[i], 16)
#                            print('self.unknown_bc = ' + str(self.unknown_bc))
                        elif(code == '04'):  # attention
                            i = i + 1
                            self.attention = int(payload[i], 16)
                        elif(code == '05'):  # meditation
                            i = i + 1
                            self.meditation = int(payload[i], 16)
                        elif(code == '16'):  # blink strength
                            i = i + 1
                            self.blinkStrength = int(payload[i], 16)
                        elif(code == '80'):  # raw value
                            i = i + 1  # for length/it is not used since length =1 byte long and always=2
                            #print('verbose packet length: ' + str(int(payload[i], 16)) + ' code==' + str(code))
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            rawVal = val0 * 256 + int(payload[i], 16)
                            if rawVal > 32768:
                                rawVal = rawVal - 65536

                            self.rawValue = rawVal
                            #print('self.rawValue = ' + str(self.rawValue))

                                #print('self.rawValue = ' + str(self.rawValue))
                        elif(code == '83'):  # ASIC_EEG_POWER
                            self.VerbosedpacketReceived += 1
                            #print('raw packet ' + str(self.__packetsReceived) + ' code==' + str(code))
                            #print('verbose packet ' + str(self.__verbosePacketsReceived) + ' code==' + str(code))
                            i = i + 1  # for length/it is not used since length =1 byte long and always=2
                            # delta:
                            #print('verbose packet length: ' + str(int(payload[i], 16)) + ' code==' + str(code))
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.delta = val0 * 65536 + \
                                val1 * 256 + int(payload[i], 16)
                            
                            # theta:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.theta = val0 * 65536 + \
                                val1 * 256 + int(payload[i], 16)
                            
                            # lowAlpha:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.lowAlpha = val0 * 65536 + \
                                val1 * 256 + int(payload[i], 16)
                            
                            # highAlpha:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.highAlpha = val0 * 65536 + \
                                val1 * 256 + int(payload[i], 16)
                            
                            # lowBeta:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.lowBeta = val0 * 65536 + \
                                val1 * 256 + int(payload[i], 16)
                            
                            # highBeta:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.highBeta = val0 * 65536 + \
                                val1 * 256 + int(payload[i], 16)
                            
                            # lowGamma:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.lowGamma = val0 * 65536 + \
                                val1 * 256 + int(payload[i], 16)
                            
                            # midGamma:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.midGamma = val0 * 65536 + \
                                val1 * 256 + int(payload[i], 16)
                            
                        else:
                            pass
                        i = i + 1
                else:
                    print('wrong checksum!!!')