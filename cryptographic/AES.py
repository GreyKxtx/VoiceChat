from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def generate_aes_key(lenght=32):
    """
    Генерирует ключ AES.

    :param lenght: Длина ключа в байтах. По умолчанию 32 байта (256 бит).
    :return: Ключ AES.
    """
    return os.urandom(lenght)

def generate_aes_iv(lenght=16):
    """
    Генерирует инициализационный вектор (IV) для AES.

    :param lenght: Длина вектора в байтах. По умолчанию 16 байт (128 бит).
    :return: Инициализационный вектор (IV).
    """
    return os.urandom(lenght)

def encrypt_with_aes(key, iv, plaintext):
    """
    Шифрует данные с использованием ключа AES и инициализационного вектора (IV)
    в режиме CFB (Cipher Feedback).

    :param key: Ключ AES.
    :param iv: Инициализационный вектор (IV).
    :param plaintext: Данные для шифрования.
    :return: Зашифрованные данные.
    """
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()

def decrypt_with_aes(key, iv, ciphertext):
    """
    Расшифровывает данные с использованием ключа AES и инициализационного вектора (IV)
    в режиме CFB (Cipher Feedback).

    :param key: Ключ AES.
    :param iv: Инициализационный вектор (IV).
    :param ciphertext: Зашифрованные данные.
    :return: Расшифрованные данные.
    """
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()
