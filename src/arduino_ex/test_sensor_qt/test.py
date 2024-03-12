import serial
import json

# 시리얼 포트 연결 설정
ser = serial.Serial('/dev/ttyACM2', 9600, timeout=1)  # 포트 번호는 시스템에 따라 달라질 수 있음

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()  # 시리얼 포트에서 한 줄 읽기
            try:
                data = json.loads(line)  # JSON 문자열을 파이썬 딕셔너리로 변환
                # 받은 데이터 출력
                print("air_humi", data["air_humi"])
                print("air_temp:", data["air_temp"])
                print("pledval:", data["pledval"])
                print("psoil_humi1:", data["psoil_humi1"])
                print("psoil_humi2:", data["psoil_humi2"])
                print("tank_wlevel:", data["tank_wlevel"])
                print("distance1:", data["distance1"])
                print("distance2:", data["distance2"])
      

                command = {"led": "on"} if data["pledval"] > 30 else {"led": "off"}
                command_json = json.dumps(command) + '\n'  # JSON 문자열로 변환 후 줄바꿈 추가
                ser.write(command_json.encode())  # 아두이노로 명령 전송

            except json.JSONDecodeError:
                print("JSON decode error:", line)
except KeyboardInterrupt:
    print("프로그램 종료")
    ser.close()