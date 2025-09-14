## Discord Server Member Monitor Bot
This is a Discord bot that monitors the number of members in a server and sends a message to a specified channel when the member count reaches a certain threshold.


## Manual Installation Commands

### For self_env (self-bot environment):
```bash
python -m venv self_env
source self_env/bin/activate  # Linux/Mac
# OR
self_env\Scripts\activate     # Windows

pip install -r requirements-self-env.txt
```

### For real_env (official bot environment):
```bash
python -m venv real_env
source real_env/bin/activate  # Linux/Mac
# OR  
real_env\Scripts\activate     # Windows

pip install -r requirements-real-env.txt
```

## ⚠️ Important Notes

- **self_env** uses discord.py-self (violates Discord ToS)
- **real_env** uses official discord.py (recommended for production)
- Each environment is completely isolated
- The `-r requirements-common.txt` line includes shared dependencies