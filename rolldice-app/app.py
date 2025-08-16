"""Rolldice Flask app with clean linting."""

import logging
import random
from flask import Flask, jsonify

app = Flask(__name__)
log = logging.getLogger("rolldice")


@app.get("/rolldice")
def roll():
    """Return a pseudo-random dice result (1..6)."""
    value = random.randint(1, 6)
    log.info("rolled=%d", value)
    return jsonify({"dice": value})


@app.get("/healthz")
def healthz():
    """Liveness probe endpoint."""
    return "ok", 200


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=8080)
