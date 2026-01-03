#!/usr/bin/env python3
"""
Index projects data into ChromaDB vector database.

Run this script to populate the vector database with Ido's portfolio projects.

Usage:
    python3 backend/vector_db/index_data.py
"""

import sys
import os

# Add backend directory to path so we can import knowledge
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from knowledge.projects import projects_data
from vector_db.setup import index_projects, get_vector_db


def main():
    """Index all projects into vector database."""
    print("🚀 Starting vector database indexing...")
    print(f"📊 Found {len(projects_data)} projects to index")

    try:
        # Index projects
        count = index_projects(projects_data)
        print(f"✅ Successfully indexed {count} projects!")

        # Verify indexing
        collection = get_vector_db()
        total_docs = collection.count()
        print(f"📈 Total documents in vector DB: {total_docs}")

        # Show sample data
        print("\n📝 Sample indexed projects:")
        sample = collection.peek(limit=2)
        if sample and sample['metadatas']:
            for metadata in sample['metadatas']:
                print(f"  - {metadata['title']} ({metadata['year']})")

        print("\n✨ Indexing complete! Vector search is ready to use.")

    except Exception as e:
        print(f"❌ Error during indexing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
