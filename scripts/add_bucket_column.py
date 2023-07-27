import psycopg2

host = "localhost"
port = "6000"
database = "postgres"
user = "postgres"
password = "password"

conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password,
)

cursor = conn.cursor()

alter_like_table_query = 'ALTER TABLE "like" ADD COLUMN bucket VARCHAR'
cursor.execute(alter_like_table_query)

alter_session_table_query = "ALTER TABLE session ADD COLUMN bucket VARCHAR"
cursor.execute(alter_session_table_query)

conn.commit()

cursor.close()
conn.close()