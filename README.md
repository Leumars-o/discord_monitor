# Discord Server Member Monitor Bot

This is a Discord bot system that monitors server members and sends notifications when new members join. The project includes two separate environments:

- **Self-bot environment** (`selfbot.py` + `self_env`) - Uses discord.py-self to monitor members
- **Real bot environment** (`realbot_server.py` + `real_env`) - Uses official Discord API to send notifications

## ⚠️ Important Security & Legal Warnings

- **self_env** uses discord.py-self which **VIOLATES Discord Terms of Service**
- Self-bots can result in account termination (dont use your main account)
- **real_env** uses official discord.py (recommended for production)
- Each environment is completely isolated with separate dependencies

## Project Structure

```
discord_monitor/
├── selfbot.py                    # Self-bot script (monitors members)
├── realbot_server.py            # Official bot API server (sends notifications)
├── discord_msg_test.py          # Test script for message sending
├── print-env.py                 # Environment diagnostic script
├── setup-self-env.sh           # Linux/Mac setup for self-bot environment
├── setup-real-env.sh           # Linux/Mac setup for real bot environment
├── requirements-common.txt      # Shared dependencies
├── requirements-self-env.txt    # Self-bot specific dependencies
├── requirements-real-env.txt    # Real bot specific dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Prerequisites

- Python 3.9+
- Discord bot token (for real bot)
- Discord user token (for self-bot, **use at your own risk**)
- Target channel ID for notifications

## Environment Setup

### Option 1: Automated Setup (Linux/Mac)

#### Self-bot Environment
```bash
chmod +x setup-self-env.sh
./setup-self-env.sh
```

#### Real Bot Environment
```bash
chmod +x setup-real-env.sh
./setup-real-env.sh
```

### Option 2: Manual Setup

#### For self_env (self-bot environment):
```bash
python -m venv self_env
source self_env/bin/activate  # Linux/Mac
# OR
self_env\Scripts\activate     # Windows

pip install -r requirements-self-env.txt
```

#### For real_env (official bot environment):
```bash
python -m venv real_env
source real_env/bin/activate  # Linux/Mac
# OR  
real_env\Scripts\activate     # Windows

pip install -r requirements-real-env.txt
```

## Environment Configuration

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your values:**
   ```env
   SELF_TOKEN=your_discord_user_token_here
   REAL_TOKEN=your_bot_token_here
   CHANNEL_ID=your_channel_id_here
   API_PORT=8000
   POLL_INTERVAL=30
   ```

### Environment Variables Explained

- `SELF_TOKEN`: Your Discord user account token (**risky to use**)
- `REAL_TOKEN`: Your Discord bot application token
- `CHANNEL_ID`: Target channel ID where notifications will be sent
- `API_PORT`: Port for the FastAPI server (default: 8000)
- `POLL_INTERVAL`: How often to check for new members in seconds (default: 30)

## Running the Programs

### Open two terminal windows:

1. **Start the Real Bot Server** (in terminal 1):
   ```bash
   source real_env/bin/activate
   python realbot_server.py
   ```

2. **Start the Self-bot Monitor** (in terminal 2):
   ```bash
   source self_env/bin/activate
   python selfbot.py
   ```

## How It Works

1. **Self-bot Component** (`selfbot.py`):
   - Logs into Discord using your user token
   - Monitors all servers you're in for new members
   - Polls every `POLL_INTERVAL` seconds for membership changes
   - Sends HTTP POST requests to the FastAPI server when new members join

2. **Real Bot Component** (`realbot_server.py`):
   - Runs a FastAPI web server on the specified port
   - Receives member join notifications from the self-bot
   - Uses official Discord bot API to send notifications to the target channel

## Testing

### Test Message Sending
```bash
source real_env/bin/activate
python discord_msg_test.py
```

### Check Environment Variables
```bash
python print-env.py
```

## Requirements Files Breakdown

- **requirements-common.txt**: Shared dependencies (FastAPI, pydantic, python-dotenv, etc.)
- **requirements-self-env.txt**: Includes common + discord.py-self from GitHub
- **requirements-real-env.txt**: Includes common + official discord.py

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're in the correct virtual environment
2. **Token errors**: Verify your tokens in `.env` file
3. **Permission errors**: Ensure your bot has proper permissions in the target channel
4. **Connection errors**: Check if the API server is running on the correct port

### Getting Discord Tokens

- **Bot Token**: Create a bot application at https://discord.com/developers/applications
- **User Token** (**NOT RECOMMENDED**): Can be obtained from browser dev tools, but violates ToS

### Port Conflicts
If port 8000 is in use, change `API_PORT` in your `.env` file and restart the services.