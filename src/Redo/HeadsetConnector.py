import serial
import time
import sys
import threading as thread

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


class NeuroPy(object):

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

    callBacksDictionary = {}

    def __init__(self, port = 'COM3', baudRate=115200, devid = "BTHENUM\Dev_C464E3E6E244"):
        if port == None:
            platform = sys.platform
            if platform == "win32":
                port = "COM6"
            elif platform.startswith("linux"):
                port = "/dev/rfcomm0"
            else:
                port = "/dev/cu.MindWaveMobile-SerialPo"

        self.__devid = devid
        self.__serialPort = port
        self.__serialBaudRate = baudRate
        self.__packetsReceived = 0

        self.__parserThread = None
        self.__threadRun = False
        self.__srl = None
        self.__connected = False

    def __del__(self):
        if self.__threadRun == True:
            self.stop()

    def disconnect(self):
        self.__srl.write(DISCONNECT)

    def connect(self):
        if not self.__devid:
            self.__connected = True
            return # Only connect RF devices

        self.__srl.write(CONNECT.encode())

    def start(self):
        if self.__threadRun == True:
            print("Mindwave has already started!")
            return

        if self.__srl == None:
            try:
                self.__srl = serial.Serial(
                    self.__serialPort, self.__serialBaudRate)
            except Exception as e:
                print (str(e))
                return
        else:
            self.__srl.open()

        if self.__devid:
            self.connect()

        self.__packetsReceived = 0
        self.__verbosePacketsReceived = 0
        self.__parserThread = thread.Thread(target=self.__packetParser)
        self.__threadRun = True
        self.__parserThread.start()

    def packetParser(self):
        "packetParser runs continously in a separate thread to parse packets from mindwave and update the corresponding variables"
        while self.__threadRun:
            p1 = self.__srl.read(1).hex()  # read first 2 packets
            p2 = self.__srl.read(1).hex()
            while (p1 != 'aa' or p2 != 'aa') and self.__threadRun:
                p1 = p2
                p2 = self.__srl.read(1).hex()
            else:
                if self.__threadRun == False:
                    break
                # a valid packet is available
                self.__packetsReceived += 1
                payload = []
                checksum = 0
                payloadLength = int(self.__srl.read(1).hex(), 16) #PLENGTH
                #print('payloadLength: ' + str(payloadLength))
                for i in range(payloadLength):
                    tempPacket = self.__srl.read(1).hex()
                    payload.append(tempPacket)
                    checksum += int(tempPacket, 16) #sum every byte in the payload
                checksum = ~checksum & 0x000000ff #take the lowest 8 bits and invert them
                if checksum == int(self.__srl.read(1).hex(), 16): #read the next byte of the package after the payload and check it with the checksum just calculated
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
                            self.__verbosePacketsReceived += 1
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

    def stop(self):
        # Stops a running parser thread
        if self.__threadRun == True:
            self.__threadRun = False
            self.__parserThread.join()
            self.__srl.close()
