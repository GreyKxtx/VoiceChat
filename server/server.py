import socket
import threading
import uuid
from cryptographic.RSA import generate_rsa_keypair, serialize_public_key, deserialize_public_key

# Словарь для хранения связи между UUID клиентов и их публичными ключами
clients = {}

# Функция для обработки соединения с клиентом
def handle_client(client_socket, client_id, server_private_key, clients):
    while True:
        try:
            data = client_socket.recv(2048)
            if not data:
                break
            for uuid, socket in clients.items():
                if uuid != client_id:  # Отправляем аудио всем клиентам, кроме отправителя
                    socket.sendall(data)
        except ConnectionResetError:
            break
    # Удаляем связь с клиентом из списка клиентов при разрыве соединения
    if client_id in clients:
        del clients[client_id]

# Функция для создания сервера
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12346))
    server.listen(2)  # Ожидание двух клиентов
    print("[*] Сервер запущен на порту 12345")

    # Генерация ключей RSA для сервера
    server_private_key, server_public_key = generate_rsa_keypair()
    print("[*] Сгенерированы ключи RSA для сервера")

    while True:
        # Ожидание подключения клиента
        client_socket, addr = server.accept()
        print("[*] Принято соединение от клиента:", addr)

        # Генерация UUID для клиента
        client_id = str(uuid.uuid4())[:8]  # Сокращаем UUID до 8 символов

        # Отправка публичного ключа сервера и UUID клиенту
        serialized_server_public_key = serialize_public_key(server_public_key)
        client_socket.sendall(serialized_server_public_key)
        client_socket.sendall(client_id.encode())

        # Получение публичного ключа клиента
        serialized_client_public_key = client_socket.recv(4096)
        client_public_key = deserialize_public_key(serialized_client_public_key)
        print("[*] Получен публичный ключ клиента")

        # Сохранение связи между UUID клиента и его публичным ключом
        clients[client_id] = client_socket
        print("[*] Связь сохранена")

        # Запуск отдельного потока для обработки соединения с клиентом
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id, server_private_key, clients))
        client_thread.start()
        print("[*] Связь установлена")

# Запуск сервера
start_server()
