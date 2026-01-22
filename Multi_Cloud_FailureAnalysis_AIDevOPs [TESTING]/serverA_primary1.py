# server_template.py  (copy to serverA_primary.py and serverB_backup.py, edit NAME & PORT)
from fastapi import FastAPI, Response
import uvicorn
import time
import threading

# configure per server file
NAME = "Primary Cloud A"   
PORT = 8000                

app = FastAPI()

# internal state
_state = {
    "enabled": True,      
    "latency_ms": 0,      
}

@app.get("/")
def root():
    """Main endpoint used by client to check server health and response."""
    if not _state["enabled"]:
        return Response(content='{"error":"service disabled"}', status_code=503, media_type="application/json")
    # simulate latency
    latency = _state.get("latency_ms", 0)
    if latency and latency > 0:
        time.sleep(latency / 1000.0)
    return {"server": NAME, "status": "running"}

# Admin endpoints for attack runner
@app.post("/admin/disable")
def admin_disable():
    _state["enabled"] = False
    return {"result": "disabled", "server": NAME}

@app.post("/admin/enable")
def admin_enable():
    _state["enabled"] = True
    return {"result": "enabled", "server": NAME}

@app.post("/admin/latency")
def admin_latency(ms: int = 0):
    _state["latency_ms"] = max(0, int(ms))
    return {"result": "latency_set", "ms": _state["latency_ms"], "server": NAME}

@app.post("/admin/cpu")
def admin_cpu(seconds: int = 1):
    """Simulate CPU load asynchronously for safety."""
    def busy(sec):
        end = time.time() + sec
        x = 0
        while time.time() < end:
            x += 1  # busy loop (light)
    t = threading.Thread(target=busy, args=(max(0, int(seconds)),), daemon=True)
    t.start()
    return {"result": "cpu_task_started", "seconds": seconds, "server": NAME}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)
