import socket

HOST = "127.0.0.1"
PORT = 65222

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Сервер запущен")
    conn, addr = s.accept()
    with conn:
        data = conn.recv(1024)
        print(f"Полученно: {data}")
        conn.send(data)
        print(f"Отправлено: {data}")
