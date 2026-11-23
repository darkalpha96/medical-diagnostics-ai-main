"""
Medical Diagnosis AI - Railway Deployment
HIGH-RISK SYSTEM - HIPAA Compliant
"""

import os
import time
import random
from datetime import datetime
from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Configuration from environment
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")
API_KEY = os.environ.get("API_KEY", "")
SYSTEM_ID = os.environ.get("SYSTEM_ID", "")
PUSH_INTERVAL = int(os.environ.get("PUSH_INTERVAL", "20"))

# Stats
stats = {"push_count": 0, "last_push": None, "last_score": None}


def get_metrics():
    """Generate HIPAA-compliant medical AI metrics.
    
    NOTE: Simulating a system with some compliance issues for demo purposes.
    This will trigger alerts in the dashboard.
    """
    # Simulate some compliance issues - lower scores in certain areas
    return [
        {"metric_type": "phi_encryption", "value": 100, "category": "privacy"},
        {"metric_type": "access_control_score", "value": round(random.uniform(65, 78), 2), "category": "security"},  # Low - trigger alert
        {"metric_type": "audit_log_coverage", "value": round(random.uniform(70, 85), 2), "category": "security"},  # Moderate
        {"metric_type": "session_timeout_compliance", "value": 100, "category": "security"},
        {"metric_type": "data_encryption_score", "value": round(random.uniform(85, 95), 2), "category": "privacy"},
        {"metric_type": "data_retention_compliance", "value": round(random.uniform(60, 75), 2), "category": "privacy"},  # Low
        {"metric_type": "model_accuracy", "value": round(random.uniform(82, 90), 2), "category": "performance"},  # Moderate
        {"metric_type": "fairness_score", "value": round(random.uniform(55, 70), 2), "category": "fairness"},  # Low - trigger fairness alert
        {"metric_type": "explainability_score", "value": round(random.uniform(60, 75), 2), "category": "explainability"},  # Low
        {"metric_type": "robustness_score", "value": round(random.uniform(70, 82), 2), "category": "security"},
        {"metric_type": "drift_detection_score", "value": round(random.uniform(75, 88), 2), "category": "monitoring"},
        {"metric_type": "sensitivity", "value": round(random.uniform(85, 93), 2), "category": "performance"},
        {"metric_type": "specificity", "value": round(random.uniform(80, 90), 2), "category": "performance"},
    ]


def push_metrics():
    """Push metrics to the compliance monitor."""
    if not API_KEY or not SYSTEM_ID:
        print("ERROR: API_KEY or SYSTEM_ID not configured")
        return False

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "system_id": SYSTEM_ID,
        "metrics": get_metrics(),
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/monitoring/{SYSTEM_ID}/metrics",
            json=payload,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            score = result.get("compliance_score", "N/A")
            alerts = result.get("alerts_created", 0)
            stats["push_count"] += 1
            stats["last_push"] = datetime.utcnow().isoformat()
            stats["last_score"] = score
            alert_msg = f" | {alerts} alerts" if alerts > 0 else ""
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Pushed | Score: {score}%{alert_msg}")
            return True
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Error: {response.status_code} - {response.text[:100]}")
            return False

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Exception: {e}")
        return False


@app.route("/")
def index():
    return jsonify({
        "service": "Medical Diagnosis AI",
        "type": "HIGH-RISK - HIPAA Compliant",
        "status": "running",
        "api_target": API_BASE_URL,
        "system_id": SYSTEM_ID,
        "configured": bool(API_KEY and SYSTEM_ID),
        "stats": stats
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


def run_simulator():
    """Background loop to push metrics."""
    print("=" * 50, flush=True)
    print("  Medical Diagnosis AI", flush=True)
    print("  ⚠ HIGH-RISK - HIPAA Compliant", flush=True)
    print("=" * 50, flush=True)
    print(f"  API: {API_BASE_URL}", flush=True)
    print(f"  System ID: {SYSTEM_ID}", flush=True)
    print(f"  Interval: {PUSH_INTERVAL}s", flush=True)
    print("=" * 50, flush=True)

    while True:
        push_metrics()
        time.sleep(PUSH_INTERVAL)


# Start simulator thread when app loads (works with gunicorn)
import threading
import atexit

simulator_thread = None

def start_simulator():
    global simulator_thread
    if os.environ.get("GITHUB_ACTIONS"):   # <-- add these two lines
        return
    if simulator_thread is None or not simulator_thread.is_alive():
        if API_KEY and SYSTEM_ID:
            simulator_thread = threading.Thread(target=run_simulator, daemon=True)
            simulator_thread.start()
            print(f"[STARTUP] Simulator thread started", flush=True)
        else:
            print(f"[STARTUP] Skipping simulator - API_KEY or SYSTEM_ID not configured", flush=True)

# Start on app load
start_simulator()


if __name__ == "__main__":
    # Run Flask directly (for local testing)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
