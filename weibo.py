import os
import shutil
import time
from selenium import webdriver
import requests
from pyquery import PyQuery as pq
import pymongo

client=pymongo.MongoClient(host='localhost',port=27017)

db=client.weibo #指定数据库

proxy = "http://171.211.13.89:4257"#设置代理IP

def make_dir(name):
    global path
    path=name
    if not os.path.exists(name):
        os.mkdir(name)
    else:
        shutil.rmtree(name)
        os.mkdir(name)

def save_image(title,url):
    print("正在下载图片:%s..." % url)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(os.getcwd() + '/'+path, title, 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('已经下载了', file_path)
            return 1
    except requests.ConnectionError:
        print('存储图片失败')
        return 0

# 测试代理IP
def check_ip():
    print(r'正在检查代理IP是否可用...')
    # 测试ip是否可用

    proxies = {
        'http': proxy,
        'https': proxy,
    }

    print('当前测试的代理IP为：' + proxy)

    print('...')

    print('测试结果：')

    try:
        # 超时设置,避免使用不稳定的IP
        r = requests.get('http://ip111.cn/',
                         proxies=proxies,timeout=3)

        r.encoding = 'utf-8'

        doc = pq(r.text)
        # print(doc)
        ip = doc('body > div.container '
                 '> div.card-deck.mb-3.text-center')

        ip = str(ip.find('div:nth-child(1) > div.card-header').text()) + \
             " : " + \
             str(ip.find('div:nth-child(1) > div.card-body > p:nth-child(1)').text())

        print(ip)

        print('ip可正常使用...')

    except:

        print("抱歉，此IP无法使用，请更换IP重试")

        os._exit(0)

def log_in():

    chromeOptions = webdriver.ChromeOptions()

    chromeOptions.add_argument("--proxy-server={0}".format(proxy))#设置代理

    chromeOptions.add_argument('lang=zh_CN.UTF-8')

    chromeOptions.add_argument(
        'User-Agent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/76.0.3809.100 Safari/537.36"'
    )

    global browser

    browser = webdriver.Chrome(chrome_options=chromeOptions)

    try:

        print(u'正在登陆新浪微博手机端...')

        #给定登陆的网址
        url = 'https://passport.weibo.cn/signin/login'

        browser.get(url)

        time.sleep(3)
        #找到输入用户名的地方，并将用户名里面的内容清空，然后送入你的账号
        username = browser.find_element_by_css_selector('#loginName')

        time.sleep(2)

        username.clear()

        username.send_keys('2vg58g0y3b@touzi580.com')#输入自己的账号
        #找到输入密码的地方，然后送入你的密码

        password = browser.find_element_by_css_selector('#loginPassword')

        time.sleep(2)

        password.send_keys('91ih6d7j')

        #点击登录
        browser.find_element_by_css_selector('#loginAction').click()

        #这里给个15秒非常重要，因为在点击登录之后，新浪微博会有个验证码，
        #下图有，通过程序执行的话会有点麻烦，这里就手动
        time.sleep(15)


    except:

        print('登录出现错误，请检查网速或者代理IP是否稳定!!!')

        os._exit(0)

    browser.get('http://weibo.cn/' + id + '/info')

    doc = pq(browser.page_source, parser='html')

    if doc.find('.login-wrapper'):

        print('登录出现错误，请检查网速或者代理IP是否稳定!!!')

        browser.close()

        os._exit(0)

    print('完成登陆!')

def get_basic_info(id):

    dict = {
        '_id':'基本信息'
    }

    global url
    url = 'http://weibo.cn/' + id

    try:

        browser.get(url + '/info')#这里可能出现获取不到页面的情况

    except TimeoutError:

        print("请求超时，节点可能不太稳定，请跟换节点")

        os._exit(0)

    except:

        print("出现错误，错误uid")

        os._exit(0)

    doc = pq(browser.page_source,parser='html')

    if doc.find('.tm'): j=1
    else : j=0

    info = doc('body > div:nth-child('+str(6+j)+')').text()

    nickname = str(info).split('\n', 1)[0]
    print(nickname)

    dict[nickname.split(':')[0]] = nickname.split(':')[1]

    #创建存储该用户图片的文件夹，命名为用户昵称
    make_dir(dict[nickname.split(':')[0]])

    dict['uid'] = id

    other_info = str(info).split('\n', 1)[1].strip()[:-5]

    img = doc('body > div:nth-child('+str(3+j)+')> img').attr('src')
    img = '头像:' + str(img)
    print(img)

    dict[img.split(':',1)[0]] = img.split(':',1)[1]

    rank = doc('body > div:nth-child('+str(4+j)+')').text()

    rank = str(rank).split('\n', 1)[0].split('：')[1].strip()[:2]
    rank = '会员等级:' + rank

    print(rank)

    dict[rank.split(':')[0]] = rank.split(':')[1]

    other_info=other_info.replace('：',':')

    print(other_info)

    other_info=other_info.strip()

    for a in other_info.split('\n'):

        dict[a.split(':')[0]]=a.split(':')[1]

    browser.get(url)

    doc = pq(browser.page_source, parser='html')

    follow_and_fans = str(doc('body > div.u > div').text()).strip().split('分')[0]

    follow_and_fans=follow_and_fans.strip() #去处前后空格

    for a in follow_and_fans.split():

        t = a.split('[')[1]

        dict[a.split('[')[0]+'数']=t.split(']')[0]

    if save_image(nickname.split(':')[1]+'的头像',dict[img.split(':',1)[0]]):
        print(nickname.split(':')[1]+'的头像下载成功')

    try:
        collection.insert_one(dict)

    except:
        print('基本信息存储进mongodb出现错误')
        os._exit(0)

    finally:
        tot_page = doc('#pagelist > form > div').text()

        tot_page = str(tot_page).split('/')[1][:-1]

        return tot_page

def get_weibo(tot_page):

    for k in range(1,int(tot_page)+1):

        browser.get(url+'?page='+str(k))

        doc=pq(browser.page_source,parser='html')

        c = doc('.c')
        lens = len(c)
        c = c.items()

        i = 0;j=1


        for cc in c:

            dict = {}

            i = i + 1

            if (i == 1): continue
            if (i == lens - 1): break

            print("正在爬取第"+str(k)+"页，第"+str(j)+"条微博...")

            dict['_id'] = cc.find('div > span.ct').text()

            dict['info'] = cc.find('.ctt').text()

            dict['img'] = cc.find('div:nth-child(2) > a:nth-child(1) > img').attr('src')

            if dict['img']:

                dict['img']=dict['img'].replace('wap180', 'large')

                if save_image(dict['_id'], dict['img']):

                    print("微博图片下载成功...")

                dict['active'] = str(cc.find('div:nth-child(2) > a:nth-child(4)').text()) + '，' + str(cc.find('div:nth-child(2) > a:nth-child(5)').text()) + '，' + str(cc.find('.cc').text())

            else:

                dict['active'] = str(cc.find('div > a:nth-child(3)').text()) + '，' + str(cc.find('div > a:nth-child(4)').text()) + '，' + str(cc.find('.cc').text())

            try:
                collection.insert_one(dict)
                print("第" + str(k) + "页，第" + str(j) + "条微博存储成功...")
            except:
                print("第" + str(k) + "页，第" + str(j) + "条微博存储失败!!!")

            j = j + 1

            print('')

            time.sleep(0.5)

def main():
    check_ip()

    print('\n...\n')

    global id

    id = input('请输入微博用户id:')

    log_in()

    global collection

    collection=db[id]

    print('\n...\n')

    tot_page=get_basic_info(id)

    print('\n...\n')

    get_weibo(tot_page)

    print('爬取完毕...')

    browser.close()

if __name__ == "__main__":

    main()

#5953248868
#6516252862
#6463404407
