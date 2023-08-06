import abc
import requests
import redis
import json
from .errors import Api2Error
import logging

__all__ = ['LocalCache', 'RedisCache']


class BaseCache(metaclass=abc.ABCMeta):
    def __init__(self, api2_host, **kwargs):
        self.api2_host = api2_host
        pre_cache = kwargs.pop('pre_cache', None)
        if pre_cache:
            self.pre_cache()

    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def set(self, key, value):
        pass

    @abc.abstractmethod
    def clean(self):
        pass

    def get_keys(self, cid, gid, agent_id):
        p = [cid, gid, agent_id]
        key = '_'.join([str(x) for x in p if x is not None])
        _keys = self.get(key)
        if not _keys:
            _keys = self.get_data_from_remote(key)
        return _keys

    def pre_cache(self):
        rep = requests.get('{}/security-service-api/digicloud/encDecAnn/v1/encDec'.format(self.api2_host))
        result = rep.json()
        if result['errcode'] != 200:
            raise Api2Error(result['errmsg'])
        for item in result['data']:
            self.set(item['propertiesName'], item['propertiesValue']['keys'])

    def get_data_from_remote(self, key):
        rep = requests.get('{}/security-service-api/digicloud/encDecAnn/v1/encDec'.format(self.api2_host), params={'key': key})
        result = rep.json()
        if result['errcode'] != 200:
            raise Api2Error(result['errmsg'])
        if len(result['data']) == 0:
            logging.warning('can not find key {key}'.format(key=key))
            return None
        result = result['data'][0]
        self.set(result['propertiesName'], result['propertiesValue']['keys'])
        return result['propertiesValue']['keys']


class LocalCache(BaseCache):

    def __init__(self, api2_host, **kwargs):
        super().__init__(api2_host, **kwargs)
        self._cache = {}

    def get(self, key):
        return self._cache.get(key, None)

    def set(self, key, value):
        self._cache[key] = value

    def clean(self):
        self._cache = {}


class RedisCache(BaseCache):

    def __init__(self, api2_host, **kwargs):
        instance = kwargs.pop('cache_instance', None)
        if not instance:
            url = kwargs.pop('cache_uri', None) or 'redis://localhost/0'
            instance = redis.Redis.from_url(url)
        self.instance = instance
        self.cache_prefix = kwargs.pop('cache_prefix', 'doubao-keys-')
        is_clean = kwargs.pop('clean', False)
        if is_clean:
            self.clean()
        super().__init__(api2_host, **kwargs)

    def get_key(self, key):
        return '{}{}'.format(self.cache_prefix, key)

    def get(self, key):
        value = self.instance.get(self.get_key(key))
        return json.loads(value) if value else value

    def set(self, key, value):
        self.instance.set(self.get_key(key), json.dumps(value))

    def clean(self):
        for x in self.instance.scan_iter(match='{}*'.format(self.cache_prefix)):
            self.instance.delete(x)
