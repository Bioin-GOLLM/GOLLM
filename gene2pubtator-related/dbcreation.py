import sqlite3
import os

# Input file (uncompressed gene2pubtator3)
INPUT_FILE = "gene2pubtator3"

# SQLite database file
DB_FILE = "gene2pubtator3_all.sqlite"

def main():
    # If you want a fresh database, remove any existing file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    # Connect to (or create) the SQLite database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create a table for storing gene data
    cursor.execute("""
        CREATE TABLE gene_data (
            pmid TEXT,
            gene_id TEXT,
            gene_text TEXT
        )
    """)
    
    lines_inserted = 0
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip empty or comment lines
            if not line or line.startswith("#"):
                continue
            
            cols = line.split("\t")
            if len(cols) < 4:
                continue
            
            pmid = cols[0]
            gene_id = cols[2]
            gene_text = cols[3]
            
            # Insert into the table
            cursor.execute("""
                INSERT INTO gene_data (pmid, gene_id, gene_text)
                VALUES (?, ?, ?)
            """, (pmid, gene_id, gene_text))
            
            lines_inserted += 1
            
            # OPTIONAL: commit in batches to improve performance
            if lines_inserted % 10000 == 0:
                conn.commit()
                print(f"{lines_inserted} lines inserted so far...")
                # break
    
    # Final commit to ensure all changes are saved
    conn.commit()
    conn.close()
    
    print(f"Finished inserting {lines_inserted} lines into '{DB_FILE}'.")

if __name__ == "__main__":
    main()
