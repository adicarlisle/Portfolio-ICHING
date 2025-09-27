#!/usr/bin/env python3
import requests
import sys
import json

def quick_query(question: str, base_url="http://localhost:8000"):
    """Quick one-line query to the I Ching API"""
    try:
        response = requests.post(
            f"{base_url}/queries/",
            json={"query": question}
        )
        
        if response.ok:
            result = response.json()
            
            print(f"\nYour question: {result['query']}\n")
            print("The I Ching responds with these hexagrams:\n")
            
            for i, hex_data in enumerate(result['hexagram_set'], 1):
                relevance = int(hex_data['score'] * 100)
                print(f"{i}. {hex_data['hexagram_unicode']} {hex_data['hexagram_name']:<30} ({relevance}% relevance)")
            
            print(f"\n(Query saved with ID: {result['id']})")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Cannot connect to API. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 quick_query.py 'Your question here'")
        print("Example: python3 quick_query.py 'What should I focus on today?'")
        sys.exit(1)
    
    question = ' '.join(sys.argv[1:])
    quick_query(question)