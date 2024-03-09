import socket
"""

"""


host = '0.0.0.0'  # ESP32의 IP 주소
port = 8080  # 포트 번호

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

print(f"Server is listening on {host}:{port}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    data = client_socket.recv(1024)
    if data:
        print(f"Received data: {data.decode('utf-8')}")
    else:
        print("connection end")

    client_socket.close()
