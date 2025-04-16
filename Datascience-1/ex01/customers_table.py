import os
import psycopg2 as psy
import pandas as pd

CSV_FOLDER = "../customer"
DB_NAME = "piscineds"
USER = "ojimenez"
PASSWORD = "mysecretpassword"
HOST = "localhost"
PORT = "5432"

COLUMNS = """
    event_time TIMESTAMP,
    event_type VARCHAR(100),
    product_id INTEGER,
    price NUMERIC,
    user_id BIGINT,
    user_session UUID
"""

connection = psy.connect (
    dbname = DB_NAME,
    user = USER,
    password = PASSWORD,
    host = HOST,
    port = PORT
)

cursor = connection.cursor()




