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

# 삽입할 데이터
user_name = "guest"
user_pwd = "guest_pwd"

# INSERT 쿼리 실행
query = 'INSERT INTO "user" (user_name, user_pwd) VALUES (%s, %s)'
values = (user_name, user_pwd)
cursor.execute(query, values)

# 변경 사항 저장
conn.commit()

# 연결 종료
cursor.close()
conn.close()
