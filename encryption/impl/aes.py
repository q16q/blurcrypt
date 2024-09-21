from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

def gen_key() -> tuple:
    aes_key = get_random_bytes(16)
    
    return aes_key

def encrypt(content: str, aes_key: bytes) -> tuple:
    data = content.encode()
    
    cipher = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
        
    return (cipher.nonce, ciphertext, tag)

def decrypt(nonce: bytes, ciphertext: bytes, tag: bytes, aes_key: bytes) -> str:
    cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    content = cipher.decrypt_and_verify(ciphertext, tag)
    
    return content.decode('utf-8')