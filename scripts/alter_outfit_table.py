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

# 새로운 컬럼들(tags_filtered, cat_base, cat_gpt)을 outfit 테이블에 추가
alter_outfit_table_query = """
ALTER TABLE outfit 
ADD COLUMN tags_filtered VARCHAR[],
ADD COLUMN cat_base VARCHAR,
ADD COLUMN cat_gpt VARCHAR
"""
cursor.execute(alter_outfit_table_query)

# CSV 파일에서 데이터 읽어서 outfit 테이블에 추가
csv_file = "your_csv_file_path.csv"

with open(csv_file, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    for row in reader:
        outfit_id = int(row["outfit_id"])
        tags_filtered = ast.literal_eval(row["tags_filtered"])
        cat_base = row["cat_base"]
        cat_gpt = row["cat_gpt"]
        tags = ast.literal_eval(row["tags"])

        # outfit_id가 이미 존재하는지 확인
        check_query = "SELECT COUNT(*) FROM outfit WHERE outfit_id = %s"
        cursor.execute(check_query, (outfit_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            print(f"Outfit_id {outfit_id} not found in outfit table. Skipping...")
            continue

        # outfit 테이블의 해당 outfit_id 행에 데이터 추가 및 기존 tags 컬럼 업데이트
        update_query = """
        UPDATE outfit
        SET tags_filtered = %s,
            cat_base = %s,
            cat_gpt = %s,
            tags = %s
        WHERE outfit_id = %s
        """
        cursor.execute(update_query, (tags_filtered, cat_base, cat_gpt, tags, outfit_id))

conn.commit()

cursor.close()
conn.close()