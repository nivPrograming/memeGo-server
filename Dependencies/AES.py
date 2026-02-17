from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os


def aes_gcm_encrypt(plaintext: bytes, key: bytes) -> bytes:
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext_with_tag = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ciphertext_with_tag


def aes_gcm_decrypt(data: bytes, key: bytes) -> bytes:
    nonce = data[:12]
    ciphertext_with_tag = data[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext_with_tag, None)