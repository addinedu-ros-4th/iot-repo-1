import serial

# 시리얼 포트 설정 (아두이노와 연결된 포트에 맞게 변경)
arduino_port = '/dev/ttyUSB0'  # Linux
# arduino_port = 'COM3'  # Windows

# 시리얼 통신 속도 설정 (아두이노와 동일한 값으로 설정)
baud_rate = 9600

# 시리얼 통신 객체 생성
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

while True:
    # 아두이노로부터 데이터 읽기
    received_data = ser.readline().decode('utf-8').strip()
    if received_data:
        print("아두이노로부터 받은 데이터:", received_data)
    
    # PC로 데이터 전송
    send_data = input("PC에 보낼 데이터를 입력하세요: ")
    ser.write(send_data.encode() + b'\n')  # 개행문자 추가

# 시리얼 포트 닫기
ser.close()
