import os
import psycopg2
import csv
import ast

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

# 기존 컬럼 similar_outfits 삭제
alter_similar_table_query = 'ALTER TABLE "similar" DROP COLUMN IF EXISTS similar_outfits'
cursor.execute(alter_similar_table_query)

# 새로운 컬럼들(kkma, gpt)을 similar 테이블에 추가
alter_similar_table_query = """
ALTER TABLE "similar" 
ADD COLUMN kkma INTEGER[],
ADD COLUMN gpt INTEGER[]
"""
cursor.execute(alter_similar_table_query)

# CSV 파일에서 데이터 읽어서 similar 테이블에 추가
csv_file = os.path.join(os.path.dirname(__file__), "../similar.csv")

with open(csv_file, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    for row in reader:
        outfit_id = int(row["outfit_id"])
        kkma_data = ast.literal_eval(row["reporter_kkma"]) if row["reporter_kkma"] != "[]" else None
        gpt_data = ast.literal_eval(row["tag_gpt"]) if row["tag_gpt"] != "[]" else None

        # outfit_id가 이미 존재하는지 확인
        check_query = 'SELECT COUNT(*) FROM "similar" WHERE outfit_id = %s'
        cursor.execute(check_query, (outfit_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            print(f"Outfit_id {outfit_id} not found in similar table. Skipping...")
            continue

        # similar 테이블의 해당 outfit_id 행에 데이터 추가
        update_query = """
        UPDATE "similar"
        SET kkma = %s,
            gpt = %s
        WHERE outfit_id = %s
        """
        cursor.execute(update_query, (kkma_data, gpt_data, outfit_id))

conn.commit()

cursor.close()
conn.close()
