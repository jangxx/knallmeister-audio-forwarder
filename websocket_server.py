import websockets
import asyncio

class WebsocketServer:
    def __init__(self, log_function):
        self.logFn = log_function
        self._server = None
        self._clients = set()

    def startServer(self, port):
        self.logFn("Websocket Server started on port %s" % (port))

        self._server = asyncio.get_event_loop().run_until_complete(websockets.serve(self.connectionHandler, "localhost", port))

    async def stopServer(self):
        self._server.close()
        await self._server.wait_closed()
        self.logFn("Websocket Server stopped")

    async def connectionHandler(self, socket, path):
        self.logFn("Client connected")

        try:
            async for msg in socket:
                if msg == "register":
                    self._clients.add(socket)
                elif msg == "discover":
                    await socket.send("success")

        except websockets.ConnectionClosedError:
            pass
        finally:
            self._clients.discard(socket)
            self.logFn("Client disconnected")

    async def sendToConnected(self, data):
        if self._clients:
            await asyncio.wait([ socket.send(data) for socket in self._clients ])