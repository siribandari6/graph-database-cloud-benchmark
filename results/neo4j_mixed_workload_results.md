# Neo4j Mixed Read/Write Benchmark Results

## Configuration

- Database: Neo4j
- Dataset: 9,904 nodes
- Relationships: 100,000
- Workload: 70% reads, 30% writes
- Operations per client: 20
- Concurrency levels: 1, 10, 40 clients

## Results

| Clients | Throughput (queries/sec) | P50 (ms) | P95 (ms) |
|---:|---:|---:|---:|
| 1 | 46.15 | 6.36 | 72.76 |
| 10 | 838.92 | 9.95 | 20.07 |
| 40 | 835.60 | 47.87 | 75.52 |

## Analysis

At single-client concurrency, the workload achieved 46.15 queries/sec with a median latency of 6.36 ms.

Increasing concurrency to 10 clients significantly improved throughput to 838.92 queries/sec while maintaining a relatively low P50 latency of 9.95 ms.

At 40 clients, throughput remained stable at 835.60 queries/sec, indicating that the benchmark reached a throughput plateau. However, P50 latency increased to 47.87 ms and P95 latency increased to 75.52 ms, showing increased contention under higher concurrency.

## Conclusion

Neo4j demonstrated strong throughput scaling from 1 to 10 concurrent clients. Beyond 10 clients, throughput remained approximately stable while latency increased, suggesting that the local benchmark environment reaches its practical throughput limit around this workload level.