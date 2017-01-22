import discord
import youtube_dl
from asyncio import Queue
from random import shuffle

ytdl_format_options = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'verbose': False,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}


class Playlist:

    # Init a playlist object
    def __init__(self):
        self.__queue = Queue()

    # Add a song with Discords Voice Client and the Youtube Downloader
    async def add(self, song_url: str, voice_client: discord.VoiceClient, user=None):
        try:
            song_player = await voice_client.create_ytdl_player(song_url, ytdl_options=ytdl_format_options)
        except youtube_dl.DownloadError:
            return youtube_dl.DownloadError
        except youtube_dl.SameFileError:
            return youtube_dl.SameFileError
        except youtube_dl.utils.ExtractorError:
            return youtube_dl.utils.ExtractorError
        except youtube_dl.utils.UnavailableVideoError:
            return youtube_dl.utils.UnavailableVideoError
        user_name = "********"
        if user is not None:
            user_name = user.display_name
        song = {"player": None, "url": song_player.url, "title": song_player.title,
                "uploader": song_player.uploader, "user": user_name}
        await self.__queue.put(song)
        return song

    # Get next song and delete it
    async def pop(self, voice_client: discord.VoiceClient):
        item = await self.__queue.get()
        item['player'] = await voice_client.create_ytdl_player(item['url'], ytdl_options=ytdl_format_options)
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
