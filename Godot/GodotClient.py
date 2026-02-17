import asyncio

class GodotClient:

    HOST, PORT = "127.0.0.1", 4001

    def __init__(self, ID=int):
        self.data = None
        self.streamWriter = None
        self.streamReader = None 

        self.clientID = f"PYTHON-GodotClient({ID})"

        self._lock = asyncio.Lock()

        asyncio.run(self.start())


    async def start(self):
        await self._lock.acquire()
        try:
            self.streamReader, self.streamWriter = await asyncio.open_connection(self.HOST, self.PORT)
        except Exception() as e:
            print(e)
        finally:
            self._lock.release()

        print("Connected to Godot Server!")

        try:
            self.streamWriter.write(f"Confirmation : {self.clientID}".encode("utf-8"))
            await self.streamWriter.drain()
            print("Printed Dev ID!")
            #connectionConfirm = await self.streamReader.readline()
            #print(f"Server: {connectionConfirm}")
        except Exception() as e:
            print(e)
        finally:
            print("\nClosing the Connection")
            self.streamWriter.close()
            await self.streamWriter.wait_closed()
            print("\nClosed Connection, quiting...")


    def stop(self):
        pass


    def __del__(self):
        pass




