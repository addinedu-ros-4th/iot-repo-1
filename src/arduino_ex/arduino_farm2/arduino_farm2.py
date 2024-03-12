import serial
import json

# 시리얼 포트 연결 설정
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # 포트 번호는 시스템에 따라 달라질 수 있음
def create_command(data):
    commands = {}
 
    commands["ledCommand"] =  "on" if data["pledval"] < 50 else "off"
    commands["soilwaterCommand"] = "on" if data["psoil_humi2"] > 20 else"off"

    print("led will "+commands["ledCommand"])
    print("pump will "+commands["soilwaterCommand"])
    return commands

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()  # 시리얼 포트에서 한 줄 읽기
            try:
                data = json.loads(line)  # JSON 문자열을 파이썬 딕셔너리로 변환
                # 받은 데이터 출력
                # 보내는 센서값 (토양습도2, 거리2, 조도, 탱크수위, 가습기 수위)
                print("psoil_humi2:", data["psoil_humi2"])
                print("distance2:", data["distance2"])
                print("pledval:", data["pledval"])
                print("tank_wlevel", data["tank_wlevel"])
                print("humi_wlevel:", data["humi_wlevel"])

                command = create_command(data)            
                command_json = json.dumps(command) + '\n'  # JSON 문자열로 변환 후 줄바꿈 추가
                ser.write(command_json.encode())  # 아두이노로 명령 전송


                

                #  if (pledval > 20) { // 조도센서값이 60이 넘으면
                #     analogWrite(ledpin, pledval);  // LED는 조도센서 값의 밝기로 켜라 
                #     } 
                #     else{  // 그 외 조도센서값이면 LED를 꺼라
                #     analogWrite(ledpin, LOW);    
                #     }
                    
                #     if(psoil_humi2 < 20) { // 토양수분값이 20미만이면
                #     analogWrite(B_1A, 220); // 값을 변화(0~255)시키면서 호스에서 나오는 물의 양을 적정하게 설정
                #     digitalWrite(B_2B, LOW);
                #     delay(5000);
                #     Serial.println("화분2 물공급!"); 
                #     digitalWrite(B_1A, LOW); // 워터펌프 중단
                #     digitalWrite(B_2B, LOW);
                #     }
                #     else{  // 그 외 토양수분값이 측정되면 워터모터를 꺼라
                #     digitalWrite(B_1A, LOW);
                #     digitalWrite(B_2B, LOW);
                #     } 

                #     delay(2000); 

            except json.JSONDecodeError:
                print("JSON decode error:", line)
                
        
except KeyboardInterrupt:
    print("프로그램 종료")
    ser.close()
