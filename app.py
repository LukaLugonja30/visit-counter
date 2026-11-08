import logging
import os
import socket
import sys
import redis
from flask import Flask, jsonify, request


APP_PORT = int(os.getenv("APP_PORT", "8080"))#cita promenljivu okruzenja, druga prom je rezervna za slucaj da prva nije postavjena
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,# Kazemo dockeru da koristimo standardni izlaz
    format="%(asctime)s %(levelname)s %(message)s",
)

logging.getLogger("werkzeug").setLevel(logging.WARNING)#gasi ugradjeni log da se ne bi ispisivalo 2 puta

app = Flask(__name__)
db = redis.Redis(# pravimo vezu sa redisom
    host=REDIS_HOST,
    port=REDIS_PORT,
    socket_connect_timeout=2,# ne cekaj duze od 2 sekunde
    decode_responses=True,#vraca tekst umesto bajtova
)


@app.after_request#posle svakog zahteva upise u log metodu put i status
def log_request(response):
    app.logger.info("%s %s -> %s", request.method, request.path, response.status_code)
    return response


@app.route("/")
def index():
    return jsonify(message="Hello DevOps", host=socket.gethostname())


@app.route("/visits")
def visits():
    count = db.incr("visits")# povecava posete za 1, ako kljuc ne postoji redis pravi novi sa vrednosti 1
    return jsonify(visits=count)


@app.route("/health")
def health():
    try:
        db.ping() #pita redis jel ziv ako nije baca exp sa kodom 503
        return jsonify(status="ok"), 200
    except redis.exceptions.RedisError:
        return jsonify(status="error"), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)#da bi aplikacija bila dostupna na svim mrezama