#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_script import Manager
from flask import request
import json
import rsa
import os
from flask import jsonify
from werkzeug.utils import secure_filename
import time
import random
import base64
# import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')

app = Flask(__name__)

manager = Manager(app)


UPLOAD_FOLDER='upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt','json','xls','xlsx'])


def allowed_file(filename):
    '''
    用于判断文件后缀
    :param filename:
    :return:
    '''
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/json' , methods=['GET', 'POST'])
def post_test():
    '''
    验证数据（数字签名）
    :return:
    '''
    if request.method == 'POST':

        all_data = request.values
        print(all_data)

        data = request.values.get('data')
        # print(type(data))
        # print(data)

        sign = request.values.get('sign')
        # print(type(sign))
        # print(sign)

        # 导入公钥
        with open('public.pem', 'r') as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())

        # print(sign.encode('iso-8859-15'))

        try:
            if rsa.verify(data.encode(),sign.encode('iso-8859-15'), pubkey):
                json_loads = json.loads(data)
                name = json_loads['name']
                print(name)
                return name
            else:
                return jsonify({"result":"verify false"})
        except:
            return jsonify({"result":"verify false"})
    else:
        return jsonify({"result":"post only"})



@app.route('/json2' , methods=['GET', 'POST'])
def post_test2():
    '''
    解密数据
    :return:
    '''
    if request.method == 'POST':

        all_data = request.values
        print(all_data)

        data_sign = request.values.get('data')
        print(type(data_sign))
        print(data_sign)

        # 导入私钥
        with open('private.pem', 'r') as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

        # 私钥解密
        data_str = rsa.decrypt(data_sign.encode('iso-8859-15'), privkey).decode('unicode-escape')
        print(data_str)

        try:
            data_dic = json.loads(data_str)
            name_ = data_dic["name"]
            return jsonify({"name":name_})

        except Exception as e:
            print(e)
            return jsonify({"result":"type error"})

    else:
        return jsonify({"result":"post only"})


@app.route('/file' , methods=['GET', 'POST'])
def file_upload():
    '''
    上传文件
    :return:
    '''
    if request.method == 'POST':
        file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = request.files['myfile']  # 文件的key
        if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
            file_all_name = f.filename
            file_name = file_all_name.rsplit('.', 1)[0] # 文件名（无后缀）
            ext = file_all_name.rsplit('.', 1)[1] # 后缀名
            file_name_no_chinese = str(file_name.encode())
            file_all_name_new = file_name_no_chinese + '.' + ext

            fname = secure_filename(file_all_name_new)
            # ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
            print(fname)
            unix_time = int(time.time() * 1000)
            new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
            f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
            # token = base64.b64encode(new_filename)
            # print(token)
            return jsonify({"result": 1, "msg": "upload success"})
        else:
            return jsonify({"result": 0, "msg": "upload failed"})
    else:
        return jsonify({"result":"post only"})



@app.route('/test/<info>')
def user(info):
    return '{"return":"true","meg":\"%s\"}' % info


if __name__ == '__main__':
    # manager.run()
    app.run(debug=True)
