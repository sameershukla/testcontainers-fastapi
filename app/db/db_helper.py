import os
import psycopg2


def get_connection():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    username = os.getenv("DB_USERNAME", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    database = os.getenv("DB_NAME", "mydb")
    return psycopg2.connect(f"host={host} dbname={database} user={username} password={password} port={port}")