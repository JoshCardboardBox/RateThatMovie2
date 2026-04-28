from di_toolbox import *


#get cast and total number of rows
csv_path = di_getpath("cast.csv")
total_rows = di_count_rows(csv_path)



with open(csv_path, encoding="utf8") as f:
    reader = csv.DictReader(f)

    batch = []
    batch_size = 1000

    for row in tqdm(reader, total=total_rows, desc="Importing cast.csv", unit="rows"):

        batch.append((
            clean(row["id"]),
            clean(row["movie_id"]),
            clean(row["person_id"]),
            clean(row["name"]),
            clean(row["character"]),
            clean(row["cast_order"]),
            clean(row["movie_title"]),
            clean(row["movie_release_date"])
        ))

        if len(batch) >= batch_size:
            psycopg2.extras.execute_batch(cur, """
                INSERT INTO temp_cast (
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
            INSERT INTO temp_cast (
                id, movie_id, person_id, name, character, cast_order,
                movie_title, movie_release_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, batch)
        conn.commit()


di_closing()