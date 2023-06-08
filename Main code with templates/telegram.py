import telebot
import subprocess

# Set your Telegram bot token here
TOKEN = '-'

# Set your specific Telegram chat ID here
SPECIFIC_CHAT_ID = '-'

# Create the bot instance
bot = telebot.TeleBot(TOKEN)

# Function to handle the '/start' command
@bot.message_handler(commands=['start'])
def start(message):
    if str(message.chat.id) == SPECIFIC_CHAT_ID:
        bot.send_message(chat_id=message.chat.id, text="Welcome! Use the /turnon or /turnoff command to control the program.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Sorry, you are not authorized to use this bot.")

# Function to handle the '/turnon' command
@bot.message_handler(commands=['turnon'])
def turn_on(message):
    if str(message.chat.id) == SPECIFIC_CHAT_ID:
        # Code to turn on the program
        subprocess.Popen(['python', 'app.py'])  # Replace 'app.py' with your program's filename
        bot.send_message(chat_id=message.chat.id, text="Program turned on.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Sorry, you are not authorized to use this command.")

# Function to handle the '/turnoff' command
@bot.message_handler(commands=['turnoff'])
def turn_off(message):
    if str(message.chat.id) == SPECIFIC_CHAT_ID:
        # Code to turn off the program
        subprocess.call(['pkill', '-f', 'app.py'])  # Replace 'app.py' with your program's filename
        bot.send_message(chat_id=message.chat.id, text="Program turned off.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Sorry, you are not authorized to use this command.")

# Function to handle incoming messages
@bot.message_handler(func=lambda message: True)
def echo(message):
    if str(message.chat.id) == SPECIFIC_CHAT_ID:
        # Check if the message is either "turnon" or "turnoff"
        if message.text.lower() == 'turnon':
            turn_on(message)
        elif message.text.lower() == 'turnoff':
            turn_off(message)
    else:
        bot.send_message(chat_id=message.chat.id, text="Sorry, you are not authorized to use this bot.")

# Start the bot
bot.polling()
