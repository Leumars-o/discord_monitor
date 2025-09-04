import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("SELF_TOKEN")
print(f"Bot token: {bot_token}")

user_token = os.getenv("REAL_TOKEN")
print(f"User token: {user_token}")

channel = os.getenv("CHANNEL_ID")
print(f"Channel ID: {channel}")