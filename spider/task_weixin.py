import json
import os

import jsonpath as jsonpath
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from spider.byweixin import login_wechat, get_file_name, csv_head, get_content
from spider.fs_robot_send_message import upload, send, get_string_data, get_chat
from spider.token import get_token


class file_stream:
    def __init__(self, name, path):
        self.name = name
        self.path = path


def task_job():
    print(f'定时任务在执行{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(os.getcwd())
    # 读取JSON文件
    with open('./config/wechat_test.json') as file:
        weixin_conf = json.load(file)

    for item in weixin_conf:
        get_content(item)

    print(f'定时任务结束{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    print(f'获取爬虫的cvs内容，并把文件发送到群的流程结束-------{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    path = os.path.dirname(os.getcwd()) + "\\file"

    data_string = get_string_data()
    token_data = get_token()
    token_json = json.loads(token_data)
    authorization = token_json['tenant_access_token']

    json_file = os.path.dirname(os.getcwd()) + "\\config\\authorization.json"
    chat_id = get_chat(json_file)

    file_list = []

    files = os.listdir(path)
    for f in files:
        if (data_string in f) and (f.endswith(".csv")):
            file_list.append(path + "\\" + f)
            file_stream.name = os.path.basename(path + "\\" + f)
            file_stream.path = path + "\\" + f
            file_key = upload(file_stream, authorization)
            file_data = json.loads(file_key)
            message = file_data['data']['file_key']
            send(message, chat_id, authorization)

    print(f'获取爬虫的cvs内容，并把文件发送到群的流程结束-------{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
