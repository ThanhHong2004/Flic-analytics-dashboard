import sqlalchemy as sa
import pandas as pd
import streamlit as st

server_name = '.' 
database_name = 'FLIC_3'
user_name = 'YOUR_SERVER_NAME'
password = '123456'

connection_url = (f"mssql+pyodbc://{user_name}:{password}@{server_name}/{database_name}"
                  "?driver=ODBC+Driver+17+for+SQL+Server&charset=utf8")

engine = sa.create_engine(connection_url, fast_executemany=True)
@sa.event.listens_for(engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    if executemany:
        cursor.fast_executemany = True
file_path = r'C:\Users\hangv\Documents\DE AN FLIC_3\data\DuLieuDemo_3.xlsx'
def get_engine():
    return engine
def get_connection():
    return engine.connect()
@st.cache_data 
def load_data(query):
    try:
        with engine.connect() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Lỗi truy vấn SQL: {e}")
        return pd.DataFrame()

def get_unique_list(query, column_name):
    df = load_data(query)
    if not df.empty:
        return sorted(df[column_name].dropna().unique().tolist())
    return []