import os
from google.cloud.sql.connector import Connector, IPTypes
import pymysql

# Cloud SQL 연결 설정
instance_connection_name = os.environ["vocal-clone-411002:asia-northeast3:yhryu96"]  # 예: 'project:region:instance'
db_user = os.environ["root"]  # 예: 'root'
db_pass = os.environ["1"]  # 예: 'your-root-password'

ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
connector = Connector(ip_type)

def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        instance_connection_name,
        "pymysql",
        user=db_user,
        password=db_pass,
    )
    return conn

# 새 사용자 생성
new_user = 'yoonha'
new_password = '**'
create_user_query = f"CREATE USER '{new_user}'@'%' IDENTIFIED BY '{new_password}';"

conn = getconn()
cursor = conn.cursor()
try:
    cursor.execute(create_user_query)
    conn.commit()
    print("User created successfully.")
except pymysql.MySQLError as err:
    print("Failed to create user:", err)

cursor.close()
conn.close()
