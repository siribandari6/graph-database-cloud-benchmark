import gzip

SOURCE = "data/raw/ca-HepPh.txt.gz"
OUTPUT = "data/raw/ca-HepPh_sample.txt.gz"
LIMIT = 100_000

count = 0

with gzip.open(SOURCE, "rt", encoding="utf-8") as source:
    with gzip.open(OUTPUT, "wt", encoding="utf-8") as output:

        for line in source:
            if line.startswith("#") or not line.strip():
                continue

            output.write(line)
            count += 1

            if count >= LIMIT:
                break

print(f"Created {OUTPUT}")
print(f"Relationships: {count:,}")