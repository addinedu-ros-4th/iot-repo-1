from iot_database import Database

import socket
import threading
import json
from iot_database import Database

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            try:
                data_dict = json.loads(data.decode('utf-8'))

                if "selected_date" in data_dict:  # Qt data
                    process_db_query(data_dict, client_socket)

            except json.JSONDecodeError:
                # if not JSON, ESP32 data
                process_sensor_data_from_esp(data.decode('utf-8'))

            except ConnectionResetError:
                print("Client disconnected unexpectedly.")

    finally:
        client_socket.close()

def process_db_query(data_dict, client_socket):
    iot_db = Database("iot-project.czcywiaew4o2.ap-northeast-2.rds.amazonaws.com", 3306, "admin", "qwer1234", "iot_project")
    iot_db.connect()
    df = iot_db.watch_log(data_dict["selected_date"])
    df_json = df.to_json(orient='records')

    if df.empty:
        # 데이터가 없으면 빈 DataFrame을 JSON 형태로 변환
        df_json = df.to_json(orient='records')
    else:
        df_json = df.to_json(orient='records')

    with open("server_data.json", "w") as file:
        file.write(df_json)

    client_socket.sendall(df_json.encode('utf-8'))

# JSON type sensor data(option)
def process_sensor_data(data_dict):
   pass


def process_sensor_data_from_esp(data_str):

    print(f"Received data from ESP32: {data_str}")

def start_server():
    host = '172.30.1.9'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()


