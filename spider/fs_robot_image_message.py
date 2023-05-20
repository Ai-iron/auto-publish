import json
import logging

import requests
from requests_toolbelt import MultipartEncoder


# 上传文件
def upload(file,authorization):
  url = "https://open.feishu.cn/open-apis/im/v1/files"
  form = {'file_type': 'stream',
          'file_name': file.name,
          'file':  ('text.txt', open(file.path, 'rb'), 'text/plain')}
  multi_form = MultipartEncoder(form)
  headers = {
    'Authorization': 'Bearer '+authorization, ## 获取tenant_access_token, 需要替换为实际的token
  }
  headers['Content-Type'] = multi_form.content_type
  response = requests.request("POST", url, headers=headers, data=multi_form)
  print(response.headers['X-Tt-Logid']) # for debug or oncall
  print(response.content) # Print Response
  return response


# 发送文件消息
# 接口调用限制 1000 次/分钟、50 次/秒
def send(msg,chatId,authorization):
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": chatId}
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
    if status != 0:
        logging.error("发送图片失败，错误信息："+response.content)