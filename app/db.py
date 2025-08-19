import snowflake.connector
import pandas as pd
import streamlit as st

# connection setup (reads from Streamlit secrets)
def get_connection():
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database="BOOTCAMP_RALLY",
        schema="PUBLIC"  # schema will be changed in queries
    )
    return conn

# --- helper to sanitize numpy/pandas types ---
def _sanitize_params(params):
    clean = {}
    for k, v in (params or {}).items():
        if hasattr(v, "item"):  # numpy scalar (np.int64, np.float64, etc.)
            clean[k] = v.item()
        elif isinstance(v, (list, tuple)):
            clean[k] = [x.item() if hasattr(x, "item") else x for x in v]
        else:
            clean[k] = v
    return clean

# run SELECT query, return DataFrame
def run_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, _sanitize_params(params))
    df = pd.DataFrame(cur.fetchall(), columns=[col[0] for col in cur.description])
    cur.close()
    conn.close()
    return df

# run INSERT/UPDATE/DELETE
def run_command(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, _sanitize_params(params))
    conn.commit()
    cur.close()
    conn.close()
