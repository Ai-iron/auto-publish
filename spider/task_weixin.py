import json
import os

import jsonpath as jsonpath
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from spider.byweixin import login_wechat, get_file_name, csv_head, get_content
from spider.fs_robot_image_message import upload, send


class file_stream:
    def __init__(self,name,path):
        self.name=name
        self.path=path

def task_job():
    print(f'定时任务在执行{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    sources = {"ai圈": ['量子位', '36kr', '虎嗅','智东西','三次方','AIGC开放社区','AI进化社','AI前线','机器之心'],
               "北京本地": ['北京市成公信息发布平台', '大北京早知道', '北京本地宝', '最爱大北京', '北京人社', '北京日报', '北京新闻']}
    login_wechat(False)
    for ky in sources:
        fn = get_file_name(ky)
        csv_head(fn)
        for account in sources[ky]:
            get_content(account, fn)
    print(f'定时任务结束{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    print(f'获取爬虫的cvs内容，并发送到群流程开始-------{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    path = os.path.dirname(os.getcwd()) + "\\file"

    now_time = datetime.now().date()
    date_str = str(now_time);
    data_string = date_str.replace('-', '_', 3)

    json_file = os.path.dirname(os.getcwd()) + "\\config\\authorization.json"
    with open(json_file, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
        print(data)
        authorization = data['Authorization']

    file_list = []

    files = os.listdir(path)
    for f in files:
        if (data_string in f) and (f.endswith(".csv")):
            file_list.append(path + "\\" + f);
            file_stream.name = data_string
            file_stream.path = path + "\\" + f
            file_key = upload(file_stream, authorization);
            send(file_key);

    print(f'获取爬虫的cvs内容，并发送到群流程j结束-------{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')


