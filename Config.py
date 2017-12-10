import yaml
import os
import requests


class Config:

    # Create Config file (protected)
    def _create(self):
        print("Creating Config File")
        # Only create if file isn't existing already
        if not self._exists():
            # Open Stream
            with open(self.dir_link, 'a', encoding="UTF-8") as file:
                print("Downloading Config File")
                request = requests.get("https://raw.githubusercontent.com/Mondanzo/vlt-Music/master/config.yml")
                if request.text is not None:
                    file.write(request.text)
                file.close()

    # Test if File Exists (private)
    def _exists(self):
        if os.path.exists(self.dir_link):
            if os.path.isfile(self.dir_link):
                return True
        return False

    # Save Config File
    def save(self):
        if self._exists():
            # Open Stream
            with open(self.dir_link, 'w', encoding="UTF-8") as file:
                yaml.dump(self.__dict__, file)
                file.close()
        else:
            self._create()
            self.load()

    # Load Config file
    def load(self):
        print("Loading Config...", end="")
        if self._exists():
            # Open Stream
            with open(self.dir_link, 'r', encoding="UTF-8") as file:
                self.__dict__ = yaml.load(file)
                file.close()
        else:
            self._create()
            self.load()
        print("Done")

    def __getitem__(self, item):
        assert isinstance(item, str)
        if self.__dict__[item] is not None:
            return self.__dict__[item]
        else:
            return None

    # Initialization
    def __init__(self, dire="config.yml"):
        self.__dict__ = dict()
        self.dir_link = dire
        self.load()
