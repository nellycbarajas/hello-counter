from flask import Flask, jsonify

from app.domain.counter import increment, initial

app = Flask(__name__)

_state = initial()


@app.get("/count")
def get_count():
    return jsonify({"value": _state.value})


@app.post("/increment")
def increment_counter():
    global _state
    _state = increment(_state.value)
    return jsonify({"value": _state.value, "updated_at": _state.updated_at})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})