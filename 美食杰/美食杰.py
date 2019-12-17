import csv
import json
import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
url=[]
fenlei=['https://so.meishi.cc/?&q=%E5%AE%B6%E5%B8%B8%E8%8F%9C&gy=130']
def each_page(html):
    soup = BeautifulSoup(html, 'lxml')
    a = soup.find_all(class_='search2015_cpitem')
    for li in a:
        url.append(li.find('a').get('href'))
        # print(url)
# 翻页,得到所有的url
def next_page():
    for i in fenlei:
        browser = webdriver.Chrome()
        browser.get(i)
        while True:
            if '下一页' in browser.page_source:
                html = browser.page_source
                each_page(html)
                a = browser.find_element_by_link_text('下一页')
                a.click()
                continue
            else:
                # return urls
                html = browser.page_source
                each_page(html)
                browser.close()
                break
    return url
# 根据url获取每页的信息
def get_message(urls):
    # tongjititle 菜谱名称
    # tongjind  菜谱难度
    # tongjiprsj 菜谱烹饪时间
    # 用料
    # 做法
    s=''
    l=''
    shicaizhu=''
    shicaifu=''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    response = requests.get(urls, headers=headers)
    # print(response.content)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    # 获取菜谱的名称
    if soup.find(id='tongji_title')==None:
        tongjititle=''
    else:
        tongjititle=soup.find(id='tongji_title').string
    # print(tongjititle.string)
    # 获取难度
    if soup.find(id='tongji_nd')==None:
        tongjind=''
    else:
        tongjind = soup.find(id='tongji_nd').string
    # print(tongjind.string)
#     获取烹饪口味
    if soup.find(id='tongji_kw')==None:
        tongjikw=''
    else:
        tongjikw = soup.find(id='tongji_kw').string
    # tongjikw = soup.find(class_='w270 bb0 br0')
    # 获取烹饪时间
    # print(tongjikw)
    if soup.find('li',class_='w270 bb0 br0')==None:
        tongjiprsj=None
    else:
        tongjiprsj=soup.find('li',class_='w270 bb0 br0').contents[1].text
    # print(tongjiprsj)
    # 获取烹饪的食材
    # 获取辅料
    for fuliao in soup.find_all(class_='yl fuliao clearfix'):
        shicaifu=fuliao.find(class_='clearfix')
    for zhuliao in soup.find_all(class_='yl zl clearfix'):
        shicaizhu=zhuliao.find(class_='clearfix')
        # print(shicaizhu)
#     获取烹饪步骤
    for ls in soup.find_all(class_='content clearfix'):
        # print(ls.contents[1].string,ls.contents[3].text)
        l=l+ls.contents[1].string+ls.contents[3].text
    l=l.replace('\n','')
    # print(l)
    if shicaifu=='':
        if shicaizhu!='':
            s=shicaizhu.text.replace('\n','')
    elif shicaizhu=='':
        s='没有食材'
    else:
        s=shicaizhu.text.replace('\n','')+shicaifu.text.replace('\n','')
    # print(tongjititle.string, tongjind.string, tongjikw.string, tongjiprsj, s, l)
    return tongjititle,tongjind,tongjikw,tongjiprsj, s, l
# get_message('https://www.meishij.net/zuofa/fuqixiaocanbaozhijiefa.html')
# print(caipu,nd,kouwei,sj,s1,l1)
if __name__=='__main__':
    ur=next_page()
    csvFile = open("meishijie_shaokao.csv", "w", newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    writer.writerow(['菜谱名称', '难度','口味','烹饪时间','食材','步骤'])
    for urls in ur:
        caipu, nd, kouwei, sj, s1, l1 = get_message(urls)
        writer.writerow([caipu, nd, kouwei, sj, s1, l1])
