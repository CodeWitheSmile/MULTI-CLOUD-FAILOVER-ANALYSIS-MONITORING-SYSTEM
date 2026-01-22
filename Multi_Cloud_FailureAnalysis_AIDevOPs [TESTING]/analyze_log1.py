import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

LOGFILE = "failover_log.json"
df = pd.read_json(LOGFILE)


df['ts'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('ts')


# Focus only on the latest failover -> recovery cycle

failover_rows = df[df['status'].isin(['failover','error'])]
last_failover = failover_rows['ts'].max() if not failover_rows.empty else None

if last_failover:
    # keep only events after the last failover
    df = df[df['ts'] >= last_failover]

# compute total duration (from first to last in this subset)
start, end = df['ts'].min(), df['ts'].max()
total_seconds = (end - start).total_seconds()

# -----------------------------
# Compute MTTR (Mean Time To Recovery)
# -----------------------------
mttrs = []
if last_failover:
    # find the first recovery event after the last failover
    future = df[(df['ts'] > last_failover) & (df['status'].isin(['recovery','running']))]
    if not future.empty:
        mttrs.append((future['ts'].iloc[0] - last_failover).total_seconds())

mttr = sum(mttrs)/len(mttrs) if mttrs else None

# -----------------------------
# Compute success rate
# -----------------------------
success_rate = len(df[df['status'] == 'running']) / len(df) if len(df) > 0 else 0

# -----------------------------
# Print results
# -----------------------------
print("Analyzed time window:", start, "to", end)
print("Duration (s):", total_seconds)
print("MTTR (s):", mttr if mttr else "No recovery observed yet")
print("Success rate:", round(success_rate*100, 2), "%")

# -----------------------------
# Plot timeline
# -----------------------------
plt.figure(figsize=(10,3))
y = 1
for _, r in df.iterrows():
    plt.scatter(r['ts'], y, color='black' if r['status']=='running' else 'red', s=20)
plt.title("Latest Failover-Recovery Cycle Timeline")
plt.yticks([])
plt.tight_layout()
plt.savefig("timeline_latest.png")
print("Saved timeline_latest.png")
