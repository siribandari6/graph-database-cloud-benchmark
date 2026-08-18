import os
import time
import random
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")


# Concurrency levels required for the benchmark
CONCURRENCY_LEVELS = [1, 10, 40]

# Number of operations per concurrency level
OPERATIONS_PER_CLIENT = 20


def create_driver():
    """Create Neo4j driver for CognoDB."""

    driver = GraphDatabase.driver(
        COGNODB_URI,
        auth=(COGNODB_USERNAME, COGNODB_PASSWORD),
        max_connection_pool_size=100
    )

    driver.verify_connectivity()

    return driver


def read_query(driver):
    """Execute a simple graph read."""

    start = time.perf_counter()

    with driver.session() as session:
        session.run(
            """
            MATCH (p:Person)
            RETURN p.id
            LIMIT 10
            """
        ).consume()

    return time.perf_counter() - start


def write_query(driver, worker_id):
    """Execute a small graph write."""

    start = time.perf_counter()

    node_id = random.randint(100000000, 999999999)

    with driver.session() as session:
        session.run(
            """
            MERGE (p:Person {id: $id})
            SET p.benchmark_worker = $worker
            """,
            id=node_id,
            worker=worker_id
        ).consume()

    return time.perf_counter() - start


def worker(driver, worker_id):
    """Perform a mixture of reads and writes."""

    latencies = []

    for i in range(OPERATIONS_PER_CLIENT):

        # 70% reads, 30% writes
        if random.random() < 0.7:
            latency = read_query(driver)
        else:
            latency = write_query(driver, worker_id)

        latencies.append(latency)

    return latencies


def percentile(values, percentile):
    """Calculate percentile latency."""

    values = sorted(values)

    index = (len(values) - 1) * percentile / 100

    lower = int(index)
    upper = min(lower + 1, len(values) - 1)

    weight = index - lower

    return values[lower] * (1 - weight) + values[upper] * weight


def run_concurrency_test(driver, clients):
    """Run benchmark at a specific concurrency level."""

    print()
    print("=" * 60)
    print(f"CONCURRENCY: {clients} CLIENTS")
    print("=" * 60)

    start = time.perf_counter()

    all_latencies = []

    with ThreadPoolExecutor(max_workers=clients) as executor:

        futures = [
            executor.submit(worker, driver, worker_id)
            for worker_id in range(clients)
        ]

        for future in as_completed(futures):
            all_latencies.extend(future.result())

    elapsed = time.perf_counter() - start

    total_operations = len(all_latencies)

    throughput = total_operations / elapsed

    p50 = percentile(all_latencies, 50) * 1000
    p95 = percentile(all_latencies, 95) * 1000

    print(f"Total operations : {total_operations}")
    print(f"Total time      : {elapsed:.2f} seconds")
    print(f"Throughput      : {throughput:.2f} queries/sec")
    print(f"P50 latency     : {p50:.2f} ms")
    print(f"P95 latency     : {p95:.2f} ms")

    return {
        "clients": clients,
        "operations": total_operations,
        "time": elapsed,
        "throughput": throughput,
        "p50": p50,
        "p95": p95,
    }


def main():

    print("=" * 60)
    print("CognoDB Mixed Read/Write Benchmark")
    print("=" * 60)

    driver = create_driver()

    print("\nCognoDB connection successful!")

    try:

        results = []

        for clients in CONCURRENCY_LEVELS:

            result = run_concurrency_test(
                driver,
                clients
            )

            results.append(result)

        print()
        print("=" * 60)
        print("FINAL MIXED WORKLOAD RESULTS")
        print("=" * 60)

        print(
            f"{'Clients':<10}"
            f"{'Throughput':<18}"
            f"{'P50 (ms)':<15}"
            f"{'P95 (ms)':<15}"
        )

        print("-" * 60)

        for result in results:

            print(
                f"{result['clients']:<10}"
                f"{result['throughput']:<18.2f}"
                f"{result['p50']:<15.2f}"
                f"{result['p95']:<15.2f}"
            )

    finally:

        driver.close()

        print("\nCognoDB connection closed.")


if __name__ == "__main__":
    main()