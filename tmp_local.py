import mysql.connector
import random
from datetime import datetime
import time

sensor_type_list = ["light", "humidity", "soil humidity", "temperature", "water_tank", "capture"]

event_command_dict = {
#   "밝기 상승" : ???    
    "밝기 하락" : "LED 동작", 
    "습도 상승" : "펜 동작",
    "습도 하락" : "가습기 동작",
    "토양 수분 상승" : "알림",
    "토양 수분 하락" : "물 공급",
    "온도 상승" : "팬 동작",
    "온도 하락" : "방열 코일 동작",
    "물탱크 물부족" : "알림",
    "캡쳐버튼 클릭" : "캡쳐"
    }


conn = mysql.connector.connect(
    host = "iot-project.czcywiaew4o2.ap-northeast-2.rds.amazonaws.com",
    port = 3306,
    user = "admin",
    password = "qwer1234",
    database = "iot_project"
)

def insert_sensor_data(data):
    cursor = conn.cursor()
    query = "INSERT INTO sensor_data (time_stamp, sensor_type, value) VALUES (%s, %s, %s)"
    cursor.execute(query, data)
    conn.commit()
    cursor.close()

def get_data_id(time_stamp, sensor_type, value):
    cursor = conn.cursor()
    query = "SELECT id FROM sensor_data WHERE  time_stamp = %s AND sensor_type = %s AND value = %s"
    cursor.execute(query, (time_stamp, sensor_type, value))
    result = cursor.fetchall()
    cursor.close()
    if result:
        return int(result[0][0])
    else:
        return None  # 조회된 결과가 없는 경우

def insert_event_log(log):
    cursor = conn.cursor()
    query = "INSERT INTO event_log (data_id, time_stamp, event, command) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, log)
    conn.commit()
    cursor.close()

sensor_type_list = ["light", "humidity", "soil humidity", "temperature", "water_tank"]
def check_event(time_stamp, sensor_type, value):
    sensor_data_id = get_data_id(time_stamp, sensor_type, value)
    if sensor_type == sensor_type_list[0]:
        if value < 3:
            event = "밝기 하락"
            command = event_command_dict[event]
        else:
            event = None
            command = None
    elif sensor_type == sensor_type_list[1]:
        if value > 7:
            event = "습도 상승"
            command = event_command_dict[event]
        elif value < 3:
            event = "습도 하락"
            command = event_command_dict[event]
        else:
            event = None
            command = None
    elif sensor_type == sensor_type_list[2]:
        if value > 7:
            event = "토양 수분 상승"
            command = event_command_dict[event]
        elif value < 3:
            event = "토양 수분 하락"
            command = event_command_dict[event]
        else:
            event = None
            command = None
    elif sensor_type == sensor_type_list[3]:
        if value > 7:
            event = "온도 상승"
            command = event_command_dict[event]
        elif value < 3:
            event = "온도 하락"
            command = event_command_dict[event]
        else:
            event = None
            command = None
    elif sensor_type == sensor_type_list[4]:
        if value > 7:
            event = "물탱크 물부족"
            command = event_command_dict[event]
        else:
            event = None
            command = None
    elif sensor_type == sensor_type_list[5]:
        if value > 7:
            event = "캡쳐버튼 클릭"
            command = event_command_dict[event]
        else:
            event = None
            command = None
    else:
        event = None
        command = None
    return sensor_data_id, event, command

def main():
    for i in range(10):
        for sensor_type in sensor_type_list:
            now = datetime.now()
            time_stamp = now.strftime('%Y-%m-%d %H:%M:%S')
            value = random.randint(0, 10)
            data = (time_stamp, sensor_type, value)
            insert_sensor_data(data)
            sensor_data_id, event, command = check_event(time_stamp, sensor_type, value)
            
            print(sensor_data_id)
            
            if event is not None:
                log = (sensor_data_id, time_stamp, event, command)
                insert_event_log(log)
        time.sleep(1)

if __name__ == "__main__":
    main()
