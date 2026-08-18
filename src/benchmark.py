import os
import random
import statistics
import time

from dotenv import load_dotenv
from neo4j import GraphDatabase


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")

WARMUP_ITERATIONS = 10
BENCHMARK_ITERATIONS = 100


# ============================================================
# DATABASE CONNECTION
# ============================================================

def create_driver():
    driver = GraphDatabase.driver(
        COGNODB_URI,
        auth=(COGNODB_USERNAME, COGNODB_PASSWORD)
    )

    driver.verify_connectivity()

    return driver


# ============================================================
# PERCENTILE CALCULATION
# ============================================================

def percentile(values, percentile_value):
    values = sorted(values)

    if not values:
        return 0.0

    index = (len(values) - 1) * percentile_value / 100

    lower = int(index)
    upper = min(lower + 1, len(values) - 1)

    if lower == upper:
        return values[lower]

    weight = index - lower

    return (
        values[lower] * (1 - weight)
        + values[upper] * weight
    )


# ============================================================
# QUERY EXECUTION
# ============================================================

def execute_query(session, query, parameters=None):

    start = time.perf_counter()

    result = session.run(
        query,
        parameters or {}
    )

    result.consume()

    end = time.perf_counter()

    return (end - start) * 1000


# ============================================================
# BENCHMARK RUNNER
# ============================================================

def run_benchmark(
    session,
    name,
    query,
    parameters=None
):

    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    # --------------------------------------------------------
    # Warm-up
    # --------------------------------------------------------

    print(
        f"Warm-up: {WARMUP_ITERATIONS} iterations..."
    )

    for _ in range(WARMUP_ITERATIONS):

        execute_query(
            session,
            query,
            parameters
        )

    # --------------------------------------------------------
    # Measurement
    # --------------------------------------------------------

    print(
        f"Benchmark: {BENCHMARK_ITERATIONS} iterations..."
    )

    latencies = []

    for i in range(BENCHMARK_ITERATIONS):

        latency = execute_query(
            session,
            query,
            parameters
        )

        latencies.append(latency)

        if (i + 1) % 25 == 0:

            print(
                f"  Completed {i + 1}/"
                f"{BENCHMARK_ITERATIONS}"
            )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    average = statistics.mean(latencies)

    p50 = percentile(
        latencies,
        50
    )

    p95 = percentile(
        latencies,
        95
    )

    minimum = min(latencies)

    maximum = max(latencies)

    print()
    print(f"Average: {average:.2f} ms")
    print(f"P50:     {p50:.2f} ms")
    print(f"P95:     {p95:.2f} ms")
    print(f"Min:     {minimum:.2f} ms")
    print(f"Max:     {maximum:.2f} ms")

    return {
        "metric": name,
        "average_ms": average,
        "p50_ms": p50,
        "p95_ms": p95,
        "min_ms": minimum,
        "max_ms": maximum,
    }


# ============================================================
# GET RANDOM START NODE
# ============================================================

def get_random_node(session):

    result = session.run(
        """
        MATCH (p:Person)
        RETURN p.id AS id
        LIMIT 1000
        """
    )

    node_ids = [
        record["id"]
        for record in result
    ]

    if not node_ids:

        raise RuntimeError(
            "No Person nodes found in CognoDB."
        )

    return random.choice(node_ids)


# ============================================================
# MAIN BENCHMARK
# ============================================================

def main():

    print()
    print("=" * 60)
    print("COGNODB GRAPH DATABASE BENCHMARK")
    print("=" * 60)

    print()
    print("Connecting to CognoDB...")

    driver = create_driver()

    print("Connection successful!")

    results = []

    try:

        with driver.session() as session:

            # ------------------------------------------------
            # Database counts
            # ------------------------------------------------

            print()
            print("Checking database...")

            count_result = session.run(
                """
                MATCH (p:Person)
                RETURN count(p) AS nodes
                """
            ).single()

            relationship_result = session.run(
                """
                MATCH ()-[r:COAUTHOR]->()
                RETURN count(r) AS relationships
                """
            ).single()

            nodes = count_result["nodes"]

            relationships = relationship_result[
                "relationships"
            ]

            print(f"Nodes:         {nodes:,}")
            print(f"Relationships: {relationships:,}")

            # ------------------------------------------------
            # Random start node
            # ------------------------------------------------

            start_node = get_random_node(
                session
            )

            print()
            print(
                f"Random start node: {start_node}"
            )

            # ------------------------------------------------
            # 1-HOP TRAVERSAL
            # ------------------------------------------------

            results.append(
                run_benchmark(
                    session,

                    "1-Hop Traversal",

                    """
                    MATCH (
                        p:Person {id: $node_id}
                    )-[:COAUTHOR]->(neighbor)
                    RETURN neighbor.id
                    """,

                    {
                        "node_id": start_node
                    }
                )
            )

            # ------------------------------------------------
            # 2-HOP TRAVERSAL
            # ------------------------------------------------

            results.append(
                run_benchmark(
                    session,

                    "2-Hop Traversal",

                    """
                    MATCH (
                        p:Person {id: $node_id}
                    )-[:COAUTHOR*2]->(neighbor)
                    RETURN neighbor.id
                    """,

                    {
                        "node_id": start_node
                    }
                )
            )

            # ------------------------------------------------
            # 3-HOP TRAVERSAL
            # ------------------------------------------------

            results.append(
                run_benchmark(
                    session,

                    "3-Hop Traversal",

                    """
                    MATCH (
                        p:Person {id: $node_id}
                    )-[:COAUTHOR*3]->(neighbor)
                    RETURN neighbor.id
                    """,

                    {
                        "node_id": start_node
                    }
                )
            )

            # ------------------------------------------------
            # POINT LOOKUP
            # ------------------------------------------------

            results.append(
                run_benchmark(
                    session,

                    "Point Lookup by ID",

                    """
                    MATCH (p:Person {id: $node_id})
                    RETURN p.id
                    """,

                    {
                        "node_id": start_node
                    }
                )
            )

            # ------------------------------------------------
            # FILTERED LOOKUP
            # ------------------------------------------------

            results.append(
                run_benchmark(
                    session,

                    "Filtered Lookup",

                    """
                    MATCH (p:Person)
                    WHERE p.id >= $lower
                      AND p.id < $upper
                    RETURN p.id
                    LIMIT 100
                    """,

                    {
                        "lower": start_node,
                        "upper": start_node + 100
                    }
                )
            )

            # ------------------------------------------------
            # AGGREGATION
            # ------------------------------------------------

            results.append(
                run_benchmark(
                    session,

                    "Count Aggregation",

                    """
                    MATCH (p:Person)
                    RETURN count(p)
                    """
                )
            )

            # ------------------------------------------------
            # RELATIONSHIP AGGREGATION
            # ------------------------------------------------

            results.append(
                run_benchmark(
                    session,

                    "Relationship Count Aggregation",

                    """
                    MATCH ()-[r:COAUTHOR]->()
                    RETURN count(r)
                    """
                )
            )

    finally:

        driver.close()

        print()
        print("CognoDB connection closed.")

    # ========================================================
    # FINAL RESULTS
    # ========================================================

    print()
    print()
    print("=" * 70)
    print("FINAL BENCHMARK RESULTS")
    print("=" * 70)

    print()

    print(
        f"{'Metric':<35}"
        f"{'P50 (ms)':>12}"
        f"{'P95 (ms)':>12}"
    )

    print("-" * 70)

    for result in results:

        print(
            f"{result['metric']:<35}"
            f"{result['p50_ms']:>12.2f}"
            f"{result['p95_ms']:>12.2f}"
        )

    print()
    print("Benchmark completed successfully.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()