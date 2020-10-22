from subprocess import Popen, PIPE
import time
import sys
from telethon.sync import TelegramClient
from telethon.sessions import MemorySession

from threading import Thread
from queue import Queue, Empty


lines = Queue(100)

def stream_stdout(args):
    process = Popen(args, stdout=PIPE)
    while process.poll() == None:
        l = process.stdout.readline()
        l = l.decode()
        _, _, timestamp, _, _, *text = l.split(' ')
        l = ' '.join([timestamp] + text)
        lines.put(l)


def main():
    _, api_id, api_hash, bot_token, destination_id, *args = sys.argv
    destination_id = int(destination_id)
    client = TelegramClient(MemorySession(), api_id, api_hash).start(bot_token=bot_token)
    Thread(target=stream_stdout, args=(['journalctl', '-f']+args,)).start()
    last_message = None
    while True:
        if lines.empty():
            time.sleep(0.1)
        else:
            send_lines = []
            while True:
                try:
                    send_lines.append(lines.get(block=False))
                except Empty:
                    break
            sending_message = '\n\n'.join(send_lines)
            editing_message = (last_message.message + '\n\n' + sending_message) if last_message != None else None
            if editing_message and len(editing_message) < 4096:
                last_message = last_message.edit(editing_message)
            else:
                last_message = client.send_message(destination_id, sending_message)
        print(lines.qsize())
        time.sleep(1)


if __name__=='__main__':
    main()
