# Streamlit dashboard to visualize historical exchange rates

import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(layout="wide")

db_name = "historico_divisas.db"
table_name = "tasas_cambio"

@st.cache_data  
def fetch_historical_data():
    """Extracts data from the SQLite database and returns the DataFrame and date ranges."""
    
    try:
        conn = sqlite3.connect(db_name)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        df["date"] = pd.to_datetime(df["date"])
        conn.close() # Good practice to always close the connection
        
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return pd.DataFrame(), None, None

    first_date = df["date"].min()
    last_date = df["date"].max()

    return df, first_date, last_date

# Load data into cache
df, first_date, last_date = fetch_historical_data()

# Dashboard Header
st.title("Currency Exchange Comparison")
st.markdown("Interactive dashboard to analyze historical exchange rates against the Euro (EUR).")

# Layout columns for date inputs
col1, col2 = st.columns(2)

# Sidebar filters
quotes = st.sidebar.multiselect(label="Select Currencies", options=df["quote"].unique(), default=df["quote"].unique())

with col1:
    start_date = pd.to_datetime(st.date_input("From:", value=first_date, min_value=first_date, max_value=last_date))
with col2:
    end_date = pd.to_datetime(st.date_input("To:", value=last_date, min_value=first_date, max_value=last_date))

show_base = st.checkbox(label="Show Base (EUR)")

# Data filtering and transformation
df_filtered = df[df["date"].between(start_date, end_date)]
df_filtered = df_filtered[df_filtered["quote"].isin(quotes)]
df_filtered = df_filtered.pivot(index="date", columns="quote", values="rate")

# Add base currency reference line if checked
if show_base:
    df_filtered["EUR"] = 1.0

# Visualizations
st.dataframe(df_filtered)
st.line_chart(data=df_filtered, y_label="Exchange Rate")