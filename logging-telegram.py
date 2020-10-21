import subprocess, sys
from telethon import TelegramClient, MemorySession

destination_id, bot_token, api_id, api_hash, *args = sys.argv
client = await TelegramClient(MemorySession(), api_id, api_hash).start(bot_token=bot_token)
