import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import pymysql

# Connect to MySQL database
connection = pymysql.connect(
    host="localhost",       
    user="root",       
    password="root",   
    database="scraper_db"      
)

# Read data from MySQL
query = "SELECT * FROM  view_apple_iphone_15_128gb  "  # Modify based on your table
df = pd.read_sql(query, connection)

# Page layout settings
st.set_page_config(layout="wide")

# Styling the title and last updated section
html_title = """
    <style>
    .title-test {
        font-weight: bold;
        padding: 5px;
        border-radius: 6px;
        margin-top: -50px;  /* Move heading upwards */
    }
    .update-text {
        font-size: 16px;
        text-align: center;
        margin-top: -30px;  /* Move last updated text upwards */
    }
    </style>
    <center><h1 class="title-test">IPHONE 15 128GB PRICE COMPARISON</h1></center>
"""
st.markdown(html_title, unsafe_allow_html=True)

# Display last updated date in the center
box_date = datetime.datetime.now().strftime("%d %B %Y")
st.markdown(f"<p class='update-text'><b>Last updated on:</b> {box_date}</p>", unsafe_allow_html=True)

# Define custom colors for Amazon and Flipkart
custom_colors = {
    "Amazon": "#064adc",  # Blue (Amazon's brand color)
    "Flipkart": "#fff033"  # Yellow (Flipkart's brand color)
}

# Center-align the chart and title using Streamlit's columns
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

with col2:
    st.markdown("<h3 style='text-align: center;'>Price Comparison: Amazon vs Flipkart</h3>", unsafe_allow_html=True)
    fig = px.bar(df, 
                 x="date",
                 y="current_price",
                 color="source",
                 barmode="group",
                 labels={"current_price": "Current Price (₹)", "date": "Date"},
                 template="plotly_dark",
                 height=500,
                 color_discrete_map=custom_colors)
    
    st.plotly_chart(fig, use_container_width=True)

# Display recent price in the expander

expander = st.expander("Recent Supplier Wise Price")

# Get the most recent date in the dataset
latest_date = df["date"].max()
recent_prices = df[df["date"] == latest_date][["source", "current_price"]]

# Show the latest prices
expander.write(recent_prices.set_index("source"))
