# -*- coding: utf-8 -*-

# IMPORT LINE: from bombril.cryptography import rsa

import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization import PublicFormat


def generate_private_key_pem():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption()
    )

    return pem.decode()


def export_public_key_pem(private_key_pem):
    private_key_pem_bytes = private_key_pem.encode('utf8')
    private_key = load_pem_private_key(private_key_pem_bytes, password=None, backend=default_backend())
    public_key = private_key.public_key()

    pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.PKCS1
    )

    return pem.decode()


def generate_pair(file_prefix=None):
    priv_pem = generate_private_key_pem()
    pub_pem = export_public_key_pem(priv_pem)

    if file_prefix:
        with open('{}.priv'.format(file_prefix), 'w') as f:
            f.write(priv_pem)
        with open('{}.pub'.format(file_prefix), 'w') as f:
            f.write(pub_pem)

    return (priv_pem, pub_pem)


def encrypt(message, public_key_pem):
    message_bytes = message.encode('utf8')
    public_key_pem_bytes = public_key_pem.encode('utf8')

    public_key = load_pem_public_key(public_key_pem_bytes, backend=default_backend())

    encrypted_message = public_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    encrypted_message = base64.b64encode(encrypted_message)
    encrypted_message = encrypted_message.decode()

    return encrypted_message


def decrypt(encrypted_message, private_key_pem):
    encrypted_message_bytes = encrypted_message.encode('utf8')
    private_key_pem_bytes = private_key_pem.encode('utf8')

    encrypted_message_bytes = base64.b64decode(encrypted_message_bytes)

    private_key = load_pem_private_key(private_key_pem_bytes, password=None, backend=default_backend())

    decrypted_message = private_key.decrypt(
        encrypted_message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    decrypted_message = decrypted_message.decode()

    return decrypted_message


def encrypt_chunks(message, public_key_pem, offset=100):
    message_size = len(message)
    left = 0
    right = offset

    output = list()

    while left < message_size:
        right_limit = right if right < message_size else message_size

        chunk = message[left : right_limit]
        encrypted = encrypt(chunk, public_key_pem)
        output.append(encrypted)

        left = left + offset
        right = right + offset

    return '\n'.join(output)


def decrypt_chunks(message, private_key_pem):
    chunks = message.split('\n')
    decrypted_chunks = list()

    for chunk in chunks:
        decrypted_chunk = decrypt(chunk, private_key_pem)
        decrypted_chunks.append(decrypted_chunk)

    return ''.join(decrypted_chunks)
