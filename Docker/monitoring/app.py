from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter("app_requests_total", "Total app requests")


@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return "Hello from monitored app\n"


@app.route("/slow")
def slow():
    REQUEST_COUNT.inc()
    time.sleep(2)
    return "Slow endpoint finished\n"


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


@app.route("/health")
def health():
    return "OK\n", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)