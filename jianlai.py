# -*- coding: UTF-8 -*-
import requests
from pyquery import PyQuery as pq
# 简单的防反爬处理：修改请求头内容
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
           'Referer': 'http://www.jianlaixiaoshuo.com/',
           }
# 定义一个下载小说内容的函数，需要的参数为每章小说的链接
def download(url):
    #  获取每章小说的标题和内容
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding  # 防止响应体出现乱码
    html = pq(response.text)
    title = html('#BookCon > h1').text()  # 标题
    print('正在下载：' + title)            # 提示爬取进度
    content = html('#BookText').text()    # 内容
    #  保存到本地文件
    with open('剑来.txt', mode='a+', encoding='utf-8') as f:
        f.write(title)
        f.write('\n')   # 调整格式
        f.write(content)
        f.write('\n')
# 获取每章小说的链接地址
response = requests.get("http://www.jianlaixiaoshuo.com/", headers=headers)
response.encoding = response.apparent_encoding  # 防止响应体出现乱码
html = pq(response.text)
links = html('body > div:nth-child(2) > div > dl > dd > a')
for link in links.items():
    url = 'http://www.jianlaixiaoshuo.com' + link.attr.href  # 拼接出完整链接
    download(url)   # 调用下载函数
