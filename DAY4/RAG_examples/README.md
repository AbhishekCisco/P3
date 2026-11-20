# Embedding-Based Retrieval with Sentence Transformers and FAISS

## Overview

This short Python example retrieves the closest matching sentence from a tiny, hard-coded set of workplace-policy statements. It demonstrates the retrieval part of a retrieval-augmented generation (RAG) workflow, but it does not generate an answer with a language model.

## Learning Objectives

- Convert text into numerical embeddings with a pretrained sentence-transformer model.
- Store vectors in a FAISS similarity-search index.
- Embed a question and retrieve its nearest text item.
- Understand the difference between retrieval and the generation step in RAG.

## Topics Covered

- **Text embeddings:** `all-MiniLM-L6-v2` maps each sentence to a 384-dimensional vector intended to represent semantic similarity.
- **Vector search:** FAISS `IndexFlatL2` searches the stored vectors using squared Euclidean distance.
- **Top-k retrieval:** the script requests one neighbor (`k=1`) and prints the corresponding source sentence.
- **RAG boundaries:** the retrieved sentence is displayed directly; no generative model or answer synthesis is present.

## Project Structure

```text
RAG_examples/
├── rag_examples.py # Embedding, indexing, and nearest-neighbor retrieval
└── README.md
```

## How the Script Works

`rag_examples.py` defines two policy sentences, loads the pretrained model, and encodes the sentences into vectors. It adds those vectors to a 384-dimension FAISS index. The hard-coded question is encoded in the same vector space, and the index returns the closest stored document, which is printed as `Retrieved: ...`.

With the included question, the expected match is `Employees get 20 paid leaves per year`.

## Setup and Run

Use Python 3 and install the libraries used by the script:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install sentence-transformers faiss-cpu
python rag_examples.py
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`. The first run may download the model files, so it requires network access and enough disk space. There is no `requirements.txt` or test suite in this folder.

## Current Status and Limitations

- The document collection and question are hard-coded, with only two documents; this is a demonstration, not a practical knowledge base.
- The vector index exists only in memory and is rebuilt on every run.
- The code uses a fixed vector dimension of 384, which must match the selected embedding model.
- Search results are based on L2 distance and are not converted into a natural-language answer or checked for factual completeness.

## What to Study Next

Try additional documents and questions, inspect multiple nearest neighbors, and measure retrieval quality. A fuller RAG system would also pass retrieved context to a language model and verify that the generated response stays grounded in that context.