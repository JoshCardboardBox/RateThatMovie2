from di_toolbox import *

#get cast and total number of rows
csv_path = di_getpath("genres.csv")
total_rows = di_count_rows(csv_path)


with open(csv_path, encoding="utf8") as f:
    reader = csv.DictReader(f)

    batch = []
    batch_size = 1000

    for row in tqdm(reader, total=total_rows, desc="Importing genres.csv", unit="rows"):

        batch.append((
            clean(row["id"]),
            clean(row["name"]),
            clean(row["movie_count"])
        ))

        if len(batch) >= batch_size:
            psycopg2.extras.execute_batch(cur, """
                INSERT INTO temp_genres (id, name, movie_count)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, batch)
            conn.commit()
            batch = []

    if batch:
        psycopg2.extras.execute_batch(cur, """
            INSERT INTO temp_genres (id, name, movie_count)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, batch)
        conn.commit()


di_closing()