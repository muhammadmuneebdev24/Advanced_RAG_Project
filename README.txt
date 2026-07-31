# PDF RAG Chatbot

## Overview

This project is a Retrieval-Augmented Generation (RAG) based PDF Chatbot built using Python.

It allows users to ask questions from one or multiple PDF documents. The system retrieves the most relevant information from the documents and uses a Large Language Model (LLM) to generate accurate answers along with source references.

---

# Features

- Supports single or multiple PDF documents
- Automatically loads every PDF from a folder
- Detects document headings
- Splits PDFs into meaningful text chunks
- Attaches section headings to every chunk
- Generates embeddings for all chunks
- Stores embeddings in a FAISS vector database
- Retrieves the most relevant chunks using semantic search
- Re-ranks retrieved chunks using a Cross Encoder
- Dynamically filters irrelevant chunks
- Uses Groq LLM for final answer generation
- Displays source file, page number and heading for every answer

---

# Project Workflow

The complete workflow is:

1. Load all PDF files from the data folder.
2. Extract text from every PDF.
3. Detect document headings using PyMuPDF.
4. Split the document into text chunks.
5. Attach the nearest heading to every chunk.
6. Generate embeddings for each chunk.
7. Store all embeddings in FAISS.
8. User asks a question.
9. Retrieve top matching chunks.
10. Re-rank retrieved chunks using Cross Encoder.
11. Dynamically filter less relevant chunks.
12. Send filtered chunks to the Groq LLM.
13. Generate the final answer.
14. Display answer with references.

---

# Technologies Used

## Programming Language

- Python

## LLM

- Groq
- Llama 3.3 70B Versatile

## Embedding Model

- Sentence Transformers

## Re-ranker

- Cross Encoder
- ms-marco-MiniLM-L6-v2

## Vector Database

- FAISS

## PDF Processing

- PyPDF
- PyMuPDF

## Frameworks

- LangChain
- LangChain Community
- LangChain Text Splitters

---

# Folder Structure

```
project/
│
├── data/
│     ├── PDF1.pdf
│     ├── PDF2.pdf
│     └── ...
│
├── faiss_index/
│
├── source/
│     ├── loader.py
│     ├── splitter.py
│     ├── heading_detector.py
│     ├── attach_heading.py
│     ├── embeddings.py
│     ├── vector_database.py
│     ├── retriever.py
│     ├── reranker.py
│     ├── chunk_filter.py
│     ├── citation_ids.py
│     └── llm.py
│
├── create_db.py
├── main.py
├── requirements.txt
└── README.md
```

---

# Installation

Create a virtual environment.

```
python -m venv venv
```

Activate it.

Windows

```
venv\Scripts\activate
```

Install all required libraries.

```
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

Example:

```
GROQ_API_KEY=your_api_key_here
```

---

# Creating the Vector Database

Place all PDF files inside the `data` folder.

Run:

```
python create_db.py
```

This will:

- Load every PDF
- Detect headings
- Split into chunks
- Attach headings
- Generate embeddings
- Create the FAISS database

---

# Running the Chatbot

Run:

```
python main.py
```

Example:

```
Ask your question:

What is a digital wallet?
```

The chatbot retrieves relevant chunks and generates an answer with references.

---

# Output Example

```
Answer

Digital wallets are linked to a card or bank account...

Sources

Heading:
Choosing the right payment methods for your business

File:
Stripe.pdf

Page:
4/33
```

---

# Retrieval Pipeline

```
Question
      │
      ▼
Semantic Retrieval (FAISS)
      │
      ▼
Top Retrieved Chunks
      │
      ▼
Cross Encoder Re-ranking
      │
      ▼
Dynamic Chunk Filtering
      │
      ▼
Groq LLM
      │
      ▼
Final Answer + References
```

---

# Heading Detection

The project automatically detects document headings by analyzing:

- Font size
- Bold text
- Text position
- Page number

The detected heading is attached to every chunk so that retrieved answers include meaningful section names.

---

# Dynamic Chunk Filtering

Instead of sending every retrieved chunk to the LLM, the project:

- Retrieves top matching chunks
- Re-ranks them using a Cross Encoder
- Dynamically filters irrelevant chunks
- Sends only the most relevant chunks to the LLM

This improves answer quality and reduces unnecessary context.

---

# Current Features

- PDF loading
- Multiple PDF support
- Automatic heading detection
- Heading attachment
- Semantic search
- Cross Encoder re-ranking
- Dynamic chunk filtering
- FAISS vector database
- Source citations
- Groq LLM integration

---

# Future Improvements

- Better heading assignment for chunks spanning multiple sections
- Table extraction support
- Image extraction support
- Hybrid (keyword + vector) search
- Metadata-based filtering
- Streaming responses
- Web interface
- Conversation memory
- Support for DOCX and TXT documents

---

# Author

Developed as a Python RAG-based PDF Question Answering System using LangChain, FAISS, Sentence Transformers, Cross Encoder Re-ranking, and Groq LLM.