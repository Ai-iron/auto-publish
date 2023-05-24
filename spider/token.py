import requests
import json


def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({
        "app_id": "cli_a4e27a496ff8500c",
        "app_secret": "yO7d2BNRCUlu6qSYhT0drbHD4NKK6gZj"
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    # todo redis 两个小时缓存复用
    return json.loads(response.text)['tenant_access_token']


if __name__ == '__main__':
    bb = get_token()
    print(bb)
