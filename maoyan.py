"""
1,pyquery get the data and save as csv
2,pyquery get the data and save as txt
"""

# pyquery get the data and save as csv
from pyquery import PyQuery as pq
import csv
import time

begin = time.clock()  # 添加程序开始时间


def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
    doc = pq(url, headers=headers)
    return doc


def parse_page(doc):
    dict = {}
    dd = doc('.board-wrapper').find('dd')
    for item in dd.items():
        yield {
            'rank': item.find('.board-index').text(),
            'name': item.find('.name').text(),
            'img': item.find('.board-img').attr('data-src'),
            'star': item.find('.star').text(),
            'time': item.find('.releasetime').text().strip(),
            'score': item.find('.score').find('.integer').text().strip() + item.find('.score').find(
                '.fraction').text().strip(),
        }


def write_to_file(item):
    writer.writerow((item['rank'], item['name'], item['img'], item['star'], item['time'], item['score']))


def main():
    for i in range(10):
        url = 'https://maoyan.com/board/4?offset=' + str(i * 10)
        doc = get_page(url)
        # print(doc)
        for item in parse_page(doc):
            print(item)
            write_to_file(item)
        # 线程推迟1s,一些反爬取网站,如果速度过快会无响应,故增加一个延时等待
        time.sleep(1)


if __name__ == '__main__':
    f = open('test.csv', 'a', newline='', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(('Rank', 'Name', 'Picture', 'Star', 'Time', 'Score'))
    main()
    f.close()
    end = time.clock()  # 添加程序结束时间
    # 输出CPU耗时,不包括线程推迟的时间,是正常情况下（不考虑等待）程序的耗时
    print("爬取完毕,CPU耗时：%f s" % (end - begin))




# '''pyquery get the data and save as txt'''
# import json
# import time
# import requests
# from pyquery import PyQuery as pq
#
# def get_page(url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
#     }
#     doc=pq(url)
#     return doc
#
#
# def parse_page(doc):
#
#      dd=doc('.board-wrapper').find('dd')
#
#      for item in dd.items():
#          yield {
#              'index': item.find('.board-index').text(),
#              'image': item.find('.board-img').attr('data-src'),
#              'title': item.find('.name').text(),
#              'actor': item.find('.star').text().strip()[3:],
#              'time': item.find('.releasetime').text(),
#              'score': item.find('.score').find('.integer').text().strip() + item.find('.score').find(
#                  '.fraction').text().strip()
#          }
#
# def write_to_file(item):
#     with open('test.csv','a',encoding='utf-8') as f:
#         f.write(json.dumps(item,ensure_ascii=False)+'\n')#False表示不使用ascii表示中文，可以直接显示中文
#
#
# def main():
#     for i in range(10):
#         url = 'https://maoyan.com/board/4?offset='+str(i*10)
#         doc=get_page(url)
#         for item in parse_page(doc):
#             print(item)
#             write_to_file(item)
#
# # url = 'https://maoyan.com/board/4?offset='+str(0*10)
# # doc=get_page(url)
# # dd=doc('#app > div > div > div.main > dl > dd > div > div > div.movie-item-info > p.name > a')
# # for d in dd.items():
# #     print(d.text())
#

