import pyodbc
import pandas as pd

def get_connection():
    return pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=KWPCICDBA002;DATABASE=DataAnalysis;Trusted_Connection=yes;")

def load_callfloor():
    sql="select * from dws.vw_CallFloorOverview"
    return pd.read_sql(sql,get_connection())
