# CognoDB Benchmark Results

## Dataset

- Dataset: ca-HepPh
- Sample size: 100,000 relationships
- Nodes: 9,904
- Relationships: 100,000

## Load Performance

- Relationships loaded: 100,000
- Load time: 200.71 seconds
- Throughput: 498.24 relationships/second

## Query Benchmark

| Metric | P50 (ms) | P95 (ms) |
|---|---:|---:|
| 1-Hop Traversal | 306.91 | 369.81 |
| 2-Hop Traversal | 615.09 | 1229.56 |
| 3-Hop Traversal | 1637.90 | 1843.13 |
| Point Lookup by ID | 306.98 | 345.90 |
| Filtered Lookup | 306.52 | 363.59 |
| Count Aggregation | 307.05 | 370.51 |
| Relationship Count Aggregation | 307.00 | 345.31 |

## Mixed Workload Benchmark

| Clients | Throughput (queries/sec) | P50 (ms) | P95 (ms) |
|---:|---:|---:|---:|
| 1 | 3.25 | 306.93 | 345.58 |
| 10 | 23.56 | 306.80 | 357.35 |
| 40 | 91.86 | 275.26 | 379.76 |

## Summary

The CognoDB benchmark completed successfully.

The system loaded 100,000 graph relationships and created 9,904 nodes. Query performance was measured using traversal, lookup, filtering, and aggregation workloads.

The mixed workload achieved a maximum measured throughput of 91.86 queries/second at 40 concurrent clients.

Multi-hop traversal became progressively more expensive as the traversal depth increased, with 3-hop traversal showing the highest latency.

## Notes

- Benchmark was executed using the CognoDB cloud database.
- Results may vary depending on network conditions and database availability.
- The benchmark is intended to provide a baseline for evaluating graph database performance.