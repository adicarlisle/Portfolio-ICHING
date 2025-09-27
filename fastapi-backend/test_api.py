import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_query():
    """Test creating a new query"""
    print("Testing query creation...")
    response = requests.post(
        f"{BASE_URL}/queries/",
        json={"query": "I seek wisdom about conflict and peace in my life"}
    )
    print(f"Status: {response.status_code}")
    if response.ok:
        data = response.json()
        print(f"Query ID: {data['id']}")
        print(f"Hexagram set:")
        for hexagram in data['hexagram_set']:
            print(f"  - {hexagram['hexagram_unicode']} {hexagram['hexagram_name']} (score: {hexagram['score']:.3f})")
    else:
        print(f"Error: {response.text}")
    return response.json() if response.ok else None

def test_get_hexagrams():
    """Test getting all hexagrams"""
    print("\nTesting hexagram list...")
    response = requests.get(f"{BASE_URL}/hexagrams/")
    if response.ok:
        hexagrams = response.json()
        print(f"Total hexagrams: {len(hexagrams)}")
        print("First 5 hexagrams:")
        for hex_data in hexagrams[:5]:
            print(f"  {hex_data['unicode']} {hex_data['id']}. {hex_data['name']}")
    else:
        print(f"Error: {response.text}")

def test_similar_queries():
    """Test finding similar queries"""
    print("\nTesting similar query search...")
    response = requests.get(
        f"{BASE_URL}/queries/search/similar",
        params={"query": "peace and harmony", "limit": 5}
    )
    if response.ok:
        results = response.json()
        print(f"Found {len(results)} similar queries")
        for result in results:
            print(f"  Query: '{result['query']}' (similarity: {result['similarity']:.3f})")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    # Test all endpoints
    test_get_hexagrams()
    query_data = test_create_query()
    
    # Create a few more queries for similarity testing
    test_queries = [
        "What does the future hold for my career?",
        "How can I find balance between work and family?",
        "I am facing a difficult decision about moving",
        "Seeking guidance on a new relationship",
        "Need clarity about financial investments"
    ]
    
    print("\nCreating additional test queries...")
    for q in test_queries:
        response = requests.post(f"{BASE_URL}/queries/", json={"query": q})
        if response.ok:
            print(f"  ✓ Created: {q}")
        else:
            print(f"  ✗ Failed: {q}")
    
    test_similar_queries()