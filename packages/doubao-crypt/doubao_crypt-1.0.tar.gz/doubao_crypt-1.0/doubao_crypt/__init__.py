import functools
from .aes import aes_decrypt, aes_encrypt
from .ecies import encryptedECIES, decryptedECIES, privateKey2publicKey
from . import cache
from .errors import ParameterError, NotKeyError
import copy
import logging


__keys_cache = None


def init_cache(host, cache_type='LocalCache', cache_prefix='doubao-keys-', cache_instance=None, cache_uri=None, pre_cache=False, clean=True):
    global __keys_cache
    if not __keys_cache:
        cls = getattr(cache, cache_type)
        __keys_cache = cls(host, cache_instance=cache_instance, cache_prefix=cache_prefix, cache_uri=cache_uri, pre_cache=pre_cache, clean=clean)


def doubao_ecies_encrypt(data, fields=None, cid=None, gid=None, agent_id=None):
    global __keys_cache

    def _encrypt(text, public_key):
        if not text or len(text) < 4 or not public_key or '*' in text:
            return text
        if ('X' in text and text[-1] != 'X') or ('x' in text and text[-1] != 'x'):
            return text
        encrypted_text = encryptedECIES(text, public_key)
        encrypted_text = encrypted_text[2:] if encrypted_text[:2] == '0x' else encrypted_text
        return 'JM_' + encrypted_text + '_' + text[-4:]

    def _encrypt_fields(d, public_key):
        _data = copy.deepcopy(d)
        for field in fields:
            field_list = field.split('.')
            if len(field_list) == 1:
                if field_list[0] in _data:
                    _data[field_list[0]] = _encrypt(_data[field_list[0]], public_key)
            elif len(field_list) > 1:
                try:
                    code_str = '_data' + ''.join(["['{}']".format(x) if isinstance(x, str) else '[{}]'.format(x) for x in field_list])
                    v = eval(code_str)
                    code_str = '_data' + ''.join(["['{}']".format(x) if isinstance(x, str) else '[{}]'.format(x) for x in field_list[:-1]])
                    dv = {field_list[-1]: _encrypt(v, public_key)}
                    eval("{code_str}.update({dv})".format(code_str=code_str, dv=dv))
                except Exception as e:
                    logging.warning('field[{}] not exists'.format(field))
        return _data

    if not fields and not isinstance(data, str):
        return data
    if not cid:
        raise ParameterError('need kwargs `cid`')
    keys = __keys_cache.get_keys(cid, gid, agent_id)
    if not keys:
        raise NotKeyError('can not get keys form cid({cid}), gid({gid}), agent_id({agent_id})'.format(cid=cid, gid=gid, agent_id=agent_id))

    if isinstance(data, dict):
        return _encrypt_fields(data, keys['publicKey'])
    elif isinstance(data, list):
        return [_encrypt_fields(item, keys['publicKey']) for item in data]
    elif isinstance(data, str):
        return _encrypt(data, keys['publicKey'])
    else:
        return data


def safe_doubao_ecies_encrypt(data, fields=None, cid=None, gid=None, agent_id=None):
    try:
        _data = doubao_ecies_encrypt(data, fields=fields, cid=cid, gid=gid, agent_id=agent_id)
    except Exception as e:
        return False, str(e), data
    return True, "", _data


def doubao_privacy_policy(fields=None, cid=None, gid=None, agent_id=None):
    def wrapper(func):
        @functools.wraps(func)
        def _wrapper(data, *args, **kwargs):
            _data = doubao_ecies_encrypt(data, fields=fields, cid=cid, gid=gid, agent_id=agent_id)
            return func(_data, *args, **kwargs)
        return _wrapper
    return wrapper
