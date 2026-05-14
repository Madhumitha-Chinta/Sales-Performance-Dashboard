import pandas as pd
import numpy as np
import datetime
import random
import os

def generate_mock_superstore_data(num_rows=5000, filename='superstore_data.csv'):
    np.random.seed(42)
    random.seed(42)
    
    # Define categories and sub-categories
    categories = {
        'Furniture': ['Bookcases', 'Chairs', 'Labels', 'Tables', 'Furnishings'],
        'Office Supplies': ['Appliances', 'Art', 'Binders', 'Envelopes', 'Fasteners', 'Paper', 'Storage', 'Supplies'],
        'Technology': ['Accessories', 'Copiers', 'Machines', 'Phones']
    }
    
    regions = ['East', 'West', 'Central', 'South']
    segments = ['Consumer', 'Corporate', 'Home Office']
    ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
    
    data = []
    
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    
    for i in range(num_rows):
        # Generate random dates
        random_number_of_days = random.randrange(days_between_dates)
        order_date = start_date + datetime.timedelta(days=random_number_of_days)
        ship_delay = random.choice([0, 1, 2, 3, 4, 5, 6])
        ship_date = order_date + datetime.timedelta(days=ship_delay)
        
        # Determine product
        cat = random.choice(list(categories.keys()))
        sub_cat = random.choice(categories[cat])
        
        # Generate metrics
        quantity = random.randint(1, 14)
        
        # Base price and profit margins based on category
        if cat == 'Furniture':
            base_price = round(random.uniform(50, 1500), 2)
            margin = random.uniform(-0.1, 0.3)
        elif cat == 'Technology':
            base_price = round(random.uniform(100, 3000), 2)
            margin = random.uniform(0.1, 0.5)
        else: # Office Supplies
            base_price = round(random.uniform(5, 200), 2)
            margin = random.uniform(0.0, 0.4)
            
        sales = round(base_price * quantity, 2)
        profit = round(sales * margin, 2)
        discount = round(random.choice([0.0, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]), 2)
        
        # Apply discount to sales and profit
        sales = round(sales * (1 - discount), 2)
        # Discount hits profit harder
        profit = round(profit - (sales * discount), 2)
        
        row = {
            'Order ID': f'CA-20{order_date.strftime("%y")}-{random.randint(100000, 999999)}',
            'Order Date': order_date.strftime('%Y-%m-%d'),
            'Ship Date': ship_date.strftime('%Y-%m-%d'),
            'Ship Mode': random.choice(ship_modes),
            'Customer ID': f'CUST-{random.randint(1000, 9999)}',
            'Segment': random.choice(segments),
            'Country': 'United States',
            'City': random.choice(['New York City', 'Los Angeles', 'Seattle', 'San Francisco', 'Philadelphia', 'Houston', 'Chicago', 'San Diego', 'Dallas', 'Columbus']),
            'State': random.choice(['New York', 'California', 'Washington', 'Texas', 'Pennsylvania', 'Illinois', 'Ohio']),
            'Region': random.choice(regions),
            'Product ID': f'{cat[:3].upper()}-{sub_cat[:2].upper()}-{random.randint(1000, 9999)}',
            'Category': cat,
            'Sub-Category': sub_cat,
            'Product Name': f'{sub_cat} Product {random.randint(1, 100)}',
            'Sales': sales,
            'Quantity': quantity,
            'Discount': discount,
            'Profit': profit
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    
    # Add a bit of realistic missing data
    # Let's say 1% of Cities are missing
    mask = np.random.rand(len(df)) < 0.01
    df.loc[mask, 'City'] = np.nan
    
    filepath = os.path.join(os.path.dirname(__file__), filename)
    df.to_csv(filepath, index=False)
    print(f"Successfully generated mock dataset with {num_rows} rows at {filepath}")

if __name__ == '__main__':
    generate_mock_superstore_data()
