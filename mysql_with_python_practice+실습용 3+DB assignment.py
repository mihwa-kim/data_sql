
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
