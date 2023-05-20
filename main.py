from apscheduler.schedulers.blocking import BlockingScheduler

from spider.byweixin import get_file_name, login_wechat, csv_head, get_content
from spider.task_weixin import task_job

if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(task_job, 'cron', hour="11", minute="33", id='spider_weixin')
    sched.start()
