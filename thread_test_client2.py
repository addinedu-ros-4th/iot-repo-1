import socket
import threading

def send_message(client_socket):
    try:
        while True:
            message = input("test 2.Enter message: ")
            client_socket.sendall(message.encode())
    except Exception:
        print("error")
    finally:
        client_socket.close()
def receive_message(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        print("Received from server:", data)

def main():
    server_host = '127.0.0.1'
    server_port = 8080

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_message, args=(client_socket,))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    client_socket.close()

if __name__ == "__main__":
    main()
