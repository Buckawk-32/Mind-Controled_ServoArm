import asyncio
import threading

class GodotClient:

    HOST, PORT = "127.0.0.1", 4001

    def __init__(self):
        self.data = None
        self.streamWriter = None
        self.streamReader = None 

        self.clientID = f"PYTHON-GodotClient({self.saveID()})"
        self.isClientConnected = False

        self.handleMsgThread = None

        self._lock = asyncio.Lock()

        asyncio.run(self.start())

    
    def saveID(self):
        usrID = input("What is your ID: ")
        return usrID

# Starting Connection Loop and Connection Confirmation
    async def start(self):
        await self._lock.acquire()
        try:
            self.streamReader, self.streamWriter = await asyncio.open_connection(self.HOST, self.PORT)
        except Exception() as e:
            print(e)
        finally:
            self._lock.release()

        print("-- Connected to Godot Server!")

        try:
            self.streamWriter.write(f"CON: {self.clientID}\r\n".encode("utf-8"))
            await self.streamWriter.drain()
            print("-- Printed Dev ID!")
            connectionConfirm = await self.streamReader.readline()
            print(f"{connectionConfirm.decode("utf-8")}")
        except Exception() as e:
            print(e)
        finally:
            await self.handleConnection()

# Main communication Loop
    async def handleConnection(self):
        await self._lock.acquire()
        try: 
            self.isClientConnected = True
            # await self.testEchoCommunication()
            # await self.testCrossCommunication()
            await self.testListentoServer()
        except Exception as e:
            print(e)    
        finally:
            self._lock.release()
            print("-- Cleaning Client!\n")
            await self.stop()


# Functions that can be used for the main Communication Loop
    async def testEchoCommunication(self):
        while True:
            usrInput = input("> ")
            if usrInput is not None:
                if usrInput == "q":
                    self.streamWriter.write(f"QUIT: {self.clientID}\r\n".encode("utf-8"))
                    await self.streamWriter.drain()
                    print("-- Printed Quit Statement!")
                    quitConfirm = await self.streamReader.readline()
                    print(f"{quitConfirm.decode("utf-8")}")
                    break
                else:
                    self.streamWriter.write(f"MSG: {usrInput}\r\n".encode("utf-8"))
                    await self.streamWriter.drain()


    async def testListentoServer(self):
        while True:
            print("-- Listening to Server Data")
            incomingData = await self.streamReader.readline()
            if incomingData.decode("utf-8").startswith("QUIT"):
                print(f"{incomingData.decode("utf-8")[-4:]}")
                break
            else:
                print(f"{incomingData.decode("utf-8")}")
    

    async def testCrossCommunication(self):
        self.handleMsgThread = threading.Thread(target=self.startAsyncMsgLoop)
        self.handleMsgThread.start()

        while True:
            usrInput = input("> ")
            if usrInput is not None:
                if usrInput == "q":
                    self.handleMsgThread.join()
                    self.streamWriter.write(f"QUIT: {self.clientID}\r\n".encode("utf-8"))
                    await self.streamWriter.drain()
                    print("-- Printed Quit Statement!")
                    quitConfirm = await self.streamReader.readline()
                    print(f"{quitConfirm.decode("utf-8")}")
                    break
                else:
                    self.streamWriter.write(f"MSG: {usrInput}\r\n".encode("utf-8"))
                    await self.streamWriter.drain()
                    

    async def seperateHandleIncomingMsg(self, loop=asyncio.new_event_loop()):
        incomingMsg = await self.streamReader.readline() 
        if incomingMsg.decode("utf-8").startswith("1"):
            print("-- Msg Loop Stopping --")
            loop.stop()
        else:
            print(f"{incomingMsg.decode("utf-8")}")

    def startAsyncMsgLoop(self):
        msgLoop = asyncio.new_event_loop()
        asyncio.set_event_loop(msgLoop)

        msgLoop.create_task(self.seperateHandleIncomingMsg(msgLoop))

        msgLoop.run_forever()
        msgLoop.close()


# Handling Stopping Connections and Cleaning
    async def stop(self):
        await self._lock.acquire()
        try:
            if self.handleMsgThread.is_alive():
                self.handleMsgThread.join()
                print("-- MsgThread -- Closed\n")

            if self.isClientConnected:
                self.data = None
                print("-- Cleared Data... \n")

                self.streamWriter.close()
                await self.streamWriter.wait_closed()
                print("-- StreamWriter -- Connection Closed")
                print("-- StreamReader -- Connection Closed")

                print("-- UnityClient -- Connection Closed")
                self.isClientConnected = False
        except Exception as e:
            print(e)
        finally:
            self._lock.release()
            # exit(1)

    def __del__(self):
        asyncio.run(self.stop())
