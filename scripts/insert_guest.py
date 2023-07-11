import psycopg2

host = "localhost"
port = "6000"
database = "postgres"
user = "postgres"
password = "password"

conn = psycopg2.connect(
    host=host, port=port, database=database, user=user, password=password
)
cursor = conn.cursor()

user_name = "guest"
user_pwd = "guest_pwd"

# user_name이 이미 존재하는지 확인
check_query = 'SELECT COUNT(*) FROM "user" WHERE user_name = %s'
cursor.execute(check_query, (user_name,))
count = cursor.fetchone()[0]

if count > 0:
    print(f"User with user_name '{user_name}' already exists. Exiting...")
    cursor.close()
    conn.close()
    exit()

query = 'INSERT INTO "user" (user_name, user_pwd) VALUES (%s, %s)'
values = (user_name, user_pwd)
cursor.execute(query, values)

conn.commit()

cursor.close()
conn.close()
