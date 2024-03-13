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
from datetime import datetime


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

class SensorManager(threading.Thread):
    def __init__(self, port, baudrate, callbacks):
        threading.Thread.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.callbacks = callbacks 
        self.running = False

    def run(self):
        self.running = True
        ser = serial.Serial(self.port, self.baudrate, timeout=1)
        iot_db = Database("iot-project.czcywiaew4o2.ap-northeast-2.rds.amazonaws.com", 3306, "admin", "qwer1234", "iot_project")
        iot_db.connect()
        try:
            while self.running:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').rstrip()
                    try:
                        data = json.loads(line)
                        with open("serial_data.json", "w") as file:
                            json.dump(data, file, indent=4)
                        for sensor_id, callback in self.callbacks.items():
                            now = datetime.now()
                            time_stamp = now.strftime('%Y-%m-%d %H:%M:%S')
                            sensor_data = (time_stamp, sensor_id, data[sensor_id])
                            iot_db.insert_sensor_data(sensor_data)
                            sensor_data_id, event, command = iot_db.check_event(time_stamp, sensor_id, data[sensor_id])
                            if event is not None:
                                camera_image_path = f"capture_data/{time_stamp}.jpg"
                                event_log = (sensor_data_id, time_stamp, event, command, camera_image_path)
                                iot_db.insert_event_log(event_log)
                                
                        # 모든 콜백을 실행
                            if sensor_id in data:
                                callback(data)
                    except json.JSONDecodeError:
                        print(f"JSON decode error:", line)
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
    updateGroundHumidVal_1_Signal = pyqtSignal(str)
    updateGroundHumidVal_2_Signal = pyqtSignal(str)
    updateBrightValSignal = pyqtSignal(str)
    updateHeighttVal_1_Signal = pyqtSignal(str)
    updateHeighttVal_2_Signal = pyqtSignal(str)

    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("../iot-repo-1/iot_project.ui", self)

        #test actuator dict
        self.commands = {}
        self.image_label = self.findChild(QLabel, 'VisionLabel')
        self.active_camera_thread = None
        
        #Camera thread setting
        self.camera_thread1 = Camera(0)  
        self.camera_thread2 = Camera(3)
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
        self.defaultImage = QPixmap('/home/ryu/amr_ws/arduino/iot-repo-1/icon_pictogram/smart_farm.png')

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
        self.tableWidget = self.findChild(QtWidgets.QTableWidget,'tableWidget')
        self.DisplaySensorLog()

        #Table connect with QlineEdit
        self.TempVal = self.findChild(QLineEdit, 'TempVal')
        self.AirHumidVal = self.findChild(QLineEdit, 'AirHumidVal')
        self.GroundHumidVal = self.findChild(QLineEdit, 'GroundHumidVal')
        self.GroundHumidVal_2 = self.findChild(QLineEdit, 'GroundHumidVal_2')
        self.BrightVal = self.findChild(QLineEdit, 'BrightVal')
        self.HeightVal_1 = self.findChild(QLineEdit, 'HeightVal')
        self.HeightVal_2 = self.findChild(QLineEdit, 'HeightVal_2')

        self.tableWidget.cellClicked.connect(self.onTableWidgetCellClicked)

        self.startSensorThreads()

    def updateBright(self, value):
        self.BrightVal.setText(value)
 
    def updateTempVal(self, value):
        self.TempVal.setText(value)
 
    def updateAirHumid(self, value):
        self.AirHumidVal.setText(value)
 
    def updateGndHumid_1(self, value):
        self.GroundHumidVal.setText(value)

    def updateGndHumid_2(self, value):
        self.GroundHumidVal_2.setText(value)

    def updateHeight_1(self, value):
        self.HeightVal_1.setText(value)

    def updateHeight_2(self, value):
        self.HeightVal_2.setText(value)

    def startSensorThreads(self):
        # 센서별 콜백 함수들을 딕셔너리에 정의
        callbacks = {
            "air_temp": self.temp_control,
            "air_humi": self.airhum_control,
            "psoil_humi1": self.Gnd_hum_1_control,
            "psoil_humi2": self.Gnd_hum_2_control,
            "distance1": self.Height_1_control,
            "distance2": self.Height_2_control,
            "pledval": self.bright_control
        }

        # 단일 SensorManager 인스턴스 생성
        self.sensorManager = SensorManager('/dev/ttyACM2', 9600, callbacks)
        self.sensorManager.start()

        # UI 업데이트용 신호 연결
        self.updateTempValSignal.connect(self.updateTempVal)
        self.updateAirHumidValSignal.connect(self.updateAirHumid)
        self.updateGroundHumidVal_1_Signal.connect(self.updateGndHumid_1)
        self.updateGroundHumidVal_2_Signal.connect(self.updateGndHumid_2)
        self.updateHeighttVal_1_Signal.connect(self.updateHeight_1)
        self.updateHeighttVal_2_Signal.connect(self.updateHeight_2)
        self.updateBrightValSignal.connect(self.updateBright)

    def temp_control(self, data):
        temp_value = data["air_temp"] 
        self.updateTempValSignal.emit(str(temp_value))
        self.sendCommandToArduino()

    def airhum_control(self, data):
        airhum_value = data["air_humi"]  

        if airhum_value > 45 :
            self.commands["servor1"] = 'on'
            self.commands["propeller"] = 'on'
        else :
            self.commands["servor"] = 'off'
            self.commands["propeller"] = 'off'
        
        self.updateAirHumidValSignal.emit(str(airhum_value))
        self.sendCommandToArduino() 
        
    def Gnd_hum_1_control(self, data):
        GND1_value = data["psoil_humi1"]  

        if GND1_value < 20 :
            self.commands["water"] = 'on'
        else :
            self.commands["water"] = 'off'
        self.updateGroundHumidVal_1_Signal.emit(str(GND1_value)) 
        self.sendCommandToArduino()

    def Gnd_hum_2_control(self, data):
        GND2_value = data["psoil_humi2"]  
        self.updateGroundHumidVal_2_Signal.emit(str(GND2_value)) 
        self.sendCommandToArduino()

    def Height_1_control(self, data):
        height1_value = data["distance1"] 
        self.updateHeighttVal_1_Signal.emit(str(height1_value)) 
        self.sendCommandToArduino()

    def Height_2_control(self, data):
        height2_value = data["distance2"] 
        self.updateHeighttVal_2_Signal.emit(str(height2_value)) 
        self.sendCommandToArduino()

    def bright_control(self, data):
        # logic
        light = data["pledval"]
        if light > 30: 
            self.commands['led'] = 'on'
        else :
            self.commands['led'] = 'off'
        # UI update
        self.updateBrightValSignal.emit(str(light))
        # transmitte
        self.sendCommandToArduino()

    def sendCommandToArduino(self):
        command_json = json.dumps(self.commands) + '\n'
        with open("emit_data.json", "w") as file:
            json.dump(self.commands, file, indent=4) 
        with serial.Serial('/dev/ttyACM2', 9600, timeout=1) as ser:
            ser.write(command_json.encode())

    def stopSensorThreads(self):
        if self.sensorManager and self.sensorManager.is_alive():
            self.sensorManager.stop()

    # #tablewidget with qlinedit
    # def onTableWidgetCellClicked(self, row, column):
    #     time_column_index = 0

    #     if column == time_column_index:
    #         # temp_column_index = 1
    #         # temp_value = self.tableWidget.item(row, temp_column_index).text()
    #         # self.TempVal.setText(temp_value)

    #         # air_hum_column_index = 2
    #         # air_hum_value = self.tableWidget.item(row, air_hum_column_index).text()
    #         # self.AirHumidVal.setText(air_hum_value)

    #         # gnd_hum_column_index = 3
    #         # gnd_hum_value = self.tableWidget.item(row, gnd_hum_column_index).text()
    #         # self.GroundHumidVal.setText(gnd_hum_value)

    #         # bright_column_index = 4
    #         # bright_value = self.tableWidget.item(row, bright_column_index).text()
    #         # self.BrightVal.setText(bright_value)

    #         # # T.B.D(수수깡높이측정)
    #         # # height_column_index = 5
    #         # # height_value = self.tableWidget.item(row, height_column_index).text()
    #         # # self.HeightVal.setText(height_value)

    #         camera_image_column_index = 1
    #         image_path = self.tableWidget.item(row, camera_image_column_index).text()
    #         pixmap = QPixmap(image_path)
    #         self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    def onTableWidgetCellClicked(self, row, column):
        time_column_index = 0

        if column == time_column_index:
            camera_image_column_index = 1
            item = self.tableWidget.item(row, camera_image_column_index)

            if item is not None:
                image_path = item.text()
                pixmap = QPixmap(image_path)
                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


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
                other_button.setText(f"Plant {plant_number if plant_number == 1 else 2} \n on")
                self.image_label.setPixmap(self.defaultImage.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                other_button.show()

            camera_thread_to_toggle.start()
            self.active_camera_thread = camera_thread_to_toggle
            button.setText(f"Plant {plant_number} \n On")
            other_button.hide()
            self.BtnCapture.show()
    
    def startCameraThreads(self):
        # 카메라 스레드 시작 로직
        if self.camera_thread1 and not self.camera_thread1.isRunning():
            self.camera_thread1.start()
        if self.camera_thread2 and not self.camera_thread2.isRunning():
            self.camera_thread2.start()

    def stopCameraThreads(self):
        # 카메라 스레드 중단 로직
        if self.camera_thread1 and self.camera_thread1.isRunning():
            self.camera_thread1.stop()
            self.camera_thread1.wait()
        if self.camera_thread2 and self.camera_thread2.isRunning():
            self.camera_thread2.stop()
            self.camera_thread2.wait()
        self.image_label.setPixmap(self.defaultImage.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
       

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
            iot_db = Database("iot-project.czcywiaew4o2.ap-northeast-2.rds.amazonaws.com", 3306, "admin", "qwer1234", "iot_project")
            iot_db.connect()
            now = datetime.now()
            time_stamp = now.strftime('%Y-%m-%d %H:%M:%S')
            event = "capture"
            command = "capture"
            camera_image_path = f"capture_data/{time_stamp}.jpg"
            log = (None, time_stamp, event, command, camera_image_path)
            iot_db.insert_capture_log(log)
            iot_db.close()

    def updateImage(self, qt_image):
        if self.active_camera_thread and self.active_camera_thread.isRunning():
            self.image_label = self.findChild(QLabel, 'VisionLabel') 
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        else:
            # 카메라 스레드가 실행되지 않을 때 기본 이미지 표시
            self.image_label.setPixmap(self.defaultImage)

    #Resizing Method
    def onLogButtonClicked(self):
        if not self.expanded:
            self.parentWidget().resize(1811, 735)
            self.expanded = True
            self.LogButton.setText("Event Log \n Off")
            # 스레드 시작 로직을 여기에 추가
            self.stopSensorThreads()
            
            self.stopCameraThreads()

        else:
            self.parentWidget().resize(1200, 735)
            self.expanded = False
            self.LogButton.setText("Event Log \n On")
            # 스레드 중단 로직을 여기에 추가
            self.startSensorThreads()
            self.startCameraThreads()

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

