from PyQt5.QtWidgets import *
from ui_mainwindow import Ui_MainWindow
import websocket_server
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)

        self.startButton.clicked.connect(self.startServer)

    def startServer(self, checked):
        print("Start server")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())