import os
import psycopg2 as psy
import pandas as pd
import glob

DB_NAME = "piscineds"
USER = "ojimenez"
PASSWORD = "mysecretpassword"
HOST = "localhost"
PORT = "5432"

# Crearemos indices para mejorar el coste computacional
# Los crearemos con el product_id que es la fila que usaremos para unir las tablas
index_query = '''
    CREATE INDEX IF NOT EXISTS idx_customers ON customers(product_id);
    CREATE INDEX IF NOT EXISTS idx_items ON items(product_id);
'''

join_query = '''
    
'''

# pgweb
# adminer