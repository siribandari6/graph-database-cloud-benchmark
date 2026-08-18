# CognoDB Cloud Graph Database Benchmark

A reproducible benchmark project for evaluating graph database performance using the ca-HepPh collaboration network dataset on CognoDB Cloud.

## Overview

This project evaluates CognoDB Cloud using realistic graph database workloads including:

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

The benchmark records latency and throughput to provide a reproducible performance baseline.

## Dataset

The benchmark uses the **ca-HepPh** collaboration network dataset.

For reproducible testing, a 100,000-relationship sample was generated from the original dataset.

### Sample Dataset

- Relationships: 100,000
- Nodes: 9,904
- Format: GZIP-compressed edge list
- Graph model: Person nodes connected by COAUTHOR relationships

The raw dataset is intentionally excluded from Git because of its size.

## Project Structure

```text
graph-database-cloud-benchmark/
│
├── results/
│   └── cognodb_results.md
│
├── src/
│   ├── benchmark.py
│   ├── create_sample.py
│   ├── loader.py
│   └── mixed_workload.py
│
├── .gitignore
├── requirements.txt
└── README.md

## Neo4j vs CognоDB Benchmark Comparison

The benchmark was executed using the same graph dataset and workload categories to compare query performance.

| Metric | CognоDB P50 (ms) | Neo4j P50 (ms) | CognоDB P95 (ms) | Neo4j P95 (ms) |
|---|---:|---:|---:|---:|
| 1-Hop Traversal | 306.91 | 18.98 | 369.81 | 146.22 |
| 2-Hop Traversal | 615.09 | 28.29 | 1229.56 | 69.98 |
| 3-Hop Traversal | 1637.90 | 15.88 | 1843.13 | 31.73 |
| Point Lookup by ID | 306.98 | 10.44 | 345.90 | 18.19 |
| Filtered Lookup | 306.52 | 9.78 | 363.59 | 16.35 |
| Count Aggregation | 307.05 | 5.87 | 370.51 | 12.00 |
| Relationship Count Aggregation | 307.00 | 8.79 | 345.31 | 22.07 |

### Observations

- Neo4j achieved substantially lower median latency across all tested workloads.
- Point lookups and filtered lookups were particularly fast in Neo4j.
- CognоDB showed increasing latency as traversal depth increased.
- The largest P50 difference was observed for 3-hop traversal.
- Neo4j also showed lower P95 latency for every benchmark category.
- The results demonstrate the importance of evaluating graph databases under realistic workload patterns rather than relying only on single-query performance.

### Dataset

- Nodes: 9,904
- Relationships: 100,000
- Neo4j relationship loading time: 602.33 seconds
- Neo4j loading throughput: 166.02 relationships/second