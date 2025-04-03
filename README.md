# GOLLM
A pipeline to identify proteins and extract Gene Ontology terms from PubMed literature using an LLM, demonstrating its potential to replace human annotators by evaluating model performance.

This project implements a complete pipeline for processing gene-related data from research articles. The pipeline extracts gene annotations from XML files, generates Gene Ontology (GO) term predictions using a Llama-based language model, matches these predictions with official GO terms using semantic similarity from SAPBERT embeddings, and compares the final annotations against NCBI Gene records. In short, it bridges automated text mining with curated GO annotations for improved gene functional analysis.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [License](#license)

---

## Features

- **XML Parsing**: Extracts gene annotations and context snippets from article XML files.
- **NCBI Gene Integration**: Fetches and updates gene information (symbol, organism, full name, aliases) using NCBI Entrez.
- **Prompt Generation for Llama**: Constructs detailed prompts for Llama-3.3 to generate candidate GO terms based on in-text gene occurrences.
- **Inference Storage**: Organizes and saves individual gene inferences in temporary directories and merges them into a final JSON file.
- **GO Term Embedding & Matching**:  
  - Loads GO terms from a local `go.obo` file using `obonet`.  
  - Uses SAPBERT (via SentenceTransformer) to embed GO term names.  
  - Matches Llama-generated GO term predictions with official GO terms based on cosine similarity.
- **Annotation Replacement & Processing**: Replaces Llama predictions with matched official GO term metadata.
- **NCBI GO Annotation Comparison**:  
  - Fetches GO annotations from NCBI Gene records (in XML).  
  - Computes semantic similarities between local annotations and NCBI GO terms.  
  - Classifies matches as True Positive (TP), Novel Positive (NP), Database Confirmed but Unreferenced (DCU), or Not Detected (ND).
- **Reporting & Summary**: Outputs per-gene and global summaries of the annotation classification.

---

## Project Structure

├─ README.md # Project documentation\
├─ data # folder for data preprocessing\
├─ \
└─ go.obo # Local Gene Ontology file

---

## Installation

Download the Gene Ontology file:

Ensure that go.obo is available at the path specified in the code (or update the path accordingly).

---

## License
This project is licensed under the MIT License.
