import sys
from PyQt5 import uic
import cv2, imutils
import time
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice  # QIODevice를 import 추가
from PyQt5.QtWidgets import QApplication, QMainWindow
import serial

# 나머지 코드 생략


from_class = uic.loadUiType("/home/ryu/amr_ws/arduino/iot-repo-1/IotProject.ui")[0]

# class Camera(QThread):
#     update = pyqtSignal()
    
#     def __init__(self, sec=0, parent = None) :
#         super().__init__()
#         self.main = parent
#         self.running = True

#     def run(self) :

#         while self.running == True :
#             self.update.emit()
#             time.sleep(0.1)

#     def stop(self) :
#         self.running = False

class WindowClass(QMainWindow, from_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.serialPort = QSerialPort(self)
        self.serialPort.setBaudRate(QSerialPort.Baud9600)
        self.serialPort.setPortName("/dev/ttyACM0")

        self.BtnPressTest.clicked.connect(self.BtnWithArd)
        
    def BtnWithArd(self):
        if not self.serialPort.isOpen():
            if not self.serialPort.open(QIODevice.ReadWrite):
                print("Failed to open serial port")
                return
        self.serialPort.write(b'button_pressed\n')



if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec_())
