#!/usr/bin/env python
# coding: utf-8

# <div class="alert alert-block" style="border: 1px solid #455A64;background-color:#ECEFF1;padding:5px;font-size:0.9em;">
#   본 자료와 관련 영상 컨텐츠는 저작권법 제25조 2항에 의해 보호를 받습니다. <br>본 컨텐츠 및 컨텐츠 일부 문구 등을 외부에 공개하거나, 요약해서 게시하지 말아주세요.<br>Copyright <a href="https://www.fun-coding.org">잔재미코딩</a> Dave Lee
# </div>

# ### 파이썬 크롤링
# > 데이터를 자동으로 저장하는 모습을 보여드리기 위해, 크롤링 기술을 가볍게 활용하기로 함 <br>
# > 파이썬 입문과 크롤링 부트캠프에서 익힌 크롤링 기술을 활용하기로 함

# In[35]:


import requests
from bs4 import BeautifulSoup

for page_num in range(10):
    if page_num == 0:
        res = requests.get('https://www.amazon.com.au/s?rh=n%3A4851799051&fs=true&ref=lp_4851799051_sar')
    else:
        res = requests.get('https://www.amazon.com.au/s?i=electronics&rh=n%3A4851799051&fs=true&page='
                           +str(page_num)+'&qid=1693022601&ref=sr_pg_'+str(page_num))

        
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.select('div.sg-col-inner')

    for item in data:
        name = item.select_one('h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-4')
        dis_price = item.select_one('span.a-offscreen')
        ori_price = item.select_one('div > span.a-price.a-text-price > span.a-offscreen')
        category = "Electronics"
        if name and dis_price and ori_price != None:
            dis_price_conv = dis_price.get_text()
            ori_price_conv = ori_price.get_text()
            ori_quantity = 1000
            print(name.get_text(),"||",category,"||", ori_price_conv,"||", dis_price_conv,"||",ori_quantity)
        
        


# ### Schema 구성
# > workbench 를 통해, schema 구성 <br>
# > 일회성 schema 는 파이썬으로 자동으로 하기보다는 workbench 를 활용하는 것이 일반적임
# 
# ```sql
# DROP DATABASE IF EXISTS ecommerce;
# CREATE DATABASE ecommerce;
# USE ecommerce;
# CREATE TABLE teddyproducts (
#     ID INT UNSIGNED NOT NULL AUTO_INCREMENT,
#     TITLE VARCHAR(200) NOT NULL,
#     CATEGORY VARCHAR(20) NOT NULL,
#     PRIMARY KEY(ID)
# );
# ```

# ### 크롤링 + mysql 저장

# In[7]:


import requests
from bs4 import BeautifulSoup
import pymysql

db = pymysql.connect(
    host='hostname',
    port=portnumber,
    user='username',
    passwd='password',
    db='dbname',
    charset='utf8')

cursor = db.cursor()

import requests
from bs4 import BeautifulSoup

for page_num in range(3):
    if page_num == 0:
        res = requests.get('https://www.amazon.com.au/s?rh=n%3A4851567051&fs=true&ref=lp_4851567051_sar')
    else:
        res = requests.get('https://www.amazon.com.au/s?i=beauty&rh=n%3A4851567051&fs=true&page='
                           +str(page_num)+'&qid=1693027215&ref=sr_pg_'+str(page_num))
        
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.select('div.sg-col-inner')

    for item in data:
        name = item.select_one('h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-4')
        dis_price = item.select_one('span.a-offscreen')
        ori_price = item.select_one('div > span.a-price.a-text-price > span.a-offscreen')
        category = "Beauty"
        if name and dis_price and ori_price != None:
            name_conv = name.get_text().replace("'","")
            dis_price_conv = dis_price.get_text()
            ori_price_conv = ori_price.get_text()
            ori_quantity = 100
            print(name_conv, category, ori_price_conv, dis_price_conv,ori_quantity)      
        
            SQL = """
                INSERT INTO product (name,category,original_price,discount_price,store_quantity)
                VALUES('"""+name_conv+"""',
                        '"""+category+"""',
                        '"""+ori_price_conv+"""',
                        '"""+dis_price_conv+"""',
                        '"""+str(ori_quantity)+"""');"""

            cursor.execute(SQL)
            print(SQL)
        
db.commit()
db.close()


# ### mysql 데이터 읽기

# In[11]:


import pymysql

db = pymysql.connect(
    host='hostname',
    port=portnumber,
    user='username',
    passwd='password',
    db='dbname',
    charset='utf8')

cursor = db.cursor()

SQL = """
    SELECT * FROM teddyproducts;
"""
cursor.execute(SQL)
rows = cursor.fetchall()
for row in rows:
    print(row[1])

db.close()


# <div class="alert alert-block" style="border: 2px solid #E65100;background-color:#FFF3E0;padding:10px">
# <font size="4em" style="font-weight:bold;color:#BF360C;">기본 데이터 분석</font><br>
# <font size="3em" style="color:#BF360C;">카테고리 종류를 알려주세요</font>
#     
# 
#     
# </div>

# "SELECT DISTINCT CATEGORY FROM teddyproducts;"

# <div class="alert alert-block" style="border: 2px solid #E65100;background-color:#FFF3E0;padding:10px">
# <font size="4em" style="font-weight:bold;color:#BF360C;">기본 데이터 분석</font><br>
# <font size="3em" style="color:#BF360C;">카테고리별 상품 갯수를 알려주세요</font>
#     
# 
#     
# </div>

# SELECT CATEGORY, COUNT(*) FROM teddyproducts
# GROUP BY CATEGORY;

# <div class="alert alert-block" style="border: 1px solid #455A64;background-color:#ECEFF1;padding:5px;font-size:0.9em;">
#   본 자료와 관련 영상 컨텐츠는 저작권법 제25조 2항에 의해 보호를 받습니다. <br>본 컨텐츠 및 컨텐츠 일부 문구 등을 외부에 공개하거나, 요약해서 게시하지 말아주세요.<br>Copyright <a href="https://www.fun-coding.org">잔재미코딩</a> Dave Lee
# </div>
