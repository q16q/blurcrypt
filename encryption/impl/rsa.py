from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

def encrypt(data: bytes, public_key: bytes) -> bytes:
    rsa_public_key = RSA.import_key(public_key)
    rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
    encrypted_text = rsa_public_key.encrypt(data)
    
    return encrypted_text

def decrypt(encrypted: bytes, private_key: bytes) -> str:
    rsa_private_key = RSA.import_key(private_key)
    rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
    decrypted_text = rsa_private_key.decrypt(encrypted)
    
    return decrypted_text

def gen_keys() -> tuple:
    key = RSA.generate(2048)
    private_key = key.export_key('PEM')
    public_key = key.public_key().export_key('PEM')
    
    return (private_key, public_key)