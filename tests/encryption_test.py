import sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(SCRIPT_DIR, '..')
sys.path.append(PROJECT_DIR)

from encryption.messages import decrypt_message, encrypt_message
from encryption.impl.aes import gen_key as gen_aes_key
from encryption.impl.rsa import gen_keys as gen_rsa_keys

def test():
    message = 'Hello, World!'

    aes_key = gen_aes_key()
    private_key, public_key = gen_rsa_keys()

    encrypted_bytestr = encrypt_message(message, aes_key, public_key)
    decrypted_message = decrypt_message(encrypted_bytestr, aes_key, private_key)

    assert message == decrypted_message

if __name__ == '__main__':
    test()