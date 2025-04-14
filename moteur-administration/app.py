import psycopg2

conn = psycopg2.connect(
    dbname="mydb",
    user="user",
    password="password",
    host="db",  # c'est le nom du service PostgreSQL dans le docker-compose
    port="5432"
)

cur = conn.cursor()
cur.execute("SELECT version();")
print("PostgreSQL version:", cur.fetchone())
cur.close()
conn.close()
