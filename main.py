from spider.byweixin import get_file_name, login_wechat, csv_head, get_content

if __name__ == '__main__':

    # sources =
    sources = {"ai圈": ['量子位', '36kr', '虎嗅','智东西','三次方','AIGC开放社区','AI进化社','AI前线','机器之心'],
               "北京本地": ['北京市成公信息发布平台', '大北京早知道', '北京本地宝', '最爱大北京', '北京人社', '北京日报', '北京新闻']}

    login_wechat(False)

    for ky in sources:
        fn = get_file_name(ky)
        csv_head(fn)
        for account in sources[ky]:
            get_content(account, fn)
