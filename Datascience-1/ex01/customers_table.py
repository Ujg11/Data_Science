import os
import psycopg2 as psy
import pandas as pd
import glob

CSV_FOLDER = "../../customer"
PATTERN = "data_202*_*.csv"
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

# We create a check_columns func to chek files by pattern
def check_columns(file_pattern):
    csv_files = glob.glob(file_pattern)

    # We need to load the first file to have a column reference
    reference = pd.read_csv(csv_files[0])
    column_ref = set(reference.columns)

    # We go through all the files
    for file in csv_files[1:]:
        df = pd.read_csv(file)
        current_col = set(df.columns)
        if current_col != column_ref:
            print(f"Columns mismatch in file: {file}")
            print(f"Expected: {column_ref}")
            print(f"Got: {current_col}")
            return False
    print(f"All files starting with {file_pattern} have the same columns")
    return True

def find_csv_files(folder_path, pattern):
    file_pattern = os.path.join(folder_path, pattern)
    csv_files = glob.glob(file_pattern)
    if not csv_files:
        raise ValueError(f"No CSV files found matching {file_pattern}")
    if check_columns(file_pattern):
        return csv_files
    return None

def combine_csv_files(csv_files, output_file):
    with open(output_file, 'w') as outfile:
        # Escribimos el header
        with open(csv_files[0], 'r') as infile:
            header = infile.readline()
            outfile.write(header)

        for file in csv_files:
            with open(file, 'r') as infile:
                next(infile)
                for line in infile:
                    outfile.write(line)
    return output_file

def start_connection_pgadmin():
    connection = psy.connect (
        dbname = DB_NAME,
        user = USER,
        password = PASSWORD,
        host = HOST,
        port = PORT
    )
    cur = connection.cursor()
    return connection, cur

if __name__ == "__main__":
    table_name = "customers"
    combined_csv_file = "customers.csv"
    
    csv_files = find_csv_files(CSV_FOLDER, PATTERN)
    out_file = combine_csv_files(csv_files, combined_csv_file)
    
    con, cur = start_connection_pgadmin()

    try:
        cur.execute(f"DROP TABLE IF EXISTS {table_name};")
        cur.execute(f"CREATE TABLE {table_name} ({COLUMNS});")
        print(f"Table {table_name} created")

        chunk_size = 5000
        with open(combined_csv_file, 'r') as f:
            next(f)
            while True:
                # Es la funcion readline la que itera y mueve el puntero
                lines = [f.readline() for _ in range(chunk_size)]
                if not any(lines):
                    break
                cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV", f)
        con.commit()
        print(f"Copied data from {combined_csv_file} into table {table_name}.")
        
    except Exception as e:
        print(f"Error: {e}")
        # Borramos los cambios hechos
        con.rollback() 
    finally:
        cur.close()
        con.close()

    print("Process completed successfully.")
