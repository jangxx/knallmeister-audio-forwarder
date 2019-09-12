from PyQt5.QtWidgets import *
from ui_mainwindow import Ui_MainWindow
from main_thread import ServerThread
import sys
import soundcard as sc
import multiprocessing

def getDevices():
    devices = []

    for device in sc.all_microphones(include_loopback=True):
        if not device.isloopback:
            continue

        devices.append({
            "name": device.name,
            "device": device,
            "speaker": sc.get_speaker(device.id)
        })

    return devices

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)
        self.serverThread = None

        self.startButton.clicked.connect(self.startServer)

        audioDevices = getDevices()

        for d in audioDevices:
            self.inputSelect.addItem(d["name"], d)

        if len(audioDevices) > 0:
            self.inputSelect.setCurrentIndex(0)
            self.outputBox.append("Select the device of which you want to forward audio above and then click on 'Start'.")
        else:
            self.outputBox.append("No audio devices found. Please install one and then restart the application.")
    
    def startServer(self, checked):
        if self.serverThread:
            return

        device = self.inputSelect.currentData()["device"]
        speaker = self.inputSelect.currentData()["speaker"]

        # print("startServer with device %s" % (deviceIndex))

        self.serverThread = ServerThread(device, speaker)
        self.serverThread.log.connect(self.log)
        self.serverThread.start()
    
        self.startButton.setText("Stop")
        self.inputSelect.setEnabled(False)
        self.startButton.clicked.disconnect()
        self.startButton.clicked.connect(self.stopServer)

    def stopServer(self, checked):
        if not self.serverThread:
            return

        # print("stopServer")

        self.serverThread.stop()
        self.serverThread = None

        self.startButton.setText("Start")
        self.inputSelect.setEnabled(True)
        self.startButton.clicked.disconnect()
        self.startButton.clicked.connect(self.startServer)

    def log(self, text):
        self.outputBox.append(text)

if __name__ == '__main__':
    multiprocessing.freeze_support()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    code = app.exec_()
    sys.exit(code)