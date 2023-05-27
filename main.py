from apscheduler.schedulers.blocking import BlockingScheduler

from spider.byweixin import get_file_name, login_wechat, csv_head, get_content
from spider.fs_robot_send_message import get_hour, get_minute
from spider.task_weixin import task_job

if __name__ == '__main__':
    sched = BlockingScheduler()

    hour = get_hour()
    minute = get_minute()
    sched.add_job(task_job, 'cron', hour=hour, minute=minute, id='spider_weixin')
    sched.start()
