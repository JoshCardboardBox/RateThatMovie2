import csv
import psycopg2
import psycopg2.extras
from tqdm import tqdm

def clean(value):
    if value is None or value == "":
        return None
    return value

def clean_date(value):
    if value is None or value == "":
        return None
    return value  # PostgreSQL will parse YYYY-MM-DD

conn = psycopg2.connect(
    host="dbclass.rhodescs.org",
    database="practice",
    user="watmj-26",
    password="watmj-26"
)
cur = conn.cursor()

csv_path = "/Users/malikwaters/Downloads/ratethatmoviecsv/cast.csv"

print("Counting rows...")
with open(csv_path, encoding="utf8") as f:
    total_rows = sum(1 for _ in f) - 1

print(f"Total rows: {total_rows}")

with open(csv_path, encoding="utf8") as f:
    reader = csv.DictReader(f)

    batch = []
    batch_size = 1000

    for row in tqdm(reader, total=total_rows, desc="Importing movies", unit="rows"):

        batch.append((
            clean(row["id"]),
            clean(row["movie_id"]),
            clean(row["person_id"]),
            clean(row["name"]),
            clean(row["character"]),
            clean(row["cast_order"]),
            clean(row["movie_title"]),
            clean_date(row["movie_release_date"])
        ))

        if len(batch) >= batch_size:
            psycopg2.extras.execute_batch(cur, """
                INSERT INTO movies (
                    id, movie_id, person_id, name, character, cast_order,
                    movie_title, movie_release_date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, batch)
            conn.commit()
            batch = []

    if batch:
        psycopg2.extras.execute_batch(cur, """
            INSERT INTO movies (
                id, movie_id, person_id, name, character, cast_order,
                movie_title, movie_release_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, batch)
        conn.commit()

cur.close()
conn.close()

print("Import complete!")