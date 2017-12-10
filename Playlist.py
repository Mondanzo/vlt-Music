import youtube_dl
import random


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

    # Get the next Object of the Playlist and remove it
    def next(self):
        return self.__list.pop()

    # Randomize the Playlist
    def shuffle(self):
        random.shuffle(self.__list)

    # Clear the Playlist and it's whole content
    def clear(self):
        self.__list.clear()

    # Initialize a new Playlist Object
    def __init__(self):
        self.ytdl = youtube_dl.YoutubeDL({"simulate": True, "quiet": True, "no_warnings": True})
        self.__list = list()
