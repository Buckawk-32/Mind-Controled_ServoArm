import socket
import threading
import time
import asyncio

class UnityClient:

    HOST, PORT = "10.79.40.170", 25001
    # HOST, PORT = "localhost", 25001
    # HOST, PORT = "192.168.2.149", 25001

    def __init__(self, ID=int):
        self.data = None
        self.devID = f"PYTHON-UnityClient({ID})"

        self.streamWriter = None
        self.streamReader = None

        self._lock = asyncio.Lock()

        asyncio.run(self.start())

    def __del__(self):
        self.stop()

    async def stop(self):
        await self._lock.acquire()
        try:
            self.data = None
            print("Cleared Data...\n")

            self.streamWriter.close()
            await self.streamWriter.wait_closed()
            print("StreamWriter -- Connection Closed")
            print("StreadReader -- Connection Closed")

            print("UnityClient -- Conneciton Closed")
        except Exception as e:
            print(e)
        finally:
            self._lock.release()


    async def start(self):
        await self._lock.acquire()
        try:
            self.streamReader, self.streamWriter = await asyncio.open_connection(self.HOST, self.PORT)
            print("Starting Client...")
        except Exception as e:
            print(e)
        finally:
            self._lock.release()

        print("Connected to UnityServer...")

        try:
            self.streamWriter.write(f"CON: {self.devID}\r\n".encode())
            await self.streamWriter.drain()
            connectionConfirm = await self.streamReader.readline()
            print("\n"+connectionConfirm.decode()+"\n")
        except Exception as e:    
            print(e)
        finally:
            await self.startHandleServerData()
        

    async def startHandleServerData(self):
        try:
            await self.handleData()
        except Exception as e:
            print(e)
        finally:
            await self.stop()
        
    async def handleData(self):
        print("check handleData")
        PATH = f"D:\\NETHIKA\\CODE\\Offical Projects\\Research\\Mind-Controled_ServoArm\\Unity\\DATA\\data-{self.devID}.txt"
        usr = input("> ")

        while True:
            await self._lock.acquire()
            try:
                self.data = await self.streamReader.readline()
                with open(PATH, "w") as file:
                    file.write(f"{self.data.decode()}\n") 
            finally:
                self._lock.release()

            if usr == "q":
                try:
                    self.streamWriter.write(f"QUIT: {self.devID}".encode())
                    await self.streamWriter.drain()

                    quitMsg = await self.streamReader.readline()
                    print(quitMsg.decode())
                except Exception as e:
                    print(e)
                finally:
                    break

        print("Closing Connetion...")

    # async def confirmConnection(self):
    #     self.streamWriter.write(f"CON: {self.devID}".encode())
    #     await self.streamWriter.drain()
    #     connectionConfirm = await self.streamReader.readline()
    #     print("check connectionConfirm")
    #     return connectionConfirm.decode()