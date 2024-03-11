import serial
import json

# 시리얼 포트 연결 설정
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # 포트 번호는 시스템에 따라 달라질 수 있음

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()  # 시리얼 포트에서 한 줄 읽기
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

                command = {"led": "on"} if data["led"] > 60 else {"led": "off"}
                command_json = json.dumps(command) + '\n'  # JSON 문자열로 변환 후 줄바꿈 추가
                ser.write(command_json.encode())  # 아두이노로 명령 전송

            except json.JSONDecodeError:
                print("JSON decode error:", line)
except KeyboardInterrupt:
    print("프로그램 종료")
    ser.close()