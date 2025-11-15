"""Build RAG vector store from documents"""

import argparse
from pathlib import Path
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL

class RAGBuilder:
    def __init__(self, docs_path: str, output_path: str):
        self.docs_path = Path(docs_path)
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def load_documents(self) -> List[Document]:
        """Load all documents from directory"""
        documents = []
        
        # Support .txt, .md files
        for file_path in self.docs_path.rglob("*"):
            if file_path.suffix in [".txt", ".md"]:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    documents.append(Document(
                        page_content=content,
                        metadata={"source": str(file_path)}
                    ))
        
        return documents
    
    def build_vector_store(self):
        """Build FAISS vector store"""
        print("Loading documents...")
        documents = self.load_documents()
        print(f"Loaded {len(documents)} documents")
        
        if not documents:
            print("No documents found! Add .txt or .md files to the docs directory.")
            return
        
        print("\nSplitting documents into chunks...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks")
        
        print("\nBuilding vector store...")
        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        
        print(f"\nSaving vector store to {self.output_path}")
        vectorstore.save_local(str(self.output_path))
        
        print("✓ Vector store built successfully!")
        
        # Test retrieval
        print("\nTesting retrieval...")
        test_query = "What are the key skills for a software engineer?"
        results = vectorstore.similarity_search(test_query, k=3)
        
        print(f"\nTest query: {test_query}")
        print(f"Retrieved {len(results)} chunks:")
        for i, doc in enumerate(results, 1):
            print(f"\n{i}. {doc.page_content[:200]}...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build RAG vector store")
    parser.add_argument("--docs", default="data/ats_docs", help="Documents directory")
    parser.add_argument("--output", default="vector_store", help="Output directory")
    
    args = parser.parse_args()
    
    builder = RAGBuilder(args.docs, args.output)
    builder.build_vector_store()
