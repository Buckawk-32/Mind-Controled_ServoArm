import serial, threading, sys

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

class Headset(object):

    _attention = 0
    _meditation = 0
    _rawValue = 0
    _delta = 0
    _theta = 0
    _lowAlpha = 0
    _highAlpha = 0
    _lowBeta = 0
    _highBeta = 0
    _lowGamma = 0
    _midGamma = 0
    _poorSignal = 0
    _blinkStrength = 0

    def __init__(self, port=None, baudrate=9600, devid='BTHENUM\Dev_C464E3E6E244'):
        if port == None:
            os = sys.platform
            if os == "win32":
                port = 'COM6'

        self._devid = devid
        self._srl = None
        self._serialPort = port
        self._serialBaudRate = baudrate
        self._parserThread = None
        self._threadBool = False
        self._connected = False


    def __del__(self):
        if self._threadBool == True:
            self.stop()


    def connect(self):
        self._srl.write(CONNECT.encode())


    def disconnect(self):
        self._srl.write(DISCONNECT.encode())

    
    def start(self):
        if self._threadBool == True:
            print("Mindwave is already running")
            
        if self._srl == None:
            try:
                # Opens up a new serial port, if one isn't declared already
                self._srl = serial.Serial(self._serialPort, self._serialBaudRate)

            # Catches Serial Exceptions
            except Exception as a:
                print(str(a))

        # Otherwise open and existing port
        else:
            self._srl.open()
        

        if self._devid:
            self.connect()

        self._parserThread = threading.Thread(target=self.packetparser)
        self._threadBool = True
        self._parserThread.start()


    def stop(self):
        if self._threadBool == True:
            self._parserThread.join()
            self._threadBool = False
            self._srl.close()

    
    def packetparser(self):
        while self._threadBool:
            p1 = self._srl.read(1).hex()
            p2 = self._srl.read(1).hex()
            while (p1 != 'aa' or p2 != 'aa') and self._threadBool:
                p1 = p2 
                p2 = self._srl.read(1).hex()
            else:
                if self._threadBool == False:
                    break

                payload = []
                checksum = 0
                payloadLength = int(self._srl.read(1).hex(), 16)

                for i in range(payloadLength):
                    tempPacket = self._srl.read(1).hex()
                    payload.append(tempPacket)
                    checksum += int(tempPacket, 16)
                
                checksum = ~checksum & 0x000000ff
                if checksum == int(self._srl.read(1).hex(), 16):
                    i = 0
                    # print('payload ' + str(i) + ' = ' + str(payload[i]))
                    
                    while i < payloadLength:
                        
                        while payload[i] == '55':
                            i = i + 1

                        code = payload[i]

                        if (code == 'd0'):
                            print("Headset connected!")
                            self._connected = True

                        elif (code == 'd1'):
                            print("Headset not found, reconnecting")
                            self.connect()

                        elif (code == 'd2'):
                            print("Disconnected!")
                            self.connect()

                        elif (code == 'd3'):
                            print("Headset denied operation!")

                        elif (code == "d4"):
                            print("Headset denied operation!")

                        elif (code == '02'): # Poor Signal
                            i = i + 1
                            self._poorSignal = int(payload[i], 16)

                        elif (code == '04'): # Attention
                            i = i + 1
                            self._attention = int(payload[i], 16)

                        elif (code == '05'): # Meditation
                            i = i + 1
                            self._meditation = int(payload[i], 16)

                        elif (code == '16'): # Blink Strength
                            i = i + 1
                            self._blinkStrength = int(payload[i], 16)

                        # elif (code == '80'): # raw value
                        #     i = i + 1
                        #     i = i + 1
                        #     val0 = int(payload[i], 16)
                        #     i = i + 1
                        #     rawValue = val0 * 256 + int(payload[i], 16)
                        #     if rawValue > 32768:
                        #         rawValue = rawValue - 65536

                        #     self._rawValue = rawValue 

                        # elif (code == '83'):
                        #     i = i + 1

                        #     # delta:
                        #     i = i + 1
                        #     self._delta = int(payload[i], 16)

                        #     # theta:
                        #     i = i + 1
                        #     self._theta = int(payload[i], 16)

                        #     # lowAlpha:
                        #     i = i + 1
                        #     self._lowAlpha = int(payload[i], 16)

                        #     # highAlpha:
                        #     i = i + 1
                        #     self._highAlpha = int(payload[i], 16)

                        #     # lowBeta:
                        #     i = i + 1
                        #     self._lowBeta = int(payload[i], 16)

                        #     # highBeta:
                        #     i = i + 1
                        #     self._highAlpha = int(payload[i], 16)

                        #     # lowGamma:
                        #     i = i + 1
                        #     self._lowGamma = int(payload[i], 16)

                        #     # midGamma:
                        #     i = i + 1
                        #     self._midGamma = int(payload[i], 16)

                        else:
                            pass

                        i = i + 1

                    


    def getData(self):
        string = f""" 
-----------------------------------------------------------------
                     Headset Data:
Attention: {self._attention}
Meditation: {self._meditation}
-----------------------------------------------------------------
"""
        return string