# import psycopg2
# from fastapi import FastAPI

# app = FastAPI()


# def get_conn():
#     return psycopg2.connect(
#     dbname="les-loups",
#     user="user",
#     password="password",
#     host="db",
#     port="5432"
# )


# @app.get("/insert")
# def insert():
#     conn = get_conn()
#     cur = conn.cursor()
#     cur.execute("INSERT INTO public.players (pseudo) VALUES (%s);", ("Rebecca",))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return {"message": "Insertion OK"}