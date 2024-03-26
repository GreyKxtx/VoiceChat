from cryptographic.AES import generate_aes_key, encrypt_with_aes, decrypt_with_aes , generate_aes_iv

# Тестовые данные
plaintext = b"Hello, World!"

# Генерация ключа AES и вектора инициализации (IV)
aes_key = generate_aes_key()
iv = generate_aes_iv()  # Генерация случайного IV длиной 16 байт

# Шифрование данных
ciphertext = encrypt_with_aes(aes_key, iv, plaintext)
print("Зашифрованные данные:", ciphertext)

# Расшифрование данных
decrypted_text = decrypt_with_aes(aes_key, iv, ciphertext)
print("Расшифрованные данные:", decrypted_text)

# Проверка соответствия исходных данных и расшифрованных данных
if decrypted_text == plaintext:
    print("Шифрование и расшифрование прошли успешно.")
else:
    print("Проблема с шифрованием или расшифрованием данных.")
