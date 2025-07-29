# eBay Listing Monitor with Browse API

A modern eBay listing monitor that uses the official eBay Browse API to search for items and send notifications via Telegram.

## Features

- ✅ **eBay Browse API Integration**: Uses official eBay API for reliable data
- ✅ **Seller Filtering**: Automatically excludes specified sellers
- ✅ **Pagination Support**: Fetches multiple batches until finding valid items
- ✅ **Configurable Thresholds**: Set maximum results to process
- ✅ **Telegram Notifications**: Sends formatted messages to Telegram
- ✅ **Item Tracking**: Prevents duplicate notifications
- ✅ **Error Handling**: Comprehensive error handling and logging
- ✅ **Modular Design**: Clean, maintainable code structure

## Project Structure

```
ebay_api_monitor/
├── config.py           # Configuration settings
├── ebay_api.py         # eBay API client and search logic
├── message_handler.py  # Message formatting and Telegram integration
├── monitor.py          # Main monitoring script
├── test_api.py         # Test script for verification
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── items.txt          # Processed items tracking (created automatically)
```

## Quick Start

### 1. Install Dependencies

```bash
cd ebay_api_monitor
pip install -r requirements.txt
```

### 2. Setup Configuration

1. **Copy the sample configuration file:**
   ```bash
   cp config.sample.py config.py
   ```

2. **Edit `config.py` with your actual credentials:**
   ```python
   EBAY_CLIENT_ID = "your_actual_client_id"
   EBAY_CLIENT_SECRET = "your_actual_client_secret"
   ```

### 3. Configure eBay API Credentials

1. Register at [eBay Developer Program](https://developer.ebay.com/)
2. Create a new application with **Browse API** enabled
3. Get your Client ID and Client Secret
4. Update `config.py` with your credentials

### 4. Configure Telegram Bot

1. Create a bot via [@BotFather](https://t.me/botfather)
2. Get your bot token and chat ID
3. Set environment variable:

```bash
export TELEGRAM_API_KEY="your_telegram_bot_token"
```

### 5. Customize Configuration

Edit `config.py` to match your needs:

```python
# Search settings
KEYWORDS = ["Brompton", "Brompton"]
CATEGORY_ID = "177831"
EXCLUDED_SELLERS = ["seller1", "seller2"]

# Telegram settings
CHAT_IDS = [1160971557]

# API settings
MAX_TOTAL_RESULTS = 200
MAX_RESULTS_PER_BATCH = 50
DELAY = 10
```

### 6. Test the Implementation

```bash
python test_api.py
```

### 7. Start Monitoring

```bash
python monitor.py
```

## Configuration Options

### Search Configuration

- `KEYWORDS`: List of search terms
- `CATEGORY_ID`: eBay category ID to search in
- `EXCLUDED_SELLERS`: List of seller usernames to exclude

### API Configuration

- `MAX_TOTAL_RESULTS`: Maximum items to process before giving up
- `MAX_RESULTS_PER_BATCH`: Results per API call (max 200)
- `DELAY`: Delay between searches in seconds

### Telegram Configuration

- `CHAT_IDS`: List of Telegram chat IDs to send messages to
- `TELEGRAM_API_KEY`: Environment variable for bot token

## How It Works

### 1. API Authentication
- Gets OAuth access token from eBay
- Automatically refreshes when expired
- Handles authentication errors gracefully

### 2. Search & Pagination
- Searches eBay listings with specified criteria
- Implements pagination to handle large result sets
- Continues fetching batches until finding valid items

### 3. Seller Filtering
- Checks each item's seller against excluded list
- Skips items from excluded sellers
- Continues searching if all items in batch are excluded

### 4. Message Formatting
Creates formatted messages with:
- Item title
- eBay link
- Auction price (if applicable)
- Buy-it-now price (if applicable)
- Best offer status
- Listing time

### 5. Telegram Integration
- Sends messages to all configured chat IDs
- Handles network errors and rate limiting
- Provides detailed success/failure feedback

## Message Format

```
Item Title
https://www.ebay.co.uk/itm/ITEM_ID
AUC: £XX.XX GBP (if auction)
BIN: £XX.XX GBP (if buy-it-now)
Best Offer Allowed (if applicable)
HH:MM AM/PM DD/MM (listing time)
```

## Error Handling

The implementation includes comprehensive error handling for:

- **API Authentication Failures**: Retries with proper error messages
- **Network Issues**: Graceful handling of connection problems
- **Rate Limiting**: Automatic delays between requests
- **Invalid Responses**: Safe parsing of API responses
- **Missing Data**: Fallback values for missing fields
- **Telegram Errors**: Individual chat error handling

## Monitoring Features

- **Item Deduplication**: Tracks processed items to prevent duplicates
- **Detailed Logging**: Comprehensive console output for debugging
- **Graceful Shutdown**: Handles Ctrl+C interruption properly
- **Status Indicators**: Visual feedback for all operations

## Testing

The `test_api.py` script verifies:

1. **API Authentication**: Tests eBay API connection
2. **Search Functionality**: Tests item search and filtering
3. **Item Parsing**: Tests data extraction and formatting
4. **Message Formatting**: Tests message generation
5. **Telegram Integration**: Tests notification sending

Run tests before starting the monitor:

```bash
python test_api.py
```

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Check eBay API credentials in `config.py`
   - Verify your application is approved on eBay Developer Portal

2. **No Items Found**
   - Check category ID is correct
   - Verify keywords are valid
   - Check if all sellers are excluded

3. **Telegram Not Working**
   - Verify `TELEGRAM_API_KEY` environment variable is set
   - Check bot token is correct
   - Verify chat IDs are valid

4. **Rate Limiting**
   - Increase `DELAY` in configuration
   - Reduce `MAX_RESULTS_PER_BATCH`

### Debug Mode

For detailed debugging, the script provides comprehensive logging. Check console output for:

- API request/response details
- Item processing status
- Error messages and stack traces
- Telegram message status

## Dependencies

- `requests`: HTTP requests for API calls
- Standard Python libraries: `os`, `json`, `datetime`, `time`, `base64`

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review console output for error messages
3. Verify all configuration settings
4. Test with the provided test script 