import json
import logging
import os
from datetime import datetime

import requests
from requests_toolbelt import MultipartEncoder


# 上传文件
def upload(file, authorization):
    url = "https://open.feishu.cn/open-apis/im/v1/files"
    form = {'file_type': 'stream',
            'file_name': os.path.basename(file.name),
            'file': (file.name, open(file.name, 'rb'), 'text/plain')}
    multi_form = MultipartEncoder(form)
    headers = {
        'Authorization': 'Bearer ' + authorization,  ## 获取tenant_access_token, 需要替换为实际的token
    }
    headers['Content-Type'] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=multi_form)
    print(response.headers['X-Tt-Logid'])  # for debug or oncall
    print(response.content)  # Print Response
    file_data = json.loads(response.content)
    file_key = file_data['data']['file_key']
    return file_key


def upload_img(file_path, authorization):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {'image_type': 'message',
            'image': (open(file_path, 'rb'))}  # 需要替换具体的path
    multi_form = MultipartEncoder(form)
    headers = {
        'Authorization': 'Bearer ' + authorization,  ## 获取tenant_access_token, 需要替换为实际的token
    }
    headers['Content-Type'] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=multi_form)
    print(response.headers['X-Tt-Logid'])  # for debug or oncall
    print(response.content)  # Print Response
    j = json.loads(response.content)
    image_key = j["data"]["image_key"]
    return image_key


# 发送文件消息
# 接口调用限制 1000 次/分钟、50 次/秒
def send_file(file, chatId, authorization):
    file_key = upload(file, authorization)
    response = send(authorization,
                    chatId,
                    # 文件Key，可通过上传文件接口获取文件的 file_key。
                    {"file_key": file_key},
                    "file")
    status = response.headers['X-Tt-Logid']
    print(response.content)


# 发送富文本消失
def send_post(img_file_path, chatId, authorization, user_id):
    image_key = upload_img(img_file_path, authorization)
    if image_key is not None:
        msg_content = {
            "zh_cn": {
                "title": "登陆失效请扫码重新登陆",
                "content": [
                    [{
                        "tag": "at",
                        "user_id": user_id
                    }],
                    [{
                        "tag": "img",
                        "image_key": image_key
                    }]
                ]
            }
        }
        send(authorization, chatId, msg_content, "post")


def send(authorization, chatId, msg_content, msg_type):
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": 'chat_id'}

    req = {
        "receive_id": chatId,  # chat id  消息接收者的ID,这里是群的id
        "msg_type": msg_type,  # 文件
        "content": json.dumps(msg_content)
    }
    payload = json.dumps(req)
    headers = {
        'Authorization': 'Bearer ' + authorization,  # your access token
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, params=params, headers=headers, data=payload)
    return response


def get_string_date():
    now_time = datetime.now().date()
    date_str = str(now_time);
    data_string = date_str.replace('-', '_', 3)
    return data_string


def get_chat():
    #__file__ 是一个特殊的变量，它包含当前脚本的路径
    path = os.path.abspath(os.path.dirname(__file__))
    print(path)
    json_file_path = os.path.join(path, 'config/authorization.json')
    print(json_file_path)
    with open(json_file_path, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
        print(data)
        chat_id = data['chat_id']
        return chat_id
