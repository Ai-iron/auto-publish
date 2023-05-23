import json
import logging
from datetime import datetime

import requests
from requests_toolbelt import MultipartEncoder


# 上传文件
def upload(file,authorization):
  url = "https://open.feishu.cn/open-apis/im/v1/files"
  form = {'file_type': 'stream',
          'file_name': file.name,
          'file':  (file.name, open(file.path, 'rb'), 'text/plain')}
  multi_form = MultipartEncoder(form)
  headers = {
    'Authorization': 'Bearer '+authorization, ## 获取tenant_access_token, 需要替换为实际的token
  }
  headers['Content-Type'] = multi_form.content_type
  response = requests.request("POST", url, headers=headers, data=multi_form)
  print(response.headers['X-Tt-Logid']) # for debug or oncall
  print(response.content) # Print Response
  return response.content


# 发送文件消息
# 接口调用限制 1000 次/分钟、50 次/秒
def send(msg,chatId,authorization):
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": 'chat_id'}
    msgContent = {
        "file_key": msg #文件Key，可通过上传文件接口获取文件的 file_key。
    }
    req = {
        "receive_id": chatId,  # chat id  消息接收者的ID,这里是群的id
        "msg_type": "file", #文件
        "content": json.dumps(msgContent)
    }
    payload = json.dumps(req)
    headers = {
        'Authorization': 'Bearer '+authorization,  # your access token
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, params=params, headers=headers, data=payload)
    status = response.headers['X-Tt-Logid']
    print(response.content)

def get_string_data():
    now_time = datetime.now().date()
    date_str = str(now_time);
    data_string = date_str.replace('-', '_', 3)
    return data_string

def get_chat(json_file):
    with open(json_file, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
        print(data)
        chat_id = data['chat_id']
        return chat_id
