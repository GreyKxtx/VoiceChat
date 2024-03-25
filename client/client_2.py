import socket
import pyaudio
from rsa.rsa_utils import deserialize_public_key, generate_rsa_keypair, serialize_public_key


def receive_audio(client_socket):
    CHUNK = 2048
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=CHUNK)
    while True:
        try:
            data = client_socket.recv(CHUNK)
           # print("[*] Размер полученных аудиоданных:", len(data))
            stream.write(data)
        except ConnectionResetError:
            break
    stream.stop_stream()
    stream.close()
    p.terminate()


def client():
    # Подключение к серверу
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12346))

    # Получение публичного ключа сервера
    serialized_server_public_key = client_socket.recv(4096)
    server_public_key = deserialize_public_key(serialized_server_public_key)
    print("[CLIENT 2] Получен публичный ключ сервера:", server_public_key)
    print(server_public_key)
    # Получение UUID от сервера и сокращение до 8 символов
    server_uuid = client_socket.recv(4096).decode()[:8]
    print("[CLIENT 2] Получение UUID от сервера " + server_uuid)

    # Генерация ключей RSA для клиента
    client_private_key, client_public_key = generate_rsa_keypair()

    print("[CLIENT 2] Генерация ключей RSA для клиента " + str(generate_rsa_keypair()))

    # Отправка публичного ключа клиента на сервер
    serialized_client_public_key = serialize_public_key(client_public_key)
    client_socket.sendall(serialized_client_public_key)

    print("[CLIENT 2]  Отправка публичного ключа клиента на сервер " + serialized_client_public_key.hex())

    # Запуск приема аудио данных
    receive_audio(client_socket)
    print("[CLIENT 2] Запуск передачи аудио ")

    client_socket.close()
    print("[CLIENT 2] Закрытие соединения ")
client()
