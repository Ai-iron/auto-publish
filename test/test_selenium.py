from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# 设置Chrome浏览器驱动的路径
driver_path = '/path/to/chromedriver'

# 创建Chrome浏览器驱动
service = Service(driver_path)
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=service, options=options)




# 获取发布时间
def get_webpage(driver, url):
    # 打开链接
    driver.get(url)

    # 等待页面加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'rich_media_meta_list')))

    # 获取页面文本
    webpage_text = driver.page_source

    # 创建一个BeautifulSoup对象
    soup = BeautifulSoup(webpage_text, 'html.parser')
    # js_content
    print(soup.find(id='js_content').text.strip())
    # 查找发布时间元素，并获取文本内容
    publish_time_element = soup.find(id='publish_time')
    publish_time_text = publish_time_element.text

    # 返回发布时间和页面文本
    return publish_time_text, webpage_text

# 微信公众号文章的链接
url = 'https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247676121&idx=1&sn=ae5fe85804061a53f6f8751e33601581&chksm=e8de87abdfa90ebde071416983541a3f81bcf7fbf7082be9d417e9227ad24229267859cfe790&token=1542279541&lang=zh_CN#rd'
get_webpage(driver, url)
# print(t,c)
# 关闭浏览器
driver.quit()
