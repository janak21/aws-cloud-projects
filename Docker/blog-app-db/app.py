from flask import Flask
import os
import time
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO visits DEFAULT VALUES")
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM visits")
    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return f"Blog app is running. Total visits recorded in DB: {count}\n"


@app.route("/health")
def health():
    try:
        conn = get_connection()
        conn.close()
        return "OK\n", 200
    except Exception as e:
        return f"DB connection failed: {e}\n", 500


if __name__ == "__main__":
    # optional small wait to make startup logs easier to read in practice
    time.sleep(1)
    init_db()
    app.run(host="0.0.0.0", port=5001)