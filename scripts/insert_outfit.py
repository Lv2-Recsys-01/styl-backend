import ast
import codecs
import csv
import os

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


# csv_file = os.path.join(os.path.dirname(__file__), "../season_new_meta_22-23.csv")
# csv_file = os.path.join(os.path.dirname(__file__), "../mab_meta.csv")
csv_file = os.path.join(os.path.dirname(__file__), "../filtered_meta.csv")

cursor = conn.cursor()

with codecs.open(csv_file, "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    headers = next(reader)

    # 열 인덱스 동적으로 결정
    outfit_id_index = headers.index("outfit_id")
    gender_index = headers.index("gender")
    age_index = headers.index("age")
    img_url_index = headers.index("img_url")
    origin_url_index = headers.index("origin_url")
    reporter_index = headers.index("reporter")
    tags_index = headers.index("tags")
    # filtered
    tags_filtered_index = headers.index("tags_filtered")
    brands_index = headers.index("brands")
    region_index = headers.index("region")
    occupation_index = headers.index("occupation")
    style_index = headers.index("style")
    date_index = headers.index("date")
    season_index = headers.index("season")
    # for category
    cat_base_index = headers.index("cat_base")
    cat_gpt_index = headers.index("cat_gpt")

    for row in reader:
        outfit_id = int(row[outfit_id_index])

        # outfit_id가 이미 존재하는지 확인
        check_query = "SELECT COUNT(*) FROM outfit WHERE outfit_id = %s"
        cursor.execute(check_query, (outfit_id,))
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"Skipping duplicate outfit_id: {outfit_id}")
            continue

        age = int(row[age_index]) if row[age_index] != "연령미상" else None
        occupation = row[occupation_index] if row[occupation_index] != "정보없음" else None
        tags = ast.literal_eval(row[tags_index])
        tags_filtered = ast.literal_eval(row[tags_filtered_index])
        brands = (
            ast.literal_eval(row[brands_index]) if row[brands_index] != "[]" else None
        )

        # 16개
        query = f'INSERT INTO outfit (outfit_id, img_url, origin_url, \
        gender, age, reporter, tags, tags_filtered, brands, region, occupation, style, date, season, \
        cat_base, cat_gpt) \
                VALUES ({"%s," * 15} %s)'

        values = (
            outfit_id,
            row[img_url_index],
            row[origin_url_index],
            row[gender_index],
            age,
            row[reporter_index],
            tags,
            tags_filtered,
            brands,
            row[region_index],
            occupation,
            row[style_index],
            row[date_index],
            row[season_index],
            row[cat_base_index],
            row[cat_gpt_index],
        )

        cursor.execute(query, values)

    conn.commit()

cursor.close()
conn.close()
