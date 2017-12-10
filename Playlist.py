import youtube_dl
import random
import asyncio


class Playlist:
    # Add a new Song to the Playlist
    def add_song(self, url, user=None):
        try:
            info = self.ytdl.extract_info(url)
            # Song Object
            self.__list.append({
                "user": user,
                "info": {
                    "url": info['webpage_url'],
                    "uploader": info['uploader'],
                    "title": info['title'],
                    "duration": info['duration'],
                    "thumbnails": info['thumbnails'],
                    "extractor": info['extractor']
                }
            })
            return len(self.__list) - 1
        except youtube_dl.utils.GeoRestrictedError as e:
            return e
        except Exception as e:
            return e

    # ###### #
    # Events #
    # ###### #

    # Update Events
    def __update_events(self):
        if len(self.__list) <= 0:
            self._is_empty.set()
            self._is_not_empty.clear()
        else:
            self._is_empty.clear()
            self._is_not_empty.set()

    # ########### #
    # Empty Event #
    # ########### #

    # Is Empty?
    def empty(self):
        return self._is_empty.is_set()

    # Blocking Empty
    async def wait_for_empty(self):
        return await self._is_empty.wait()

    # ############### #
    # Not Empty Event #
    # ############### #

    # Blocking Not Empty
    def wait_for_item(self):
        return

    # Get the next Object of the Playlist and remove it
    def next(self):
        item = self.__list.pop()
        self.__update_events()
        return item

    # Randomize the Playlist
    def shuffle(self):
        random.shuffle(self.__list)

    # Clear the Playlist and it's whole content
    def clear(self):
        self.__list.clear()
        self.__update_events()

    # Initialize a new Playlist Object
    def __init__(self, loop=None):
        self.ytdl = youtube_dl.YoutubeDL({"simulate": True, "quiet": True, "no_warnings": True})
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.__list = list()
        self._is_empty = asyncio.Event(loop=self.loop)
        self._is_not_empty = asyncio.Event(loop=self.loop)

    # Destructor
    def __del__(self):
        if self.loop.is_running():
            self.loop.close()
