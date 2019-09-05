import websockets
import asyncio

class WebsocketServer:
    def __init__(self, log_function):
        self.logFn = log_function
        self._server = None

    def startServer(self, port):
        self.logFn("Websocket Server started on port %s" % (port))

        self._server = asyncio.get_event_loop().run_until_complete(websockets.serve(self.connectionHandler, "localhost", port, reuse_port=True))

    async def stopServer(self):
        self._server.close()
        await self._server.wait_closed()
        self.logFn("Websocket Server stopped")

    async def connectionHandler(self, socket, path):
        self.logFn("Client connected")

        try:
            async for msg in socket:
                print(msg)
                await socket.send(msg)
        except websockets.ConnectionClosedError:
            pass
        finally:
            self.logFn("Client disconnected")