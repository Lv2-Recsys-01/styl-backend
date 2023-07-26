import csv
import os
import ast
import codecs

import psycopg2

host = "localhost"
port = "6000"
database = "postgres"
user = "postgres"
password = "password"


# csv_file = os.path.join(os.path.dirname(__file__), "../top3_22-23.csv")
csv_file = os.path.join(os.path.dirname(__file__), "../similar.csv") # kkma, gpt 두 종류 similar

conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password,
)
cursor = conn.cursor()

# with open(csv_file, "r") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         outfit_id = int(row["id"])
#         similar_outfits = [
#             int(outfit.strip()) for outfit in row["top3"].strip("[]").split(",")
#         ]

#         # outfit_id(FK)가 "outfit" 테이블에 존재하는지 확인
#         check_query = 'SELECT COUNT(*) FROM "outfit" WHERE outfit_id = %s'
#         cursor.execute(check_query, (outfit_id,))
#         count = cursor.fetchone()[0]

#         if count == 0:
#             print(f"Skipping outfit_id not found in 'outfit' table: {outfit_id}")
#             continue

#         similar_outfits_str = (
#             "{" + ",".join(str(outfit) for outfit in similar_outfits) + "}"
#         )

#         # outfit_id가 이미 존재하는지 확인
#         check_query = 'SELECT COUNT(*) FROM "similar" WHERE outfit_id = %s'
#         cursor.execute(check_query, (outfit_id,))
#         count = cursor.fetchone()[0]

#         if count > 0:
#             print(f"Skipping duplicate outfit_id: {outfit_id}")
#             continue

#         query = 'INSERT INTO "similar" (outfit_id, similar_outfits) VALUES (%s, %s)'
#         values = (outfit_id, similar_outfits_str)
#         cursor.execute(query, values)

with codecs.open(csv_file, "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    headers = next(reader)
    
    outfit_id_index = headers.index("outfit_id")
    kkma_index = headers.index("reporter_kkma")
    gpt_index = headers.index("tag_gpt")
    
    for row in reader:
        outfit_id = int(row[outfit_id_index])
        
        # outfit_id(FK)가 "outfit" 테이블에 존재하는지 확인
        check_query = 'SELECT COUNT(*) FROM "outfit" WHERE outfit_id = %s'
        cursor.execute(check_query, (outfit_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            print(f"Skipping outfit_id not found in 'outfit' table: {outfit_id}")
            continue
        
        # outfit_id가 이미 존재하는지 확인
        check_query = 'SELECT COUNT(*) FROM "similar" WHERE outfit_id = %s'
        cursor.execute(check_query, (outfit_id,))
        count = cursor.fetchone()[0]
    
        if count > 0:
            print(f"Skipping duplicate outfit_id: {outfit_id}")
            continue
        
        kkma = ast.literal_eval(row[kkma_index]) if row[kkma_index] != "[]" else None
        gpt = ast.literal_eval(row[gpt_index]) if row[gpt_index] != "[]" else None
        
        query = 'INSERT INTO "similar" (outfit_id, kkma, gpt) VALUES (%s, %s, %s)'
        values = (outfit_id, kkma, gpt)
        cursor.execute(query, values)

conn.commit()

cursor.close()
conn.close()
