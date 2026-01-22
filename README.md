# MULTI-CLOUD-FAILOVER-ANALYSIS-MONITORING-SYSTEM
A fault-tolerant multi-cloud failover system that simulates real-world cloud outages, performs automatic failover and rollback, and provides quantitative resilience analysis using metrics such as MTTR, availability, latency, and success rate.
This project demonstrates how distributed systems can be made self-healing using health checks, intelligent routing, and observability-driven insights.

Key Features
Primary–Backup Cloud Architecture
Automatic Failover & Rollback
Attack & Fault Injection Framework
Resilience Metrics (MTTR, Availability, Success Rate)
Graph-based System Analysis & Visualization
Cost-Efficiency Comparison (Adaptive vs Always-On Backup)

System Architecture
Primary Cloud (A) and Backup Cloud (B) expose identical APIs.
A client-side failover controller continuously monitors health and routes traffic.

When failures are detected:

Traffic is automatically redirected to Backup.
Primary is periodically probed for recovery.
System rolls back once Primary is confirmed healthy.

📌 A detailed workflow diagram is included in the report and methodology section.

🗂️ Project Structure
.
├── serverA_primary.py       # Primary cloud service
├── serverB_backup.py        # Backup cloud service
├── client_failover.py       # Failover + rollback controller
├── attack_runner.py         # Fault injection engine
├── attacks.json             # Attack scenarios
├── analyze_log.py           # MTTR & resilience analysis
├── analysis_plots.py        # Graphs & visualization
├── failover_log.json        # Event logs (auto-generated)
├── timeline_latest.png      # Failover timeline plot
└── README.md

⚙️ Technologies Used
Python 3
FastAPI – Cloud service simulation
Requests – Health probing
Matplotlib & Seaborn – Visualization
Pandas & NumPy – Log analysis
Threading – CPU load simulation

How to Run the Project
1️⃣ Start Primary Server
python serverA_primary.py

2️⃣ Start Backup Server
python serverB_backup.py

3️⃣ Start Failover Client
python client_failover.py

4️⃣ Inject Failures (Attacks)
python attack_runner.py

5️⃣ Analyze Logs & Generate Insights
python analyze_log.py
python analysis_plots.py

Fault Injection Capabilities
The attack engine can simulate:
Service outages (/admin/disable)
Network latency spikes
CPU saturation
Sequential multi-failure scenarios
Attack scenarios are defined in attacks.json, enabling reproducible experiments.

📊 Metrics & Evaluation
The system evaluates resilience using:
Metric	Description
MTTR	Mean Time To Recovery after failure
Availability	Percentage of successful service responses
Success Rate	Ratio of healthy responses over total probes
Latency	Request round-trip time during normal & failure states
Failover Time	Time taken to switch clouds

Graphs include:
Failover timeline
Latency during attack & recovery
Throughput comparison
Availability improvement
Cost efficiency analysis
Sample Results
Rapid automatic failover
Stable rollback without oscillation
Reduced downtime vs traditional systems
Lower cost than always-on backup architectures
Exact results vary depending on injected attack severity.

🔍 Why This Project Matters
Modern cloud-hosted systems (LLMs, APIs, inference engines) require:
High availability
Fast recovery
Cost-efficient redundancy
This project demonstrates how adaptive failover strategies outperform static backup models while maintaining reliability and sustainability.

Future Extensions
Kubernetes / Docker integration
Multi-region failover
LLM inference routing
Circuit breaker patterns

Prometheus & Grafana monitoring

Chaos engineering automation
