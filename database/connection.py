import pyodbc
import pandas as pd

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=KWPCICDBA002;"
        "DATABASE=DataAnalysis;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

def load_callfloor():
    sql = "SELECT * FROM dws.vw_CallFloorOverview"
    return pd.read_sql(sql, get_connection())
