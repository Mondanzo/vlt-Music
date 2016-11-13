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
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}


class Playlist:

    # Init a playlist object
    def __init__(self):
        self.__queue = Queue()

    # Add a song with Discords Voice Client and the Youtube Downloader
    async def add_song(self, song_url: str, voice_client: discord.VoiceClient, user=None):
        song_player = await voice_client.create_ytdl_player(song_url, ytdl_options=ytdl_format_options)
        user_name = "********"
        if user is not None:
            user_name = "__" + user.display_name + "__"
        if self.get_queue_length() >= 1:
            await self.__queue.put([False, {"url": song_player.url, "title": song_player.title, "uploader": song_player.uploader, "user": user_name}])
        else:
            await self.__queue.put(
                [song_player,
                 {"url": song_player.url, "title": song_player.title, "uploader": song_player.uploader,
                  "user": user_name}])
        return True

    # Get next song and delete it
    async def get_next_song(self):
        item = await self.__queue.get()
        if item[0] is False:
            return await item[1]['url'].create_ytdl_player(item[1]['url'], ytdl_options=ytdl_format_options)
        return item

    # Get if queue is empty
    def is_empty(self):
        return self.__queue.empty()

    # Get the whole queue
    def get_queue(self):
        f_list = list()
        while not self.is_empty():
            f_list.append(self.__queue.get_nowait())
        for x in f_list:
            self.__queue.put_nowait(x)
        return f_list

    # Get the queue length
    def get_queue_length(self):
        return self.__queue.qsize()

    # Shuffle the whole queue
    def shuffle_queue(self):
        shuffle(self.__queue)
