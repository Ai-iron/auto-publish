import json
import os

import jsonpath as jsonpath
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from spider.byweixin import login_wechat, get_file_name, csv_head, get_content
from spider.fs_robot_send_message import upload, send_file, get_string_date, get_chat
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


