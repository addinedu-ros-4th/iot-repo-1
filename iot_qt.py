import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit,QDialog, QApplication, QStackedWidget
from PyQt5.QtCore import QPropertyAnimation, QSize, QThread, pyqtSignal, Qt, QPoint
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from iot_database import Database


import time
import cv2
import requests
from io import BytesIO

class Camera(QThread):
    update = pyqtSignal(QImage)
    
    def __init__(self, parent=None):
        super(Camera, self).__init__(parent)
        self.running = False
        self.cap = cv2.VideoCapture(0)

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

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("login.ui", self)
        self.login.clicked.connect(self.gotoLogin)
        self.passwordfield.setEchoMode(QLineEdit.Password)
        widget.resize(1200, 735) 

    def gotoLogin(self):
        login_screen = LoginScreen()
        widget.addWidget(login_screen)
        widget.setCurrentIndex(1)

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("iot_project.ui", self)
        
        #Camera Thread
        self.camera_thread = Camera()
        self.camera_thread.update.connect(self.updateImage)  
        self.BtnCamera = self.findChild(QPushButton, 'BtnCamera')
        self.BtnCamera.clicked.connect(self.toggleCamera)

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
        
        self.displayImageOnLabel("icon_pictogram/temp.png", self.TempDisplay)
        self.displayImageOnLabel("icon_pictogram/airhumid.png", self.AirHumidDisplay)
        self.displayImageOnLabel("icon_pictogram/ground_humid.png", self.GroundHumidDisplay)
        self.displayImageOnLabel("icon_pictogram/bright.png", self.BrightDisplay)
        self.displayImageOnLabel("icon_pictogram/height.png", self.HeightDisplay)
        self.displayImageOnLabel("icon_pictogram/camera.png", self.CamerDisplay)

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

    #connect table with DB
    def DisplaySensorLog(self):
        iot_db = Database("iot-project.czcywiaew4o2.ap-northeast-2.rds.amazonaws.com", 3306, "admin", "qwer1234", "iot_project")
        iot_db.connect()

        df = iot_db.watch_log()

        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setHorizontalHeaderLabels(df.columns)

        for row in range(len(df)):
            for col in range(len(df.columns)):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(df.iloc[row, col])))

        iot_db.close()

    # #connect table with DB (T.B.D)
    # def DisplaySensorLog(self, selected_date):
    #     iot_db = Database("iot-project.czcywiaew4o2.ap-northeast-2.rds.amazonaws.com", 3306, "admin", "**", "iot_project")
    #     iot_db.connect()

    #     df = iot_db.watch_log(selected_date)  

    #     self.tableWidget.setRowCount(len(df))
    #     self.tableWidget.setColumnCount(len(df.columns))
    #     self.tableWidget.setHorizontalHeaderLabels(df.columns)

    #     for row in range(len(df)):
    #         for col in range(len(df.columns)):
    #             self.tableWidget.setItem(row, col, QTableWidgetItem(str(df.iloc[row, col])))

    #     iot_db.close()
            
    #Camera Method
    def closeEvent(self, event):
        if self.camera_thread.isRunning():
            self.camera_thread.stop()
        super(LoginScreen, self).closeEvent(event)            

    def toggleCamera(self):
        if self.camera_thread.isRunning():
            self.camera_thread.stop()
            self.camera_thread.wait()  
            self.BtnCamera.setText("Plant 1 \n On")
            self.image_label.setPixmap(self.defaultImage)
            self.camera_thread = Camera()  
            self.camera_thread.update.connect(self.updateImage)
        else:
            self.camera_thread.start()
            self.BtnCamera.setText("Plant 1 \n Off")

    def updateImage(self, qt_image):
        self.image_label = self.findChild(QLabel, 'VisionLabel') 
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    #Resizing Method
    def onLogButtonClicked(self):
        if not self.expanded:
            self.parentWidget().resize(1811, 735)  
            self.expanded = True
        else:
            self.parentWidget().resize(1200, 735)  
            self.expanded = False

    #Calender Method
    def onDateSelected(self):
        selected_date = self.calender.selectedDate()
        self.DateField.setText(selected_date.toString("yyyy-MM-dd"))
        # self.DisplaySensorLog(selected_date) ****set with TBD method

    #png upload
    def displayImageOnLabel(self, imagePath, labelWidget):
        pixmap = QPixmap(imagePath)
        pixmap = pixmap.scaled(labelWidget.width(), labelWidget.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
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

