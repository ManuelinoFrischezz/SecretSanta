from cryptography.fernet import Fernet


def generate_cipher():

    encryption_key = Fernet.generate_key()

    cipher = Fernet(encryption_key)

    return cipher, encryption_key


def encrypt_name(
    cipher: Fernet,
    name: str,
):

    return cipher.encrypt(name.encode()).decode()


def decrypt_name(
    encrypted_name: str,
    key: str,
):

    cipher = Fernet(key.encode())

    return cipher.decrypt(encrypted_name.encode()).decode()
