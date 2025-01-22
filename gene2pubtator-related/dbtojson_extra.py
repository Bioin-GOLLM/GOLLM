import sqlite3
import json
from collections import defaultdict

conn = sqlite3.connect("gene2pubtator3_all.sqlite")
cursor = conn.cursor()

BATCH_SIZE = 10000
start = 0

with open("gene2pubtator3_all.jsonl", "w", encoding="utf-8") as out:
    while True:
        rows = cursor.execute(
            "SELECT pmid, gene_id, gene_text FROM gene_data LIMIT ? OFFSET ?",
            (BATCH_SIZE, start)
        ).fetchall()
        if not rows:
            break
        
        for pmid, gene_id, gene_text in rows:
            synonyms = gene_text.split("|")
            record = {
                "pmid": pmid,
                "gene_id": gene_id,
                "synonyms": synonyms
            }
            out.write(json.dumps(record) + "\n")
        
        start += len(rows)

conn.close()