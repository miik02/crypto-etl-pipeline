# Progarama estilo playground para trastear con streamlit y los datos guadados en la BBDD

import streamlit as st
import pandas as pd
import sqlite3

db_name = "historico_divisas.db"
table_name = "tasas_cambio"

@st.cache_data  
def obtener_datos():
    try:
        conn = sqlite3.connect(db_name)
        query = f"SELECT * from {table_name}"
        df = pd.read_sql_query(query, conn)
        df["date"] = pd.to_datetime(df["date"])
            
        print(f"Carga exitosa")
            
    except Exception as e:
        print(f"Error al cargar los datos de la base de datos: {e}")

    first_date = df["date"].min()
    last_date = df["date"].max()

    return df, first_date, last_date

df, first_date, last_date = obtener_datos()




st.set_page_config(layout="wide")
st.title("Comparacion Divisas")
st.markdown("Esto es una **prueba** a ver q tal")

col1, col2 = st.columns(2)


quotes = st.sidebar.multiselect(label="Currency", options=df["quote"].unique(), default=df["quote"].unique())
with col1:
    start_date = pd.to_datetime(st.date_input("From:", value=first_date, min_value=first_date, max_value=last_date))
with col2:
    end_date = pd.to_datetime(st.date_input("To:", value=last_date, min_value=first_date, max_value=last_date))
show_base = st.checkbox(label=f"Show Base (EUR)")


print(type(start_date))

df_filtered = df[df["date"].between(start_date, end_date)]
df_filtered = df_filtered[df_filtered["quote"].isin(quotes)]
df_filtered = df_filtered.pivot(index="date", columns="quote", values="rate")

if show_base:
    df_filtered["EUR"] = 1

st.dataframe(df_filtered)
st.line_chart(data=df_filtered, y_label=f"{quotes} rate")