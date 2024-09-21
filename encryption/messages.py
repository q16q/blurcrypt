from .impl.aes import encrypt as AES_encrypt, decrypt as AES_decrypt
from .impl.rsa import encrypt as RSA_encrypt, decrypt as RSA_decrypt

def encrypt_message(message: str, aes_key: bytes, public_key: bytes) -> bytes:
    """
    Encrypts a given message using a combination of AES and RSA encryption.
    Parameters:
        message (str): The message to be encrypted.
        aes_key (bytes): The key used for AES encryption.
        public_key (bytes): The public key used for RSA encryption.
    Returns:
        bytes: The encrypted message.
    """
    nonce, ciphertext, tag = AES_encrypt(message, aes_key)
    bytestr = b',x,'.join([tag, nonce, ciphertext])    
    
    splitted = [ bytestr[i:i+180] for i in range(0, len(bytestr), 180) ]
    encrypted_chunks = [RSA_encrypt(chunk, public_key) for chunk in splitted]
    chunk_bytestr = b',x,'.join(encrypted_chunks)
    return chunk_bytestr

def decrypt_message(bytestr: bytes, aes_key: bytes, private_key: bytes) -> str:
    """
    Decrypts a given message using a combination of RSA and AES decryption.
    Parameters:
        bytestr (bytes): The message to be decrypted.
        aes_key (bytes): The key used for AES decryption.
        private_key (bytes): The private key used for RSA decryption.
    Returns:
        str: The decrypted message.
    """
    chunks = bytestr.split(b',x,')
    decrypted_chunks = [RSA_decrypt(chunk, private_key) for chunk in chunks]
    decrypted_bytestr = b''.join(decrypted_chunks)
    
    tag, nonce, cipher = decrypted_bytestr.split(b',x,')
    return AES_decrypt(nonce, cipher, tag, aes_key)