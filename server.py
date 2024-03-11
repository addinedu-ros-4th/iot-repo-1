import socket
import threading
import json
import iot_database as idb
import subprocess
import re
import iot_qt as iqt
import multiprocessing
import serial



def get_ip_address(interface):
    try:
        # ifconfig 명령 실행
        output = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
        # IP 주소를 찾기 위한 정규 표현식
        ip_pattern = r"inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        # 결과에서 IP 주소 찾기
        match = re.search(ip_pattern, output)
        if match:
            ip_address = match.group(1)
            return ip_address
        else:
            return None
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return None
    

class Server:
    def __init__(self, port):
        self.host = get_ip_address("wlo1")
        self.port = port
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # 포트 번호는 시스템에 따라 달라질 수 있음
        self.db = idb.Database("localhost", 3306, "root", "amrbase1", "iot_project")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}")


    def qt_client(self, qt_socket):
        try:
            while True:
                data = qt_socket.recv(1024)
                if not data:
                    break

                try:
                    data_dict = json.loads(data.decode('utf-8'))

                    if "selected_date" in data_dict:  # Qt data
                        self.process_db_query(data_dict, qt_socket)

                    else:
                        # if not JSON, ESP32 data
                        self.process_sensor_data_from_esp(data.decode('utf-8'))
                except Exception as e:
                    print(e)

        finally:
            qt_socket.close()


    def adu_client(self,adu_socket):
        pass



    def process_db_query(self, data_dict, client_socket):
        iot_db = idb.Database("iot-project.czcywiaew4o2.ap-northeast-2.rds.amazonaws.com", 3306, "admin", "qwer1234", "iot_project")
        iot_db.connect()
        df = iot_db.watch_log(data_dict["selected_date"])
        df_json = df.to_json(orient='records')

        with open("server_data.json", "w") as file:
            file.write(df_json)

        client_socket.sendall(df_json.encode('utf-8'))

    # JSON type sensor data(option)
    def process_sensor_data(self, data_dict):
        print(data_dict)

    def process_sensor_data_from_esp(self, data_str):
        print(f"Received data from ESP32: {data_str}")
        esp32_ip = '192.168.0.39'
        esp32_port = 8080
        # 소켓 생성
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # ESP32에 연결
        client_socket.connect((esp32_ip, esp32_port))

        # 정수 1을 바이트로 변환하여 ESP32로 전송
        client_socket.sendall(b'1')

        # 소켓 닫기
        client_socket.close()


    def qt_request_to_db(self,client_socket):
        #ex) date sensor data
        data = client_socket.recv(1024).decode()
        self.db.connect()
        client_socket.close()


    def qt_request_to_adu(self,client_socket):
        data = client_socket.recv(1024).decode()
        self.ser.write(data)
        
    
    def db_send_to_qt(self):
        self.db.watch_log()

    def process_adu_data(self):
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').rstrip()  # 시리얼 포트에서 한 줄 읽기
            try:
                data = json.loads(line)  # JSON 문자열을 파이썬 딕셔너리로 변환
                return data
                
                # 받은 데이터 출력
               
                
            except json.JSONDecodeError:
                print("JSON decode error:", line)    
                
    def adu_send_to_db(self):
        self.db.connect()
        data = self.process_adu_data()
        self.temperature = data["temperature"]
        self.humidity = data["humidity"]
        self.soil_1 = data["soil_1"]
        self.soil_2 = data["soil_2"]
        self.led = data["led"]
        self.distance = data["distance"]
        self.tank = data["tank"]
        self.humi = data["humi"]
        
        


    def adu_send_to_qt(self):
        data = self.process_adu_data()
        




    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            client_thread_qt = threading.Thread(target=self.qt_client, args=(client_socket,))
            client_thread_adu= threading.Thread(target=self.adu_client, args=(client_socket,))

            client_thread_qt.start()
            client_thread_adu.start()


    
if __name__ == "__main__":
    
    server = Server(8080)
    server.start_server()
