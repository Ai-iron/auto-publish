import json
import os

import jsonpath as jsonpath
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from spider.byweixin import login_wechat, get_file_name, csv_head, get_content
from spider.token import get_token


def task_job():
    print(f'定时任务在执行{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(os.getcwd())
    # 读取JSON文件
    with open('./config/wechat_test.json',encoding='utf-8') as file:
        weixin_conf = json.load(file)

    for item in weixin_conf:
        get_content(item)

    print(f'定时任务结束{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')


