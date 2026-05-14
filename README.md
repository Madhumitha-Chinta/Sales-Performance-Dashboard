# Sales-Performance-Dashboard
A comprehensive end-to-end data analysis project using the Superstore dataset. This project features a professional Sales Performance Dashboard built with Streamlit, designed to track key business metrics and provide actionable insights into product performance, regional sales, and customer segments.

## Features

- **Interactive Dashboard**: Built with Streamlit for a dynamic and responsive user experience.
- **Key Performance Indicators (KPIs)**: Calculates and displays Total Revenue, Total Profit, Profit Margin, and Total Orders.
- **Data Visualizations**: Utilizes Plotly Express for beautiful, interactive charts:
  - Sales Trend Over Time (Line Chart)
  - Revenue by Region (Bar Chart)
  - Top 10 Products by Revenue (Horizontal Bar Chart)
  - Revenue by Customer Segment (Donut Chart)
- **Advanced Filtering**: Allows users to filter data dynamically by Date Range, Region, and Category.
- **Data Processing Workflow**: Modularized code with clear separation of concerns (data loading, cleaning, filtering, and metric calculation).

## Project Structure

- `app.py`: The main Streamlit application containing the dashboard layout and visualization logic.
- `data_processing.py`: Contains functions for data loading, cleaning, filtering, and KPI calculations.
- `data_generator.py`: Script to generate or simulate the Superstore dataset if needed.
- `superstore_data.csv`: The primary dataset used for the dashboard.
- `requirements.txt`: List of Python dependencies required to run the project.
- `summary_report.md`: A summary report of the analysis findings.

## Installation and Setup

1. **Clone the repository** (if you haven't already) or navigate to the project directory:
   ```bash
   cd "Sales Performance Dashboard"
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Dashboard

To launch the Streamlit dashboard, run the following command in your terminal:

```bash
streamlit run app.py
```

The application will open automatically in your default web browser (typically at `http://localhost:8501`).

## Technologies Used

- **Python 3**
- **Streamlit**: For building the web application interface.
- **Pandas**: For data manipulation and analysis.
- **Plotly**: For interactive data visualizations.
- **NumPy**: For numerical computing.

## Data Source

This project uses the classic **Superstore dataset**, which contains sales data for a fictional retail company, including details on orders, customers, products, and geographical regions.
