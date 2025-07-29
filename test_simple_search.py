#!/usr/bin/env python3
"""
Simple test to check eBay API access
"""

from ebay_api import EbayAPI

def main():
    print("🔍 Testing Simple eBay Search")
    print("=" * 40)
    
    ebay_api = EbayAPI()
    
    try:
        # Test authentication
        print("1. Testing authentication...")
        token = ebay_api.get_access_token()
        print(f"✓ Authentication successful: {token[:20]}...")
        
        # Test simple search
        print("\n2. Testing simple search...")
        result = ebay_api.search_listings("test", [], "177831")
        
        if result:
            print("✓ Found item!")
            print(f"   Title: {result.get('title', 'N/A')}")
            print(f"   Seller: {result.get('seller', {}).get('username', 'N/A')}")
            print(f"   Price: {result.get('price', {}).get('value', 'N/A')}")
        else:
            print("✗ No items found")
            
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    main() 