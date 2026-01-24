from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


# Generate RSA keys (private and public)
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Serialize the keys to get them as PEM strings
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem


# Encrypt a message using the RSA public key
def encrypt_message(message, public_key_pem):
    public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
    encrypted_message = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message


# Decrypt a message using the RSA private key
def decrypt_message(encrypted_message, private_key_pem):
    private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message





'''# Example usage
if __name__ == "__main__":
    # Generate RSA keys
    private_key_pem, public_key_pem = generate_rsa_keys()

    # Print the keys (optional, be careful with private keys)
    print("Private Key:", private_key_pem.decode())
    print("Public Key:", public_key_pem.decode())

    # Original message
    message = "Hello, this is a secret message!"

    # Encrypt the message using the public key
    encrypted_message = encrypt_message(message, public_key_pem)
    print("Encrypted Message:", encrypted_message)

    # Decrypt the message using the private key
    decrypted_message = decrypt_message(encrypted_message, private_key_pem)
    print("Decrypted Message:", decrypted_message)
'''