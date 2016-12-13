import discord
from asyncio import Queue
from random import shuffle

ytdl_format_options = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'scsearch',
    'source_address': '0.0.0.0'
}


class Song:
    def __init__(self, player, url, title, uploader, user):
        self.player = player,
        self.url = url,
        self.title = title,
        self.uploader = uploader,
        self.user = user


class Playlist:

    # Init a playlist object
    def __init__(self):
        self.__queue = Queue()

    # Add a song with Discords Voice Client and the Youtube Downloader
    async def add(self, song_url: str, voice_client: discord.VoiceClient, user=None):
        try:
            song_player = await voice_client.create_ytdl_player(song_url, ytdl_options=ytdl_format_options)
        except:
            return False
        user_name = "********"
        if user is not None:
            user_name = "__" + user.display_name + "__"
        song = Song(song_player, song_player.url, song_player.title, song_player.uploader, user_name)
        await self.__queue.put(song)
        return song

    # Get next song and delete it
    async def get_next(self):
        item = await self.__queue.get()
        return item

    # Get if queue is empty
    def empty(self):
        return self.__queue.empty()

    # Get the whole queue
    def get(self):
        f_list = list()
        while not self.empty():
            f_list.append(self.__queue.get_nowait())
        for x in f_list:
            self.__queue.put_nowait(x)
        return f_list

    # Get the queue length
    def __len__(self):
        return self.__queue.qsize()

    # Shuffle the whole queue
    def shuffle(self):
        f_list = list()
        while not self.empty():
            f_list.append(self.__queue.get_nowait())
        shuffle(f_list)
        for x in f_list:
            self.__queue.put_nowait(x)
