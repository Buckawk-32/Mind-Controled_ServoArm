import asyncio

class GodotClient:

    HOST, PORT = "127.0.0.1", 4001

    def __init__(self, ID=int):
        self.data = None
        self.streamWriter = None
        self.streamReader = None 

        self.clientID = f"PYTHON-GodotClient({ID})"
        self.isClientConnected = False

        self._lock = asyncio.Lock()

        asyncio.run(self.start())

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
            await self.testCommunication()
        except Exception as e:
            print(e)    
        finally:
            self._lock.release()
            print("-- Cleaning Client!\n")
            await self.stop()


# Functions that can be used for the main Communication Loop
    async def testCommunication(self):
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
                    self.streamWriter.write(f"MSG: {usrInput}".encode("utf-8"))
                    await self.streamWriter.drain()


# Handling Stopping Connections and Cleaning
    async def stop(self):
        await self._lock.acquire()
        try:
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



