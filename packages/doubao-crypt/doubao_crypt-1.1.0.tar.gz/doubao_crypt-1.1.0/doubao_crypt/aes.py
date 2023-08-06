from Crypto.Cipher import AES
import base64


def add_16(par):
    par = par.encode('utf-8')
    while len(par) % 16 != 0:
        par += b'\x00'
    return par


def aes_encrypt(text, key):
    text = add_16(text)
    aes = AES.new(add_16(key), AES.MODE_ECB)
    encrypt_text = aes.encrypt(text)
    return base64.encodebytes(encrypt_text).decode().strip()


def aes_decrypt(text, key):
    text = base64.decodebytes(text.encode('utf-8'))
    aes = AES.new(add_16(key), AES.MODE_ECB)
    decrypt_text = aes.decrypt(text)
    return decrypt_text.decode('utf-8').strip('\0')
