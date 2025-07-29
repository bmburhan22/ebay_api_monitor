#!/usr/bin/env python3
"""
Message Handler
Handles message formatting and item tracking
"""

import os
from datetime import datetime
from config import ITEMS_FILE, CHAT_IDS
import requests


class MessageHandler:
    """Handles message formatting and item tracking"""
    
    def __init__(self):
        self.items_file = ITEMS_FILE
        
    def read_processed_items(self):
        """Read list of processed item IDs"""
        if not os.path.exists(self.items_file):
            open(self.items_file, "w").close()
        return open(self.items_file).read().splitlines()
    
    def add_processed_item(self, item_id):
        """Add item ID to processed items list"""
        items = self.read_processed_items()
        if item_id not in items:
            items.append(item_id)
            with open(self.items_file, 'w') as f:
                f.write('\n'.join(items))
            print(f"✓ Added item {item_id} to processed items")
    
    def is_item_processed(self, item_id):
        """Check if item has been processed before"""
        return item_id in self.read_processed_items()
    
    def format_message(self, item):
        """Format item data into Telegram message"""
        link = f"https://www.ebay.co.uk/itm/{item['item_id']}"
        title = item["title"]
        auc = item.get("auction_price")
        bin_price = item.get("buy_now_price")
        
        # Parse listing time if available
        listing_time = ""
        if item.get("listing_time"):
            try:
                # Parse the ISO format time from API
                dt = datetime.fromisoformat(item["listing_time"].replace("Z", "+00:00"))
                listing_time = dt.strftime("%I:%M %p %d/%m")
            except Exception as e:
                print(f"Warning: Could not parse listing time: {e}")
                listing_time = item["listing_time"]
        
        print(f"Formatting message for: {listing_time} - {title}")
        
        # Build message list
        message_list = [title, link]
        
        if auc:
            message_list.append(f'AUC: {auc}')
        if bin_price:
            message_list.append(f'BIN: {bin_price}')
        if item["best_offer_enabled"]:
            message_list.append("Best Offer Allowed")
        if listing_time:
            message_list.append(listing_time)
        
        return '\n'.join(message_list)
    
    def send_telegram_message(self, message):
        """Send message to Telegram"""
        telegram_token = os.environ.get("TELEGRAM_API_KEY")
        
        if not telegram_token:
            print("✗ TELEGRAM_API_KEY environment variable not set")
            return False
        
        success_count = 0
        for chat_id in CHAT_IDS:
            try:
                url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
                data = {'chat_id': chat_id, 'text': message}
                
                response = requests.post(url, data=data)
                response.raise_for_status()
                
                print(f"✓ Message sent to chat {chat_id}")
                success_count += 1
                
            except Exception as e:
                print(f"✗ Failed to send message to chat {chat_id}: {e}")
        
        return success_count > 0 