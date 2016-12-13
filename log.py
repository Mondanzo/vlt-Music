import datetime
import os


class Logger:

    @staticmethod
    def get_time():
        return "{:%S: % M: % H}".format(datetime.datetime.now())

    @staticmethod
    def get_date():
        return "{:%d-%m-%y}".format(datetime.datetime.now())

    @staticmethod
    def get_time():
        return "{:%d-%m-%y %S:%M:%H}".format(datetime.datetime.now())

    def __init__(self, folder):
        self.log_dir = folder
        if not os.path.isdir(self.log_dir):
            os.mkdir(folder)
        self.date = datetime.date.today()

    def print(self, msg: str):
        with open(self.log_dir + "{}.log".format(self.get_date()), "a", encoding="UTF-8") as file:
            file.write("[{}] {}\n".format(self.get_time(), msg))
            file.close()
        print("[{}] {}".format(self.get_time(), msg))
