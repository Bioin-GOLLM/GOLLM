import json

input_file = "gene2pubtator3"  # Update with your actual input file name
output_file = "gene2pubtator3_all.json"
line_number = 0
with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    outfile.write("{\n")
    current_pmid = None
    current_genes = []
    first_entry = True

    for line_number, line in enumerate(infile, start=1):
        # Strip newline characters and split by tab
        parts = line.strip().split("\t")
        
        # Ensure the line has at least 4 columns
        if len(parts) < 4:
            print(f"Skipping malformed line {line_number}: {line.strip()}")
            continue
        
        pmid = parts[0]
        # parts[1] is "Gene", which we ignore
        gene_id = parts[2]
        gene_text = parts[3]
        
        # Split synonyms by '|'
        synonyms = gene_text.split("|")
        
        gene_entry = {
            "gene_id": gene_id,
            "synonyms": synonyms
        }

        if pmid != current_pmid:
            if current_pmid is not None:
                if not first_entry:
                    outfile.write(",\n")
                else:
                    first_entry = False
                # Write the previous pmid group
                json_record = json.dumps(current_genes, indent=2)
                outfile.write(f'  "{current_pmid}": {json_record}')
            # Start new group
            current_pmid = pmid
            current_genes = []

        current_genes.append(gene_entry)

        # Optional: Print progress every 1,000,000 lines
        if line_number % 1_000_000 == 0:
            print(f"Processed {line_number} lines")

    # Write the last pmid group
    if current_pmid is not None:
        if not first_entry:
            outfile.write(",\n")
        json_record = json.dumps(current_genes, indent=2)
        outfile.write(f'  "{current_pmid}": {json_record}\n')

    outfile.write("}\n")

print("JSON conversion completed successfully. ", line_number, "lines processed.")