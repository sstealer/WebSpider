# 可以运行，但是内容处理的不是很完美
from pyquery import PyQuery as pq
import csv
import time

begin=time.clock()

def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
    doc=pq(url,headers=headers)
    return doc

def parse_page(doc):
    lis=doc('.bang_list.clearfix.bang_list_mode li')
    #print(lis)
    for item in lis.items():     
        yield{
            'name':item.find('.name').find('a').attr('title'),
            'author':item.find('div:nth-child(5)').text(),
            'img':item.find('.pic a img').attr('src'),
            'star':item.find('.star').text(),
            'data_locate':item.find('div:nth-child(6)').text(),
            'count':item.find('.biaosheng').text(),
            'price':item.find('.price').find('p:nth-child(1)').find('.price_n').text(),


        }

def write_to_file(item):
     writer.writerow((item['name'], item['author'], item['img'], item['star'], item['data_locate'], item['count'],item['price']))

def main():
    for i in range(1,26):
        url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-'+str(i)
        doc = get_page(url)
        for item in parse_page(doc):
            print(item)
            write_to_file(item)
        time.sleep(1)#推迟线程，防止被检测出时爬虫


if __name__ == '__main__':
    f=open('dangdang.csv','a',newline='',encoding='utf-8')
    writer=csv.writer(f)
    writer.writerow(('Name','Author','Img','Star','Data_Locate','Count','Price'))
    main()
    f.close()
    end=time.clock()
    print("爬取完毕，CPU耗时：%f s"%(end-begin))
