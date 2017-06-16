#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/15 09:21
# @Author  : GuoChang
# @Site    : https://github.com/xiphodon
# @File    : test.py
# @Software: PyCharm Community Edition

import requests
import json
import rsa


def get(url,params):
    r = requests.get(url=url, params=params)
    print("get:" + r.text + "\n")


def post(url,params):
    r = requests.post(url=url, data=params)
    print("post:" + r.text + "\n")

def get_post_args(post_mode=True):
    '''
    普通参数请求
    :return:
    '''
    # 导入私钥
    with open('private.pem', 'r') as f:
        privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

    # url = "http://u.ikuaichuan.com:8080/olms/api/account/login"
    url = r"http://127.0.0.1:5000/json"

    # 数据
    json_data = {"name": "admin汉字", "password": "11111111"}
    params_data = json.dumps(json_data)

    # 数据数字签名
    sign_data_bytes = rsa.sign(params_data.encode(), privkey, 'SHA-1')
    sign_data_str = sign_data_bytes.decode('iso-8859-15')
    # print(sign_data_str)

    params = {"data": params_data, "sign": sign_data_str}
    print(params)

    print("===============")

    if(post_mode):
        post(url, params)
    else:
        get(url,params)


def post_file():
    '''
    上传文件
    :return:
    '''

    url = r"http://127.0.0.1:5000/file"

    fp = open(r'files/中文名字试试.json', 'rb')

    files = {'myfile': fp}

    print("--------------------------------")

    r = requests.post(url=url, files=files)
    print("post:" + r.text + "\n")



if __name__ == "__main__":
    # get_post_args()
    post_file()