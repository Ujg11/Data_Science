import os # Read files, directories,...
import psycopg2 as ps # Connect with postgreSQL database
import csv # Read and write CSV

# Parameters
CSV_FOLDER = "./customer"
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

# Establish Connection with credentials: dbname, user, password, host, port
con = ps.connect (
    dbname = DB_NAME,
    user = USER,
    password = PASSWORD,
    host = HOST,
    port = PORT
)
# We create cur that allows us to execute SQL queries
cur = con.cursor()

# We iterate all over the files and take the name without '.csv'
for filename in os.listdir(CSV_FOLDER):
    if filename.endswith(".csv"):
        table_name = filename [:-4] # from the beginning but not include the last 4 char
        file_path = os.path.join(CSV_FOLDER, filename)

        cur.execute(f"DROP TABLE IF EXISTS {table_name};")
        cur.execute(f"CREATE TABLE {table_name} ({COLUMNS});")
        
        # We open the .csv for reading
        with open(file_path, 'r') as f:
            next(f) # skip the header line
            cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", f)
        print(f"Tabla {file_path} creada")

con.commit() # commit all changes
cur.close()
con.close()
print("All tables created with respective data")