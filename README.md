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