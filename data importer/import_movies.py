from di_toolbox import *

#get cast and total number of rows
csv_path = di_getpath("movies.csv")
total_rows = di_count_rows(csv_path)


with open(csv_path, encoding="utf8") as f:
    reader = csv.DictReader(f)

    batch = []
    batch_size = 1000

    for row in tqdm(reader, total=total_rows, desc="Importing movies.csv", unit="rows"):

        batch.append((
            clean(row["id"]),
            clean(row["title"]),
            clean(row["original_title"]),
            clean(row["overview"]),
            clean(row["release_date"]),
            clean(row["runtime"]),
            clean(row["budget"]),
            clean(row["revenue"]),
            clean(row["vote_average"]),
            clean(row["vote_count"]),
            clean(row["popularity"]),
            clean(row["poster_path"]),
            clean(row["backdrop_path"]),
            clean(row["status"]),
            clean(row["tagline"]),
            clean(row["homepage"]),
            clean(row["original_language"]),
            clean(row["adult"]),
            clean(row["video"]),
            clean(row["updated_at"]),
            clean(row["genres"])
        ))

        if len(batch) >= batch_size:
            psycopg2.extras.execute_batch(cur, """
                INSERT INTO temp_movies (
                    id, title, original_title, overview, release_date, runtime, budget, revenue,
                    vote_average, vote_count, popularity, poster_path, backdrop_path, status,
                    tagline, homepage, original_language, adult, video, updated_at, genres
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, batch)
            conn.commit()
            batch = []

    if batch:
        psycopg2.extras.execute_batch(cur, """
            INSERT INTO temp_movies (
                id, title, original_title, overview, release_date, runtime, budget, revenue,
                vote_average, vote_count, popularity, poster_path, backdrop_path, status,
                tagline, homepage, original_language, adult, video, updated_at, genres
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, batch)
        conn.commit()


di_closing()