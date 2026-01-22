import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

sns.set(style="whitegrid", palette="muted", font_scale=1.2)

# --------------------------------------
# 1️⃣ FAILOVER TIME COMPARISON
# --------------------------------------
failover_scenarios = ['Primary→Backup', 'Backup→Secondary', 'Auto Rollback']
failover_time = [3.4, 4.1, 2.7]  

plt.figure(figsize=(8,5))
sns.barplot(x=failover_scenarios, y=failover_time)
plt.title("Failover Time Comparison", fontsize=16, fontweight='bold')
plt.ylabel("Time (seconds)")
plt.xlabel("Failover Scenario")
plt.tight_layout()
plt.show()

# --------------------------------------
# 2️⃣ UPTIME / AVAILABILITY COMPARISON
# --------------------------------------
availability = pd.DataFrame({
    'Scenario': ['Without Failover', 'With Multi-Cloud Failover'],
    'Availability (%)': [85.2, 99.4]
})

plt.figure(figsize=(7,5))
sns.barplot(x='Scenario', y='Availability (%)', data=availability)
plt.title("System Availability Comparison", fontsize=16, fontweight='bold')
plt.ylabel("Uptime Percentage")
plt.tight_layout()
plt.show()

# --------------------------------------
# 3️⃣ LATENCY DURING TRANSITION
# --------------------------------------
time = np.arange(0, 30, 1)  # seconds
latency = [120 if 8 <= t <= 10 else 60 if t < 8 else 65 if t < 15 else 58 for t in time]

plt.figure(figsize=(9,5))
plt.plot(time, latency, linewidth=3)
plt.axvspan(8, 10, color='red', alpha=0.2, label='Attack Period')
plt.axvspan(10, 13, color='yellow', alpha=0.2, label='Failover Transition')
plt.title("Latency Trend During Attack and Recovery", fontsize=16, fontweight='bold')
plt.xlabel("Time (seconds)")
plt.ylabel("Latency (ms)")
plt.legend()
plt.tight_layout()
plt.show()

# --------------------------------------
# 4️⃣ THROUGHPUT COMPARISON
# --------------------------------------
throughput = pd.DataFrame({
    'Cloud': ['Primary', 'Backup'],
    'Requests per second': [950, 910]
})

plt.figure(figsize=(7,5))
sns.barplot(x='Cloud', y='Requests per second', data=throughput)
plt.title("Throughput Comparison Between Clouds", fontsize=16, fontweight='bold')
plt.ylabel("Requests/sec")
plt.tight_layout()
plt.show()

# --------------------------------------
# 5️⃣ ATTACK IMPACT ANALYSIS
# --------------------------------------
time2 = np.arange(0, 20, 1)
success_rate = [99 if t < 5 else 80 if t < 9 else 95 for t in time2]
cpu_load = [40 if t < 5 else 85 if t < 9 else 55 for t in time2]
error_rate = [1 if t < 5 else 15 if t < 9 else 3 for t in time2]

plt.figure(figsize=(9,5))
plt.plot(time2, success_rate, label="Success Rate (%)", linewidth=2)
plt.plot(time2, cpu_load, label="CPU Load (%)", linewidth=2)
plt.plot(time2, error_rate, label="Error Rate (%)", linewidth=2)
plt.title("System Performance Under Attack", fontsize=16, fontweight='bold')
plt.xlabel("Time (seconds)")
plt.ylabel("Percentage (%)")
plt.legend()
plt.tight_layout()
plt.show()

# --------------------------------------
# 6️⃣ COST EFFICIENCY ANALYSIS (OPTIONAL)
# --------------------------------------
cost_labels = ['Traditional Always-On Backup', 'Adaptive Failover System']
costs = [100, 68]  # Example cost units (e.g., $/hour)

plt.figure(figsize=(7,7))
plt.pie(costs, labels=cost_labels, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff'])
plt.title("Cost Efficiency Comparison", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()
