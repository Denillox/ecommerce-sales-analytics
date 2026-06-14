CREATE TABLE dim_product(
    product_id INT PRIMARY KEY,
    name NVARCHAR(50) NOT NULL,
    category NVARCHAR(30),
    price FLOAT NOT NULL,
    brand NVARCHAR(30) NOT NULL,
    supplier NVARCHAR(30) NOT NULL
);

CREATE TABLE dim_orders(
    orders_id INT PRIMARY KEY,
    status NVARCHAR(20) NOT NULL CHECK (status IN('pending', 'cancelled', 'completed')),
    full_date DATE
);

CREATE TABLE dim_customer(
    customer_id INT PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    email NVARCHAR(100) NOT NULL,
    address NVARCHAR(100) NOT NULL,
    country NVARCHAR(100) NOT NULL,
    phone_number NVARCHAR(50),
    city NVARCHAR(100),
    signup_date DATE
);

CREATE TABLE dim_date(
    date_id INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT,
    month INT,
    day INT,
    quarter INT,
    weekday NVARCHAR(20),
    weekday_number INT
);

CREATE TABLE fact_ordereditem(
    order_item_id INT PRIMARY KEY,
    quantity INT NOT NULL CHECK(quantity > 0),
    unit_price FLOAT NOT NULL CHECK(unit_price > 0),
    total_amount FLOAT NOT NULL,
    customer_id INT NOT NULL, 
    product_id INT NOT NULL,  
    date_id INT NOT NULL,  
    orders_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES dim_customer (customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_product (product_id),
    FOREIGN KEY (date_id) REFERENCES dim_date (date_id),
    FOREIGN KEY (orders_id) REFERENCES dim_orders (orders_id)
);