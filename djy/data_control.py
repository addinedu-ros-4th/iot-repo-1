import socket
"""
pc에서 esp32가 보내는 메세지를 받기 위한 코드.
파이썬의 소켓 모듈을 사용하여 데이터를 주고 받습니다.
"""


host = '0.0.0.0'  # ESP32의 IP 주소
port = 8080  # 포트 번호

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓을 만들어 줍니다.
server_socket.bind((host, port)) #esp32와 연결
server_socket.listen(5) #esp32에서 데이터 보내는 걸 기다립니다. 

print(f"Server is listening on {host}:{port}")

while True:
    client_socket, addr = server_socket.accept() # esp32의 주소와 어떤 값을 받아옴.  
    #print(f"Connection from {addr}") # 받아온 값과 ip주소가 출력

    data = client_socket.recv(1024) #esp에서 보내는 데이터를 저장하는 변수
    if data:
        print(f"Received data: {data.decode('utf-8')}") #데이터 출력


    client_socket.close()
