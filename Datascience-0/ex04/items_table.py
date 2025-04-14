import os
import psycopg2 as ps
import csv

CSV_FOLDER = "./item"
DB_NAME = "piscineds"
USER = "ojimenez"
PASSWORD = "mysecretpassword"
HOST = "localhost"
PORT = "5432"

con = ps.connect (
    dbname = DB_NAME,
    user = USER,
    password = PASSWORD,
    host = HOST,
    port = PORT
)

COLUMNS = """
    product_id INTEGER,
    category_id BIGINT,
    category_code VARCHAR(255),
    brand TEXT
"""

cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS items;")
cur.execute(f"CREATE TABLE items ({COLUMNS});")

file_path = os.path.join(CSV_FOLDER, 'item.csv')
with open(file_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f) # We take a reader to iterate
    headers = next(reader) # We jump the first line

    

    # For each row, we take 
    for row in reader:

        # We have values with ''. We convert it to NULL (None in py)
        cleaned_row = [None if value == '' else value for value in row]
        
        cur.execute("""
            INSERT INTO items (product_id, category_id, category_code, brand)
            VALUES (%s, %s, %s, %s);
        """, cleaned_row)
print ("Table items created")

con.commit()
cur.close()
con.close()