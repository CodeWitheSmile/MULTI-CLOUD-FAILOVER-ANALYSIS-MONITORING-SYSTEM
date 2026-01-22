# analyze_logs.py
import json, pandas as pd, matplotlib.pyplot as plt
from datetime import datetime

LOGFILE = "failover_log.json"
df = pd.read_json(LOGFILE)

# convert timestamp to datetime
df['ts'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('ts')

# compute uptime events: status == 'running' with active_server
running = df[df['status']=='running']
# compute total duration (from first to last)
start, end = df['ts'].min(), df['ts'].max()
total_seconds = (end - start).total_seconds()

# build timeline: for simplicity, compute periods where active_server is Primary/Backup/None
# we'll compute MTTR: average time from failover to recovery for primary
failover_rows = df[df['status'].isin(['failover','error'])]
recovery_rows = df[df['status'].isin(['recovery','running']) & df['active_server'].str.contains('Primary')]

# crude MTTR: join failover -> next recovery timestamp
mttrs = []
for idx, row in failover_rows.iterrows():
    t_fail = row['ts']
    # find next recovery where active_server == 'Primary' and ts > t_fail
    future = df[(df['ts']>t_fail) & (df['status'].isin(['recovery','running']))]
    if not future.empty:
        mttrs.append((future['ts'].iloc[0] - t_fail).total_seconds())
mttr = sum(mttrs)/len(mttrs) if mttrs else None

# compute success rate: fraction of running events vs total checks
success_rate = len(df[df['status']=='running']) / len(df)

print("Time window:", start, "to", end)
print("Total miliseconds:", total_seconds)
print("MTTR (s):", mttr)
print("Success rate:", round(success_rate*100,2), "%")

# Plot timeline: mark events
plt.figure(figsize=(10,3))
colors = {'Primary':'green','Backup':'blue','None':'red'}
y = 1
for _, r in df.iterrows():
    plt.scatter(r['ts'], y, color='black' if r['status']=='running' else 'red', s=20)
plt.title("Event timeline (dots=events; inspect log for types)")
plt.yticks([])
plt.tight_layout()
plt.savefig("timeline.png")
print("Saved timeline.png")
