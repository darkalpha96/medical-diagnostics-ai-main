import os, sys, time
from main import push_metrics

RUN_SECONDS = int(os.environ.get("RUN_SECONDS", "240"))
INTERVAL = int(os.environ.get("PUSH_INTERVAL", "20"))

end = time.time() + RUN_SECONDS
successes = 0
while True:
    if push_metrics():
        successes += 1
    if time.time() + INTERVAL >= end:
        break
    time.sleep(INTERVAL)

sys.exit(0 if successes else 1)