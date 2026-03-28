#!/usr/bin/env python3
"""
Index all portfolio data into ChromaDB.

Run this after any changes to knowledge/ files.

Usage:
    cd backend && python3 vector_db/index_data.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from knowledge.projects import projects_data
from knowledge.skills import skills_data
from knowledge.experience import experience_data
from vector_db.setup import (
    index_projects,
    index_skills,
    index_experience,
    get_portfolio_collection,
)


def main():
    print("🚀 Indexing all portfolio knowledge into ChromaDB...\n")

    try:
        index_projects(projects_data)
        index_skills(skills_data)
        index_experience(experience_data)

        collection = get_portfolio_collection()
        total = collection.count()
        print(f"\n📈 Total documents in vector DB: {total}")
        print("✨ Done! All knowledge indexed and ready for semantic search.")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
