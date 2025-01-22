Assumptions: You have gene2pubtator3 from https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTator3/

converttojson.py : Took around 2-5 hr
- takes in gene2pubtator and outputs the 6GB JSON with the following structure:
```
{
"PMID1": [{GENEID, SYNONYMS[]},{GENEID, SYNONYMS},...]
"PMID2": [{GENEID, SYNONYMS},{GENEID, SYNONYMS},..]
} 

where synonyms is a list of gene names that mean the same thing.
```

count_and_list_pmids_ijson.py: took 1-5 mins
- uses the output JSON from the .py above (to use the JSON's top-level PMIDS and counts them) 
- outputs a pmids.txt (which ive sent you)

OPTIONAL (these are not really needed, the db might be useful tho)
dbcreation.py: 2hr - 5hr
- uses gene2pubtator3 to create a sqlite db version of it. I excluded some of the columns to make it a bit smaller
dbtojson_extra.py
- uses the db above to create a jsonl that is similar to gene2pubtator3 file without some of the columns
