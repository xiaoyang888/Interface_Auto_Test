import os
import base64
from time import time

import rsa

from scripts.handle_path import CONFIGS_DIR
from scripts.handle_yaml import do_yaml


class HandleSign:

    @classmethod
    def to_encrypt(cls, msg, pub_key=None):
        """
        非对称加密
        :param msg: 待加密字符串或者字节
        :param pub_key: 公钥
        :return: 密文
        """
        if isinstance(msg, str):  # 如果msg为字符串, 则转化为字节类型
            msg = msg.encode('utf-8')
        elif isinstance(msg, bytes):  # 如果msg为字节类型, 则无需处理
            pass
        else:  # 否则抛出异常
            raise TypeError('msg必须为字符串或者字节类型!')

        if not pub_key:  # 如果pub_key为空, 则使用全局公钥
            # 获取公钥文件名
            public_key_filename = do_yaml.read("api", "public_key_filename")
            # 获取公钥文件所在路径
            public_key_path = os.path.join(CONFIGS_DIR, public_key_filename)
            with open(public_key_path, 'rb') as file:  # 读取公钥
                pub_key = file.read()

        elif isinstance(pub_key, str):  # 如果pub_key为字符串, 则转化为字节类型
            pub_key = pub_key.encode('utf-8')
        elif isinstance(pub_key, bytes):  # 如果msg为字节类型, 则无需处理
            pass
        else:  # 否则抛出异常
            raise TypeError('pub_key必须为None、字符串或者字节类型!')

        public_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)  # 创建 PublicKey 对象

        cryto_msg = rsa.encrypt(msg, public_key_obj)  # 生成加密文本
        cipher_base64 = base64.b64encode(cryto_msg)  # 将加密文本转化为 base64 编码

        return cipher_base64.decode()  # 将字节类型的 base64 编码转化为字符串类型

    @classmethod
    def generate_sign(cls, token, timestamp=None):
        """
        生成sign
        :param timestamp: 当前秒级时间戳, 为int类型
        :param token: token, 为str类型
        :return: 时间戳和sign组成的字典
        """
        timestamp = timestamp or int(time())  # 获取当前的时间戳
        prefix_50_token = token[:50]  # 获取token前50位
        message = prefix_50_token + str(timestamp)  # 将token前50位与时间戳字符串进行拼接
        sign = cls.to_encrypt(message)  # 生成sign

        return {"timestamp": timestamp, "sign": sign}


if __name__ == '__main__':
    my_token = "'eyJhbGciOiJIUzUxMiJ9.eyJtZW1iZXJfaWQiOjI2NSwiZXhwIjoxNTc0NjY3MjMzfQ.ftrNcidmk_zxwl0" \
               "wzdhE5_39bsGlILoSSoTCy043fjhbjhCFG4FwCnOj4iy5svbDlSbgCJM3qRa1zsXJLJmH4A'"

    cryto_info = HandleSign.generate_sign(my_token)
    print(cryto_info)
    pass
