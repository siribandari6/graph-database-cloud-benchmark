# 🚀 CognoDB Cloud Graph Database Benchmark

A reproducible benchmark project comparing **CognoDB Cloud** and **Neo4j** using the same graph dataset and comparable workloads.

The benchmark evaluates graph database performance across:

- 📥 Data loading
- 🔎 Point lookups
- 🔍 Filtered lookups
- 🔗 1-hop, 2-hop, and 3-hop graph traversal
- 📊 Aggregations
- 🔄 Mixed read/write workloads
- 👥 Concurrent client workloads

The goal is to provide **transparent and reproducible measurements** rather than claim that one database is universally better than another.

---

## 📌 Overview

This project benchmarks two graph database environments:

| Database | Environment |
|---|---|
| **CognoDB Cloud** | Cloud-hosted free-tier instance |
| **Neo4j** | Local Neo4j Desktop instance |

Both databases were tested using the same **100,000-relationship sample** generated from the **ca-HepPh collaboration network dataset**.

### 📏 Metrics Reported

The benchmark measures:

- **P50 latency** — Median request latency
- **P95 latency** — Tail latency for slower requests
- **Throughput** — Completed operations per second
- **Dataset loading time**
- **Relationships per second**

---
# 📂 Dataset

The benchmark uses the **ca-HepPh collaboration network dataset** from the **Stanford Network Analysis Project (SNAP)**.

A reproducible sample containing **100,000 relationships** was generated from the original dataset so that the workload remains manageable on the selected database tiers.

## 📊 Dataset Statistics

| Property | Value |
|---|---:|
| Dataset | ca-HepPh |
| Nodes | 9,904 |
| Relationships | 100,000 |
| Format | GZIP-compressed edge list |

The raw dataset is intentionally excluded from GitHub because of its size.

### 🔄 Generate the Sample Dataset

Run:

```bash
python src/create_sample.py

# 🗂️ Project Structure
graph-database-cloud-benchmark/
│
├── results/
│   ├── cognodb_results.md
│   ├── neo4j_results.md
│   └── neo4j_mixed_workload_results.md
│
├── src/
│   ├── benchmark.py
│   ├── create_sample.py
│   ├── loader.py
│   ├── mixed_workload.py
│   ├── neo4j_benchmark.py
│   ├── neo4j_loader.py
│   └── neo4j_mixed_workload.py
│
├── .gitignore
├── requirements.txt
└── README.md


---

