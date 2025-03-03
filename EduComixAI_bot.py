import telebot
import logging
import os
from dotenv import load_dotenv  # Import load_dotenv
from main import generate_comic  # Import the generate_comic function from main.py

# Load environment variables from .env
load_dotenv()

# Get the bot token from the environment variable
TOKEN = os.getenv('BOT_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a bot instance
bot = telebot.TeleBot(TOKEN)

# Handler for the /start command
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me some text, and I will make a comic out of it.")

# Text message handler
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        # Generate a comic using the generate_comic function from main.py
        comic_file = generate_comic(message.text)

        if comic_file:
            # Send the comic to the user
            with open(comic_file, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.reply_to(message, "Failed to generate the comic.")

    except Exception as e:
        logging.exception("Error processing message:")
        bot.reply_to(message, "An error occurred while processing your request.")

# Start the bot
if __name__ == '__main__':
    logging.info("Starting Telegram bot...")
    bot.infinity_polling()