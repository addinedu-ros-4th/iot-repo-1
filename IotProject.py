import sys
from PyQt5 import uic
import cv2, imutils
import time
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice  # QIODevice를 import 추가
from PyQt5.QtWidgets import QApplication, QMainWindow
import serial
import time

from_class = uic.loadUiType("/home/ryu/amr_ws/arduino/iot-repo-1/IotProject.ui")[0]


class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initSerial()
       

import serial
import time

def main():
    port = "/dev/ttyACM0" 
    baudrate = 9600
    ser = serial.Serial(port, baudrate, timeout=1)

    button_count = []  

    try:
        while True:
            if ser.inWaiting() > 0:
                line = ser.readline().decode('utf-8').rstrip()
                if line.isdigit():  
                    button_count.append(int(line))
                    # print("Total button presses:", button_count)
    except KeyboardInterrupt:
        print("Program stopped")
    finally:
        ser.close()

if __name__ == "__main__":
    main()

