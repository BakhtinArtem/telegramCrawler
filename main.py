import asyncio
import json
import logging
from multiprocessing.connection import Client
import string
from typing import Iterator, List
from telethon import TelegramClient, events
from telethon.tl.types import Channel, Chat, Dialog


class Crawler:
    def __init__(self, client: Client) -> None:
        self.client = client

    async def setup(self) -> None:
        self.client.configProcess()
        # user auth
        # Your mobile number is needed in case of 2FA
        await self.client.auth()
        await self.crawler_init()

    # sync deleted
    async def crawler_init(self) -> None:
        async for dialog in self.client.client.iter_dialogs():
            if type(dialog.entity) == Channel:
                print(f'{dialog.id}:{dialog.title}')


class Client:
    def __init__(self, configPath: string) -> None:
        self.configPath = configPath
        self.config = None
        self.client = None
        self.api_id = None
        self.api_hash = None

    def configProcess(self) -> object:
        with open(self.configPath, 'r') as f:
            self.config = json.load(f)
        try:
            self.api_id = self.config['AUTH']['api_id']
            self.api_hash = self.config['AUTH']['api_hash']
        except:
            print("Config Processing Error")

    async def auth(self) -> None:
        self.client = TelegramClient('new_session', self.api_id, self.api_hash)
        await self.client.start()


if __name__ == '__main__':
    # path to config file
    CONFIG_PATH = "config.json"
    # for debug purposes
    logging.basicConfig(level=logging.DEBUG)

    client = Client(CONFIG_PATH)
    crawler = Crawler(client)
    asyncio.run(crawler.setup())
