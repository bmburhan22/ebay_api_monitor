#!/usr/bin/env python3
"""
Test script for eBay Browse API implementation
"""

import sys
import os
from ebay_api import EbayAPI, parse_ebay_item
from message_handler import MessageHandler
from config import KEYWORDS, EXCLUDED_SELLERS, CATEGORY_ID, MAX_TOTAL_RESULTS


def test_ebay_api():
    """Test the eBay Browse API implementation"""
    
    print("🧪 Testing eBay Browse API Implementation")
    print("=" * 50)
    
    # Initialize components
    ebay_api = EbayAPI()
    message_handler = MessageHandler()
    
    print(f"Keywords: {KEYWORDS}")
    print(f"Excluded sellers: {EXCLUDED_SELLERS}")
    print(f"Category ID: {CATEGORY_ID}")
    print(f"Max total results: {MAX_TOTAL_RESULTS}")
    print("-" * 50)
    
    # Test API authentication
    print("\n1. Testing API Authentication...")
    try:
        token = ebay_api.get_access_token()
        print(f"✓ Authentication successful")
        print(f"Token: {token[:20]}...")
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return False
    
    # Test search functionality
    print("\n2. Testing Search Functionality...")
    for keyword in KEYWORDS:
        print(f"\nTesting keyword: '{keyword}'")
        
        try:
            # Search for listings
            item_data = ebay_api.search_listings(
                keyword, 
                EXCLUDED_SELLERS, 
                CATEGORY_ID, 
                MAX_TOTAL_RESULTS
            )
            
            if item_data:
                print("✓ Found item from API")
                print(f"Item ID: {item_data.get('itemId', 'N/A')}")
                print(f"Title: {item_data.get('title', 'N/A')}")
                print(f"Seller: {item_data.get('seller', {}).get('username', 'N/A')}")
                
                # Test parsing
                print("\n3. Testing Item Parsing...")
                item = parse_ebay_item(item_data)
                print(f"Parsed item: {item}")
                
                # Test message formatting
                print("\n4. Testing Message Formatting...")
                message = message_handler.format_message(item)
                print(f"Generated message:\n{message}")
                
                # Test Telegram sending (if configured)
                print("\n5. Testing Telegram Integration...")
                if os.environ.get("TELEGRAM_API_KEY"):
                    success = message_handler.send_telegram_message("🧪 Test message from eBay API Monitor")
                    if success:
                        print("✓ Telegram message sent successfully")
                    else:
                        print("✗ Failed to send Telegram message")
                else:
                    print("⚠️  TELEGRAM_API_KEY not set, skipping Telegram test")
                
                return True
                
            else:
                print("✗ No valid items found")
                
        except Exception as e:
            print(f"✗ Error testing keyword '{keyword}': {e}")
            import traceback
            traceback.print_exc()
    
    return False


def main():
    """Main test function"""
    
    print("Starting eBay API tests...")
    
    success = test_ebay_api()
    
    if success:
        print("\n🎉 All tests passed!")
        print("The eBay API implementation is working correctly.")
    else:
        print("\n❌ Some tests failed.")
        print("Please check your configuration and try again.")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main()) 