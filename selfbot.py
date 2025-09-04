import os
import asyncio
import logging
import datetime
from dotenv import load_dotenv
import discord
from discord.ext import tasks
import httpx

load_dotenv()
TOKEN = os.getenv("SELF_TOKEN")
API_URL = f"http://127.0.0.1:{os.getenv('API_PORT')}/notify"
POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "30"))

logging.basicConfig(level=logging.INFO)

client = discord.Client()
known_members = {}

@client.event
async def on_ready():
    logging.info(f"[{datetime.datetime.now()}] Self-bot logged in as {client.user}")
    for guild in client.guilds:
        known_members[guild.id] = {m.id for m in guild.members}
    poll_new_members.start()

@client.event
async def on_member_join(member):
    try:
        guild_id = member.guild.id
        if member.id not in known_members.get(guild_id, set()):
            known_members.setdefault(guild_id, set()).add(member.id)
            await notify_real_bot(member.guild.name, member)
    except Exception:
        logging.exception("Error in on_member_join fallback")

@tasks.loop(seconds=POLL_INTERVAL)
async def poll_new_members():
    for guild in client.guilds:
        try:
            current = {m.id for m in guild.members}
            previous = known_members.get(guild.id, set())
            new = current - previous
            if new:
                for member in guild.members:
                    if member.id in new:
                        await notify_real_bot(guild.name, member)
                        known_members[guild.id].add(member.id)
        except Exception:
            logging.exception(f"Polling error in {guild.name}")

async def notify_real_bot(guild_name, member):
    payload = {
        "guild": guild_name,
        "username": member.name,
        "discriminator": member.discriminator
    }
    async with httpx.AsyncClient() as http_client:
        await http_client.post(API_URL, json=payload)

if __name__ == "__main__":
    client.run(TOKEN)