# -*- coding: utf-8 -*-
import re
import csv
import json
import time
import random
import requests
import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import uuid
from PIL import Image

cookie_file_path = './file/cookie.txt'


def login_wechat(relogin):
    # 不重新登陆 存在cookie 直接用cookie
    if not relogin and os.path.exists(cookie_file_path):
        return
    if relogin:
        os.remove(cookie_file_path)
    browser = webdriver.Chrome()
    browser.get("https://mp.weixin.qq.com/")
    # 等待页面加载完成
    WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'login_frame')))
    png_file = fr"./file/{uuid.uuid4()}.png"
    browser.find_element(By.CLASS_NAME, "login_frame").screenshot(png_file)
    # todo 发飞书消息
    print("请拿手机扫码二维码登录公众号")
    time.sleep(30)
    print("登录成功")
    # 获取cookies
    cookie_items = browser.get_cookies()
    post = {}
    # 获取到的cookies是列表形式，将cookies转成json形式并存入本地名为cookie的文本中
    for cookie_item in cookie_items:
        post[cookie_item['name']] = cookie_item['value']
    cookie_str = json.dumps(post)
    with open(cookie_file_path, 'w+', encoding='utf-8') as f:
        f.write(cookie_str)
    print("cookies信息已保存到本地")
    browser.quit()


def get_content(ky, file_name):
    # ky为要爬取的公众号名称
    url = 'https://mp.weixin.qq.com'  # 公众号主页
    header = {
        "HOST": "mp.weixin.qq.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    # 读取上一步获取到的cookies
    with open(cookie_file_path, 'r', encoding='utf-8') as f:
        cookie = f.read()
    cookies = json.loads(cookie)
    # 增加重试连接次数
    session = requests.Session()
    session.keep_alive = False
    # 增加重试连接次数
    session.adapters.DEFAULT_RETRIES = 10
    time.sleep(5)
    # 登录之后的微信公众号首页url变化为：https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=657944522，从这里获取token信息
    response = session.get(url=url, cookies=cookies)
    findall = re.findall(r'token=(\d+)', str(response.url))
    # 重新登陆
    try_times = 3
    while len(findall) == 0 and try_times > 0:
        print("登陆失效，请重新登陆")
        login_wechat(True)
        # 重新用cookie拿token
        with open(cookie_file_path, 'r', encoding='utf-8') as f:
            cookie = f.read()
        cookies = json.loads(cookie)
        response = session.get(url=url, cookies=cookies)
        findall = re.findall(r'token=(\d+)', str(response.url))
        print(findall)
        try_times = try_times - 1
    if len(findall) == 0:
        print(fr"获取{ky}文章中 登陆失败！！进入下一个")
        # todo  机器人告警
        return
    token = findall[0]
    time.sleep(2)
    # 搜索微信公众号的接口地址
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    # 搜索微信公众号接口需要传入的参数，有三个变量：微信公众号token、随机数random、搜索的微信公众号名字
    query_id = {
        'action': 'search_biz',
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'query': ky,
        'begin': '0',
        'count': '5'
    }
    # 打开搜索微信公众号接口地址，需要传入相关参数信息如：cookies、params、headers
    search_response = session.get(search_url, cookies=cookies, headers=header, params=query_id)
    # 取搜索结果中的第一个公众号
    lists = search_response.json().get('list')[0]
    # print(lists)
    # 获取这个公众号的fakeid，后面爬取公众号文章需要此字段
    fakeid = lists.get('fakeid')

    # 微信公众号文章接口地址
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    # 搜索文章需要传入几个参数：登录的公众号token、要爬取文章的公众号fakeid、随机数random
    query_id_data = {
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '0',  # 不同页，此参数变化，变化规则为每页加5
        'count': '5',
        'query': '',
        'fakeid': fakeid,
        'type': '9'
    }
    # 打开搜索的微信公众号文章列表页
    appmsg_response = session.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
    # 获取文章总数
    max_num = appmsg_response.json().get('app_msg_cnt')
    # 每页至少有5条，获取文章总的页数，爬取时需要分页爬
    total_num = int(int(max_num) / 5)
    print(fr'总页数：{total_num}--------------{ky}')
    # 起始页begin参数，往后每页加5
    begin = 0
    seq = 0
    # 设置Chrome浏览器驱动的路径
    driver_path = '/path/to/chromedriver'
    # 创建Chrome浏览器驱动
    service = Service(driver_path)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=service, options=options)
    while total_num + 1 > 0:
        query_id_data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '{}'.format(str(begin)),
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
        }
        print(fr'正在翻页：--------------{int(int(begin) / 5)}/{total_num}')
        time.sleep(8)

        # 获取每一页文章的标题和链接地址，并写入本地文本中
        query_fakeid_response = session.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
        fakeid_list = query_fakeid_response.json().get('app_msg_list')
        if fakeid_list:
            for item in fakeid_list:
                content_link = item.get('link')
                content_title = item.get('title')

                seq += 1
                datestr, content = get_webpage(driver, content_link)
                if not is_current_date(datestr):
                    total_num = -1
                    print(fr'翻页结束：--------------今天内容收集完毕-{ky}')
                    break
                info = [ky, content_title, content_link, content]
                save(file_name, info)
        begin = int(begin)
        begin += 5
        total_num -= 1
    # 关闭浏览器
    driver.quit()


# csv head
def csv_head(file_name):
    head = ['公众号', 'content_title', 'content_link', 'content_body', ]
    save(file_name, head)


# 存储csv
def save(file_name, info):
    csvFile = open(fr'./file/{file_name}.csv', 'a+', newline='', encoding='utf-8-sig')  # 设置newline，否则两行之间会空一行
    writer = csv.writer(csvFile)
    writer.writerow(info)
    csvFile.close()


# 获取发布时间
def get_webpage(driver, url):
    # 打开链接
    driver.get(url)

    # 等待页面加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'rich_media_meta_list')))

    # 获取页面
    webpage_text = driver.page_source

    # 创建一个BeautifulSoup对象
    soup = BeautifulSoup(webpage_text, 'html.parser')
    # 查找发布时间元素，并获取文本内容
    publish_time_element = soup.find(id='publish_time')
    publish_time_text = publish_time_element.text

    # 返回发布时间和页面文本
    return publish_time_text, soup.find(id='js_content').text.strip()


def is_current_date(publish_time_text):
    # 将publish_time_text字符串转换成datetime对象
    publish_time = datetime.datetime.strptime(publish_time_text, '%Y-%m-%d %H:%M')

    # 获取当前日期时间
    now = datetime.datetime.now()

    # 判断发布日期是否是当前日期
    return publish_time.date() == now.date()


def get_file_name(key):
    now_str = datetime.datetime.now().strftime("_%Y_%m_%d_%H_%M_%S")
    return '今日文章_' + key + now_str
