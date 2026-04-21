from flask import Flask, jsonify
import os
import psycopg2
import redis

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypass")

REDIS_HOST = os.getenv("REDIS_HOST", "cache")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def get_redis_connection():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS request_logs (
            id SERIAL PRIMARY KEY,
            path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def home():
    r = get_redis_connection()
    hits = r.incr("hits")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO request_logs (path) VALUES (%s)", ("/",))
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM request_logs")
    total_requests = cur.fetchone()[0]
    cur.close()
    conn.close()

    return jsonify({
        "message": "API is running",
        "redis_hits": hits,
        "db_logged_requests": total_requests
    })


@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()
        r = get_redis_connection()
        r.ping()
        return "OK\n", 200
    except Exception as e:
        return f"Healthcheck failed: {e}\n", 500


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001)