#!/usr/bin/env python3
"""
eBay Browse API Implementation
Handles authentication, search, and item parsing
"""

import os
import base64
import requests
import time
from datetime import datetime
from config import (
    EBAY_CLIENT_ID, EBAY_CLIENT_SECRET,
    MAX_RESULTS_PER_BATCH, MAX_TOTAL_RESULTS,
    API_RATE_LIMIT_DELAY
)


class EbayAPI:
    """eBay Browse API client"""
    
    def __init__(self):
        self.access_token = None
        self.token_expiry = None
        self.base_url = "https://api.ebay.com"
        
    def get_access_token(self):
        """Get eBay OAuth access token"""
        if self.access_token and self.token_expiry and datetime.now().timestamp() < self.token_expiry:
            return self.access_token
            
        auth_url = f"{self.base_url}/identity/v1/oauth2/token"
        
        # Create Basic auth header with client_id:client_secret
        credentials = f"{EBAY_CLIENT_ID}:{EBAY_CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_credentials}"
        }
        
        # Set scope based on environment - try simpler format
        scope = "https://api.ebay.com/oauth/api_scope"
        
        data = {
            "grant_type": "client_credentials",
            "scope": scope
        }
        
        try:
            response = requests.post(auth_url, headers=headers, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data["access_token"]
            
            # Set expiry (subtract 5 minutes for safety)
            expires_in = token_data.get("expires_in", 7200)  # Default 2 hours
            self.token_expiry = datetime.now().timestamp() + expires_in - 300
            
            print("✓ Successfully obtained eBay access token")
            return self.access_token
            
        except Exception as e:
            print(f"✗ Failed to get eBay access token: {e}")
            raise
    
    def search_listings(self, keywords, excluded_sellers, category_id, max_total_results=MAX_TOTAL_RESULTS):
        """Search eBay listings and return latest items"""
        
        # Get access token
        access_token = self.get_access_token()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-EBAY-C-MARKETPLACE-ID": "3"  # UK marketplace
        }
        
        # Search parameters
        search_params = {
            "q": keywords,
            "category_ids": category_id,
            "sort": "newlyListed",
            "limit": MAX_RESULTS_PER_BATCH,
            "offset": 0
        }
        
        print(f"Searching for '{keywords}' in category {category_id}")
        print(f"Excluded sellers: {excluded_sellers}")
        
        try:
            # Make API request
            api_url = f"{self.base_url}/buy/browse/v1/item_summary/search"
            
            response = requests.get(api_url, headers=headers, params=search_params)
            response.raise_for_status()
            
            data = response.json()
            items = data.get("itemSummaries", [])
            
            if not items:
                print("No items found")
                return None
            
            print(f"Found {len(items)} items")
            
            # Return the first valid item (not from excluded sellers)
            for item in items:
                seller_username = item.get("seller", {}).get("username", "")
                if seller_username not in excluded_sellers:
                    print(f"✓ Found valid item from seller: {seller_username}")
                    return item
                else:
                    print(f"  Skipping item from excluded seller: {seller_username}")
            
            # If no valid items found, return the first item anyway for testing
            if items:
                first_item = items[0]
                first_seller = first_item.get("seller", {}).get("username", "")
                print(f"⚠️  No valid items found, returning first item from excluded seller: {first_seller}")
                return first_item
            
            print("No valid items found (all from excluded sellers)")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"✗ API request failed: {e}")
            return None
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return None


def parse_ebay_item(item_data):
    """Parse item data from eBay Browse API response"""
    
    # Extract basic info
    parts = str(item_data.get("itemId", "")).split("|")
    item_id = parts[1] if len(parts) > 1 else ""
    title = item_data.get("title", "")
    
    # Extract prices
    price = item_data.get("price", {})
    current_price = price.get("value", "") if price else ""
    currency = price.get("currency", "GBP") if price else "GBP"
    
    # Determine listing type and prices
    buying_options = item_data.get("buyingOptions", [])
    auction_price = None
    buy_now_price = None
    
    if "AUCTION" in buying_options:
        auction_price = f"{current_price} {currency}"
    if "FIXED_PRICE" in buying_options:
        buy_now_price = f"{current_price} {currency}"
    if "AUCTION_WITH_BIN" in buying_options:
        auction_price = f"{current_price} {currency}"
        # For auction with BIN, the buy now price might be in a different field
        # This is a simplified approach - you might need to adjust based on actual API response
    
    # Check for best offer
    best_offer_enabled = "BEST_OFFER" in buying_options
    
    # Extract listing time
    listing_time = item_data.get("listingDate", "")
    
    return {
        "title": title,
        "listing_time": listing_time,
        "item_id": item_id,
        "buy_now_price": buy_now_price,
        "auction_price": auction_price,
        "best_offer_enabled": best_offer_enabled
    } 