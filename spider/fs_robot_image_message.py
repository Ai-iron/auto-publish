import json
import logging

import requests

# 发送图片消息
# 接口调用限制 1000 次/分钟、50 次/秒
def send(msg,chatId,authorization):
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": "chat_id"}
    msgContent = {
        "image_key": msg
    }
    req = {
        "receive_id": chatId,  # chat id  消息接收者的ID,这里是群的id
        "msg_type": "image_key", # 图片
        "content": json.dumps(msgContent)
        # “uuid”: xxx 由开发者生成的唯一字符串序列，用于发送消息请求去重；持有相同uuid的请求1小时内至多成功发送一条消息
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

