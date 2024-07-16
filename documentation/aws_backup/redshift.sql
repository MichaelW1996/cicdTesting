DROP TABLE Orders;
DROP TABLE Products;
DROP TABLE Order_products;
 
CREATE TABLE Orders
       
                (order_id int IDENTITY PRIMARY KEY,
                date_time TIMESTAMP,
                branch_location VARCHAR(100),
                payment_total INT,
                payment_type VARCHAR(4));
 
       
CREATE TABLE Products
       
                (product_id int IDENTITY PRIMARY KEY,
                name VARCHAR(100),
                size VARCHAR(100),
                price INT);
               
       
 
CREATE TABLE Order_Products
       
                (order_products_id int IDENTITY NOT NULL PRIMARY KEY,      
                product_id INT NOT NULL,
                order_id INT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES Orders(order_id),
                FOREIGN KEY (product_id) REFERENCES Products(product_id));