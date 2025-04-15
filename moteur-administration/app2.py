import psycopg2
import os

def insert_data():
    conn = psycopg2.connect(
        host='db',
        database='les-loups',
        user='user',
        password='password'
    )

    cur = conn.cursor()
    
    # Insertion d'une ligne dans la table users
    cur.execute("INSERT INTO players (pseudo) VALUES (%s)", ("Sissi",))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Data inserted successfully")

if __name__ == '__main__':
    insert_data()
