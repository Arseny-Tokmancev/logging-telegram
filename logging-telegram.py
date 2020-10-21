from subprocess import Popen, PIPE

import sys
from telethon.sync import TelegramClient, MemorySession

destination_id, bot_token, api_id, api_hash, *args = sys.argv
client = TelegramClient(MemorySession(), api_id, api_hash).start(bot_token=bot_token)
journald = Popen(['journalctl']+args, stdout=PIPE, stderr=PIPE)
while journald.poll() == None:
    client.send_message(destination_id, journald.read())
