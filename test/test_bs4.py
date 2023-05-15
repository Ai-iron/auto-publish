# from bs4 import BeautifulSoup
# import requests
#
# url='https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247676121&idx=1&sn=ae5fe85804061a53f6f8751e33601581&chksm=e8de87abdfa90ebde071416983541a3f81bcf7fbf7082be9d417e9227ad24229267859cfe790&token=1542279541&lang=zh_CN#rd'
# session = requests.Session()
# # 假设content_body是包含HTML文本的字符串变量
# content_body = session.get(url=url).text
#
# print(content_body)
#
# # 创建一个BeautifulSoup对象
# soup = BeautifulSoup(content_body, 'html.parser')
#
# # 使用find方法查找id为publish_time的元素
# publish_time_element = soup.find(id='publish_time')
#
# # 获取元素的文本内容
# publish_time_text = publish_time_element.text
#
# # 打印输出文本内容
# print(publish_time_text)


from bs4 import BeautifulSoup
import requests

url = 'https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247676121&idx=1&sn=ae5fe85804061a53f6f8751e33601581&chksm=e8de87abdfa90ebde071416983541a3f81bcf7fbf7082be9d417e9227ad24229267859cfe790&token=1542279541&lang=zh_CN#rd'

# 发送GET请求获取页面内容
response = requests.get(url)

# 创建一个BeautifulSoup对象
soup = BeautifulSoup(response.content, 'html.parser')

# 使用find方法查找class为rich_media_meta_list的元素
meta_list = soup.find('div', class_='rich_media_meta_list')

# 找到发布时间所在的li元素，并获取文本内容
publish_time_text = meta_list.find('span', class_='rich_media_meta rich_media_meta_text').get_text()

# 打印输出发布时间
print(publish_time_text)
