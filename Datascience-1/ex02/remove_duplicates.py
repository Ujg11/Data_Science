import os
import psycopg2 as psy
import pandas as pd
import glob

DB_NAME = "piscineds"
USER = "ojimenez"
PASSWORD = "mysecretpassword"
HOST = "localhost"
PORT = "5432"

# Con la funcion LAG creamos una columna con los datos de la fila superior llamada prev_event_time.
# Con el primer SELECT creamos la columna extra ordenando por event_time.
# El en segundo SELECT nos quedamos solo con las lineas que nos interesan. El EXTRACT(EPOCH FROM...) extrae el numero tootal de segundos
# En el tercero solo borramos las filas que no queramos
query = """
    WITH DuplicateRows AS (
        SELECT event_time, event_type, product_id, LAG(event_time) OVER (
            PARTITION BY event_type, product_id
            ORDER BY event_time
        ) AS prev_event_time FROM customers
    ),
    FilteredRows AS (
        SELECT event_time, event_type, product_id FROM DuplicateRows
        WHERE prev_event_time IS NULL OR event_time - prev_event_time = '0 seconds' OR event_time - prev_event_time = '1 second'
    )
    DELETE FROM customers 
    WHERE (event_time, event_type, product_id) NOT IN (
            SELECT event_time, event_type, product_id FROM FilteredRows
    );
"""

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

def remove_duplicates():

    con, cur = start_connection_pgadmin()
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(f"Error removing: {e}")
        con.rollback()
    finally:
        cur.close()
        con.close()
    print("Process completed successfully.")

if __name__ == "__main__":
    remove_duplicates()

# before: 20687840 rows
# after: 
