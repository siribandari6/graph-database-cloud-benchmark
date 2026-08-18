import gzip
import os
import time
from pathlib import Path

from neo4j import GraphDatabase


# -----------------------------
# Configuration
# -----------------------------

NEO4J_URI = "bolt://127.0.0.1:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

DATASET_PATH = Path("data/raw/ca-HepPh_sample.txt.gz")

BATCH_SIZE = 1000


# -----------------------------
# Parse dataset
# -----------------------------

def read_relationships():
    relationships = []

    with gzip.open(DATASET_PATH, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) >= 2:
                source = int(parts[0])
                target = int(parts[1])

                relationships.append((source, target))

    return relationships


# -----------------------------
# Load into Neo4j
# -----------------------------

def load_data(driver, relationships):

    query = """
    UNWIND $relationships AS rel
    MERGE (a:Paper {id: rel.source})
    MERGE (b:Paper {id: rel.target})
    MERGE (a)-[:CITES]->(b)
    """

    total = len(relationships)

    for start in range(0, total, BATCH_SIZE):

        batch = relationships[start:start + BATCH_SIZE]

        driver.execute_query(
            query,
            relationships=[
                {"source": source, "target": target}
                for source, target in batch
            ]
        )

        loaded = min(start + BATCH_SIZE, total)

        print(f"Loaded {loaded:,} / {total:,} relationships")


# -----------------------------
# Main
# -----------------------------

def main():

    if not NEO4J_PASSWORD:
        raise ValueError(
            "NEO4J_PASSWORD environment variable is not set."
        )

    print("Reading dataset...")

    relationships = read_relationships()

    print(f"Dataset relationships: {len(relationships):,}")

    print("Connecting to Neo4j...")

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    driver.verify_connectivity()

    print("Neo4j connection successful!")

    # Clear previous benchmark data
    print("Clearing existing benchmark data...")

    driver.execute_query(
        "MATCH (n:Paper) DETACH DELETE n"
    )

    start_time = time.time()

    print("Loading dataset into Neo4j...")

    load_data(driver, relationships)

    elapsed = time.time() - start_time

    print()
    print("=" * 50)
    print("LOAD RESULTS")
    print("=" * 50)

    print(f"Relationships loaded: {len(relationships):,}")
    print(f"Load time: {elapsed:.2f} seconds")

    if elapsed > 0:
        print(
            f"Relationships/second: "
            f"{len(relationships) / elapsed:.2f}"
        )

    # Verify database counts
    records, _, _ = driver.execute_query(
        "MATCH (n:Paper) RETURN count(n) AS count"
    )

    node_count = records[0]["count"]

    records, _, _ = driver.execute_query(
        "MATCH ()-[r:CITES]->() RETURN count(r) AS count"
    )

    relationship_count = records[0]["count"]

    print()
    print("=" * 50)
    print("DATABASE COUNTS")
    print("=" * 50)

    print(f"Nodes: {node_count:,}")
    print(f"Relationships: {relationship_count:,}")

    driver.close()

    print()
    print("Neo4j connection closed.")


if __name__ == "__main__":
    main()