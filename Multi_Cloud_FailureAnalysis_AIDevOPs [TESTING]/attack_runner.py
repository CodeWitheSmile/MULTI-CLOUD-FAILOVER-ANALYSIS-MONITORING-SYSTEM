import json, time, requests

ATTACKS_FILE = "attacks.json"
SERVERS = {
    "A": "http://127.0.0.1:8000",
    "B": "http://127.0.0.1:8001"
}

def check_health(target):
    """Ping the server to check if it's alive."""
    try:
        r = requests.get(f"{SERVERS[target]}/health", timeout=2)
        if r.status_code == 200:
            return True
        return False
    except Exception:
        return False

def wait_until_state(target, should_be_up, timeout=15):
    """Wait until server is up or down."""
    start = time.time()
    while time.time() - start < timeout:
        state = check_health(target)
        if should_be_up and state:
            print(f"[WAIT] {target} is UP ")
            return True
        elif not should_be_up and not state:
            print(f"[WAIT] {target} is DOWN ")
            return True
        time.sleep(1)
    print(f"[WARN] Timeout waiting for {target} to become {'UP' if should_be_up else 'DOWN'}")
    return False

def call_admin(target, action, value=None):
    try:
        url = SERVERS[target]
        if action == "disable":
            r = requests.post(f"{url}/admin/disable", timeout=3)
        elif action == "enable":
            r = requests.post(f"{url}/admin/enable", timeout=3)
        elif action == "latency":
            r = requests.post(f"{url}/admin/latency", params={"ms": value}, timeout=3)
        elif action == "cpu":
            r = requests.post(f"{url}/admin/cpu", params={"seconds": value}, timeout=3)
        else:
            print(f"[WARN] Unknown action {action}")
            return False, None
        return True, r.json()
    except Exception as e:
        print(f"[ERROR] Admin call failed for {target} {action}: {e}")
        return False, None

def run_attack_sequence(seq):
    name = seq.get("name", "unnamed")
    print(f"\n=== RUN ATTACK: {name} ===")

    for step in seq.get("steps", []):
        target = step.get("target")
        action = step.get("action")
        duration = step.get("duration", 0)
        value = step.get("value", None)
        print(f"[STEP] Target={target} Action={action} Duration={duration}s Value={value}")

        ok, resp = call_admin(target, action, value)
        print(f" -> ok={ok}, resp={resp}")

        # Wait for server state if disable/enable
        if action == "disable":
            wait_until_state(target, should_be_up=False)
        elif action == "enable":
            wait_until_state(target, should_be_up=True)

        if duration and duration > 0:
            print(f"  ...waiting {duration}s for system reaction")
            time.sleep(duration)

    print(f"=== END ATTACK: {name} ===\n")

def main():
    with open(ATTACKS_FILE, "r") as f:
        attacks = json.load(f).get("attacks", [])
    if not attacks:
        print("No attacks found in file.")
        return

    for seq in attacks:
        run_attack_sequence(seq)
        print("Inter-attack gap: 3s\n")
        time.sleep(3)

if __name__ == "__main__":
    main()
