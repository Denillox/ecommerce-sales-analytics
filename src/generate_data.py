from faker import Faker
import pyodbc
from dotenv import load_dotenv
import os
import pandas as pd
import random

fake = Faker()

# Creating the dim_customers table and filling it with data

customers = []
for i in range(1000):
    customers.append({
        'customer_id': i + 1,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'country': fake.country(),
        'address': fake.street_address(),
        'phone_number': fake.phone_number(),
        'signup_date': fake.date_this_decade(),
        'city': fake.city()
    })


customers_df = pd.DataFrame(customers)
customers_df.to_csv('data/raw/customers.csv', index=False)
print('Customers saved as CSV')


# Creating the dim_products table and filling it with data

categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Toys', 'Camping']
brands = ['Apple', 'Microsoft', 'Amazon', 'Google', 'Samsung', 'Toyota', 'Coca-Cola', 'Intel', 'IKEA']
suppliers = ['AliExpress', 'Spocket', 'Temu', 'BigGuy', 'Moreta', 'SaleHoo']

products = []
for i in range(100):
    category = random.choice(categories)
    products.append({
        'product_id': i + 1,
        'name': f'{category} Product {i+1}',
        'category': category,
        'price': round(random.uniform(5.0, 500.0), 2),
        'brand': random.choice(brands),
        'supplier': random.choice(suppliers)
    })


products_df = pd.DataFrame(products)
products_df.to_csv('data/raw/products.csv', index=False)
print('Products saved as CSV')


# Creating of the dim_orders table and filling it with data


orders = []
for i in range(5000):
    orders.append({
        'orders_id': i + 1,
        'customer_id': random.randint(1, 1000),
        'status': random.choices(['completed', 'pending', 'cancelled'], weights=[70, 20, 10])[0],
        'full_date': fake.date_between(start_date='-2y', end_date='today')  
    })

orders_df = pd.DataFrame(orders)
orders_df.to_csv('data/raw/orders.csv', index=False)
print('Orders saved as CSV')


# Build dim_date from order dates
all_dates = pd.to_datetime(orders_df['full_date']).drop_duplicates().reset_index(drop=True)

dim_date = pd.DataFrame()
dim_date['date_id'] = all_dates.dt.strftime('%Y%m%d').astype(int)
dim_date['full_date'] = all_dates.dt.date
dim_date['year'] = all_dates.dt.year
dim_date['month'] = all_dates.dt.month
dim_date['day'] = all_dates.dt.day
dim_date['quarter'] = all_dates.dt.quarter
dim_date['weekday'] = all_dates.dt.day_name()
dim_date['weekday_number'] = all_dates.dt.dayofweek + 1

dim_date.to_csv('data/raw/dim_date.csv', index=False)
print('Dim date saved as CSV')
print(dim_date.head())


### Creation of the fact table


# Ensure every order has at least one item
order_ids = list(range(1, 5001))
random.shuffle(order_ids)
remaining = [random.randint(1, 5000) for _ in range(5000)]
all_order_ids = order_ids + remaining

fact_ordereditem = []
for i in range(10000):
    product_id = random.randint(1, 100)
    quantity = random.randint(1, 3)
    unit_price = products_df.loc[products_df['product_id'] == product_id, 'price'].values[0]
    order_id = all_order_ids[i]
    customer_id = orders_df.loc[orders_df['orders_id'] == order_id, 'customer_id'].values[0]
    order_date = orders_df.loc[orders_df['orders_id'] == order_id, 'full_date'].values[0]
    date_id = int(pd.to_datetime(order_date).strftime('%Y%m%d'))
    fact_ordereditem.append({
        'order_item_id': i + 1,
        'orders_id': order_id,
        'customer_id': customer_id,
        'product_id': product_id,
        'date_id': date_id
        'quantity': quantity,
        'unit_price': unit_price,
        'total_amount': round(quantity * unit_price, 2)
    })

fact_df = pd.DataFrame(fact_ordereditem)
fact_df.to_csv('data/raw/fact_ordereditem.csv', index=False)
print('Fact table saved as CSV')

print(fact_df.head())