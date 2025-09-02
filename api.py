import random
from flask import Flask, jsonify
from copy import deepcopy

app = Flask(__name__)

# Base data now includes a unique ip_address for each node

base_nodes = [
    {
        "id": "us-1",
        "name": "Eagle Server",
        "country": "United States",
        "latency_ms": 54,
        "ip_address": "104.26.10.188",
    },
    {
        "id": "ca-1",
        "name": "Maple Leaf",
        "country": "Canada",
        "latency_ms": 72,
        "ip_address": "142.126.146.1",
    },
    {
        "id": "jp-1",
        "name": "Tokyo Drift",
        "country": "Japan",
        "latency_ms": 120,
        "ip_address": "103.102.160.10",
    },
    {
        "id": "uk-1",
        "name": "London Bridge",
        "country": "United Kingdom",
        "latency_ms": 35,
        "ip_address": "195.245.231.14",
    },
]


@app.route("/api/v1/nodes")
def get_nodes():
    """Returns the node list with randomized latency for simulation."""
    nodes_with_random_latency = deepcopy(base_nodes)

    for node in nodes_with_random_latency:
        fluctuation = random.randint(-5, 5)
        node["latency_ms"] += fluctuation
        if node["latency_ms"] < 10:
            node["latency_ms"] = 10
    return jsonify(nodes_with_random_latency)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
