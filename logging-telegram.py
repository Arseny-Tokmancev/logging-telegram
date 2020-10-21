from subprocess import Popen, PIPE

import sys
from telethon.sync import TelegramClient
from telethon.sessions import MemorySession

_, api_id, api_hash, bot_token, destination_id, *args = sys.argv
destination_id = int(destination_id)
client = TelegramClient(MemorySession(), api_id, api_hash).start(bot_token=bot_token)
journald = Popen(['journalctl', '-f']+args, stdout=PIPE, stderr=PIPE)
while journald.poll() == None:
    message = journald.stdout.readline()
    errors  = None#journald.stderr.readline()
    if message:
        message = message.decode()
        print(message)
        client.send_message(destination_id, message)
    if errors:
        print('errors:', errors)
        client.send_message(destination_id, 'errors:'+errors)
