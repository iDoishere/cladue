#!/usr/bin/env python3
"""
Test semantic search functionality.
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vector_db.setup import search_similar_projects

# Test queries
test_queries = [
    "real-time applications",
    "projects with maps and location",
    "chat or messaging systems",
    "apps using Firebase database",
    "mobile development",
]

print("🔍 Testing Semantic Search\n" + "="*50 + "\n")

for query in test_queries:
    print(f"Query: '{query}'")
    results = search_similar_projects(query, n_results=2)

    if results:
        for i, result in enumerate(results, 1):
            score = result.get('similarity_score', 'N/A')
            print(f"  {i}. {result['title']} (similarity: {score})")
    else:
        print("  No results found")

    print()

print("✅ Semantic search test complete!")
