#!/usr/bin/env python3
"""
eBay Listing Monitor
Main script that monitors eBay listings and sends notifications
"""

import time
import sys
from ebay_api import EbayAPI, parse_ebay_item
from message_handler import MessageHandler
from config import KEYWORDS, EXCLUDED_SELLERS, CATEGORY_ID, MAX_TOTAL_RESULTS, DELAY, SEARCH_DELAY, API_RATE_LIMIT_DELAY


def main():
    """Main monitoring loop"""
    
    print("🚀 Starting eBay Listing Monitor")
    print("=" * 50)
    
    # Initialize components
    ebay_api = EbayAPI()
    message_handler = MessageHandler()
    
    print(f"Keywords: {KEYWORDS}")
    print(f"Category ID: {CATEGORY_ID}")
    print(f"Excluded sellers: {EXCLUDED_SELLERS}")
    print(f"Max total results: {MAX_TOTAL_RESULTS}")
    print(f"Cycle delay: {DELAY} seconds")
    print(f"Search delay: {SEARCH_DELAY} seconds")
    print(f"API rate limit delay: {API_RATE_LIMIT_DELAY} seconds")
    print("=" * 50)
    
    # Test API connection
    try:
        print("Testing eBay API connection...")
        ebay_api.get_access_token()
        print("✓ eBay API connection successful")
    except Exception as e:
        print(f"✗ Failed to connect to eBay API: {e}")
        print("Please check your eBay API credentials in config.py")
        sys.exit(1)
    
    print("\nStarting monitoring loop...")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    # Send test message to confirm Telegram is working
    if message_handler.telegram_enabled:
        test_message = "🤖 eBay Monitor Started!\n\nSearching for: " + ", ".join(KEYWORDS) + "\nCategory: " + CATEGORY_ID + "\nExcluded sellers: " + ", ".join(EXCLUDED_SELLERS)
        print("📤 Sending test message to Telegram...")
        if message_handler.send_telegram_message(test_message):
            print("✓ Test message sent successfully!")
        else:
            print("✗ Failed to send test message")
        print("-" * 50)
    
    try:
        while True:
            for keyword in KEYWORDS:
                print(f"\n🔍 Searching for: {keyword}")
                
                try:
                    # Search for listings
                    item_data = ebay_api.search_listings(
                        keyword, 
                        EXCLUDED_SELLERS, 
                        CATEGORY_ID, 
                        MAX_TOTAL_RESULTS
                    )
                    
                    if item_data:
                        # Parse the item
                        item = parse_ebay_item(item_data)
                        item_id = item['item_id']
                        
                        print(f"Found item: {item['title']}")
                        print(f"Item ID: {item_id}")
                        
                        # Check if already processed
                        if message_handler.is_item_processed(item_id):
                            print(f"Item {item_id} already processed, skipping...")
                            continue
                        
                        # Format and send message
                        message = message_handler.format_message(item)
                        print(f"Generated message:\n{message}")
                        
                        # Send to Telegram
                        if message_handler.send_telegram_message(message):
                            # Mark as processed
                            message_handler.add_processed_item(item_id)
                            print("✓ Message sent and item marked as processed")
                        else:
                            print("✗ Failed to send message")
                    
                    else:
                        print(f"No valid items found for keyword: {keyword}")
                
                except Exception as e:
                    print(f"✗ Error processing keyword '{keyword}': {e}")
                    import traceback
                    traceback.print_exc()
                
                # Delay between searches
                if keyword != KEYWORDS[-1]:  # Don't delay after the last keyword
                    print(f"Waiting {SEARCH_DELAY} seconds before next search...")
                    time.sleep(SEARCH_DELAY)
            
            # Complete cycle delay
            print(f"\nCompleted search cycle. Waiting {DELAY} seconds before next cycle...")
            print("-" * 50)
            time.sleep(DELAY)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped by user")
        print("Goodbye!")
    except Exception as e:
        print(f"\n✗ Unexpected error in main loop: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 