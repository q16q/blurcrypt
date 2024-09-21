from .impl.aes import encrypt as AES_encrypt, decrypt as AES_decrypt
from .impl.rsa import encrypt as RSA_encrypt, decrypt as RSA_decrypt

def encrypt_message(message: str, aes_key: bytes, public_key: bytes) -> bytes:
    nonce, ciphertext, tag = AES_encrypt(message, aes_key)
    bytestr = b',x,'.join([tag, nonce, ciphertext])    
    
    splitted = [ bytestr[i:i+180] for i in range(0, len(bytestr), 180) ]
    encrypted_chunks = [RSA_encrypt(chunk, public_key) for chunk in splitted]
    chunk_bytestr = b',x,'.join(encrypted_chunks)
    return chunk_bytestr

def decrypt_message(bytestr: bytes, aes_key: bytes, private_key: bytes) -> str:
    chunks = bytestr.split(b',x,')
    decrypted_chunks = [RSA_decrypt(chunk, private_key) for chunk in chunks]
    decrypted_bytestr = b''.join(decrypted_chunks)
    
    tag, nonce, cipher = decrypted_bytestr.split(b',x,')
    return AES_decrypt(nonce, cipher, tag, aes_key)