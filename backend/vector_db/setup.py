import chromadb
from chromadb.config import Settings
from google import genai
from google.genai import types
import os
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from backend/.env
backend_dir = Path(__file__).parent.parent
load_dotenv(backend_dir / ".env")

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")
client = genai.Client(api_key=api_key)

# ChromaDB client singleton
_chroma_client = None
_collection = None


def get_embedding(text: str) -> List[float]:
    """
    Generate embedding for text using Google Gemini's embedding model (FREE).

    Args:
        text: Text to embed

    Returns:
        List of floats representing the embedding vector
    """
    try:
        # Use Gemini's embedding model (text-embedding-004 is free and powerful)
        result = client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return result.embeddings[0].values
    except Exception as e:
        print(f"Error generating embedding: {e}")
        import traceback
        traceback.print_exc()
        # Return zero vector as fallback
        return [0.0] * 768  # text-embedding-004 produces 768-dim vectors


def get_vector_db():
    """
    Get or create ChromaDB client and collection.

    Returns:
        ChromaDB collection for projects
    """
    global _chroma_client, _collection

    if _collection is not None:
        return _collection

    # Initialize ChromaDB client (persists to disk)
    chroma_path = backend_dir / "storage" / "chroma"
    _chroma_client = chromadb.PersistentClient(
        path=str(chroma_path),
        settings=Settings(
            anonymized_telemetry=False,
            allow_reset=True
        )
    )

    # Get or create collection for projects
    _collection = _chroma_client.get_or_create_collection(
        name="ido_projects",
        metadata={"description": "Ido Cohen's portfolio projects with semantic search"}
    )

    return _collection


def index_projects(projects: List[Dict[str, Any]]) -> int:
    """
    Index projects into ChromaDB with Gemini embeddings.

    Args:
        projects: List of project dictionaries from knowledge base

    Returns:
        Number of projects indexed
    """
    collection = get_vector_db()

    # Clear existing data if any exists
    try:
        existing_count = collection.count()
        if existing_count > 0:
            # Get all existing IDs and delete them
            existing_data = collection.get()
            if existing_data and existing_data['ids']:
                collection.delete(ids=existing_data['ids'])
                print(f"🗑️  Cleared {existing_count} existing documents")
    except Exception as e:
        print(f"Note: Could not clear existing data: {e}")

    documents = []
    embeddings = []
    metadatas = []
    ids = []

    for project in projects:
        # Create rich text representation for embedding
        # Combine title, description, technologies, and features
        text_for_embedding = f"""
Title: {project['title']}

Description: {project['description']}

Technologies: {', '.join(project['technologies'])}

Features:
{chr(10).join(['- ' + feature for feature in project['features']])}

Year: {project['year']}
"""

        # Generate embedding using Gemini (FREE)
        embedding = get_embedding(text_for_embedding.strip())

        # Prepare data for ChromaDB
        documents.append(text_for_embedding.strip())
        embeddings.append(embedding)
        ids.append(project['id'])

        # Store metadata (all project fields for retrieval)
        metadatas.append({
            "title": project['title'],
            "description": project['description'],
            "technologies": ", ".join(project['technologies']),
            "year": str(project['year']),
            "id": project['id']
        })

    # Add to ChromaDB
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print(f"✅ Indexed {len(projects)} projects into vector database")
    return len(projects)


def search_similar_projects(query: str, n_results: int = 3) -> List[Dict[str, Any]]:
    """
    Search for projects semantically similar to the query.

    Args:
        query: Natural language search query
        n_results: Number of results to return

    Returns:
        List of matching projects with similarity scores
    """
    collection = get_vector_db()

    # Generate embedding for the search query
    query_embedding = get_embedding(query)

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count())
    )

    # Format results
    matches = []
    if results and results['metadatas']:
        for i, metadata in enumerate(results['metadatas'][0]):
            # Extract distance/similarity score
            distance = results['distances'][0][i] if results.get('distances') else None

            matches.append({
                "id": metadata['id'],
                "title": metadata['title'],
                "description": metadata['description'],
                "technologies": metadata['technologies'].split(", "),
                "year": int(metadata['year']),
                "similarity_score": round(1 - distance, 3) if distance else None  # Convert distance to similarity
            })

    return matches
