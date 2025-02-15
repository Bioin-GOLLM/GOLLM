import xml.etree.ElementTree as ET
from Bio import Entrez
import re
import time

# Set your email (and API key if available)
Entrez.email = "email here"
# Entrez.api_key = "your_api_key"

class Gene:
    def __init__(self, gene_id):
        self.gene_id = gene_id
        self.occurrences = []  # list to store snippet(s) where the gene was mentioned
        self.symbol = None
        self.organism = None
        self.full_name = None
        self.also_known_as = None
        self.name_from_article = None

    def add_occurrence(self, snippet):
        if snippet not in self.occurrences:  # Avoid duplicates
            self.occurrences.append(snippet)

    def set_name_from_article(self, name_from_article):
        """Sets the temporary name of the gene. This is the name accroding to the article"""
        # will be used if the official name is not available
        self.name_from_article = name_from_article

    def get_name_from_article(self):
        return self.name_from_article

    def get_occurrences(self):
        return self.occurrences

    def get_also_known_as(self):
        return self.also_known_as

    def update_info(self, symbol, organism, full_name, also_known_as):
        self.symbol = symbol
        self.organism = organism
        self.full_name = full_name
        self.also_known_as = also_known_as

    def __repr__(self):
        return (f"Gene({self.gene_id})\n"
                f"  Symbol          : {self.symbol}\n"
                f"  Organism        : {self.organism}\n"
                f"  Full Name       : {self.full_name}\n"
                f"  Also Known As   : {self.also_known_as}\n"
                f"  In-text Name    : {self.name_from_article}\n"
                f"  Occurrences     : {self.occurrences}")   # occurrences is a list of 3-sentence snippets
def parse_xml_file(xml_path):
    """Parses the XML file and returns a gene dictionary keyed by gene ID."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    gene_dict = {}

    for document in root.findall('document'):
        for passage in document.findall('passage'):
            # Get the full passage text.
            passage_text_elem = passage.find("text")
            passage_text = passage_text_elem.text if passage_text_elem is not None else ""
            # determine the starting offset for this passage.
            passage_offset_elem = passage.find("offset")
            passage_offset = int(passage_offset_elem.text) if passage_offset_elem is not None else 0
            # Split the passage into sentences using regex.
            sentences = re.split(r'(?<=[.!?])\s+', passage_text)
            # Compute start indices for each sentence within the passage text.
            start_indices = []
            current_index = passage_offset
            for sentence in sentences:
                start_indices.append(current_index)
                current_index += len(sentence) + 1  # account for the delimiter space

            processed_ranges = set()  # To track which sentences have already been covered

            # Process each annotation in the passage.
            for annotation in passage.findall('annotation'):
                ann_type = annotation.find("infon[@key='type']")
                if ann_type is not None and ann_type.text == "Gene":
                    gene_id_elem = annotation.find("infon[@key='identifier']")
                    gene_id = gene_id_elem.text if gene_id_elem is not None else None
                    
                    # Extract the gene name from the annotation text. (Temporary name if official name is not available)
                    in_text_gene_name_elem = annotation.find("text")
                    in_text_gene_name = in_text_gene_name_elem.text if in_text_gene_name_elem is not None else None

                    # Extract the annotation location (offset) to find the sentence containing the gene.
                    location_elem = annotation.find("location")
                    ann_offset = int(location_elem.attrib.get('offset', 0)) if location_elem is not None else 0

                    # Determine which sentence contains the annotation based on its offset.
                    sentence_index = None
                    for i, start in enumerate(start_indices):
                        if start <= ann_offset < start + len(sentences[i]):
                            sentence_index = i
                            break

                    if sentence_index is not None:
                        start_sentence = max(0, sentence_index - 1)  # one sentence before
                        end_sentence = min(len(sentences), sentence_index + 2)  # one sentence after
                        range_tuple = (start_sentence, end_sentence)
                        if range_tuple in processed_ranges:
                            continue  # Skip duplicate extractions
                        processed_ranges.add(range_tuple)
                        snippet = " ".join(sentences[start_sentence:end_sentence])
                        if gene_id:
                            if gene_id in gene_dict:
                                gene_dict[gene_id].add_occurrence(snippet)
                            else:
                                gene_obj = Gene(gene_id)
                                gene_obj.add_occurrence(snippet)
                                gene_obj.set_name_from_article(in_text_gene_name)       # Temporary name if official name is not available
                                gene_dict[gene_id] = gene_obj
    return gene_dict

def fetch_and_update_gene_info(gene_dict):
    """Retrieves gene information from NCBI and updates the genes in gene_dict."""
    gene_ids = list(gene_dict.keys())
    if gene_ids:
        # Post the gene IDs to NCBI.
        handle = Entrez.epost(db="gene", id=",".join(gene_ids))
        result = Entrez.read(handle)
        handle.close()

        webenv = result["WebEnv"]
        query_key = result["QueryKey"]

        handle = Entrez.esummary(db="gene", webenv=webenv, query_key=query_key)
        record = Entrez.read(handle)
        handle.close()

        for docsum in record["DocumentSummarySet"]["DocumentSummary"]:
            gene_id = docsum.attributes["uid"]
            symbol = docsum.get('NomenclatureSymbol', 'No symbol')
            organism = docsum.get('Organism', {}).get('ScientificName', 'No organism')
            full_name = docsum.get('NomenclatureName', gene_dict[gene_id].get_name_from_article())
            also_known_as = docsum.get('OtherAliases', gene_dict[gene_id].get_name_from_article())
            
            # if full name and also known as are not available, use the name from the article
            if (full_name == ''):
                full_name = gene_dict[gene_id].get_name_from_article()
            if (also_known_as == ''):
                also_known_as = gene_dict[gene_id].get_name_from_article()
            
            if gene_id in gene_dict:
                gene_dict[gene_id].update_info(symbol, organism, full_name, also_known_as)
            # Pause briefly to avoid overwhelming NCBI servers.
            time.sleep(0.5)

def main():
    xml_path = r"Llama3.2-3B-Instruct-Inference\input\full_text_annotated_example2.xml"
    gene_dict = parse_xml_file(xml_path)
    fetch_and_update_gene_info(gene_dict)
    # Output updated gene information.
    for gene in gene_dict.values():
        print(gene)

if __name__ == '__main__':
    main()