import serial
import socket
import threading
import mysql

# 아두이노 시리얼 포트 설정
ARDUINO_PORT = '/dev/ttyACM0'  # 아두이노의 시리얼 포트
BAUD_RATE = 9600  # 시리얼 통신 속도

# 데이터베이스 연결 설정
DB_HOST = 'localhost'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_NAME = 'your_database'

# 파이큐티 소켓 통신 설정
PYQT_HOST = '127.0.0.1'
PYQT_PORT = 5000

# 아두이노와 시리얼 통신하는 함수
def read_from_arduino():
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE)
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()  # 아두이노에서 데이터 수신
            print("Received from Arduino:", data)
            save_to_database(data)

# 데이터를 데이터베이스에 저장하는 함수
def save_to_database(data):
    # 데이터 파싱 및 데이터베이스에 저장하는 로직 구현
    # 예: 데이터베이스에 연결하여 INSERT 쿼리 실행
    try:
        conn = mysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = conn.cursor()
        # 여기에 적절한 INSERT 쿼리를 작성하여 데이터베이스에 데이터 저장
        cursor.execute("INSERT INTO your_table_name (data) VALUES (%s)", (data,))
        conn.commit()
        conn.close()
        print("Data saved to database:", data)
    except Exception as e:
        print("Error saving data to database:", e)

# 파이큐티와 소켓 통신하는 함수
def communicate_with_pyqt():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((PYQT_HOST, PYQT_PORT))
    server_socket.listen(1)
    print("Waiting for PyQt client connection...")
    client_socket, addr = server_socket.accept()
    print("Connected to PyQt client:", addr)

    while True:
        # 디비에서 데이터를 가져와서 파이큐티에 전송
        # 예: 데이터베이스에서 데이터를 가져오고 소켓을 통해 전송
        try:
            conn = mysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM your_table_name")
            rows = cursor.fetchall()
            for row in rows:
                data = row[0]  # 예시: 첫 번째 컬럼의 데이터를 전송
                client_socket.sendall(data.encode())
        except Exception as e:
            print("Error communicating with PyQt client:", e)

# 메인 함수
def main():
    # 아두이노와 시리얼 통신 쓰레드 시작
    arduino_thread = threading.Thread(target=read_from_arduino)
    arduino_thread.daemon = True
    arduino_thread.start()

    # 파이큐티와 소켓 통신 쓰레드 시작
    pyqt_thread = threading.Thread(target=communicate_with_pyqt)
    pyqt_thread.daemon = True
    pyqt_thread.start()

    # 메인 쓰레드가 종료되지 않도록 루프 유지
    while True:
        pass

if __name__ == "__main__":
    main()
