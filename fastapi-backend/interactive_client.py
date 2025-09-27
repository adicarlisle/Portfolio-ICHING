#!/usr/bin/env python3
import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
import sys
import os

class ICHingClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.check_connection()
    
    def check_connection(self):
        """Check if API is accessible"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.ok:
                print(f"✓ Connected to {response.json()['service']}")
            else:
                print(f"✗ API returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"✗ Cannot connect to API at {self.base_url}")
            print("Make sure the FastAPI server is running (python3 main.py)")
            sys.exit(1)
    
    def create_query(self, query_text: str) -> Optional[Dict]:
        """Submit a new query to the I Ching API"""
        try:
            response = requests.post(
                f"{self.base_url}/queries/",
                json={"query": query_text}
            )
            if response.ok:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error submitting query: {e}")
            return None
    
    def get_all_queries(self, limit: int = 10) -> List[Dict]:
        """Get recent queries"""
        try:
            response = requests.get(
                f"{self.base_url}/queries/",
                params={"limit": limit}
            )
            if response.ok:
                return response.json()
            else:
                print(f"Error fetching queries: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def find_similar(self, query_text: str, limit: int = 5) -> List[Dict]:
        """Find similar queries"""
        try:
            response = requests.get(
                f"{self.base_url}/queries/search/similar",
                params={"query": query_text, "limit": limit}
            )
            if response.ok:
                return response.json()
            else:
                print(f"Error finding similar queries: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def get_hexagrams(self) -> List[Dict]:
        """Get all hexagrams"""
        try:
            response = requests.get(f"{self.base_url}/hexagrams/")
            if response.ok:
                return response.json()
            else:
                print(f"Error fetching hexagrams: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def display_query_result(self, result: Dict):
        """Display a query result in a formatted way"""
        print("\n" + "═" * 60)
        print(f"Query: {result['query']}")
        print(f"ID: {result['id']}")
        print(f"Created: {result['created_at']}")
        print("\nHexagram Reading:")
        print("-" * 60)
        
        for i, hexagram in enumerate(result['hexagram_set'], 1):
            relevance = int(hexagram['score'] * 100)
            bar_length = int(relevance / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            
            print(f"{i}. {hexagram['hexagram_unicode']} {hexagram['hexagram_name']:<30} "
                  f"[{bar}] {relevance}%")
        
        print("═" * 60)
    
    def display_hexagram_list(self, hexagrams: List[Dict]):
        """Display all hexagrams in a grid"""
        print("\nI Ching Hexagrams:")
        print("═" * 80)
        
        # Display in 4 columns
        cols = 4
        for i in range(0, len(hexagrams), cols):
            row = hexagrams[i:i+cols]
            for hex_data in row:
                print(f"{hex_data['unicode']} {hex_data['id']:2d}. {hex_data['name']:<18}", end="  ")
            print()
        
        print("═" * 80)
    
    def display_similar_queries(self, results: List[Dict]):
        """Display similar queries"""
        if not results:
            print("No similar queries found.")
            return
        
        print("\nSimilar Queries:")
        print("═" * 60)
        
        for i, result in enumerate(results, 1):
            similarity = int(result['similarity'] * 100)
            print(f"\n{i}. Query: {result['query']}")
            print(f"   Similarity: {similarity}%")
            print(f"   Created: {result['created_at']}")
            
            # Show top 3 hexagrams
            print("   Top hexagrams:", end=" ")
            for hex_data in result['hexagram_set'][:3]:
                print(f"{hex_data['hexagram_unicode']}", end=" ")
            print()
        
        print("═" * 60)

def main():
    """Main interactive loop"""
    client = ICHingClient()
    
    print("\n" + "═" * 60)
    print("I CHING ORACLE - Interactive Client")
    print("═" * 60)
    print("\nCommands:")
    print("  ask <question>  - Ask the I Ching a question")
    print("  find <query>    - Find similar previous queries")
    print("  history [n]     - Show last n queries (default: 10)")
    print("  hexagrams       - List all 64 hexagrams")
    print("  help            - Show this help message")
    print("  quit/exit       - Exit the program")
    print("═" * 60)
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            
            if command in ['quit', 'exit', 'q']:
                print("\nFarewell! May the wisdom of the I Ching guide your path.")
                break
            
            elif command in ['help', 'h', '?']:
                print("\nCommands:")
                print("  ask <question>  - Ask the I Ching a question")
                print("  find <query>    - Find similar previous queries")
                print("  history [n]     - Show last n queries (default: 10)")
                print("  hexagrams       - List all 64 hexagrams")
                print("  help            - Show this help message")
                print("  quit/exit       - Exit the program")
            
            elif command == 'ask':
                if len(parts) < 2:
                    print("Please provide a question. Example: ask What should I focus on today?")
                    continue
                
                question = parts[1]
                print(f"\nConsulting the I Ching about: '{question}'")
                print("Processing...", end='', flush=True)
                
                result = client.create_query(question)
                if result:
                    print("\r" + " " * 50 + "\r", end='')  # Clear "Processing..."
                    client.display_query_result(result)
            
            elif command == 'find':
                if len(parts) < 2:
                    print("Please provide a search query. Example: find career")
                    continue
                
                search_query = parts[1]
                print(f"\nSearching for queries similar to: '{search_query}'")
                
                results = client.find_similar(search_query, limit=5)
                client.display_similar_queries(results)
            
            elif command == 'history':
                limit = 10
                if len(parts) > 1 and parts[1].isdigit():
                    limit = int(parts[1])
                
                print(f"\nFetching last {limit} queries...")
                queries = client.get_all_queries(limit=limit)
                
                if queries:
                    print(f"\nRecent Queries ({len(queries)} results):")
                    print("═" * 60)
                    for i, query in enumerate(queries, 1):
                        print(f"\n{i}. {query['query']}")
                        print(f"   Created: {query['created_at']}")
                        print(f"   Hexagrams:", end=" ")
                        for hex_data in query['hexagram_set'][:6]:
                            print(f"{hex_data['hexagram_unicode']}", end=" ")
                        print()
                else:
                    print("No queries found.")
            
            elif command == 'hexagrams':
                print("\nFetching hexagram list...")
                hexagrams = client.get_hexagrams()
                if hexagrams:
                    client.display_hexagram_list(hexagrams)
            
            else:
                # If no command recognized, treat entire input as a question
                if user_input:
                    print(f"\nConsulting the I Ching about: '{user_input}'")
                    print("Processing...", end='', flush=True)
                    
                    result = client.create_query(user_input)
                    if result:
                        print("\r" + " " * 50 + "\r", end='')  # Clear "Processing..."
                        client.display_query_result(result)
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'quit' to exit.")
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()