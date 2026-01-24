from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os


# Function to pad plaintext (PKCS7)
def pad(data):
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()


# Function to unpad plaintext (PKCS7)
def unpad(data):
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(data) + unpadder.finalize()


# AES-CBC Encryption
def aes_cbc_encrypt(plaintext, key):
    iv = os.urandom(16)  # Generate a random 16-byte IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_plaintext = pad(plaintext)
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return iv + ciphertext  # Prepend IV for later decryption


# AES-CBC Decryption
def aes_cbc_decrypt(ciphertext, key):
    iv = ciphertext[:16]  # Extract IV from the first 16 bytes
    encrypted_data = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
    return unpad(decrypted_padded)


# Example usage

if __name__ == "__main__":
    key = os.urandom(16)  # Generate a random 16-byte key for AES-128
    plaintext = b"Hello, AES-CBC encryption!"

    encrypted = aes_cbc_encrypt(plaintext, key)
    print("Ciphertext:", encrypted.hex())

    decrypted = aes_cbc_decrypt(encrypted, key)
    print("Decrypted:", decrypted.decode())
