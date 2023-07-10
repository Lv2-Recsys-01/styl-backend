import psycopg2
import csv
import ast

host = 'localhost'
port = '6000'
database = 'postgres'
user = 'postgres'
password = 'password'

conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)

csv_file = '../meta_22-23.csv'

with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    next(reader)

    cursor = conn.cursor()
    for row in reader:

        age = int(row[2]) if row[2] != '연령미상' else None
        occupation = row[9] if row[9] != '정보없음' else None
        tags = ast.literal_eval(row[6])  
        brands = ast.literal_eval(row[7]) if row[7] != '[]' else None

        query = 'INSERT INTO outfit (gender, age, img_url, origin_url, reporter, tags, brands, region, occupation, style, "date") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = (
            row[1],  # gender: CHAR(1)
            age,  # age: INTEGER
            row[3],  # img_url: VARCHAR
            row[4],  # origin_url: VARCHAR
            row[5],  # reporter: VARCHAR
            tags,  # tags: VARCHAR[]
            brands,  # brands: VARCHAR[]
            row[8],  # region: VARCHAR
            occupation,  # occupation: VARCHAR
            row[10],  # style: VARCHAR
            row[11]  # date: TIMESTAMP WITHOUT TIME ZONE
        )
        cursor.execute(query, values)

    conn.commit()

cursor.close()
