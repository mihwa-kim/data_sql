# From crawl the web to complete the query required by boss

## work flow
1. Create a schema in the MySQL.
2. Crawl the web
3. Save the web data in the DB
4. Complete the query

### Create a schema in the MySQL
```sql
CREATE TABLE product(
	product_ID INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name LONGTEXT NOT NULL,
    category VARCHAR(10) NOT NULL,
    original_price  VARCHAR(10) NOT NULL,
    discount_price VARCHAR(10),
    store_quantity VARCHAR(10),
    PRIMARY KEY(product_ID)
);

CREATE TABLE location(
	location_ID INT UNSIGNED NOT NULL AUTO_INCREMENT,
    street VARCHAR(20) NOT NULL,
    city VARCHAR(20) NOT NULL,
    state VARCHAR(20) NOT NULL,
    PRIMARY KEY(location_ID)
);

CREATE TABLE time(
	time_ID INT UNSIGNED NOT NULL AUTO_INCREMENT,
    day INT NOT NULL,
    month INT NOT NULL,
    year INT NOT NULL,
    PRIMARY KEY(time_ID)
);

CREATE TABLE sales(
	product_ID INT UNSIGNED NOT NULL,
    time_ID INT UNSIGNED NOT NULL,
    location_ID INT UNSIGNED NOT NULL,
    sold_quantity INT,
    revenue INT,
    FOREIGN KEY (product_ID) REFERENCES product(product_ID),
    FOREIGN KEY (time_ID) REFERENCES time(time_ID),
    FOREIGN KEY (location_ID) REFERENCES location(location_ID)
);
```
### Crawl the web and Save the in the DB
```python
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
```

### Complete the query
```sql
SELECT 
	p.category AS Category,
    p.name AS ProductName, 
    SUM(s.sold_quantity) AS TotalSold 
FROM 
    sales s 
JOIN product p ON s.product_ID = p.product_ID
JOIN time t ON s.time_ID = t.time_ID 
JOIN location l ON s.location_ID = l.location_ID 
WHERE
    t.year BETWEEN (2023-5) AND 2023 
    AND t.month =12 
    AND t.day = 26 
    AND l.state = 'NSW'
GROUP BY 
	p.category, p.name
ORDER BY 
    TotalSold DESC 
LIMIT 9;

```
