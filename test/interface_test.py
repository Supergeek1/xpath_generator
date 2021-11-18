import json

import requests

with open('../10-11/htmls/wangyi.html') as f:
    html = f.read()

strings = '联播+｜推动我国数字经济健康发展 习近平作出最新部署'
resp = requests.post('http://127.0.0.1:8000/xpath', data=json.dumps({'html': html, 'strings': strings}))
print(resp.json())
