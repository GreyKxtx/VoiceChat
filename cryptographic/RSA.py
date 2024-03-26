# crypto/rsa_utils.py
from cryptography.hazmat.primitives import serialization, padding, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding


def generate_rsa_keypair(public_exponent=65537, key_size=2048, backend=default_backend()):
    """
    Генерирует пару ключей RSA.

    :param public_exponent: Публичный показатель экспоненты RSA. Это целое число, которое используется в открытом ключе для шифрования.
    :param key_size: Размер ключа RSA. Определяет длину в битах для генерируемого ключа.
    :param backend: Задний конец, который будет использоваться для создания ключа. Это объект, предоставленный библиотекой cryptography, который определяет, как будет реализована операция генерации ключа.

    :return: Пара ключей RSA (приватный и публичный)
    """
    private_key = rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=key_size,
        backend=backend
    )
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_public_key(public_key):
    """
    Сериализует публичный ключ RSA в формат PEM.

    :param public_key: публичный ключ RSA
    :return: сериализованный публичный ключ в формате PEM
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def deserialize_public_key(serialized_key):
    """
    Десериализует публичный ключ RSA из формата PEM.

    :param serialized_key: сериализованный публичный ключ в формате PEM
    :return: десериализованный публичный ключ RSA
    """
    return serialization.load_pem_public_key(
        serialized_key,
        backend=default_backend()
    )

def encrypt_with_public_key(public_key, plaintext):
    """
    Шифрует данные с использованием публичного ключа RSA.

    :param public_key: публичный ключ RSA
    :param plaintext: данные для шифрования
    :return: зашифрованные данные
    """
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext


def decrypt_with_private_key(private_key, ciphertext):
    """
    Расшифровывает данные с использованием приватного ключа RSA.

    :param private_key: приватный ключ RSA
    :param ciphertext: зашифрованные данные
    :return: расшифрованные данные
    """
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext

def test():
    # Генерируем ключевую пару RSA
    private_key, public_key = generate_rsa_keypair()
    # Приветственное сообщение для шифрования
    message = b"Hello, this is a test message!"

    # Зашифруем сообщение с помощью публичного ключа
    encrypted_message = encrypt_with_public_key(public_key, message)
    print("Зашифрованное сообщение:", encrypted_message)

    # Расшифруем сообщение с помощью приватного ключа
    decrypted_message = decrypt_with_private_key(private_key, encrypted_message)
    print("Расшифрованное сообщение:", decrypted_message.decode())

if __name__ == "__main__":
    test()
