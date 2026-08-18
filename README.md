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

## ⚠️ Scope and Resource Limitation

This submission benchmarks CognoDB Cloud and Neo4j using the same 100,000-relationship graph dataset and comparable workloads.

The assignment requested four additional graph database platforms. Due to free-tier availability, subscription requirements, and resource constraints within the evaluation window, the benchmark was limited to these two platforms.

No unmeasured or fabricated results are included. All reported results are based on actual benchmark runs.

## 📂 Dataset

The benchmark uses the **ca-HepPh collaboration network dataset**.

For reproducible testing, a 100,000-relationship sample was generated from the original dataset.

### Sample Dataset

- **Relationships:** 100,000
- **Nodes:** 9,904
- **Format:** GZIP-compressed edge list
- **Graph model:** Person nodes connected by `COAUTHOR` relationships

The raw dataset is intentionally excluded from Git because of its size.
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

    python src/create_sample.py

---

# 🗂️ Project Structure

The project is organized into source code, benchmark results, and configuration files.

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

# 🗄️ Databases Tested

This benchmark evaluates two graph database environments:

## ☁️ CognoDB Cloud

CognoDB Cloud was tested using its **free cloud instance**.

The benchmark evaluated:

- 📥 Dataset loading
- 🔎 Graph queries
- 🔗 Graph traversal
- 📊 Aggregations
- 🔄 Mixed read/write workloads

The benchmark used the database's Python connectivity to execute the tests.

---

## 🟦 Neo4j

Neo4j was tested using a **local Neo4j Desktop instance**.

The Neo4j instance was accessed through the Bolt protocol:

    bolt://127.0.0.1:7687

The benchmark used the official **Neo4j Python Driver** for database communication.

---

## ⚖️ Comparison Setup

Both databases were tested using the same:

- 📦 100,000-relationship sample dataset
- 🔎 Query workload categories
- 📊 Performance metrics
- 🧪 Benchmark methodology

However, the database environments were different:

| Database | Environment |
|---|---|
| ☁️ CognoDB Cloud | Cloud-hosted free-tier instance |
| 🟦 Neo4j | Local Neo4j Desktop instance |

> ⚠️ Because the environments are different, the results should be interpreted as measurements from the documented test conditions rather than universal performance guarantees.

---
# 🧪 Benchmark Methodology

The benchmark uses the same logical dataset and workload categories for both databases.

Each database was warmed up before the measured read workloads to reduce the impact of initial connection and startup effects.

Read workloads were executed for **100 iterations**.

## 🔬 Benchmark Workloads

The benchmark evaluates the following workloads:

1. 🔎 Point lookup by ID
2. 🔍 Filtered lookup
3. 🔗 1-hop graph traversal
4. 🔗 2-hop graph traversal
5. 🔗 3-hop graph traversal
6. 📊 Node count aggregation
7. 📊 Relationship count aggregation
8. 🔄 Mixed read/write workload
9. 👥 Concurrent client workloads

---

## 📏 Performance Metrics

### 📌 P50 Latency

**P50** represents the median latency.

Approximately half of the measured operations complete faster than this value.

A lower P50 generally indicates better typical response time.

---

### 📌 P95 Latency

**P95** represents the latency below which approximately 95% of measured operations complete.

P95 is useful for understanding slower requests and latency variability.

A lower P95 generally indicates better tail-latency performance.

---

### ⚡ Throughput

**Throughput** represents the number of completed operations per second.

Higher throughput means that more operations were completed during the measured period.

---

### 📥 Dataset Loading Time

Loading performance measures the time required to load the benchmark dataset into each database.

The benchmark also reports:

**Relationships per second**

This represents the number of relationships loaded per second.

---

## 👥 Concurrency

The mixed workload benchmark evaluates:

- **1 client**
- **10 clients**
- **40 clients**

The Neo4j mixed workload uses:

- **70% read operations**
- **30% write operations**
- **20 operations per client**

The purpose of the concurrency test is to observe how throughput and latency change as the number of simultaneous clients increases.

---

## 🔥 Warm-Up and Measurement

Before collecting measured results:

1. The database connection is established.
2. The workload is warmed up.
3. The measured benchmark begins.
4. Latency and throughput are recorded.
5. Results are summarized using P50 and P95 latency.

This approach helps reduce the influence of initial connection and startup overhead.

---
# ☁️ CognoDB Results

## 📥 Dataset Loading

The following results were measured while loading the 100,000-relationship sample dataset into CognoDB Cloud.

| Metric | Result |
|---|---:|
| Nodes | 9,904 |
| Relationships | 100,000 |
| Load Time | 200.71 seconds |
| Relationships/Second | 498.24 |

---

## 🔎 Query Benchmark

The following table shows the measured latency for the tested CognoDB query workloads.

| Metric | P50 (ms) | P95 (ms) |
|---|---:|---:|
| 1-Hop Traversal | 306.91 | 369.81 |
| 2-Hop Traversal | 615.09 | 1229.56 |
| 3-Hop Traversal | 1637.90 | 1843.13 |
| Point Lookup by ID | 306.98 | 345.90 |
| Filtered Lookup | 306.52 | 363.59 |
| Count Aggregation | 307.05 | 370.51 |
| Relationship Count Aggregation | 307.00 | 345.31 |

---

# 🔄 CognoDB Mixed Workload

The CognoDB mixed workload was evaluated using different levels of concurrent clients.

| Clients | Throughput (queries/sec) | P50 (ms) | P95 (ms) |
|---:|---:|---:|---:|
| 1 | 3.25 | 306.93 | 345.58 |
| 10 | 23.56 | 306.80 | 357.35 |
| 40 | 91.86 | 275.26 | 379.76 |

### 📊 Observations

As concurrency increased, measured throughput increased:

- **1 client:** 3.25 queries/sec
- **10 clients:** 23.56 queries/sec
- **40 clients:** 91.86 queries/sec

At 40 clients, the measured P50 latency was **275.26 ms**, while P95 latency was **379.76 ms**.

These measurements represent the observed performance of CognoDB Cloud under the tested workload and environment.

---
# 🟦 Neo4j Results

## 📥 Dataset Loading

The following results were measured while loading the same 100,000-relationship sample dataset into the local Neo4j instance.

| Metric | Result |
|---|---:|
| Nodes | 9,904 |
| Relationships | 100,000 |
| Load Time | 602.33 seconds |
| Relationships/Second | 166.02 |

The Neo4j dataset loader is implemented in:

    src/neo4j_loader.py

---

## 🔎 Query Benchmark

The following table shows the measured latency for the tested Neo4j query workloads.

| Metric | P50 (ms) | P95 (ms) |
|---|---:|---:|
| 1-Hop Traversal | 18.98 | 146.22 |
| 2-Hop Traversal | 28.29 | 69.98 |
| 3-Hop Traversal | 15.88 | 31.73 |
| Point Lookup by ID | 10.44 | 18.19 |
| Filtered Lookup | 9.78 | 16.35 |
| Count Aggregation | 5.87 | 12.00 |
| Relationship Count Aggregation | 8.79 | 22.07 |

The Neo4j query benchmark is implemented in:

    src/neo4j_benchmark.py

---

# 🔄 Neo4j Mixed Read/Write Workload

The Neo4j mixed workload consists of:

- 📖 **70% read operations**
- ✍️ **30% write operations**
- 🔢 **20 operations per client**
- 👥 **1, 10, and 40 concurrent clients**

## 📊 Results

| Clients | Throughput (queries/sec) | P50 (ms) | P95 (ms) |
|---:|---:|---:|---:|
| 1 | 46.15 | 6.36 | 72.76 |
| 10 | **838.92** | 9.95 | 20.07 |
| 40 | 835.60 | 47.87 | 75.52 |

---

## 🔍 Mixed Workload Analysis

Throughput increased significantly from **1 to 10 concurrent clients**.

At 10 clients, Neo4j achieved the highest observed throughput:

> ⚡ **838.92 queries/sec**

At 40 clients, throughput remained approximately stable:

> **835.60 queries/sec**

However, latency increased at 40 clients:

- **P50:** 47.87 ms
- **P95:** 75.52 ms

This suggests that the tested local environment reached a **throughput plateau around 10 concurrent clients**, while additional concurrency increased latency.

The mixed workload implementation is available in:

    src/neo4j_mixed_workload.py

Detailed results are available in:

    results/neo4j_mixed_workload_results.md

---
# ⚖️ CognoDB vs Neo4j Comparison

This section compares the measured performance of CognoDB Cloud and Neo4j across query latency, dataset loading, and mixed workloads.

---

## 🔎 Query Latency Comparison

| Metric | CognoDB P50 | Neo4j P50 | CognoDB P95 | Neo4j P95 |
|---|---:|---:|---:|---:|
| 1-Hop Traversal | 306.91 ms | 18.98 ms | 369.81 ms | 146.22 ms |
| 2-Hop Traversal | 615.09 ms | 28.29 ms | 1229.56 ms | 69.98 ms |
| 3-Hop Traversal | 1637.90 ms | 15.88 ms | 1843.13 ms | 31.73 ms |
| Point Lookup | 306.98 ms | 10.44 ms | 345.90 ms | 18.19 ms |
| Filtered Lookup | 306.52 ms | 9.78 ms | 363.59 ms | 16.35 ms |
| Count Aggregation | 307.05 ms | 5.87 ms | 370.51 ms | 12.00 ms |
| Relationship Count | 307.00 ms | 8.79 ms | 345.31 ms | 22.07 ms |

### 💡 Observation

Neo4j produced substantially lower measured query latency across the tested lookup, traversal, and aggregation workloads.

---

# 📥 Loading Performance Comparison

| Metric | CognoDB | Neo4j |
|---|---:|---:|
| Nodes | 9,904 | 9,904 |
| Relationships | 100,000 | 100,000 |
| Load Time | **200.71 sec** | 602.33 sec |
| Relationships/sec | **498.24** | 166.02 |

### 💡 Observation

CognoDB completed the measured dataset loading process faster in the tested environment.

---

# 🔄 Mixed Workload Comparison

The mixed workload measurements were performed independently for each database.

## ☁️ CognoDB

| Clients | Throughput | P50 | P95 |
|---:|---:|---:|---:|
| 1 | 3.25 q/s | 306.93 ms | 345.58 ms |
| 10 | 23.56 q/s | 306.80 ms | 357.35 ms |
| 40 | 91.86 q/s | 275.26 ms | 379.76 ms |

---

## 🟦 Neo4j

| Clients | Throughput | P50 | P95 |
|---:|---:|---:|---:|
| 1 | 46.15 q/s | 6.36 ms | 72.76 ms |
| 10 | **838.92 q/s** | 9.95 ms | 20.07 ms |
| 40 | 835.60 q/s | 47.87 ms | 75.52 ms |

> ⚠️ **Important:** The mixed workload implementations are not identical at the individual operation level. These results should therefore be interpreted as **workload-specific measurements**, rather than a universal ranking of the two databases.

---
# 📊 Analysis

The measured results show significant performance differences between the two tested environments.

---

## 🔗 Graph Traversal Performance

CognoDB showed increasing latency as traversal depth increased:

    1-hop → 306.91 ms P50
    2-hop → 615.09 ms P50
    3-hop → 1637.90 ms P50

Neo4j produced:

    1-hop → 18.98 ms P50
    2-hop → 28.29 ms P50
    3-hop → 15.88 ms P50

The Neo4j 3-hop result should **not** be interpreted as proof that deeper traversal is universally faster.

Query execution can depend on several factors, including:

- 🌐 Graph structure
- 📦 Result cardinality
- 💾 Database caching
- ⚙️ Query execution plans
- 🔎 Query shape
- 🛠️ Database configuration

---

## 📥 Data Loading Performance

CognoDB achieved higher measured loading throughput:

    CognoDB → 498.24 relationships/sec
    Neo4j   → 166.02 relationships/sec

In the tested environment, CognoDB completed the measured dataset loading process faster than Neo4j.

---

## ⚡ Mixed Workload Performance

For the tested mixed workload, Neo4j achieved substantially higher throughput in the local environment.

The highest measured Neo4j throughput was:

> 🚀 **838.92 queries/sec at 10 concurrent clients**

At 40 clients, throughput remained approximately stable at:

> **835.60 queries/sec**

However, latency increased at 40 clients:

- **P50:** 47.87 ms
- **P95:** 75.52 ms

This suggests that the tested local environment reached a **throughput plateau around 10 concurrent clients**, while additional concurrency increased latency.

---

## 🧠 Overall Interpretation

The benchmark results show that performance depends heavily on the workload and testing environment.

### ☁️ CognoDB

CognoDB showed:

- ✅ Faster measured dataset loading
- 📈 Increasing throughput as concurrency increased
- ⚠️ Higher measured query latency in the tested workloads

### 🟦 Neo4j

Neo4j showed:

- ✅ Lower measured query latency
- ⚡ Much higher measured mixed-workload throughput
- 📈 A throughput plateau around 10 concurrent clients
- ⚠️ Increased latency when concurrency increased to 40 clients

These observations are specific to the documented benchmark configuration and should not be treated as universal database performance claims.

---
# ⚠️ Important Methodology Caveats

This benchmark is intentionally transparent about environmental differences.

## 🌐 Different Testing Environments

- ☁️ **CognoDB** was tested as a cloud-hosted database.
- 🟦 **Neo4j** was tested using a local Neo4j Desktop instance.

Therefore, this is **not a perfectly hardware-identical comparison**.

Performance can be influenced by:

- 🌐 Network latency
- 🖥️ CPU
- 🧠 Memory
- 💾 Storage
- ⚙️ Database configuration
- 📦 Query execution plans
- 💾 Caching
- 🔄 System load

The measured numbers should therefore be interpreted as results from the **documented test environments**, rather than universal performance guarantees.

---

## 📦 Dataset Limitation

The benchmark uses a **100,000-relationship sample** rather than the complete ca-HepPh dataset.

This keeps the experiment manageable on the selected database tiers but may not represent performance at much larger graph sizes.

---

## 📊 Result Selection

Only measured results are reported.

Failed or incomplete benchmark runs were not included as performance measurements.

---

# 🔁 Reproducibility

The project is designed so that the benchmark can be reproduced using the provided source code and configuration.

## 🛠️ Requirements

You will need:

- 🐍 Python 3.10+
- 🧪 Python virtual environment
- 🟦 Neo4j Python Driver
- 🖥️ Neo4j Desktop for the local Neo4j benchmark
- ☁️ CognoDB Cloud account for CognoDB benchmarks
- 🐙 Git

---

## 📦 Install Dependencies

Run:

    pip install -r requirements.txt

---

# 🔐 Environment Variables

**Never commit database credentials, API keys, or other secrets to GitHub.**

Configure CognoDB credentials locally:

    COGNODB_URI=<your-cognodb-uri>
    COGNODB_USERNAME=<your-cognodb-username>
    COGNODB_PASSWORD=<your-cognodb-password>

Configure the Neo4j password locally:

    NEO4J_PASSWORD=<your-neo4j-password>

The `.env` file containing credentials must remain excluded from Git.

Make sure `.env` is included in `.gitignore`.

---
# ▶️ Running the Project

Follow the steps below to reproduce the benchmark.

---

## 1️⃣ Generate the Sample Dataset

Generate the reproducible 100,000-relationship sample:

    python src/create_sample.py

---

## 2️⃣ Load the Dataset into CognoDB

Load the generated dataset into CognoDB Cloud:

    python src/loader.py

---

## 3️⃣ Run the CognoDB Query Benchmark

Run the standard CognoDB query benchmark:

    python src/benchmark.py

---

## 4️⃣ Run the CognoDB Mixed Workload

Run the concurrent mixed read/write workload:

    python src/mixed_workload.py

---

## 5️⃣ Load the Dataset into Neo4j

Make sure your local Neo4j Desktop instance is running and then load the dataset:

    python src/neo4j_loader.py

---

## 6️⃣ Run the Neo4j Query Benchmark

Run the standard Neo4j query benchmark:

    python src/neo4j_benchmark.py

---

## 7️⃣ Run the Neo4j Mixed Workload

Run the concurrent mixed read/write workload:

    python src/neo4j_mixed_workload.py

---

# 📁 Results Files

Detailed benchmark results are stored in the `results/` directory:

    results/
    ├── cognodb_results.md
    ├── neo4j_results.md
    └── neo4j_mixed_workload_results.md

These files contain the detailed measurements generated during the benchmark runs.

---

# 💻 Source Code

## ☁️ CognoDB

The CognoDB benchmark implementation is located in:

    src/loader.py
    src/benchmark.py
    src/mixed_workload.py

---

## 🟦 Neo4j

The Neo4j benchmark implementation is located in:

    src/neo4j_loader.py
    src/neo4j_benchmark.py
    src/neo4j_mixed_workload.py

---

## 📦 Dataset Generation

The sample dataset generation script is:

    src/create_sample.py

---
# 🔒 Security

Database passwords, connection URIs, API keys, and other sensitive information **must never be committed to the repository**.

All credentials should be supplied through environment variables or local configuration.

### 🚫 Never Commit

The repository should never contain a `.env` file with real credentials.

Make sure `.env` is included in `.gitignore`.

Example:

    .env

> 🔐 **Security reminder:** Replace placeholder credentials with your actual local configuration, but never push real credentials to GitHub.

---

# ⚠️ Limitations

This benchmark has several limitations that should be considered when interpreting the results.

### 📦 Dataset Size

- The benchmark uses a **100,000-relationship sample** rather than the complete dataset.

### 🌐 Different Environments

- Neo4j was tested locally using **Neo4j Desktop**.
- CognoDB was tested as a **cloud-hosted database**.
- Network latency affects CognoDB measurements.
- Hardware and resource configurations are not perfectly identical.

### 💻 Resource Configuration

Free-tier and local-development configurations may impose different resource limitations.

CPU, memory, storage, network conditions, caching, and database configuration can all affect performance.

### 🧪 Workload Coverage

The benchmark represents selected graph database workloads rather than every possible workload.

The mixed workload implementations use comparable workload concepts but are **not identical internally**.

### 🔄 Run-to-Run Variation

Results can vary between benchmark runs because of:

- 💾 Database caching
- 🖥️ System load
- 🌐 Network conditions
- ⚙️ Database state
- 🔧 Configuration differences

Therefore, the reported results should be treated as **observations from the documented test conditions**, not universal performance guarantees.

---
# 🚀 Future Work

The benchmark can be extended in several ways to make the comparison more comprehensive and statistically robust.

Potential improvements include:

- 🗄️ Benchmarking at least four additional graph database platforms
- ☁️ Running all platforms in equivalent cloud regions
- ⚙️ Matching CPU, RAM, and storage resources more closely
- 📈 Increasing the dataset size toward 500,000 relationships
- 🔁 Running multiple independent benchmark trials
- 📐 Reporting confidence intervals and variance
- 👥 Adding concurrency sweeps beyond 40 clients
- 🧊 Adding cold-start measurements
- 🤖 Automating result collection
- 📊 Generating charts from benchmark results
- ⚡ Automating the complete benchmark using a single command
- 🔗 Adding more graph traversal patterns
- 💻 Measuring observable resource consumption

---

# 🏁 Conclusion

This project provides a reproducible benchmark comparing **CognoDB Cloud** and **Neo4j** using the **ca-HepPh collaboration network dataset**.

The benchmark covers:

- 📥 Data ingestion
- 🔗 Graph traversal
- 🔎 Point lookups
- 🔍 Filtered lookups
- 📊 Aggregations
- 🔄 Concurrent mixed workloads

The measured results show meaningful performance differences between the tested environments while also highlighting the importance of:

- 🧪 Benchmark methodology
- ⚙️ Resource parity
- 📊 Workload design
- 🌐 Network conditions
- 🗄️ Database configuration
- 💻 Execution environment

The goal of this project is **not simply to declare a winner**.

Instead, it aims to provide **transparent measurements, reproducible experiments, and clear explanations of the conditions under which those measurements were obtained.**

---

# ⭐ Key Takeaways

| Area | Observed Result |
|---|---|
| 📥 Data Loading | **CognoDB performed faster** in the tested environment |
| 🔎 Query Latency | **Neo4j performed substantially faster** |
| 🔗 Graph Traversal | **Neo4j showed lower measured latency** |
| ⚡ Mixed Workload | **Neo4j achieved higher throughput** |
| 👥 Peak Neo4j Throughput | **838.92 queries/sec at 10 clients** |
| 🎯 Overall Interpretation | Results are **environment- and workload-specific** |

> 💡 **Benchmarking is about measurement, not marketing.**
>
> These results should be interpreted within the documented experimental conditions rather than treated as universal performance guarantees.

---

## ⭐ Thank You

Thank you for checking out this benchmark project!

If you find the project useful, feel free to ⭐ **star the repository** and explore the benchmark implementation in the `src/` directory.
