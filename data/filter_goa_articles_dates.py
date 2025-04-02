import re
import requests
import xml.etree.ElementTree as ET

def filter_pmid_dates(input_text):
    filtered_lines = []
    for line in input_text.strip().split('\n'):
        parts = re.split(r'\s+', line)  # Split by any whitespace (tab or space)
        if len(parts) == 2:
            pmid, date = parts
            year = date[:4]  # Extract the year
            if '1999' <= year <= '2001':
                pmcid = pmid_to_pmcid(pmid) or "N/A"  # Convert PMID to PMCID or use N/A if not found
                filtered_lines.append(f"{pmcid}\t{date}")
    
    return '\n'.join(filtered_lines)


def pmid_to_pmcid(pmid):
    """
    Convert a PMID to PMCID using NCBI's idconv utility.
    Returns None if conversion fails.
    """
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={pmid}&format=xml"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None

    root = ET.fromstring(resp.text)
    # The API returns a record element with attributes:
    record = root.find("record")
    if record is not None:
        return record.attrib.get("pmcid")
    return None

# Read input from a file and save the results to another file
if __name__ == "__main__":
    input_file = "/Users/crystalcho/Downloads/pmids.txt"
    output_file = "/Users/crystalcho/Downloads/filtered_pmids(1999-2001).txt"
    
    with open(input_file, "r", encoding="utf-8") as file:
        dataset = file.read()
    
    result = filter_pmid_dates(dataset)
    
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(result)
    
    print(f"Filtered results saved to {output_file}")