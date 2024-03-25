# crypto/rsa_utils.py

from cryptography.hazmat.primitives import serialization, padding, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def generate_rsa_keypair():
    """
    Генерирует пару ключей RSA.

    :return: пара ключей RSA (приватный и публичный)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
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
