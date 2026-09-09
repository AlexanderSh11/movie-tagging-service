import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Создание подключения к БД"""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        client_encoding="UTF8",
    )

    return conn


def load_movies():
    """Загрузка таблицы с фильмами"""
    conn = get_connection()

    query = " \
        SELECT \
            m.id, \
            m.movie_name, \
            m.year, \
            m.rating, \
            m.runtime,\
            m.meta_score, \
            m.age_rating, \
            m.overview, \
            STRING_AGG(DISTINCT g.name, ', ' ORDER BY g.name) AS genres, \
            STRING_AGG(DISTINCT d.name, ', ' ORDER BY d.name) AS directors, \
            STRING_AGG(DISTINCT c.name, ', ' ORDER BY c.name) AS countries \
        FROM movie m \
        LEFT JOIN movie_genre mg ON m.id = mg.movie_id \
        LEFT JOIN genres g ON mg.genre_id = g.id \
        LEFT JOIN movie_director md ON m.id = md.movie_id \
        LEFT JOIN directors d ON md.director_id = d.id \
        LEFT JOIN movie_country mc ON m.id = mc.movie_id \
        LEFT JOIN countries c ON mc.country_id = c.id \
        GROUP BY m.id, m.movie_name, m.year, m.rating, m.runtime, m.meta_score \
        ORDER BY m.id; \
    "

    df = pd.read_sql(query, conn)

    conn.close()
    return df


if __name__ == "__main__":
    df = load_movies()
    print("Загружены данные из БД, количество строк: ", len(df))
    print(df.head())
    print(df.columns.tolist())
