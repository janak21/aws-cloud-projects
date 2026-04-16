from flask import Flask
import os
import psycopg2

app = Flask(__name__)

@app.route("/")
def home():
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "appdb")
    db_user = os.getenv("DB_USER", "appuser")
    db_password = os.getenv("DB_PASSWORD", "secret")
    db_port = os.getenv("DB_PORT", "5432")

    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        conn.close()
        return f"Connected to PostgreSQL at {db_host}:{db_port}"
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)