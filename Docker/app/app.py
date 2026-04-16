import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify


app = Flask(__name__)


def app_config():
    return {
        "message": os.getenv("APP_MESSAGE", "Hello from Docker"),
        "environment": os.getenv("APP_ENV", "development"),
        "host_name": socket.gethostname(),
        "utc_time": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
def home():
    config = app_config()
    return f"""
    <html>
      <head>
        <title>Docker Learning App</title>
      </head>
      <body style="font-family: sans-serif; max-width: 720px; margin: 40px auto;">
        <h1>{config["message"]}</h1>
        <p>This is a simple Python app running in a container.</p>
        <ul>
          <li><strong>Environment:</strong> {config["environment"]}</li>
          <li><strong>Container host name:</strong> {config["host_name"]}</li>
          <li><strong>UTC time:</strong> {config["utc_time"]}</li>
        </ul>
        <p>Useful routes:</p>
        <ul>
          <li><a href="/health">/health</a></li>
          <li><a href="/api/info">/api/info</a></li>
        </ul>
      </body>
    </html>
    """


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/info")
def info():
    return jsonify(app_config())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
