import os
import time
import statistics

from neo4j import GraphDatabase


NEO4J_URI = "bolt://127.0.0.1:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

ITERATIONS = 100


def percentile(values, p):
    values = sorted(values)
    index = int(len(values) * p / 100)

    if index >= len(values):
        index = len(values) - 1

    return values[index]


def run_query(driver, query, parameters=None):

    start = time.perf_counter()

    driver.execute_query(
        query,
        parameters or {}
    )

    end = time.perf_counter()

    return (end - start) * 1000


def benchmark(driver, name, query, parameters=None):

    print()
    print(f"Running: {name}")

    times = []

    # Warm-up
    for _ in range(10):
        run_query(driver, query, parameters)

    # Actual benchmark
    for i in range(ITERATIONS):

        latency = run_query(
            driver,
            query,
            parameters
        )

        times.append(latency)

        if (i + 1) % 25 == 0:
            print(f"Completed {i + 1}/{ITERATIONS}")

    average = statistics.mean(times)
    p50 = percentile(times, 50)
    p95 = percentile(times, 95)
    minimum = min(times)
    maximum = max(times)

    print()
    print(f"{name}")
    print(f"Average: {average:.2f} ms")
    print(f"P50:     {p50:.2f} ms")
    print(f"P95:     {p95:.2f} ms")
    print(f"Min:     {minimum:.2f} ms")
    print(f"Max:     {maximum:.2f} ms")

    return {
        "name": name,
        "average": average,
        "p50": p50,
        "p95": p95,
        "min": minimum,
        "max": maximum,
    }


def main():

    if not NEO4J_PASSWORD:
        raise ValueError(
            "NEO4J_PASSWORD is not configured."
        )

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(
            NEO4J_USERNAME,
            NEO4J_PASSWORD
        )
    )

    driver.verify_connectivity()

    print("Neo4j connection successful!")

    results = []

    # -----------------------------
    # 1-Hop Traversal
    # -----------------------------

    results.append(
        benchmark(
            driver,
            "1-Hop Traversal",
            """
            MATCH (a:Paper)-[:CITES]->(b:Paper)
            RETURN a.id, b.id
            LIMIT 100
            """
        )
    )

    # -----------------------------
    # 2-Hop Traversal
    # -----------------------------

    results.append(
        benchmark(
            driver,
            "2-Hop Traversal",
            """
            MATCH (a:Paper)-[:CITES]->()-[:CITES]->(c:Paper)
            RETURN a.id, c.id
            LIMIT 100
            """
        )
    )

    # -----------------------------
    # 3-Hop Traversal
    # -----------------------------

    results.append(
        benchmark(
            driver,
            "3-Hop Traversal",
            """
            MATCH (a:Paper)
                  -[:CITES]->
                  ()
                  -[:CITES]->
                  ()
                  -[:CITES]->
                  (d:Paper)
            RETURN a.id, d.id
            LIMIT 100
            """
        )
    )

    # -----------------------------
    # Point Lookup
    # -----------------------------

    results.append(
        benchmark(
            driver,
            "Point Lookup by ID",
            """
            MATCH (n:Paper {id: 10199})
            RETURN n
            """
        )
    )

    # -----------------------------
    # Filtered Lookup
    # -----------------------------

    results.append(
        benchmark(
            driver,
            "Filtered Lookup",
            """
            MATCH (n:Paper)
            WHERE n.id > 50000
            RETURN n.id
            LIMIT 100
            """
        )
    )

    # -----------------------------
    # Count Aggregation
    # -----------------------------

    results.append(
        benchmark(
            driver,
            "Count Aggregation",
            """
            MATCH (n:Paper)
            RETURN count(n) AS count
            """
        )
    )

    # -----------------------------
    # Relationship Count
    # -----------------------------

    results.append(
        benchmark(
            driver,
            "Relationship Count Aggregation",
            """
            MATCH ()-[r:CITES]->()
            RETURN count(r) AS count
            """
        )
    )

    driver.close()

    # -----------------------------
    # Final Results
    # -----------------------------

    print()
    print("=" * 70)
    print("FINAL NEO4J BENCHMARK RESULTS")
    print("=" * 70)

    print(
        f"{'Metric':35}"
        f"{'P50 (ms)':>12}"
        f"{'P95 (ms)':>12}"
    )

    print("-" * 70)

    for result in results:

        print(
            f"{result['name']:35}"
            f"{result['p50']:12.2f}"
            f"{result['p95']:12.2f}"
        )

    print()
    print("Benchmark completed successfully.")


if __name__ == "__main__":
    main()