# CognoDB Cloud Graph Database Benchmark

A reproducible benchmark project comparing **CognoDB Cloud** and **Neo4j** using the same graph dataset and comparable workloads.

The benchmark evaluates graph database performance across data loading, graph traversal, lookups, aggregations, and concurrent mixed read/write workloads.

---

## Overview

This project evaluates graph database performance using the following workloads:

- Dataset loading
- Point lookups
- Filtered lookups
- 1-hop graph traversal
- 2-hop graph traversal
- 3-hop graph traversal
- Node count aggregation
- Relationship count aggregation
- Mixed read/write workloads
- Concurrent client workloads

The benchmark reports:

- P50 latency
- P95 latency
- Throughput
- Dataset loading time
- Relationships per second

The goal is to provide a transparent and reproducible benchmark rather than claim that one database is universally better than another.

---

## Dataset

The benchmark uses the **ca-HepPh collaboration network dataset** from the Stanford Network Analysis Project (SNAP).

A reproducible sample containing **100,000 relationships** was generated from the original dataset so that the workload remains manageable on the selected database tiers.

### Dataset Size

| Property | Value |
|---|---:|
| Dataset | ca-HepPh |
| Nodes | 9,904 |
| Relationships | 100,000 |
| Format | GZIP-compressed edge list |

The raw dataset is intentionally excluded from Git because of its size.

The sample dataset can be regenerated using:

```text
python src/create_sample.py

Project Structure
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

Databases Tested
CognoDB Cloud

CognoDB Cloud was tested using its free cloud instance.

The benchmark used the official Neo4j Python driver over the Bolt protocol.

Neo4j

Neo4j was tested using a local Neo4j Desktop instance.

The Neo4j instance was accessed through:

bolt://127.0.0.1:7687

Both databases used the same 100,000-relationship sample dataset.

Benchmark Methodology

The benchmark uses the same logical dataset and workload categories for both databases.

Each database was warmed up before the measured read workloads.

Read workloads were executed for 100 iterations.

The benchmark reports:

P50 Latency

P50 represents the median latency. Approximately half of the measured operations complete faster than this value.

P95 Latency

P95 represents the latency below which approximately 95% of measured operations complete.

P95 is useful for understanding slower requests and latency variability.

Throughput

Throughput represents completed operations per second.

Concurrency

The mixed workload benchmark evaluates:

1 client
10 clients
40 clients

The Neo4j mixed workload uses:

70% reads
30% writes
20 operations per client
CognoDB Results
Dataset Loading
Metric	Result
Nodes	9,904
Relationships	100,000
Load Time	200.71 seconds
Relationships/Second	498.24
Query Benchmark
Metric	P50 (ms)	P95 (ms)
1-Hop Traversal	306.91	369.81
2-Hop Traversal	615.09	1229.56
3-Hop Traversal	1637.90	1843.13
Point Lookup by ID	306.98	345.90
Filtered Lookup	306.52	363.59
Count Aggregation	307.05	370.51
Relationship Count Aggregation	307.00	345.31
CognoDB Mixed Workload
Clients	Throughput (queries/sec)	P50 (ms)	P95 (ms)
1	3.25	306.93	345.58
10	23.56	306.80	357.35
40	91.86	275.26	379.76
Neo4j Results
Dataset Loading
Metric	Result
Nodes	9,904
Relationships	100,000
Load Time	602.33 seconds
Relationships/Second	166.02

The Neo4j loader is implemented in:

src/neo4j_loader.py
Query Benchmark
Metric	P50 (ms)	P95 (ms)
1-Hop Traversal	18.98	146.22
2-Hop Traversal	28.29	69.98
3-Hop Traversal	15.88	31.73
Point Lookup by ID	10.44	18.19
Filtered Lookup	9.78	16.35
Count Aggregation	5.87	12.00
Relationship Count Aggregation	8.79	22.07

The Neo4j query benchmark is implemented in:

src/neo4j_benchmark.py
Neo4j Mixed Read/Write Workload

The Neo4j mixed workload consists of:

70% read operations
30% write operations
20 operations per client
1, 10, and 40 concurrent clients
Results
Clients	Throughput (queries/sec)	P50 (ms)	P95 (ms)
1	46.15	6.36	72.76
10	838.92	9.95	20.07
40	835.60	47.87	75.52
Mixed Workload Analysis

Throughput increased significantly from 1 to 10 concurrent clients.

At 10 clients, Neo4j achieved the highest observed throughput of:

838.92 queries/sec

At 40 clients, throughput remained approximately stable:

835.60 queries/sec

However, latency increased at 40 clients:

P50 = 47.87 ms
P95 = 75.52 ms

This suggests that the tested local environment reached a throughput plateau around 10 concurrent clients, while additional concurrency increased latency.

The implementation is available in:

src/neo4j_mixed_workload.py

Detailed results are available in:

results/neo4j_mixed_workload_results.md
CognoDB vs Neo4j Comparison
Query Latency
Metric	CognoDB P50	Neo4j P50	CognoDB P95	Neo4j P95
1-Hop Traversal	306.91 ms	18.98 ms	369.81 ms	146.22 ms
2-Hop Traversal	615.09 ms	28.29 ms	1229.56 ms	69.98 ms
3-Hop Traversal	1637.90 ms	15.88 ms	1843.13 ms	31.73 ms
Point Lookup	306.98 ms	10.44 ms	345.90 ms	18.19 ms
Filtered Lookup	306.52 ms	9.78 ms	363.59 ms	16.35 ms
Count Aggregation	307.05 ms	5.87 ms	370.51 ms	12.00 ms
Relationship Count	307.00 ms	8.79 ms	345.31 ms	22.07 ms
Loading Performance Comparison
Metric	CognoDB	Neo4j
Nodes	9,904	9,904
Relationships	100,000	100,000
Load Time	200.71 sec	602.33 sec
Relationships/sec	498.24	166.02

CognoDB completed the measured dataset load faster in this environment.

Mixed Workload Comparison

The mixed workload measurements were performed independently for each database.

CognoDB
Clients	Throughput	P50	P95
1	3.25 q/s	306.93 ms	345.58 ms
10	23.56 q/s	306.80 ms	357.35 ms
40	91.86 q/s	275.26 ms	379.76 ms
Neo4j
Clients	Throughput	P50	P95
1	46.15 q/s	6.36 ms	72.76 ms
10	838.92 q/s	9.95 ms	20.07 ms
40	835.60 q/s	47.87 ms	75.52 ms

The mixed workload implementations are not identical at the operation level, so these results should be interpreted as workload-specific measurements rather than a universal ranking.

Analysis

The measured results show significant differences between the two tested environments.

Neo4j produced substantially lower query latency across the tested lookup, traversal, and aggregation workloads.

CognoDB showed increasing latency as traversal depth increased:

1-hop → 306.91 ms P50
2-hop → 615.09 ms P50
3-hop → 1637.90 ms P50

Neo4j produced:

1-hop → 18.98 ms P50
2-hop → 28.29 ms P50
3-hop → 15.88 ms P50

The Neo4j 3-hop result should not be interpreted as proof that deeper traversal is universally faster. Query execution depends on graph structure, result cardinality, caching, execution plans, and the exact query shape.

For data loading, CognoDB achieved higher measured throughput:

CognoDB: 498.24 relationships/sec
Neo4j:   166.02 relationships/sec

For the mixed workload, Neo4j achieved substantially higher throughput in the tested local environment, reaching approximately 839 queries/sec at 10 concurrent clients.

Important Methodology Caveats

The benchmark is intended to be honest about environmental differences.

CognoDB was tested as a cloud-hosted database, while Neo4j was tested using a local Neo4j Desktop instance.

Therefore, the results are not a perfectly hardware-identical comparison.

The network path, CPU, memory, storage, database configuration, and execution environment can influence performance.

The measured numbers should therefore be interpreted as results from the documented test environments rather than universal performance guarantees.

The benchmark uses a 100,000-relationship sample rather than the complete source dataset.

Only measured results are reported; failed or incomplete benchmark runs were not included as performance measurements.

Reproducibility
Requirements
Python 3.10+
Python virtual environment
Neo4j Python Driver
Neo4j Desktop for the Neo4j local benchmark
CognoDB Cloud account for CognoDB benchmarks
Git

Install dependencies:

pip install -r requirements.txt
Environment Variables

Credentials should never be committed to GitHub.

Configure CognoDB credentials locally:

COGNODB_URI=<your-cognodb-uri>
COGNODB_USERNAME=<your-cognodb-username>
COGNODB_PASSWORD=<your-cognodb-password>

Configure the Neo4j password locally:

NEO4J_PASSWORD=<your-neo4j-password>

The .env file containing credentials must remain excluded from Git.

Running the Project
Generate the Sample Dataset
python src/create_sample.py
Load the Dataset into CognoDB
python src/loader.py
Run the CognoDB Query Benchmark
python src/benchmark.py
Run the CognoDB Mixed Workload
python src/mixed_workload.py
Load the Dataset into Neo4j
python src/neo4j_loader.py
Run the Neo4j Query Benchmark
python src/neo4j_benchmark.py
Run the Neo4j Mixed Workload
python src/neo4j_mixed_workload.py
Results Files

Detailed results are stored in:

results/cognodb_results.md
results/neo4j_results.md
results/neo4j_mixed_workload_results.md
Source Code
CognoDB
src/loader.py
src/benchmark.py
src/mixed_workload.py
Neo4j
src/neo4j_loader.py
src/neo4j_benchmark.py
src/neo4j_mixed_workload.py
Dataset Generation
src/create_sample.py
Security

Database passwords, connection URIs, API keys, and other secrets must not be committed to the repository.

All credentials should be supplied through environment variables or local configuration.

The repository should never contain:

.env

with real credentials.

Limitations
The benchmark uses a 100,000-relationship sample rather than the complete dataset.
Neo4j was tested locally using Neo4j Desktop.
CognoDB was tested as a cloud-hosted database.
Network latency affects CognoDB measurements.
Hardware and resource configurations are not perfectly identical.
Free-tier and local-development configurations may impose different limitations.
The benchmark represents selected workloads rather than every possible graph database workload.
The mixed workload implementations use comparable workload concepts but are not identical internally.
Results can vary between runs because of caching, system load, network conditions, and database state.
Future Work

Potential improvements include:

Benchmarking at least four additional graph database platforms.
Running all platforms in equivalent cloud regions.
Matching CPU, RAM, and storage resources more closely.
Increasing the dataset toward 500,000 relationships.
Running multiple independent benchmark trials.
Reporting confidence intervals and variance.
Adding concurrency sweeps beyond 40 clients.
Adding cold-start measurements.
Adding automated result collection.
Generating charts from benchmark results.
Automating the complete benchmark using a single command.
Adding more graph traversal patterns.
Measuring observable resource consumption.
Conclusion

This project provides a reproducible benchmark of CognoDB Cloud and Neo4j using the ca-HepPh collaboration network dataset.

The benchmark covers:

Data ingestion
Graph traversal
Point lookups
Filtered lookups
Aggregations
Concurrent mixed workloads

The results show meaningful performance differences between the tested environments while also highlighting the importance of methodology, resource parity, workload design, and environmental conditions.

The goal of this project is not simply to declare a winner, but to provide transparent measurements and explain the conditions under which those measurements were obtained.


**Important:** keep the Neo4j sections. They're a core part of your assignment now.

After you paste the entire block into `README.md`, press **Ctrl + S**. Then we can do the final Git commit and push.

