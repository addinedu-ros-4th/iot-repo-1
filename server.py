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
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
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

    def send_to_esp32(self,process_code):
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

    

    def qt_request_to_db(self):
        #ex) date sensor data
        self.db.connect()
        pass

    def qt_request_to_adu(self):
        #ex) error message
        server_address = ('localhost', 8080)

        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # 서버에 연결
            sock.connect(server_address)

            # 데이터를 받을 버퍼 크기 설정
            buffer_size = 1024

            # 데이터 받기
            received_data = sock.recv(buffer_size)

            # 받은 데이터 출력
            print("Received data:", received_data.decode())

        finally:
                # 소켓 닫기
            sock.close()
        pass
    
    def db_send_to_qt(self):
        self.db.watch_log()

    
    def adu_send_to_db(self):
        self.db.connect()
        
        pass


    def adu_send_to_qt(self):
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').rstrip()  # 시리얼 포트에서 한 줄 읽기
            try:
                data = json.loads(line)  # JSON 문자열을 파이썬 딕셔너리로 변환
                # 받은 데이터 출력
                print("Temperature:", data["temperature"])
                print("Humidity:", data["humidity"])
                print("Soil Moisture 1:", data["soil_1"])
                print("Soil Moisture 2:", data["soil_2"])
                print("Light Level:", data["led"])
                print("Distance:", data["distance"])
                print("Tank Water Level:", data["tank"])
                print("Humidity Water Level:", data["humi"])
                self.temperature = data["temperature"]
                self.humidity = data["humidity"]
                self.soil_1 = data["soil_1"]
                self.soil_2 = data["soil_2"]
                self.led = data["led"]
                self.distance = data["distance"]
                self.tank = data["tank"]
                self.humi = data["humi"]
                
            except json.JSONDecodeError:
                print("JSON decode error:", line)
            
        pass




    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            client_thread_qt = threading.Thread(target=self.qt_client, args=(client_socket,))
            client_thread_qt.start()
            client_thread_adu= threading.Thread(target=self.adu_client, args=(client_socket,))
            client_thread_adu.start()


    
if __name__ == "__main__":
    
    server = Server(8080)
    server.start_server()
