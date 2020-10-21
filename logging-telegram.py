from subprocess import Popen, PIPE

import sys
from telethon.sync import TelegramClient
from telethon.sessions import MemorySession

_, api_id, api_hash, bot_token, destination_id, *args = sys.argv
destination_id = int(destination_id)
client = TelegramClient(MemorySession(), api_id, api_hash).start(bot_token=bot_token)
journald = Popen(['journalctl', '-f']+args, stdout=PIPE, stderr=PIPE)
last_message = None
while journald.poll() == None:
    message = journald.stdout.readline()
    if message:
        message = message.decode()
        _, _, timestamp, _, _, *message_text = message.split(' ')
        message = ' '.join([timestamp] + message_text)
        # print(message)
        # print(last_message.message)
        editing_message = last_message.message + '\n\n' + message
        if last_message == None or (len(editing_message) > 4096):
            last_message = client.send_message(destination_id, message)
        else:
            last_message = last_message.edit(editing_message)
