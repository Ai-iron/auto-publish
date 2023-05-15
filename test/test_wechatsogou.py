import wechatsogou

# 可配置参数

# 直连
ws_api = wechatsogou.WechatSogouAPI()
r = ws_api.get_gzh_article_by_history('量子位')
print(r)
