# 获取京东评论时间数据
import time
from selenium import webdriver

def get_jd_num_(start_page, end_page):
    browser = webdriver.Chrome()
    browser.get('https://item.jd.com/180375.html#comment')
    # browser.get('https://item.jd.com/31292472280.html#comment')
    out = open('男士活力冰点沐浴露400ml.txt', 'w', encoding='utf-8')

    browser.maximize_window() #最大化窗口，防止有东西挡住了翻页按钮

    for i in range(start_page, end_page):
        print(i)  # 打印页数
        orderInfo = browser.find_elements_by_css_selector('.order-info')
        for item in orderInfo:
            line = item.text
            strs = line.split(' ')
            dateStr = strs[len(strs) - 2]
            out.write(dateStr + '\n')
        print('开始翻页')
        browser.find_element_by_class_name('ui-pager-next')
        browser.find_element_by_class_name('ui-pager-next').click()  # 点击翻页按钮
        time.sleep(2)
        browser.switch_to.window(browser.window_handles[0])  # 更新一下selenium的页面
    browser.close()

get_jd_num_(1, 10)
