from flask import Flask
import os
import psycopg2
import redis

app = Flask(__name__)

@app.route("/")
def home():
    db_host = os.getenv("DB_HOST", "db")
    db_name = os.getenv("DB_NAME", "appdb")
    db_user = os.getenv("DB_USER", "appuser")
    db_password = os.getenv("DB_PASSWORD", "secret")
    db_port = int(os.getenv("DB_PORT", "5432"))

    redis_host = os.getenv("REDIS_HOST", "cache")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))

    db_message = ""
    redis_message = ""

    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        db_message = f"Postgres OK: {version}"
    except Exception as e:
        db_message = f"Postgres failed: {e}"

    try:
        r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        count = r.incr("hits")
        redis_message = f"Redis OK: hits={count}"
    except Exception as e:
        redis_message = f"Redis failed: {e}"

    return f"{db_message}\n{redis_message}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)