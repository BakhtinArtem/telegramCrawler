import asyncio
import json
import logging
from telethon import functions, types
import re
from multiprocessing.connection import Client
import string
import os.path
import pickle
from telethon import TelegramClient, errors
from telethon.tl.types import Channel, Dialog, ChatInviteAlready, ChatInvite
from telethon.tl.functions.messages import ImportChatInviteRequest


class Group:
    def __init__(self, id, name, toProcess=set(), edges=set(), parent=set()) -> None:
        self.id = id
        self.name = name
        # groups awaiting to process
        self.toProcess = toProcess
        # processed groups
        self.edges = edges
        self.parent = parent


class Crawler:
    def __init__(self, client: Client) -> None:
        self.client = client
        self.processed = []
        self.CACHE_PATH = "crawlerCache"

    def groupFind(self, id: str):
        for g in self.processed:
            if(g.id == id):
                return g
        return None

    def isGroupProcessed(self, id) -> bool:
        for group in self.processed:
            if(group.id == id):
                return True
        return False

    async def joinGroup(self) -> None:
        for group in self.processed:
            group_count = len(group.toProcess)
            for i in range(group_count):
                try:
                    hash = group.toProcess.pop()
                    # check if user already in group
                    chat_status = await self.client.client(
                        functions.messages.CheckChatInviteRequest(hash))
                    # user is not invited in this chat
                    if(type(chat_status) == ChatInvite):
                        updates = await self.client.client(ImportChatInviteRequest(hash))
                        chat = updates.chats[0]
                        print("Successful joined in: " + chat.title)
                        # -100 is missing in chat id over channel id
                        new_group = Group(
                            id=int("-100"+str(chat.id)), name=chat.title, parent={group})
                        self.updateProcessed(new_group)
                        self.updateProcessed(
                            Group(id=group.id, name=group.name, edges={new_group}))
                        return
                except errors.ChannelInvalidError:
                    print("Channel is invalid")
                    pass
                except errors.ChannelPrivateError:
                    print("Error: Channel is private")
                    pass
                except errors.UserAlreadyParticipantError:
                    print("User is already in group")
                    pass
                except errors.InviteHashExpiredError:
                    print("Group invetation link expired")
                    pass
                except TypeError as err:
                    print(err)
                    return
                    # pass
        print("No group to join found")

    def removeProcessed(self, id: str):
        toBeRemoved = None
        for g in self.processed:
            if(g.id == id):
                toBeRemoved = g
        if(toBeRemoved is not None):
            self.processed.remove(toBeRemoved)

    def updateProcessed(self, group: Group):
        init_group = self.groupFind(group.id)
        if(init_group != None):
            init_group.toProcess = init_group.toProcess.union(group.toProcess)
            init_group.edges = init_group.edges.union(group.edges)
            init_group.parent = init_group.parent.union(group.parent)
        else:
            self.processed.append(group)
        # update cache
        self.serializeProcessed()

    def is_cache_file_exists(self) -> bool:
        return os.path.exists(self.CACHE_PATH)

    def serializeProcessed(self):
        with open(self.CACHE_PATH, "wb") as outfile:
            outfile.truncate(0)
            pickle.dump(self.processed, outfile)

    def deserializedProcessed(self):
        with open(self.CACHE_PATH, "rb") as infile:
            self.processed = pickle.load(infile)

    async def setup(self) -> None:
        self.client.config_process()
        await self.client.auth()
        if(self.is_cache_file_exists()):
            self.deserializedProcessed()
        else:
            # user auth
            # Your mobile number is needed in case of 2FA
            await self.crawl_init()
            self.serializeProcessed()
        print("-----------SETUP COMPLETE-----------")
        print("Processed groups:")
        self.printProcessed()

    async def test(self) -> None:
        await self.crawl_init()

    def printProcessed(self):
        print("id, name, to_process_count, edges_count, parent_group")
        for group in self.processed:
            print(group.id, group.name, len(
                group.toProcess), len(group.edges), len(group.parent), sep="|")
        print("Overall: " + str(len(self.processed)))

    async def crawl_init(self) -> None:
        async for dialog in self.client.client.iter_dialogs():
            if (type(dialog.entity) == Channel):
                links = await self.get_links(dialog)
                self.updateProcessed(
                    Group(id=dialog.id, name=dialog.name, toProcess=links))

    async def get_links(self, dialog: Dialog) -> set:
        link_set = set()
        SEARCH_PART = "https://t.me/"
        try:
            # search uses fuzzy search to find relevant responses
            async for message in self.client.client.iter_messages(dialog.id, search=SEARCH_PART):
                try:
                    # searching for group invetantion link
                    invitation_hash = re.search(
                        '(?<=joinchat\/)(\w+[-]?\S\w+)', message.text).group()
                    link_set.add(invitation_hash)
                # Message without link fires exception, which will be skipped
                except AttributeError as err:
                    pass
        # private channel cant be scanned
        except errors.rpcerrorlist.ChannelPrivateError as err:
            print(err)
            return link_set
        except TypeError as err:
            print("Link processing error " + err)
            pass
        return link_set

    async def exit(self):
        await self.client.client.disconnect()


class Client:
    def __init__(self, configPath: string) -> None:
        self.configPath = configPath
        self.config = None
        self.client = None
        self.api_id = None
        self.api_hash = None

    def config_process(self) -> object:
        with open(self.configPath, 'r') as f:
            self.config = json.load(f)
        try:
            self.api_id = self.config['AUTH']['api_id']
            self.api_hash = self.config['AUTH']['api_hash']
        except:
            print("Config Processing Error")

    async def auth(self) -> None:
        try:
            self.client = TelegramClient(
                'new_session', self.api_id, self.api_hash)
            await self.client.start()
        except ConnectionError:
            print("Connection Error")


if __name__ == '__main__':
    # path to config file
    CONFIG_PATH = "config.json"
    # uncomment for debug logs printing
    # logging.basicConfig(level=logging.DEBUG)

    # setup crawler
    client = Client(CONFIG_PATH)
    crawler = Crawler(client)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawler.setup())
    while(True):
        print("Options:\n1)Crawl \n2)List information\n3)Join one group\n4)Exit\n(write number without brackets)")
        userRespone = input()
        if(userRespone == "1"):
            # TODO: test / reconnect needed
            loop.run_until_complete(crawler.test())
        elif(userRespone == "2"):
            crawler.printProcessed()
        elif(userRespone == "3"):
            loop.run_until_complete(crawler.joinGroup())
        elif(userRespone == "4"):
            loop.run_until_complete(crawler.exit())
            loop.close()
            quit()
        else:
            print("INVALID OPTION")
