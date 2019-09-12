from PyQt5.QtCore import *
import asyncio
from websocket_server import WebsocketServer
import numpy as np
from slience_player import SilencePlayer
from multiprocessing import Event

class ServerThread(QThread):
    log = pyqtSignal(str)

    def __init__(self, device, speaker):
        QThread.__init__(self)
        self.device = device

        self._silenceStopEvent = Event()
        self._silencePlayer = SilencePlayer(speaker, self._silenceStopEvent)

        self._ws = None
        self._loop = None
        self._stopSignal = None


    def __del__(self):
        self.wait()

    def run(self):
        self._silencePlayer.start()

        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        self._stopSignal = asyncio.get_event_loop().create_future()

        self._ws = WebsocketServer(self.sendLog)
        self._ws.startServer(51116)

        asyncio.get_event_loop().run_until_complete(self.runServer())

    async def runServer(self):
        # await self._stopSignal

        while not self._stopSignal.done():
            data = self.device.record(samplerate=48000, numframes=512, channels=[0, 1])
            # print(len(data[:,0].astype("float32").tobytes('C')))

            await asyncio.sleep(0) # yield control to asyncio
            await self._ws.sendToConnected(data[:,0].astype("float32").tobytes('C'))

        await self._ws.stopServer()

    def stopGracefully(self):
        self._stopSignal.set_result(True)
        self._silenceStopEvent.set()

    def stop(self):
        self._loop.call_soon_threadsafe(self.stopGracefully)
        self.wait()

    def sendLog(self, text):
        self.log.emit(text)