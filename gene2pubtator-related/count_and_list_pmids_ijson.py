import ijson

def count_pmids_with_progress_and_save(json_file_path, pmid_output_path):
    pmid_count = 0
    progress_interval = 1000000  # Adjust as needed

    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file, \
             open(pmid_output_path, 'w', encoding='utf-8') as pmid_file:
            
            for pmid, _ in ijson.kvitems(json_file, ''):
                pmid_count += 1
                pmid_file.write(f"{pmid}\n")  # Write pmid to the text file

                if pmid_count % progress_interval == 0:
                    print(f"Processed {pmid_count} pmids...")

    except FileNotFoundError:
        print(f"Error: The file {json_file_path} was not found.")
    except PermissionError:
        print(f"Error: Permission denied when accessing the file.")
    except ijson.JSONError as e:
        print(f"JSON parsing error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return pmid_count

def main():
    json_file_path = "gene2pubtator3_all.json"  # Path to your JSON file
    pmid_output_path = "pmids.txt"             # Path to the output text file

    print(f"Starting to process {json_file_path}...")
    pmid_count = count_pmids_with_progress_and_save(json_file_path, pmid_output_path)
    print(f"JSON processing completed.")
    print(f"Total pmids: {pmid_count}")
    print(f"All pmids have been saved to {pmid_output_path}")

if __name__ == "__main__":
    main()