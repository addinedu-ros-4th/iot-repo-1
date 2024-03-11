import socket
import threading
import json
from iot_database import Database

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                try:
                    data_dict = json.loads(data.decode('utf-8'))

                    if "selected_date" in data_dict:  # Qt data
                        self.process_db_query(data_dict, client_socket)

                    else:
                        # if not JSON, ESP32 data
                        self.process_sensor_data_from_esp(data.decode('utf-8'))
                except Exception as e:
                    print(e)

        finally:
            client_socket.close()

    def process_db_query(self, data_dict, client_socket):
        iot_db = Database("iot-project.czcywiaew4o2.ap-northeast-2.rds.amazonaws.com", 3306, "admin", "qwer1234", "iot_project")
        iot_db.connect()
        df = iot_db.watch_log(data_dict["selected_date"])
        df_json = df.to_json(orient='records')

        with open("server_data.json", "w") as file:
            file.write(df_json)

        client_socket.sendall(df_json.encode('utf-8'))

    # JSON type sensor data(option)
    def process_sensor_data(self, data_dict):
        pass

    def process_sensor_data_from_esp(self, data_str):
        print(f"Received data from ESP32: {data_str}")

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    server = Server('172.30.1.50', 8080)
    server.start_server()
