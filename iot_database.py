import mysql.connector
import random
from datetime import datetime
import time
import pandas as pd


sensor_type_list = ["조도", "습도", "토양 수분", "온도", "물 탱크", "초음파"]

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
    "캡쳐" : "캡쳐",
    "성장" : "알림"
    }



class Database:
    def __init__(self, host, port, user, password, database):
        self.config = {
            "host": host,
            "port" : port,
            "user": user,
            "password": password,
            "database": database
        }
        self.conn = None

    def connect(self):
        self.conn = mysql.connector.connect(**self.config)

    def close(self):
        if self.conn:
            self.conn.close()

    def insert_sensor_data(self, data):
        cursor = self.conn.cursor()
        query = "INSERT INTO sensor_data (time_stamp, sensor_type, value) VALUES (%s, %s, %s)"
        cursor.execute(query, data)
        self.conn.commit()
        cursor.close()


    def get_data_id(self, time_stamp, sensor_type, value):
        cursor = self.conn.cursor()
        query = "SELECT id FROM sensor_data WHERE  time_stamp = %s AND sensor_type = %s AND value = %s"
        cursor.execute(query, (time_stamp, sensor_type, value))
        result = cursor.fetchall()
        cursor.close()

        if result:
            return int(result[0][0])
        else:
            return None  # 조회된 결과가 없는 경우
        
    def insert_event_log(self, log):
        cursor = self.conn.cursor()
        query = "INSERT INTO event_log (data_id, time_stamp, event, command, camera_image_path) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, log)
        self.conn.commit()
        cursor.close()

    def check_event(self, time_stamp, sensor_type, value):
        sensor_data_id = self.get_data_id(time_stamp, sensor_type, value)

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
                event = "성장"
                command = event_command_dict[event]
            else:
                event = None
                command = None
        else:
            event = None
            command = None

        return sensor_data_id, event, command


    def watch_log(self, selected_date):
        cursor = self.conn.cursor()
        query = """
        select substring(e.time_stamp, 12, 8) as "time_stamp", 
            max(case when s.sensor_type = '온도' then s.value end) as `Temp`,
            max(case when s.sensor_type = '습도' then s.value end) as `AirHum`,
            max(case when s.sensor_type = '토양 수분' then s.value end) as `GndHum`, 
            max(case when s.sensor_type = '조도' then s.value end) as `Bright`,
            max(case when s.sensor_type = '초음파' then s.value end) as `Growth`
        from event_log e
        join sensor_data s on e.time_stamp = s.time_stamp
        where date(e.time_stamp) = %s
        group by e.time_stamp
        """
        df = pd.read_sql(query, self.conn, params=[selected_date])
        cursor.close()
        return df

    def insert_capture_log(self, log):
        cursor = self.conn.cursor()
        query = "INSERT INTO event_log (data_id, time_stamp, event, command, camera_image_path) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, log)
        self.conn.commit()
        cursor.close()
    
    def watch_capture_log(self, selected_date):
        cursor = self.conn.cursor()
        query = """
        select substring(e.time_stamp, 12, 8) as "time_stamp", 
            max(case when s.sensor_type = '온도' then s.value end) as `Temp`,
            max(case when s.sensor_type = '습도' then s.value end) as `AirHum`,
            max(case when s.sensor_type = '토양 수분' then s.value end) as `GndHum`, 
            max(case when s.sensor_type = '조도' then s.value end) as `Bright`,
            max(case when s.sensor_type = '초음파' then s.value end) as `Growth`
        from event_log e
        join sensor_data s on e.time_stamp = s.time_stamp
        where date(e.time_stamp) = %s and event = '캡쳐'
        group by e.time_stamp
        """

        df = pd.read_sql(query, self.conn, params=[selected_date])
        cursor.close()
        return df

def main():

    # iot_db = Database("iot-project.czcywiaew4o2.ap-northeast-2.rds.amazonaws.com", 3306, "admin", "****", "iot_project")
    iot_db = Database("localhost", 3306, "root", "amrbase1", "iot_project")


    iot_db.connect()

    for i in range(10):
        now = datetime.now()
        time_stamp = now.strftime('%Y-%m-%d %H:%M:%S')
        for sensor_type in sensor_type_list:
            value = random.randint(0, 10)
            data = (time_stamp, sensor_type, value)
            iot_db.insert_sensor_data(data)
            sensor_data_id, event, command = iot_db.check_event(time_stamp, sensor_type, value)

            if event is not None:
                camera_image_path = f"capture_data/{time_stamp}.jpg"
                log = (sensor_data_id, time_stamp, event, command, camera_image_path)
                iot_db.insert_event_log(log)

        camera = random.randint(0, 1)
        if camera == 1:
            event = "캡쳐"
            command = event_command_dict[event]
            log = (None, time_stamp, event, command, camera_image_path)
            iot_db.insert_capture_log(log)
        time.sleep(1)

    selected_date = "2024-03-12"
    df = iot_db.watch_capture_log(selected_date)
    print(df)
    iot_db.close()
 
if __name__ == "__main__":
    main()
