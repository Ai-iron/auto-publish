import json
import logging

import requests

# 分享群名片
# 接口调用限制 1000 次/分钟、50 次/秒
def send(msg,chatId,authorization):
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": "chat_id"}
    msgContent = {
        "chat_id": msg # 群组ID（chat_id）
    }
    req = {
        "receive_id": chatId,  # chat id  消息接收者的ID,这里是群的id
        "msg_type": "share_chat",
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
        logging.error("分享群名片失败，错误信息："+response.content)

