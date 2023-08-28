CREATE DATABASE JDHub;
USE JDHub;

CREATE TABLE product(
	product_ID INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
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

ALTER TABLE  location MODIFY COLUMN city VARCHAR(20) ;
ALTER TABLE product MODIFY COLUMN discount_price VARCHAR(10) ;
ALTER TABLE product MODIFY COLUMN store_quantity VARCHAR(10) ;
ALTER TABLE product MODIFY COLUMN name longtext ;


DROP TABLE sales;
DROP TABLE location;
