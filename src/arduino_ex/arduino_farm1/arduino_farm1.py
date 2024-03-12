import serial
import json

# 시리얼 포트 연결 설정
ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)  # 포트 번호는 시스템에 따라 달라질 수 있음

def create_command(data):
    commands = {}
    commands["servo1"] = "on" if data["air_humi"] > 45 else "off"
    commands["propeller"] = "on" if data["air_humi"] > 45 else "off"
    commands["water"] = "on" if 20 > data["psoil_humi1"] else "off"
    # commands["hitter"] = "on" if 25 > data["air_temp"] else "off"
    return commands


try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()  # 시리얼 포트에서 한 줄 읽기
            try:
                data = json.loads(line)  # JSON 문자열을 파이썬 딕셔너리로 변환
                # 받은 데이터 출력
                print("air_humi", data["air_humi"])
                print("air_temp:", data["air_temp"])
                print("psoil_humi1:", data["psoil_humi1"])
                print("distance:", data["distance"])

                # command = {"servo1": "on"} if data["air_humi"] > 40 else {"servo1": "off"}
                # print(command)
                # command_json = json.dumps(command) + '\n'  # JSON 문자열로 변환 후 줄바꿈 추가
                # ser.write(command_json.encode())  # 아두이노로 명령 전송

                # command1 = {"servo1": "on", "propeller": "on"} if data["air_humi"] > 45 else {"servo1": "off", "propeller": "off"}
                # command2 = {"hitter": "on"} if 25.0 > data["air_temp"] else {"hitter": "off"}
                # command_json = json.dumps(command1) + '\n' + json.dumps(command2) # JSON 문자열로 변환 후 줄바꿈 추가
                command = create_command(data)            
                print(command)                    
                command_json = json.dumps(command) + '\n' 
                ser.write(command_json.encode())  # 아두이노로 명령 전송

                # # json data saving
                # with open("client_data.json", "w") as file:
                #     ser.write(command_json.encode)command_json



            except json.JSONDecodeError:
                print("JSON decode error:", line)
except KeyboardInterrupt:
    print("프로그램 종료")
    ser.close()
