#coding=utf-8
from uiautomator import device as d
import time
from threading import Timer
import requests

headers = {
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; ATH-AL00 Build/HONORATH-AL00) appleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.0 Mobile Safari/537.36",
            }

# print d.request("get", "https://www.baidu.com")
# print d.request("get", "https://www.ipip.net/ip.html")
print d.request("get", "https://www.ip.cn", headers=headers)

# print requests.get("https://www.ip.cn", headers=headers)








