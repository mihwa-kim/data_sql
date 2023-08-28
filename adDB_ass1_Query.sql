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
