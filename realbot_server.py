import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import discord
import asyncio
from contextlib import asynccontextmanager

load_dotenv()
TOKEN = os.getenv("REAL_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

logging.basicConfig(level=logging.INFO)

# Global bot instance
bot = discord.Client(intents=discord.Intents.default())

class JoinEvent(BaseModel):
    guild: str
    username: str
    discriminator: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the Discord bot
    bot_task = asyncio.create_task(bot.start(TOKEN))
    
    # Wait a bit for the connection to establish
    for _ in range(30):  # Try for 30 seconds
        if bot.is_ready():
            break
        await asyncio.sleep(1)
    else:
        logging.error("Bot failed to connect within 30 seconds")
        bot_task.cancel()
        raise RuntimeError("Bot startup failed")
    
    logging.info(f"Real bot ready as {bot.user}")
    
    yield
    
    # Shutdown: Close the bot
    await bot.close()
    bot_task.cancel()
    try:
        await bot_task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

@app.post("/notify")
async def notify(event: JoinEvent):
    try:
        await send_message(event)
        return {"status": "sent"}
    except Exception as e:
        logging.exception("Failed to queue message")
        raise HTTPException(status_code=500, detail=str(e))

async def send_message(ev: JoinEvent):
    if not bot.is_ready():
        await bot.wait_until_ready()
    
    ch = bot.get_channel(CHANNEL_ID)
    if not ch:
        logging.error(f"Invalid CHANNEL_ID {CHANNEL_ID} or channel not found")
        return
    
    msg = f"📥 New user **{ev.username}#{ev.discriminator}** joined **{ev.guild}**"
    try:
        await ch.send(msg)
        logging.info(f"Sent notification for {ev.username}#{ev.discriminator} in {ev.guild}")
    except Exception:
        logging.exception("Failed to send message from real bot")

@bot.event
async def on_ready():
    logging.info(f"Real bot ready as {bot.user}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT", "8000")))