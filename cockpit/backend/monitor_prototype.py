"""Module for monitoring a database interface.

Includes routes for throughput, storage_data, and runtime_information.
If run as a module, a flask server application will be started.
"""
import random
from json import dumps

import zmq
from flask import Flask
from flask_cors import CORS

import settings as s

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(f"tcp://{s.HI_HOST}:{s.HI_PORT}")  # socket of hyriseInterface instance


def send_request(data):
    """Send an IPC request with data to a database interface, return the repsonse."""
    request = dumps(data)
    socket.send_string(request)
    response = socket.recv()
    return response


@app.route("/throughput")
def get_throughput():
    """Return throughput information from database interface."""
    # data = {}
    # data["Content-Type"] = "throughput"
    # return send_request(data)
    return str(random.randint(5000, 7000))  # nosec


@app.route("/storage_data")
def get_storage_data():
    """Return storage information from database interface."""
    data = {}
    data["Content-Type"] = "storage_data"
    return send_request(data)


@app.route("/runtime_information")
def get_runtime_information():
    """Return runtime information from database interface."""
    data = {}
    data["Content-Type"] = "runtime_information"
    return send_request(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # nosec
