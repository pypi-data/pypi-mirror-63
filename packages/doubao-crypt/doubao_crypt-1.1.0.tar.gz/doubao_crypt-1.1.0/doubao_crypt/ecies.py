from ecies.utils import generate_eth_key, generate_key, hex2prv
from ecies import encrypt, decrypt
from eth_keys import keys
from coincurve.utils import get_valid_secret
from eth_utils import decode_hex, encode_hex


def privateKey2publicKey(private_key):
    # 将私钥解析为操作格式
    priv_handler = keys.PrivateKey(decode_hex(private_key))
    # 获取公钥
    pub_handler = priv_handler.public_key
    pub_key = pub_handler.to_compressed_bytes()
    # 未压缩的公钥
    # pub_key.to_hex()
    return encode_hex(pub_key)


def encryptedECIES(msg, pub_key):
    return encode_hex(
        encrypt(pub_key, msg.encode('utf-8'))
    )


def decryptedECIES(enmsg, priv_key):
    return decrypt(
        priv_key, decode_hex(enmsg)
    ).decode('utf-8')
