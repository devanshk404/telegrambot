#!/usr/bin/env python3
"""
Quick start script for the Crypto News Telegram Bot
This script checks for the required environment setup and starts the bot.
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ Missing .env file!")
        print("\n📋 Setup Instructions:")
        print("1. Copy the example file: cp .env.example .env")
        print("2. Edit .env and add your TELEGRAM_BOT_TOKEN")
        print("3. Optionally add NEWS_API_KEY for additional news sources")
        print("\n🤖 To create a Telegram bot:")
        print("• Open Telegram and search for @BotFather")
        print("• Send /newbot and follow the instructions")
        print("• Copy the bot token to your .env file")
        print("\nExample .env content:")
        print("TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
        print("NEWS_API_KEY=your_optional_news_api_key")
        return False
    
    # Check if token is present
    with open('.env', 'r') as f:
        content = f.read()
        if 'TELEGRAM_BOT_TOKEN=' not in content or content.count('TELEGRAM_BOT_TOKEN=your_') > 0:
            print("❌ TELEGRAM_BOT_TOKEN not configured in .env file!")
            print("Please edit .env and add your actual bot token.")
            return False
    
    return True

def check_dependencies():
    """Check if virtual environment and dependencies are installed"""
    venv_path = Path('venv')
    
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print("\n📦 Setup Instructions:")
        print("1. Create virtual environment: python3 -m venv venv")
        print("2. Activate it: source venv/bin/activate")
        print("3. Install dependencies: pip install -r requirements.txt")
        return False
    
    # Check if key packages are installed
    try:
        sys.path.insert(0, str(venv_path / 'lib' / 'python3.13' / 'site-packages'))
        import telegram
        print("✅ Dependencies are installed")
        return True
    except ImportError:
        print("❌ Dependencies not installed!")
        print("Please run: source venv/bin/activate && pip install -r requirements.txt")
        return False

def main():
    """Main function to check setup and start the bot"""
    print("🚀 Crypto News Telegram Bot - Quick Start")
    print("=" * 50)
    
    # Check environment file
    if not check_env_file():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ All checks passed!")
    print("🚀 Starting the crypto news bot...\n")
    
    # Import and run the bot
    try:
        from crypto_news_bot import main as run_bot
        run_bot()
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("Please check your TELEGRAM_BOT_TOKEN in the .env file")
        sys.exit(1)

if __name__ == "__main__":
    main()