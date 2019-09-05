from PyQt5.QtCore import *
import asyncio
from websocket_server import WebsocketServer

class ServerThread(QThread):
    log = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self._ws = None
        self._loop = None
        self._stopSignal = None

    def __del__(self):
        self.wait()

    def run(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        self._stopSignal = asyncio.get_event_loop().create_future()

        self._ws = WebsocketServer(self.sendLog)
        self._ws.startServer(51116)

        asyncio.get_event_loop().run_until_complete(self.runServer())

    async def runServer(self):
        await self._stopSignal
        await self._ws.stopServer()

    def stopGracefully(self):
        self._stopSignal.set_result(True)

    def stop(self):
        self._loop.call_soon_threadsafe(self.stopGracefully)
        self.wait()

    def sendLog(self, text):
        self.log.emit(text)