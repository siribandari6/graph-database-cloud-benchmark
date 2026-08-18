# Neo4j Benchmark Results

## Database

- Database: Neo4j
- Dataset: ca-HepPh sample
- Nodes: 9,904
- Relationships: 100,000

## Benchmark Results

| Metric | P50 (ms) | P95 (ms) |
|---|---:|---:|
| 1-Hop Traversal | 18.98 | 146.22 |
| 2-Hop Traversal | 28.29 | 69.98 |
| 3-Hop Traversal | 15.88 | 31.73 |
| Point Lookup by ID | 10.44 | 18.19 |
| Filtered Lookup | 9.78 | 16.35 |
| Count Aggregation | 5.87 | 12.00 |
| Relationship Count Aggregation | 8.79 | 22.07 |

## Load Results

- Relationships loaded: 100,000
- Load time: 602.33 seconds
- Relationships/second: 166.02

## Summary

The Neo4j benchmark completed successfully. Point lookups, filtered lookups, and aggregation queries showed low median latency, while traversal workloads showed higher latency depending on traversal depth.
