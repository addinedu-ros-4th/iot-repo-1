import serial

# 시리얼 포트 설정
serial_port = '/dev/ttyACM0'  # 아두이노가 연결된 시리얼 포트
baud_rate = 9600  # 아두이노와 동일한 통신 속도

# 시리얼 포트 초기화
ser = serial.Serial(serial_port, baud_rate)
while True:
    # 아두이노로 숫자 데이터 전송
    data_to_send = b'123'  # 전송할 데이터 (이 예제에서는 바이트 문자열로 전송)
    ser.write(data_to_send)