# client_failover.py
import requests, time, json, os
from datetime import datetime

PRIMARY = "http://127.0.0.1:8000"
BACKUP  = "http://127.0.0.1:8001"
LOG_FILE = "failover_log.json"

POLL_INTERVAL = 2            
REQUEST_TIMEOUT = 1.5        
ROLLBACK_CONFIRM = 2         

# load or init log
if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, "r") as f:
            failover_log = json.load(f)
    except:
        failover_log = []
else:
    failover_log = []

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def append_log(active_server, status, message, latency=None):
    entry = {
        "timestamp": now(),
        "active_server": active_server,
        "status": status,
        "message": message,
        "latency_ms": latency
    }
    failover_log.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(failover_log, f, indent=2)

def probe(url):
    """Return (healthy:bool, payload_or_error, latency_ms_or_none)."""
    t0 = time.perf_counter()
    try:
        r = requests.get(url + "/", timeout=REQUEST_TIMEOUT)
        latency = (time.perf_counter() - t0) * 1000.0
        if r.status_code != 200:
            return False, {"status_code": r.status_code, "body": r.text}, latency
        try:
            j = r.json()
            if isinstance(j, dict) and ("error" in j or j.get("status") != "running"):
                return False, j, latency
        except ValueError:
            j = {"raw": r.text}
        return True, j, latency
    except Exception as e:
        return False, {"exception": str(e)}, None

def pretty(code):
    return "Primary" if code == "A" else "Backup"

def client_loop():
    active = "A"           # start preferring Primary
    primary_confirm = 0    # consecutive successful primary probes while on Backup

    print(f"[{now()}] Client started. Preferred=Primary. Poll interval={POLL_INTERVAL}s")

    while True:
        if active == "A":
            healthy, payload, lat = probe(PRIMARY)
            if healthy:
                append_log("Primary", "running", f"OK: {payload}", lat)
                print(f"[{now()}] RUNNING  Active=Primary OK: {payload} latency: {lat:.1f}ms" if lat else f"[{now()}] RUNNING  Active=Primary OK: {payload}")
            else:
                append_log("Primary", "error", f"Unhealthy: {payload}", lat)
                print(f"[{now()}] WARN     Active=Primary UNHEALTHY: {payload}")
                # Try backup right away
                b_healthy, b_payload, b_lat = probe(BACKUP)
                if b_healthy:
                    append_log("Backup", "failover", "Switch from Primary to Backup", b_lat)
                    print(f"[{now()}] FAILOVER Switching Primary -> Backup")
                    active = "B"
                    primary_confirm = 0
                    append_log("Backup", "running", f"OK: {b_payload}", b_lat)
                    print(f"[{now()}] RUNNING  Active=Backup OK: {b_payload} latency: {b_lat:.1f}ms" if b_lat else f"[{now()}] RUNNING  Active=Backup OK: {b_payload}")
                else:
                    append_log("None", "error", f"Both down. Primary error: {payload}; Backup error: {b_payload}", None)
                    print(f"[{now()}] CRITICAL Both servers unreachable. Retrying in {POLL_INTERVAL}s...")
        else:
            # active == "B"
            # 1) Probe Primary (to detect recovery) — we prefer primary if it's back
            p_healthy, p_payload, p_lat = probe(PRIMARY)
            if p_healthy:
                primary_confirm += 1
                append_log("Primary", "probe_ok", f"Primary probe ok {primary_confirm}/{ROLLBACK_CONFIRM}", p_lat)
            else:
                primary_confirm = 0
                append_log("Primary", "probe_fail", f"Primary probe fail: {p_payload}", p_lat)

            # If primary has been confirmed enough times, rollback
            if primary_confirm >= ROLLBACK_CONFIRM:
                append_log("Primary", "recovery", "Primary healthy — rolling back", p_lat)
                print(f"[{now()}] ROLLBACK Returning Backup -> Primary (confirmed {primary_confirm})")
                active = "A"
                primary_confirm = 0
                # log running after rollback
                append_log("Primary", "running", f"OK: {p_payload}", p_lat)
                print(f"[{now()}] RUNNING  Active=Primary OK: {p_payload} latency: {p_lat:.1f}ms" if p_lat else f"[{now()}] RUNNING  Active=Primary OK: {p_payload}")
                # small sleep to let system settle
                time.sleep(POLL_INTERVAL)
                continue

            # 2) If primary not confirmed, ensure backup still healthy
            b_healthy, b_payload, b_lat = probe(BACKUP)
            if b_healthy:
                append_log("Backup", "running", f"OK: {b_payload}", b_lat)
                print(f"[{now()}] RUNNING  Active=Backup OK: {b_payload} latency: {b_lat:.1f}ms" if b_lat else f"[{now()}] RUNNING  Active=Backup OK: {b_payload}")
            else:
                append_log("Backup", "error", f"Backup unhealthy: {b_payload}", b_lat)
                print(f"[{now()}] WARN     Active=Backup UNHEALTHY: {b_payload}")
                # try primary immediately if backup fails
                p2_healthy, p2_payload, p2_lat = probe(PRIMARY)
                if p2_healthy:
                    append_log("Primary", "recovery", "Primary recovered while backup down — switching to primary", p2_lat)
                    print(f"[{now()}] ROLLBACK Returning Backup -> Primary (primary healthy)")
                    active = "A"
                    primary_confirm = 0
                    append_log("Primary", "running", f"OK: {p2_payload}", p2_lat)
                    print(f"[{now()}] RUNNING  Active=Primary OK: {p2_payload} latency: {p2_lat:.1f}ms" if p2_lat else f"[{now()}] RUNNING  Active=Primary OK: {p2_payload}")
                else:
                    append_log("None", "error", f"Both down while on backup. backup: {b_payload}; primary: {p2_payload}", None)
                    print(f"[{now()}] CRITICAL Both servers unreachable. Retrying in {POLL_INTERVAL}s...")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    client_loop()
