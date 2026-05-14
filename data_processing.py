import pandas as pd
import numpy as np

def load_data(filepath='superstore_data.csv'):
    """Loads the dataset from the given filepath."""
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: Could not find file at {filepath}")
        return None

def clean_data(df):
    """Cleans the dataset by handling missing values and data types."""
    # Convert date columns to datetime objects
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    
    # Handle missing values: Fill missing Cities with 'Unknown'
    df['City'] = df['City'].fillna('Unknown')
    
    # Optional: Handle any negative sales or profit issues if they shouldn't exist
    # For this mock dataset, negative profit is fine (discounts), but sales should be > 0.
    df = df[df['Sales'] > 0]
    
    return df

def filter_data(df, start_date, end_date, regions, categories):
    """Filters the dataset based on user selections."""
    filtered_df = df.copy()
    
    # Filter by Date
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['Order Date'].dt.date >= start_date) & 
                                  (filtered_df['Order Date'].dt.date <= end_date)]
        
    # Filter by Region
    if regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(regions)]
        
    # Filter by Category
    if categories:
        filtered_df = filtered_df[filtered_df['Category'].isin(categories)]
        
    return filtered_df

def calculate_kpis(df):
    """Calculates key performance indicators."""
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order ID'].nunique()
    
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    
    return {
        'Total Revenue': total_sales,
        'Total Profit': total_profit,
        'Profit Margin': profit_margin,
        'Total Orders': total_orders,
        'Avg Order Value': avg_order_value
    }
