import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

user_token = os.getenv("SELF_TOKEN")

# Token validation
if not user_token:
    print("❌ REAL_TOKEN not found in .env file")
    exit(1)

print(f"Token length: {len(user_token)}")
print(f"Token preview: {user_token[:10]}...{user_token[-4:]}")

# Check token format
if user_token.startswith('Bot '):
    print("⚠️  Token appears to be a bot token (starts with 'Bot ')")
    print("For user tokens, remove the 'Bot ' prefix")
elif user_token.startswith('mfa.'):
    print("✅ Token appears to be a user token (starts with 'mfa.')")
elif len(user_token) > 50:
    print("✅ Token length looks correct for user token")
else:
    print("⚠️  Token format may be incorrect")

url = "https://discord.com/api/v9/channels/1398068613365108871/messages"

headers = {
    'authorization': user_token,
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

msg = {
    'content': 'gm channel!'
}

# Send the request and capture the response
response = requests.post(url, headers=headers, json=msg)

# Check if the request was successful
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    print("✅ Message sent successfully!")
    
    # Parse and display the response data
    message_data = response.json()
    print(f"Message ID: {message_data.get('id')}")
    print(f"Message Content: {message_data.get('content')}")
    print(f"Timestamp: {message_data.get('timestamp')}")
    print(f"Channel ID: {message_data.get('channel_id')}")
    
elif response.status_code == 401:
    print("❌ Authentication failed - Invalid token")
    
elif response.status_code == 403:
    print("❌ Forbidden - No permission to send messages to this channel")
    
elif response.status_code == 404:
    print("❌ Channel not found")
    
elif response.status_code == 429:
    print("❌ Rate limited - Too many requests")
    retry_after = response.json().get('retry_after', 'Unknown')
    print(f"Retry after: {retry_after} seconds")
    
else:
    print(f"❌ Failed to send message")
    print(f"Error: {response.text}")

# Optional: Print full response for debugging
print("\n--- Full Response ---")
print(f"Headers: {dict(response.headers)}")
try:
    print(f"JSON Response: {json.dumps(response.json(), indent=2)}")
except:
    print(f"Raw Response: {response.text}")