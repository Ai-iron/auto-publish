from spider.byweixin import get_file_name, login_wechat, csv_head, get_content

if __name__ == '__main__':
    kys = ['量子位', '36kr', '虎嗅']
    fn = get_file_name()
    login_wechat(False)
    csv_head(fn)
    for ky in kys:
        get_content(ky, fn)