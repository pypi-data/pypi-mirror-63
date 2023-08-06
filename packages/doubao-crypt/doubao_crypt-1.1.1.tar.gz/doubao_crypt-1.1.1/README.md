# privacy-policy

## 使用说明

### 使用`doubao_crypt`

#### 安装

源码安装

```shell
# python setup install
python3 setup install
```

pip安装

```shell
pip3 install doubao-crypt
```

#### 通过cid(gid,uid)等直接加密(不需要密钥)

调用前先初始化cache

```python
from doubao_crypt import init_cache

# 使用本地缓存（字典cache）
init_cache('http://test.api2.17doubao.com', cache_type='LocalCache')
# 使用 redis来缓存
# init_cache('http://test.api2.17doubao.com', cache_type='RedisCache', cache_uri='redis://localhost/0')
```

方法init_cache使用redis来缓存时的可选参数：

* cache_prefix: 前缀，默认值'doubao-keys-'。
* cache_instance: 缓存实例（redis.Redis）。cache_instance和cache_uri传入任意一个即可
* cache_uri: 缓存uri，默认`redis://localhost/0`。cache_instance和cache_uri传入任意一个即可
* pre_cache: 是否预载数据，默认False，为True时会预先加载数据到缓存
* clean: 是否清空之前的缓存数据，默认True

> 使用`init_cache`方法初始化一次即可

使用完整示例如下：

```python
from doubao_crypt import init_cache, doubao_ecies_encrypt, doubao_privacy_policy, safe_doubao_ecies_encrypt
import redis


pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
init_cache('http://test.api2.17doubao.com', cache_type='RedisCache', cache_instance=r)

data = [
    {
        "birthday": "1973-03-02",
        "idCardType": 111,
        "idCardNo": "110101********5330",
        "sex": 1,
        "mobile": "13123456789",
        "name": "张三",
        "age": 29
    },
    {
        "mobile": "13123456788",
        "name": "李四",
        "idCardType": 111,
        "idCardNo": "513436201801012266"
    }
]

# 直接调用方法
crypted_data = doubao_ecies_encrypt(data, fields=['mobile', 'idCardNo'], cid=583, gid=583, agent_id=3692)

# 安全调用加密方法（不抛出异常，错误在返回值中）
flag, msg, crypted_data = safe_doubao_ecies_encrypt(data, fields=['mobile', 'idCardNo'], cid=583, gid=583, agent_id=3692)


# 使用装饰器
@doubao_privacy_policy(fields=['mobile', 'idCardNo'], cid=583, gid=583, agent_id=3692)
def test_doubao_privacy_policy(users):
    pass

test_doubao_privacy_policy(data)
```

> 关于多层结构的内数据的加密，`fields`中字段使用`.`来区分层级，如'data.info.mobile'

#### 通过密钥加解密

demo

```python
ecurity_service = SecurityService(
    private_key='4ddc101e5fc4e2820c7c5275050fc3dc7f8ca344afb41a3bb804afd3b5b1b8d6',
    public_key='5a66be441a4dc16b12effed07d6e6e3ee2e8753e0dcaac07be71190f19f43b277e10c174bccbb50286d6a65e11b25d957ef8bed80c192e8a8178a3715c56cf7a')

text_list = [
    '123456789987654321',
    '1234567****7654321',
    '1234567XXXX7654321',
    '1234567xxxx7654321',
    '123',
]
for text in text_list:
    cipher_text = security_service.ecies_encrypt(text)  # 加密
    plain_text = security_service.ecies_decrypt(cipher_text)  #  解密
    print(f'======[ {text} ]=======')
    print('cipher_text', cipher_text)
    print('plain_text', plain_text)
```
