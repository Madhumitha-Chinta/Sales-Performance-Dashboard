import streamlit as st
import pandas as pd
import plotly.express as px
from data_processing import load_data, clean_data, filter_data, calculate_kpis

# Page configuration
st.set_page_config(
    page_title="Sales Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .kpi-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .kpi-title {
        color: #6c757d;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .kpi-value {
        color: #007bff;
        font-size: 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Main Title
st.title("Sales Performance Dashboard")
st.markdown("Analyze top-performing products, regions, and customer segments based on Superstore data.")

# Load Data
@st.cache_data
def get_data():
    df = load_data()
    if df is not None:
        df = clean_data(df)
    return df

df = get_data()

if df is None:
    st.error("Could not load data. Please ensure 'superstore_data.csv' exists.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Dashboard Filters")

# Date Filter
min_date = df['Order Date'].min().date()
max_date = df['Order Date'].min().date() # bug, should be max
max_date = df['Order Date'].max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Region Filter
regions = st.sidebar.multiselect(
    "Select Region:",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Category Filter
categories = st.sidebar.multiselect(
    "Select Category:",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# Apply Filters
filtered_df = filter_data(df, start_date, end_date, regions, categories)

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selection.")
    st.stop()

# Calculate KPIs
kpis = calculate_kpis(filtered_df)

# Display KPIs in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Revenue</div>
            <div class="kpi-value">${kpis['Total Revenue']:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Profit</div>
            <div class="kpi-value">${kpis['Total Profit']:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Profit Margin</div>
            <div class="kpi-value">{kpis['Profit Margin']:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Orders</div>
            <div class="kpi-value">{kpis['Total Orders']:,}</div>
        </div>
    """, unsafe_allow_html=True)

# Visualizations
st.markdown("---")

col_charts1, col_charts2 = st.columns(2)

with col_charts1:
    # 1. Sales Over Time (Line Chart)
    st.subheader("Sales Trend Over Time")
    sales_over_time = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    sales_over_time['Order Date'] = sales_over_time['Order Date'].dt.to_timestamp()
    fig_sales_time = px.line(sales_over_time, x='Order Date', y='Sales', markers=True, 
                             labels={'Order Date': 'Month', 'Sales': 'Revenue ($)'},
                             color_discrete_sequence=['#007bff'])
    st.plotly_chart(fig_sales_time, width='stretch')

with col_charts2:
    # 2. Sales by Region (Bar Chart)
    st.subheader("Revenue by Region")
    sales_by_region = filtered_df.groupby('Region')['Sales'].sum().reset_index()
    fig_region = px.bar(sales_by_region, x='Region', y='Sales', text_auto='.2s',
                        color='Region', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_region, width='stretch')

col_charts3, col_charts4 = st.columns(2)

with col_charts3:
    # 3. Top 10 Products by Sales
    st.subheader("Top 10 Products by Revenue")
    top_products = filtered_df.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
    fig_products = px.bar(top_products, x='Sales', y='Product Name', orientation='h',
                          color='Sales', color_continuous_scale='Blues')
    fig_products.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_products, width='stretch')

with col_charts4:
    # 4. Sales by Customer Segment (Donut Chart)
    st.subheader("Revenue by Customer Segment")
    sales_by_segment = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
    fig_segment = px.pie(sales_by_segment, values='Sales', names='Segment', hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Set2)
    fig_segment.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_segment, width='stretch')

# Optional: Display raw data table
with st.expander("View Raw Data"):
    st.dataframe(filtered_df.head(100), width='stretch')
