from PyQt5.QtWidgets import *
from ui_mainwindow import Ui_MainWindow
from main_thread import ServerThread
import audio_capture
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)
        self.serverThread = None

        self.startButton.clicked.connect(self.startServer)

        audioDevices, deviceSelected = audio_capture.getDevices()

        for d in audioDevices:
            self.inputSelect.addItem(d["name"], d)

        self.inputSelect.setCurrentIndex(deviceSelected)

        self.outputBox.append("Select the device of which you want to forward audio above and then click on 'Start'.")

    def startServer(self, checked):
        if self.serverThread:
            return

        deviceIndex = self.inputSelect.currentData()["index"]

        # print("startServer with device %s" % (deviceIndex))

        self.serverThread = ServerThread(deviceIndex)
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
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    code = app.exec_()
    # audio_capture.close()
    sys.exit(code)