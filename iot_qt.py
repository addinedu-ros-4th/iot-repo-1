import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit,QDialog, QApplication, QStackedWidget
from PyQt5.QtCore import QPropertyAnimation, QSize, QThread, pyqtSignal, Qt, QPoint, QDate, pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from iot_database import Database
import os
import time
import cv2
import requests
from io import BytesIO, StringIO
import json
import pandas as pd
import serial
import threading


class Camera(QThread):
    update = pyqtSignal(QImage)
    
    def __init__(self, camera_index=0, parent=None):
        super(Camera, self).__init__(parent)
        self.camera_index = camera_index
        self.running = False
        self.cap = cv2.VideoCapture(self.camera_index)

    def run(self):
        self.running = True
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.update.emit(qt_image)
            time.sleep(0.1)

    def stop(self):
        self.running = False
        self.cap.release()  
        self.quit()     

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            if not os.path.exists('capture_data'):
                os.makedirs('capture_data')

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            filename = f"capture_data/{timestamp}.jpg"

            cv2.imwrite(filename, frame)
            print(f"Image saved: {filename}")  

class SensorThread(threading.Thread):
    def __init__(self, port, baudrate, update_signal, sensor_id, callback):
        threading.Thread.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.update_signal = update_signal
        self.sensor_id = sensor_id
        self.callback = callback
        self.running = False

    def run(self):
        self.running = True
        ser = serial.Serial(self.port, self.baudrate, timeout=1)

        try:
            while self.running:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    try:
                        data = json.loads(line)
                        # callback을통해 센서에게 명령전달
                        self.callback(data)
                    except json.JSONDecodeError:
                        print(f"JSON decode error in sensor {self.sensor_id}:", line)
        finally:
            ser.close()

    def stop(self):
        self.running = False

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("../iot-repo-1/login.ui", self)
        self.login.clicked.connect(self.gotoLogin)
        self.passwordfield.setEchoMode(QLineEdit.Password)
        widget.resize(1200, 735) 


    def gotoLogin(self):
        login_screen = LoginScreen()
        widget.addWidget(login_screen)
        widget.setCurrentIndex(1)

class LoginScreen(QDialog):

    updateTempValSignal = pyqtSignal(str)
    updateAirHumidValSignal = pyqtSignal(str)
    updateGroundHumidValSignal = pyqtSignal(str)
    updateBrightValSignal = pyqtSignal(str)

    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("../iot-repo-1/iot_project.ui", self)
        
        #Camera thread setting
        self.camera_thread1 = Camera(0)  
        self.camera_thread2 = Camera(2)
        self.camera_thread1.update.connect(self.updateImage)  
        self.camera_thread2.update.connect(self.updateImage)
        self.BtnCamera = self.findChild(QPushButton, 'BtnCamera')
        self.BtnCamera_2 = self.findChild(QPushButton, 'BtnCamera_2')
        self.BtnCamera.clicked.connect(lambda: self.toggleCamera(self.camera_thread1, self.camera_thread2, self.BtnCamera, self.BtnCamera_2, 1))
        self.BtnCamera_2.clicked.connect(lambda: self.toggleCamera(self.camera_thread2, self.camera_thread1, self.BtnCamera_2, self.BtnCamera, 2))

        #capture
        self.BtnCapture = self.findChild(QPushButton, 'BtnCapture')
        self.BtnCapture.hide()
        self.BtnCapture.clicked.connect(self.captureImage) 
        
        #Pixmap default setting and Camera connecting
        image_url = "https://blogfiles.pstatic.net/MjAxNzEwMjJfMTEx/MDAxNTA4Njc4Njc1Njc3.C85V2pebYoO1miLHHj2sy_AAHZucqI3xs6GItxNk-k8g.4S5V4XrzkeGgT7znHjFmchmdceDOTLuEGO-D-8DWmY0g.PNG.verdicorporation/%EC%8A%A4%EB%A7%88%ED%8A%B8%ED%8C%9C.png"
        response = requests.get(image_url)
        image = QImage()
        image.loadFromData(response.content)
        self.defaultImage = QPixmap(image)

        #resizing Pixmap
        self.VisionLabel.setPixmap(self.defaultImage)
        self.expanded = False
        self.LogButton.clicked.connect(self.onLogButtonClicked)

        #Calender Data
        self.calender = self.findChild(QCalendarWidget, 'calender')
        self.DateField = self.findChild(QLabel, 'DateField')
        self.calender.selectionChanged.connect(self.onDateSelected)

        #png upload
        self.TempDisplay = self.findChild(QLabel, 'TempDisplay')
        self.AirHumidDisplay = self.findChild(QLabel, 'AirHumidDisplay')
        self.GroundHumidDisplay = self.findChild(QLabel, 'GroundHumidDisplay')
        self.BrightDisplay = self.findChild(QLabel, 'BrightDisplay')
        self.AirHumidDisplay = self.findChild(QLabel, 'AirHumidDisplay')
        self.HeightDisplay = self.findChild(QLabel, 'HeightDisplay')
        self.CamerDisplay = self.findChild(QLabel, 'CamerDisplay')
        
        self.displayImageOnLabel("/home/ryu/amr_ws/arduino/iot-repo-1/icon_pictogram/temp.png", self.TempDisplay)
        self.displayImageOnLabel("/home/ryu/amr_ws/arduino/iot-repo-1/icon_pictogram/airhumid.png", self.AirHumidDisplay)
        self.displayImageOnLabel("/home/ryu/amr_ws/arduino/iot-repo-1/icon_pictogram/ground_humid.png", self.GroundHumidDisplay)
        self.displayImageOnLabel("/home/ryu/amr_ws/arduino/iot-repo-1/icon_pictogram/bright.png", self.BrightDisplay)
        self.displayImageOnLabel("/home/ryu/amr_ws/arduino/iot-repo-1/icon_pictogram/height.png", self.HeightDisplay)
        self.displayImageOnLabel("/home/ryu/amr_ws/arduino/iot-repo-1/icon_pictogram/camera.png", self.CamerDisplay)

        #pannel design
        button_direction_mapping = {
            'Temp': ['Max', 'Min'],
            'AirHum': ['Max', 'Min'],
            'GndHum': ['Max', 'Min'],
            'Bright': ['Max', 'Min']
        }

        for sensor_type, directions in button_direction_mapping.items():
            for direction in directions:
                button_name = f"{sensor_type}{direction}"
                button = self.findChild(QPushButton, button_name)
                if button:
                    icon_direction = 'up' if direction == 'Max' else 'down'
                    button.setIcon(self.createTriangleIcon(icon_direction))
        
        #DB connection on tableWidget
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.DisplaySensorLog()

        #Table connect with QlineEdit
        self.TempVal = self.findChild(QLineEdit, 'TempVal')
        self.AirHumidVal = self.findChild(QLineEdit, 'AirHumidVal')
        self.GroundHumidVal = self.findChild(QLineEdit, 'GroundHumidVal')
        self.BrightVal = self.findChild(QLineEdit, 'BrightVal')
        self.HeightVal = self.findChild(QLineEdit, 'HeightVal')

        self.tableWidget.cellClicked.connect(self.onTableWidgetCellClicked)

        #signal test
        self.updateTempValSignal.connect(self.updateTempVal)
        self.startSensorThreads()

    # Update the TempVal QLineEdit with the new value   (Hard Coding해야함 각각 센서 전부) 
    def updateTempVal(self, value):
        
        self.TempVal.setText(value)

    def startSensorThreads(self):
        # temp thred init
        self.tempSensorThread = SensorThread('/dev/ttyACM0', 9600, self.updateTempValSignal, "temperature", self.processSensorData)
        self.tempSensorThread.start()
        self.updateTempValSignal.connect(self.updateTempVal)

        # airhum thred init
        # self.airHumidSensorThread = SensorThread('/dev/ttyACM0', 9600, self.updateAirHumidValSignal, "humidity")
        # self.airHumidSensorThread.start()
        # self.updateAirHumidValSignal.connect(self.updateAirHumidVal)
        
        #other sensor also follow this format

    def processSensorData(self, data):
        # 여기에 센서 데이터 처리 로직을 추가
        light = data.get("light", 0)
        if light < 5: 
            light = 5
        elif light > 250:
            light = 250
        # UI에 데이터 업데이트
        self.updateTempValSignal.emit(str(light))
        # 명령 전송 로직
        self.sendCommandToArduino({"led": light})

    def sendCommandToArduino(self, command):
        command_json = json.dumps(command) + '\n'
        with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as ser:
            ser.write(command_json.encode())

    def stopSensorThreads(self):
    # TempVal 스레드 중단 로직
        if self.tempSensorThread and self.tempSensorThread.is_alive():
            self.tempSensorThread.stop()

        # 다른 센서 스레드 중단 로직도 추가
        # ...

    def saveDataToJsonFile(self, data):
        with open("serial_data.json", "w") as file:
            json.dump(data, file, indent=4)

    #tablewidget with qlinedit
    def onTableWidgetCellClicked(self, row, column):
        time_column_index = 0

        if column == time_column_index:
            temp_column_index = 1
            temp_value = self.tableWidget.item(row, temp_column_index).text()
            self.TempVal.setText(temp_value)

            air_hum_column_index = 2
            air_hum_value = self.tableWidget.item(row, air_hum_column_index).text()
            self.AirHumidVal.setText(air_hum_value)

            gnd_hum_column_index = 3
            gnd_hum_value = self.tableWidget.item(row, gnd_hum_column_index).text()
            self.GroundHumidVal.setText(gnd_hum_value)

            bright_column_index = 4
            bright_value = self.tableWidget.item(row, bright_column_index).text()
            self.BrightVal.setText(bright_value)

            # T.B.D(수수깡높이측정)
            # height_column_index = 5
            # height_value = self.tableWidget.item(row, height_column_index).text()
            # self.HeightVal.setText(height_value)

    #connect table with DB (T.B.D)
    def DisplaySensorLog(self, selected_date=None):
        if selected_date is None:
            selected_date = self.calender.selectedDate()
        
        # Check if selected_date is a QDate and convert to string if necessary
        if isinstance(selected_date, QDate):
            selected_date_str = selected_date.toString("yyyy-MM-dd")
        else:
            selected_date_str = selected_date

        iot_db = Database("iot-project.czcywiaew4o2.ap-northeast-2.rds.amazonaws.com", 3306, "admin", "qwer1234", "iot_project")
        iot_db.connect()

        df = iot_db.watch_log(selected_date_str) 

        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setHorizontalHeaderLabels(df.columns)

        for row in range(len(df)):
            for col in range(len(df.columns)):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(df.iloc[row, col])))

        iot_db.close()
            
    #Camera Method
    def closeEvent(self, event):
        if self.active_camera_thread and self.active_camera_thread.isRunning():
            self.active_camera_thread.stop()
            self.active_camera_thread.wait()

        super(LoginScreen, self).closeEvent(event)          

    def toggleCamera(self, camera_thread_to_toggle, other_camera_thread, button, other_button, plant_number):
        if camera_thread_to_toggle.isRunning():
            camera_thread_to_toggle.stop()
            camera_thread_to_toggle.wait()
            button.setText(f"Plant {plant_number} \n Off")
            other_button.show()
            self.BtnCapture.hide()
            self.create_new_camera_thread(camera_thread_to_toggle.camera_index)

        else:
            if other_camera_thread.isRunning():
                other_camera_thread.stop()
                other_camera_thread.wait()
                other_button.setText(f"Plant {plant_number if plant_number == 1 else 2} Off")
                other_button.show()

            camera_thread_to_toggle.start()
            self.active_camera_thread = camera_thread_to_toggle
            button.setText(f"Plant {plant_number} \n On")
            other_button.hide()
            self.BtnCapture.show()
    
    def create_new_camera_thread(self, camera_index):
        if camera_index == 0:
            self.camera_thread1 = Camera(camera_index)
            self.camera_thread1.update.connect(self.updateImage)
        else:
            self.camera_thread2 = Camera(camera_index)
            self.camera_thread2.update.connect(self.updateImage)

        if self.active_camera_thread.camera_index == camera_index:
            self.active_camera_thread = self.camera_thread1 if camera_index == 0 else self.camera_thread2

    def captureImage(self):
        if self.active_camera_thread is not None:
            self.active_camera_thread.capture_image()

    def updateImage(self, qt_image):
        self.image_label = self.findChild(QLabel, 'VisionLabel') 
        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))
        scaled_pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        self.image_label.setPixmap(scaled_pixmap)

    #Resizing Method
    def onLogButtonClicked(self):
        if not self.expanded:
            self.parentWidget().resize(1811, 735)
            self.expanded = True
            self.LogButton.setText("Event Log \n Off")
            # 스레드 시작 로직을 여기에 추가
            self.stopSensorThreads()

        else:
            self.parentWidget().resize(1200, 735)
            self.expanded = False
            self.LogButton.setText("Event Log \n On")
            # 스레드 중단 로직을 여기에 추가
            self.startSensorThreads()

    #Calender Method
    def onDateSelected(self):
        selected_date = self.calender.selectedDate()
        self.DateField.setText(selected_date.toString("yyyy-MM-dd"))
        self.DisplaySensorLog(selected_date)

    #png upload
    def displayImageOnLabel(self, imagePath, labelWidget):
        pixmap = QPixmap(imagePath)
        pixmap = pixmap.scaled(labelWidget.width(), labelWidget.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        labelWidget.setPixmap(pixmap)

    #control panel desgin
    def createTriangleIcon(self, direction):
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.black)

        if direction == 'up':
            points = QPolygon([
                QPoint(10, 5),
                QPoint(15, 15),
                QPoint(5, 15)
            ])
        elif direction == 'down':
            points = QPolygon([
                QPoint(5, 5),
                QPoint(15, 5),
                QPoint(10, 15)
            ])
        else:
            points = QPolygon() 

        painter.drawPolygon(points)
        painter.end()

        return QIcon(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    welcome = WelcomeScreen()
    widget.addWidget(welcome)
    widget.resize(1200, 735)  
    widget.show()

    sys.exit(app.exec_())

