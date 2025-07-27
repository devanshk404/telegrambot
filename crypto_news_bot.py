#!/usr/bin/env python3
"""
Crypto News Telegram Bot
Fetches top 10 crypto news stories and delivers them in under 50 words each.
"""

import os
import asyncio
import logging
from typing import List, Dict
from datetime import datetime
import aiohttp
import feedparser
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CryptoNewsBot:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
    
    async def fetch_crypto_news(self) -> List[Dict]:
        """Fetch crypto news from multiple sources"""
        news_sources = [
            {
                'name': 'CoinDesk RSS',
                'url': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
                'type': 'rss'
            },
            {
                'name': 'CryptoPanic RSS', 
                'url': 'https://cryptopanic.com/news/rss/',
                'type': 'rss'
            },
            {
                'name': 'NewsAPI',
                'url': f'https://newsapi.org/v2/everything?q=cryptocurrency OR bitcoin OR ethereum&sortBy=publishedAt&pageSize=20&apiKey={self.news_api_key}',
                'type': 'api'
            }
        ]
        
        all_news = []
        
        for source in news_sources:
            try:
                if source['type'] == 'rss':
                    news = await self.fetch_rss_news(source['url'])
                elif source['type'] == 'api' and self.news_api_key:
                    news = await self.fetch_api_news(source['url'])
                else:
                    continue
                    
                all_news.extend(news)
            except Exception as e:
                logger.error(f"Error fetching from {source['name']}: {e}")
                continue
        
        # Remove duplicates and sort by date
        seen_titles = set()
        unique_news = []
        
        for article in all_news:
            title_lower = article['title'].lower()
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                unique_news.append(article)
        
        # Sort by published date (most recent first)
        unique_news.sort(key=lambda x: x.get('published', datetime.min), reverse=True)
        
        return unique_news[:10]
    
    async def fetch_rss_news(self, url: str) -> List[Dict]:
        """Fetch news from RSS feed"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    content = await response.text()
                    
            feed = feedparser.parse(content)
            news = []
            
            for entry in feed.entries[:15]:  # Get more to filter later
                article = {
                    'title': entry.title,
                    'description': getattr(entry, 'summary', '')[:200],
                    'url': entry.link,
                    'published': getattr(entry, 'published_parsed', None),
                    'source': 'RSS Feed'
                }
                
                if article['published']:
                    article['published'] = datetime(*article['published'][:6])
                else:
                    article['published'] = datetime.now()
                    
                news.append(article)
            
            return news
            
        except Exception as e:
            logger.error(f"Error fetching RSS from {url}: {e}")
            return []
    
    async def fetch_api_news(self, url: str) -> List[Dict]:
        """Fetch news from NewsAPI"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    data = await response.json()
                    
            news = []
            if data.get('status') == 'ok':
                for article in data.get('articles', []):
                    news_item = {
                        'title': article['title'],
                        'description': article.get('description', '')[:200],
                        'url': article['url'],
                        'published': datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00')),
                        'source': article.get('source', {}).get('name', 'NewsAPI')
                    }
                    news.append(news_item)
            
            return news
            
        except Exception as e:
            logger.error(f"Error fetching from NewsAPI: {e}")
            return []
    
    def summarize_article(self, title: str, description: str) -> str:
        """Summarize article to under 50 words"""
        # Combine title and description
        text = f"{title}. {description}"
        
        # Split into words
        words = text.split()
        
        # If already under 50 words, return as is
        if len(words) <= 50:
            return text
        
        # Take first 47 words and add "..."
        summary = ' '.join(words[:47]) + "..."
        return summary
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🚀 **Crypto News Bot** 🚀

Get the latest crypto news in bite-sized summaries!

**Commands:**
• /news - Get top 10 crypto news stories
• /help - Show this help message

Each story is summarized in under 50 words with a link to the full article.
        """
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = """
📱 **How to use this bot:**

• Send /news to get the latest crypto news
• Each story is summarized in under 50 words
• Click the link to read the full article
• News is updated from multiple crypto sources

**Available commands:**
• /start - Welcome message
• /news - Get latest news
• /help - Show this message
        """
        
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /news command"""
        # Send loading message
        loading_msg = await update.message.reply_text("🔄 Fetching latest crypto news...")
        
        try:
            # Fetch news
            news_articles = await self.fetch_crypto_news()
            
            if not news_articles:
                await loading_msg.edit_text("❌ Sorry, couldn't fetch news at the moment. Please try again later.")
                return
            
            # Delete loading message
            await loading_msg.delete()
            
            # Send header
            header = f"📰 **Top {len(news_articles)} Crypto News Stories**\n" + "─" * 40 + "\n\n"
            await update.message.reply_text(header, parse_mode='Markdown')
            
            # Send each article
            for i, article in enumerate(news_articles, 1):
                summary = self.summarize_article(article['title'], article['description'])
                
                # Create inline keyboard with link
                keyboard = InlineKeyboardMarkup([[
                    InlineKeyboardButton("📖 Read Full Article", url=article['url'])
                ]])
                
                # Format message
                message = f"**{i}.** {summary}\n\n🔗 Source: {article['source']}"
                
                await update.message.reply_text(
                    message, 
                    parse_mode='Markdown',
                    reply_markup=keyboard,
                    disable_web_page_preview=True
                )
                
                # Small delay between messages to avoid rate limiting
                await asyncio.sleep(0.5)
        
        except Exception as e:
            logger.error(f"Error in news_command: {e}")
            await loading_msg.edit_text("❌ An error occurred while fetching news. Please try again later.")
    
    def run(self):
        """Run the bot"""
        if not self.bot_token:
            print("Error: TELEGRAM_BOT_TOKEN not found!")
            print("Please create a .env file with your bot token.")
            return
        
        # Create application
        app = Application.builder().token(self.bot_token).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("news", self.news_command))
        
        # Start the bot
        print("🚀 Crypto News Bot is starting...")
        print("Bot is running! Press Ctrl+C to stop.")
        
        app.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function"""
    try:
        bot = CryptoNewsBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if __name__ == "__main__":
    main()