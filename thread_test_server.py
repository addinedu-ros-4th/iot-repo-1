import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            # 클라이언트로부터 받은 메시지 출력
            data = client_socket.recv(1024).decode()
            print("클라이언트로부터 받은 메시지:", data)
        except Exception as e:
            print("에러 발생:", e)
            break
        
    client_socket.close()

def talk(client_socket):
    while True:
        message = input("클라이언트에게 보낼 메시지를 입력하세요: ")
        client_socket.sendall(message.encode())


def main():
    host = '127.0.0.1'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("서버가 시작되었습니다.")

    while True:
        client_socket, addr = server_socket.accept()
        print("클라이언트가 연결되었습니다:", addr)

        # 클라이언트와 통신하는 스레드 시작
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        server_thread = threading.Thread(target=talk, args=(client_socket,))
        server_thread.start()
        client_thread.start()
        server_thread.join()
        client_thread.join()

        # 사용자로부터 메시지 입력 받아 클라이언트에게 전송
        
if __name__ == "__main__":
    main()
