from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from spider.byweixin import login_wechat, get_file_name, csv_head, get_content


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


