import telebot
from picamera import PiCamera
import time
import io

# Telegram bot token
TOKEN = '6254032034:AAEc9zXMd_f3FOuWFSn1PGyGz9hOv6tdEMw'

# Telegram chat ID
CHAT_ID = '-1001848432375'

# Create a new Telegram bot instance
bot = telebot.TeleBot(TOKEN)

# Create a new camera object
camera = PiCamera()

# Camera warm-up time
time.sleep(2)

# Capture an image
stream = io.BytesIO()
camera.capture(stream, format='jpeg')
stream.seek(0)

# Send the image to Telegram
bot.send_photo(chat_id=CHAT_ID, photo=stream)

