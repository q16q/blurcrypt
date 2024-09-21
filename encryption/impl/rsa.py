from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

def encrypt(data: bytes, public_key: bytes) -> bytes:
    """
    Encrypts the provided data using the given public key.
    Args:
        data (bytes): The data to be encrypted.
        public_key (bytes): The public key used for encryption.
    Returns:
        bytes: The encrypted data.
    """
    rsa_public_key = RSA.import_key(public_key)
    rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
    encrypted_text = rsa_public_key.encrypt(data)
    
    return encrypted_text

def decrypt(encrypted: bytes, private_key: bytes) -> str:
    """
    Decrypts the provided encrypted data using the given private key.
    Args:
        encrypted (bytes): The encrypted data to be decrypted.
        private_key (bytes): The private key used for decryption.
    Returns:
        str: The decrypted text.
    """
    rsa_private_key = RSA.import_key(private_key)
    rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
    decrypted_text = rsa_private_key.decrypt(encrypted)
    
    return decrypted_text

def gen_keys() -> tuple:
    """
    Generate a pair of RSA keys.
    This function generates a pair of RSA keys with a key size of 2048 bits.
    The private key is exported in PEM format and the public key is exported
    in PEM format.
    Returns:
        tuple: A tuple containing the private key and the public key.
              Each key is a bytes object.
    """
    key = RSA.generate(2048)
    private_key = key.export_key('PEM')
    public_key = key.public_key().export_key('PEM')
    
    return (private_key, public_key)