# -*- coding: utf-8 -*-

import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import dsa, rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key


def encrypt(message, public_key_pem):
    public_key_pem_bytes = public_key_pem.encode('utf8')
    message_bytes = message.encode('utf8')

    pubkey = load_pem_public_key(public_key_pem_bytes, backend=default_backend())
    encrypted_message = pubkey.encrypt(
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
    private_key_pem_bytes = private_key_pem.encode('utf8')
    encrypted_message_bytes = encrypted_message.encode('utf8')

    encrypted_message_bytes = base64.b64decode(encrypted_message_bytes)

    privkey = load_pem_private_key(private_key_pem_bytes, password=None, backend=default_backend())
    decrypted_message = privkey.decrypt(
        encrypted_message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    decrypted_message = decrypted_message.decode()

    return decrypted_message
