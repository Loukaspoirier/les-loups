import psycopg2
from function import *
conn = psycopg2.connect(
    dbname="les-loups",
    user="user",
    password="password",
    host="db",  # c'est le nom du service PostgreSQL dans le docker-compose
    port="5432"
)

try :
    cur = conn.cursor()
    
    cur.execute("SELECT version();")
    print("Connected successfully.")
except Exception as e:
    print("caca:", e)


print("PostgreSQL version:", cur.fetchone())
print('caca')
cur.close()
conn.close()
