import gzip
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase


# Load environment variables
load_dotenv()

COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")

DATASET_PATH = Path("data/raw/ca-HepPh_sample.txt.gz")

BATCH_SIZE = 1000


def load_edges():
    """Read edges from the compressed ca-HepPh dataset."""

    edges = []

    with gzip.open(DATASET_PATH, "rt", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) >= 2:
                source = int(parts[0])
                target = int(parts[1])
                edges.append((source, target))

    return edges


def create_database_driver():
    """Create and return the CognoDB driver."""

    driver = GraphDatabase.driver(
        COGNODB_URI,
        auth=(COGNODB_USERNAME, COGNODB_PASSWORD)
    )

    driver.verify_connectivity()

    return driver


def clear_database(driver):
    """Delete existing benchmark data."""

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n").consume()


def create_indexes(driver):
    """Create indexes used by the benchmark."""

    with driver.session() as session:
        session.run(
            """
            CREATE INDEX person_id_index IF NOT EXISTS
            FOR (p:Person)
            ON (p.id)
            """
        ).consume()


def insert_batch(tx, batch):
    """Insert one batch of graph relationships."""

    tx.run(
        """
        UNWIND $edges AS edge

        MERGE (a:Person {id: edge.source})
        MERGE (b:Person {id: edge.target})

        MERGE (a)-[:COAUTHOR]->(b)
        """,
        edges=[
            {"source": source, "target": target}
            for source, target in batch
        ],
    ).consume()


def load_into_cognodb(driver, edges):
    """Load the complete dataset into CognoDB and measure throughput."""

    start_time = time.perf_counter()

    with driver.session() as session:

        for i in range(0, len(edges), BATCH_SIZE):

            batch = edges[i:i + BATCH_SIZE]

            session.execute_write(insert_batch, batch)

            if (i // BATCH_SIZE) % 50 == 0:
                print(
                    f"Loaded {min(i + BATCH_SIZE, len(edges)):,} "
                    f"/ {len(edges):,} relationships"
                )

    elapsed = time.perf_counter() - start_time

    relationships_per_second = len(edges) / elapsed

    return elapsed, relationships_per_second


def get_counts(driver):
    """Return node and relationship counts."""

    with driver.session() as session:

        node_result = session.run(
            "MATCH (p:Person) RETURN count(p) AS count"
        ).single()

        relationship_result = session.run(
            """
            MATCH ()-[r:COAUTHOR]->()
            RETURN count(r) AS count
            """
        ).single()

    return node_result["count"], relationship_result["count"]


def main():

    print("Reading dataset...")

    edges = load_edges()

    print(f"Dataset relationships: {len(edges):,}")

    print("Connecting to CognoDB...")

    driver = create_database_driver()

    print("CognoDB connection successful!")

    try:

        print("Clearing existing benchmark data...")
        clear_database(driver)

        print("Creating index...")
        create_indexes(driver)

        print("Loading dataset into CognoDB...")

        elapsed, relationships_per_second = load_into_cognodb(
            driver,
            edges
        )

        print()
        print("========== LOAD RESULTS ==========")
        print(f"Relationships loaded: {len(edges):,}")
        print(f"Load time: {elapsed:.2f} seconds")
        print(f"Relationships/second: {relationships_per_second:,.2f}")

        nodes, relationships = get_counts(driver)

        print()
        print("========== DATABASE COUNTS ==========")
        print(f"Nodes: {nodes:,}")
        print(f"Relationships: {relationships:,}")

    finally:

        driver.close()

        print()
        print("CognoDB connection closed.")


if __name__ == "__main__":
    main()