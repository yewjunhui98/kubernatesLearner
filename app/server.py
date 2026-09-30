from flask import Flask, jsonify
import os
import socket
from datetime import datetime, timezone

app = Flask(__name__)


@app.get("/")
def root():
    return jsonify(
        {
            "message": "Hello from Kubernetes on Podman!",
            "hostname": socket.gethostname(),
            "pod_note": os.getenv("POD_NOTE", "default-note"),
            "utc_time": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.get("/healthz")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
