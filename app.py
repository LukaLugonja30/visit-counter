import logging
import os
import socket
import sys
import redis
from flask import Flask, jsonify, request


APP_PORT = int(os.getenv("APP_PORT", "8080"))
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(message)s",
)

logging.getLogger("werkzeug").setLevel(logging.WARNING)

app = Flask(__name__)
db = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    socket_connect_timeout=2,
    decode_responses=True,
)


@app.after_request
def log_request(response):
    app.logger.info("%s %s -&gt; %s", request.method, request.path, response.status_code)
    return response


@app.route("/")
def index():
    return jsonify(message="Hello DevOps", host=socket.gethostname())


@app.route("/visits")
def visits():
    count = db.incr("visits")
    return jsonify(visits=count)


@app.route("/health")
def health():
    try:
        db.ping()
        return jsonify(status="ok"), 200
    except redis.exceptions.RedisError:
        return jsonify(status="error"), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)