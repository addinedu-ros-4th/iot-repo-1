import socket

# 서버 설정
host = "0.0.0.0"   # 모든 인터페이스에서 접속 허용
port = 8080

# 서버 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print("서버가", port, "포트에서 실행 중입니다.")

# 클라이언트 연결 대기
client_socket, client_address = server_socket.accept()
print("클라이언트가 연결되었습니다:", client_address)

try:
    while True:
        # 클라이언트로부터 데이터 수신
        data = client_socket.recv(1024).decode()
        if data:
            print("ESP32로부터 받은 데이터:", data)
        
        else:# 클라이언트에게 데이터 전송
            message = input("전송할 데이터를 입력하세요: ")
            client_socket.sendall(message.encode())
finally:
    # 연결 종료
    print("연결이 종료되었습니다.")
    client_socket.close()
    server_socket.close()
