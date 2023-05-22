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
    return response.text

if __name__ == '__main__':
    bb = get_token()
    df = json.loads(bb)
    authorization = df['tenant_access_token']
    print(authorization)

