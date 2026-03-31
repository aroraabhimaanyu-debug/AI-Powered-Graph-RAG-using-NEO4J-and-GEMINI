# AI-Powered-Graph-RAG-using-NEO4J-and-GEMINI
An AI-driven Graph Retrieval-Augmented Generation (Graph RAG) system built using Python, Google Gemini, and Neo4j to transform unstructured textbook PDF content into a structured knowledge graph for improved information retrieval and semantic understanding.
Problem Solved

Traditional document search systems rely on keyword matching and often fail to capture relationships between concepts. This project addresses that by extracting entities and semantic relationships from textbook content and storing them in a graph database, enabling more contextual and relationship-aware retrieval.

My Contribution

I independently designed and built the end-to-end pipeline, including:

PDF text extraction using pdfplumber
intelligent text chunking with overlap windows
knowledge graph extraction using Gemini
schema-constrained JSON validation
graph normalization and node mapping
Neo4j node and relationship ingestion
Cypher-based graph queries
end-to-end pipeline testing and debugging
Tech Stack

Python, Neo4j, Cypher, Google Gemini API, pdfplumber, JSON pipelines
