import pyaudio
from cryptographic.AES import generate_aes_iv, generate_aes_key, encrypt_with_aes, decrypt_with_aes
from cryptographic.RSA import generate_rsa_keypair, serialize_public_key, encrypt_with_public_key, decrypt_with_private_key
from audio.audio_streams import open_input_stream , open_output_stream


def main():
    CHUNK = 1024
    stream_input = open_input_stream()
    stream_output = open_output_stream()

    # Остальной код без изменений
    aes_key = generate_aes_key()
    iv = generate_aes_iv()

    private_key, public_key = generate_rsa_keypair()

    print("Публичный ключ RSA:")
    print(serialize_public_key(public_key))

    try:
        while True:
            data = stream_input.read(CHUNK)
            encrypted_aes_key = encrypt_with_public_key(public_key, aes_key)
            encrypted_data = encrypt_with_aes(aes_key, iv, data)

            decrypted_aes_key = decrypt_with_private_key(private_key, encrypted_aes_key)
            decrypted_data = decrypt_with_aes(decrypted_aes_key, iv, encrypted_data)

            stream_output.write(decrypted_data)
    except KeyboardInterrupt:
        pass
    finally:
        stream_input.stop_stream()
        stream_input.close()
        stream_output.stop_stream()
        stream_output.close()

if __name__ == "__main__":
    main()
