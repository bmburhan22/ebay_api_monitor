# eBay API Monitor Configuration - SAMPLE FILE
# Copy this file to config.py and fill in your actual values

# Search Configuration
KEYWORDS = ["Brompton", "Brompton"]
CATEGORY_ID = "177831"
EXCLUDED_SELLERS = [
    "nomorecorona",
    "acousticv8"
]

# Telegram Configuration
CHAT_IDS = [1160971557]
TELEGRAM_API_KEY = "your_telegram_bot_token"  # Set via environment variable

# eBay API Configuration
EBAY_CLIENT_ID = "your_ebay_client_id_here"  # Replace with your actual client ID
EBAY_CLIENT_SECRET = "your_ebay_client_secret_here"  # Replace with your actual client secret

# Browse API Configuration
MAX_RESULTS_PER_BATCH = 50  # Maximum results to fetch per API call
MAX_TOTAL_RESULTS = 200  # Maximum total results to process before giving up

# Monitoring Configuration
DELAY = 3600  # Delay between searches in seconds
ITEMS_FILE = "items.txt"  # File to store processed item IDs 