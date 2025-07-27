# Crypto News Telegram Bot 🚀

A Telegram bot that fetches the top 10 crypto-related news stories from multiple sources and delivers them in concise summaries (under 50 words each) with links to the original articles.

## Features

- 📰 Fetches news from multiple sources (CoinDesk RSS, CryptoPanic RSS, NewsAPI)
- ✂️ Automatically summarizes articles to under 50 words
- 🔗 Provides direct links to full articles
- 🚀 Fast and responsive with async processing
- 🔄 Removes duplicates and sorts by recency
- 💬 Easy-to-use Telegram interface

## Setup Instructions

### 1. Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` to create a new bot
3. Follow the instructions to set a name and username
4. Copy the bot token provided by BotFather

### 2. Get NewsAPI Key (Optional)

1. Visit [NewsAPI.org](https://newsapi.org/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. **Note**: The bot works without NewsAPI using RSS feeds, but NewsAPI provides additional news sources

### 3. Install Dependencies

```bash
# Clone or download this repository
cd telegrambot

# Install required packages
pip install -r requirements.txt
```

### 4. Configure Environment

1. Create a `.env` file in the project directory:

```bash
cp .env.example .env
```

2. Edit the `.env` file with your credentials:

```
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
NEWS_API_KEY=your_news_api_key_here  # Optional but recommended
```

### 5. Run the Bot

#### Option 1: Quick Start (Recommended)
```bash
python start_bot.py
```

#### Option 2: Manual Start
```bash
source venv/bin/activate
python crypto_news_bot.py
```

The bot will start and display:
```
🚀 Crypto News Bot is starting...
Bot is running! Press Ctrl+C to stop.
```

## Usage

### Bot Commands

- `/start` - Welcome message and introduction
- `/help` - Display help information
- `/news` - Get the latest top 10 crypto news stories

### Example Interaction

1. Start a chat with your bot on Telegram
2. Send `/start` to get started
3. Send `/news` to fetch the latest crypto news
4. Each news story will be delivered as a separate message with:
   - Summary in under 50 words
   - "Read Full Article" button linking to the source
   - Source information

## News Sources

The bot aggregates news from:

1. **CoinDesk RSS** - Major crypto news outlet
2. **CryptoPanic RSS** - Crypto-focused news aggregator  
3. **NewsAPI** - General news API with crypto filtering (requires API key)

## Technical Features

- **Async Processing**: Fast concurrent news fetching
- **Duplicate Removal**: Intelligent deduplication by title
- **Smart Summarization**: Maintains readability while staying under 50 words
- **Error Handling**: Graceful handling of network issues
- **Rate Limiting**: Built-in delays to respect Telegram limits
- **Logging**: Comprehensive logging for debugging

## File Structure

```
telegrambot/
├── crypto_news_bot.py    # Main bot application
├── start_bot.py          # Quick start script with setup checks
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Your actual environment variables (create this)
├── .gitignore           # Git ignore file
└── README.md           # This file
```

## Troubleshooting

### Common Issues

1. **"TELEGRAM_BOT_TOKEN not found"**
   - Make sure you created the `.env` file
   - Verify your bot token is correct
   - Check there are no extra spaces in the `.env` file

2. **"No news fetched"**
   - Check your internet connection
   - Some RSS feeds might be temporarily unavailable
   - Try adding a NewsAPI key for additional sources

3. **"Bot not responding"**
   - Ensure the bot is running (`python crypto_news_bot.py`)
   - Check if the bot token is valid
   - Make sure you've started a chat with the bot on Telegram

### Development

To modify news sources, edit the `news_sources` list in the `fetch_crypto_news` method.

To change the summary length, modify the word limit in the `summarize_article` method.

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests!