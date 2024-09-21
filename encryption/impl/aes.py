from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

def gen_key() -> tuple:
    """
    Generates a random AES key.
    
    Returns:
        tuple: A tuple containing the generated AES key.
    """
    aes_key = get_random_bytes(16)
    
    return aes_key

def encrypt(content: str, aes_key: bytes) -> tuple:
    """
    Encrypts the given content using the provided AES key.
    Args:
        content (str): The content to be encrypted.
        aes_key (bytes): The AES key used for encryption.
    Returns:
        tuple: A tuple containing the nonce, ciphertext, and tag.
    """
    data = content.encode()
    
    cipher = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
        
    return (cipher.nonce, ciphertext, tag)

def decrypt(nonce: bytes, ciphertext: bytes, tag: bytes, aes_key: bytes) -> str:
    """
    Decrypts the given ciphertext using the provided AES key, nonce, and tag.
    Args:
        nonce (bytes): The nonce used for decryption.
        ciphertext (bytes): The encrypted data.
        tag (bytes): The authentication tag.
        aes_key (bytes): The AES key used for decryption.
    Returns:
        str: The decrypted content.
    """
    cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    content = cipher.decrypt_and_verify(ciphertext, tag)
    
    return content.decode('utf-8')