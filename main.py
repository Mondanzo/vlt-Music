# -*- coding: UTF-8 -*-
import discord
import yaml
import asyncio
import utils
import music
import time
from log import Logger

Reconnect = False
with open("config.yml", "r") as file:
    cfg = yaml.load(file)
    Reconnect = cfg['AutoReconnect']

# TODO: Add Warn Function, implement API, Current Time of the song, fix this crazy bug where all values are Tuples


class Main(discord.Client):

    # Load Opus
    def _load_opus(self):
        discord.opus.load_opus(self.cfg['Opusfile'])
        if discord.opus.is_loaded():
            self.log.print("[INFO] Opus loaded successfully!")
        else:
            self.log.print("[ERROR] An error occured while loading opus!"
                           " The bot won't be able to play music!\nShutting down!")
            exit(1)

    # Start the bot
    def __start_bot(self, token, **kwargs):
        self.loop.run_until_complete(self.start(token, **kwargs))

    # Overriden Functions
    async def delete_message(self, message: discord.Message):
        await super().delete_message(message)

    # Load Allowed Sites
    def _load_allowed_sites(self):
        if self.cfg['AllowedSites'] == "":
            return None
        else:
            return self.cfg['AllowedSites'].split(';')

    # Autojoin feature

    def _get_admin_role(self):
        for s in self.servers:
            for r in s.roles:
                if r.name == self.cfg['AdminRole']:
                    return r
        self.log.print("ERROR Couldn't find a role! Using @everyone instead")
        return None

    def _get_req_skips(self):
        min_skips = 0
        for u in self.voiceClient.channel.voice_members:
            if not u.bot:
                if not u.deaf:
                    min_skips += 1
        return int(min_skips / self.skips)

    @staticmethod
    def _get_time(time):
        m, s = divmod(time, 60)
        return "{}:{}".format(m, s)

    async def _auto_join(self):
        await super().wait_until_ready()
        if self.cfg['Autojoin'] is True:
            self.log.print("[INFO] Autojoin is active!")
            auto_channel = self.get_channel(self.cfg['AutojoinChannel'])
            if auto_channel is not None:
                self.log.print("[AUTOJOIN] Channel found! Connecting...")
                self.voiceClient = await super().join_voice_channel(auto_channel)
                if self.voiceClient is not None:
                    self.log.print("[AUTOJOIN] Done!")
                else:
                    self.log.print("[AUTOJOIN - ERROR] Error! Skipping Autojoin")
            else:
                self.log.print("[AUTOJOIN] Channel was not found! Skipping Autojoin")
        else:
            self.log.print("[INFO] Autojoin is deactivated! skipping it")

    # Delete the message after a delay
    async def ddelete_message(self, message, delay=10):
        await asyncio.sleep(delay)
        await self.delete_message(message)

    # Play next Song
    async def _play_song(self):
        print("_play_song()")
        if self.stream_player is not None and not self.stream_player.is_done():
            self.log.print("Last Streamplayer wasn't done! Stopping it now!")
            self.stream_player.stop()
        next_song = await self.queue.get_next()
        self.stream_player = next_song.player[0]
        self.timer = utils.get_time_in_seconds()
        self.skip_list = []
        setattr(self.stream_player, "after", self._next_song)
        self.log.print("Start playing song...")
        self.is_playing = True
        self.stream_player.volume = self.volume
        await self.change_presence(status=discord.Status.online,
                                   game=discord.Game(name=self.stream_player.title, url=self.stream_player.url,
                                                     type=1))
        self.stream_player.start()

    # Next Song
    def _next_song(self):
        print("_next_song()")
        if len(self.queue) >= 1:
            if not self.stream_player.is_done():
                self.log.print("Streamplayer is not done! Stopping it now!")
                self.stream_player.stop()
            self.log.print("Playing next song...")
            coro = self._play_song()
            fut = asyncio.run_coroutine_threadsafe(coro, self.loop)
            try:
                fut.result()
            except:
                self.log.print("Error while trying to play next song!")
                pass
        else:
            self.is_playing = False
            coru = self.change_presence(status=discord.Status.idle, game=discord.Game(name="{}help".format(self.p)))
            fat = asyncio.run_coroutine_threadsafe(coru, self.loop)
            try:
                fat.result()
            except:
                # an error happened sending the message
                pass

    # Init Function
    def __init__(self):
        super().__init__()

        # Load Config
        self.configPath = "config.yml"
        with open(self.configPath, "r") as config:
            cfg = yaml.load(config)
            self.cfg = cfg

        # Inti default variables.
        self.voiceClient = None
        self.info_channel = None
        self.stream_player = None
        self.is_playing = False
        self.skip_list = list()
        self.role = None
        self.log = Logger("logs/")
        self.conditions = asyncio.Condition()
        self.queue = music.Playlist()
        self.__version__ = '2.7.0'

        # Get the settings from the config.
        self.skips = self.cfg['ReqSkips']
        self.p = self.cfg['Prefix']
        self.volume = self.cfg['Volume']
        self.allowedLinks = self._load_allowed_sites()
        self._load_opus()
        self.__start_bot(self.cfg['Token'], bot=True)

    # On message event (Commands)
    # #MoreCommandsIncomming
    async def on_message(self, msg: discord.Message):
        await super().wait_until_ready()
        if msg.content == "":
            return
        if msg.content.startswith(self.p) or msg.author == self.user:
            self.log.print("[CHATLOG] ({1}) [{2}] <{3}> {4}".format(msg.timestamp, msg.server.name, msg.channel.name,
                                                                    msg.author.display_name, msg.content))
        args = msg.content.split()
        cmd = args[0].lower()
        del(args[0])

        # User commands without Voice Client
        if cmd == self.p + "help":
            await self.delete_message(msg)
            await self.send_message(msg.author,
                                    """--------------------------------- HELP ------------------------------------------
                                    User Commands:
                                    - {0}help - Shows this Help.
                                    - {0}play <Song Url> - adds a Song to the playlist from a link.
                                    - {0}skip - Vote to skip the current song. You can only skip one time per song.
                                    - {0}queue - Shows the current queue.
                                    - {0}np - Shows the currently playing song (If a song is playing)
                                    - {0}status - Shows the currently playing song (If a song is playing)

                                    Admin Commands:
                                    - {0}shutdown{0} - Turns the bot off.
                                    - {0}connect <Channel Name> - Connect the bot to the entered channel.
                                    - {0}disconnect - Closes all connections and stop playing music.
                                                               """.format(self.p))
            await self.ddelete_message(await self.send_message(msg.channel,
                                                               ":information_source: Check your private chat!"
                                                               " :information_source:"))
        elif cmd == self.p + "version":
            await self.delete_message(msg)
            await self.ddelete_message(await self.send_message(msg.channel,
                                                               "You're using the vlt. Music Bot" +
                                                               " \nby Mondanzo\nVersion: {}".format(
                                                                   self.__version__
                                                               )))
        # Admin commands without Voice
        elif cmd == self.p + "shutdown" + self.p and self.role in msg.author.roles:
            await self.delete_message(msg)
            await self.send_message(msg.channel, "Shutting down! Goodbye :hand_splayed:")
            self.log.print("[INFO] Shutting down...")
            await super().logout()
            exit(1)
        elif cmd == self.p + "connect" and self.role in msg.author.roles:
            await self.delete_message(msg)
            if self.is_voice_connected(msg.server):
                await self.ddelete_message(self.send_message(msg.channel, "[ERROR]"
                                                                          " I'm already connected to a channel!"))
            if len(args) >= 1:
                await self.delete_message(msg)
                channel = utils.get_channel_by_name(msg.server, ''.join(args), stype=discord.ChannelType.voice)
                if not channel:
                    await self.ddelete_message(await self.send_message(msg.channel,
                                                                       "[ERROR] Channel was not found! " +
                                                                       ":negative_squared_cross_mark:"))
                    return
                self.voiceClient = await super().join_voice_channel(channel)
                if self.is_voice_connected(msg.server):
                    await self.ddelete_message(
                        await self.send_message(msg.channel, "[INFO] Connected successfully! :ok_hand:"))

        # Commands WITH VoiceClient
        elif self.voiceClient is not None:
            # Admin Commands
            if cmd == self.p + "disconnect":
                await self.delete_message(msg)
                await self.voiceClient.disconnect()

            # User Commands

            # play Command (Adds Songs)
            if cmd == self.p + "play":
                await self.delete_message(msg)
                if len(args) >= 1:
                    if self.allowedLinks is not None:
                        if any(args[0].startswith(x) for x in self.allowedLinks):
                            song = await self.queue.add(args[0], self.voiceClient, msg.author)
                            if isinstance(song, music.Song):
                                if self.is_playing is False:
                                    self.loop.create_task(self._play_song())
                                await self.ddelete_message(
                                    await self.ddelete_message(await super().send_message(msg.channel,
                                                               "Added your Song {} successfully! {}".format(
                                                                   song.title[0],
                                                                   msg.author.mention))), delay=5)
                    else:
                        song = await self.queue.add(msg.content.replace("{}play ".format(self.p), ""), self.voiceClient,
                                                    msg.author)
                        if isinstance(song, music.Song):
                            if self.is_playing is False:
                                self.loop.create_task(self._play_song())
                            await self.ddelete_message(
                                await super().send_message(msg.channel,
                                                           "Added your Song {} successfully! {}".format(
                                                               song.title[0],
                                                               msg.author.mention)), delay=5)
                        else:
                            await self.ddelete_message(await super().send_message(msg.channel,
                                                                                  "[ERROR] Couldn't add your song!" +
                                                                                  "\nUnknown error"
                                                                                  .format(self.p)), delay=5)
                else:
                    await self.ddelete_message(await super().send_message(msg.channel,
                                                                          "[ERROR] Wrong Command! Use: `{}play <Link>`!"
                                                                          .format(self.p)))
            # queue Command
            elif cmd == self.p + "queue":
                await self.delete_message(msg)
                if not self.queue.empty():
                    queue = ""
                    number = 1
                    for item in self.queue.get():
                        queue += "\n{0}. **{1}** by *{2}*, submitted by __{3}__\n".format(number, item.title[0],
                                                                                          item.uploader[0],
                                                                                          item.user[0])
                        number += 1
                    await self.ddelete_message(
                        await super().send_message(msg.channel, "__**[Queue]**__\n{}".format(queue)))

            # Skip Command
            elif cmd == self.p + "skip":
                if not msg.author.id in self.voiceClient.channel.voice_members:
                    return
                await self.delete_message(msg)
                if msg.author.id not in self.skip_list:
                    self.skip_list.append(msg.author.id)
                    self.ddelete_message(await super().send_message(msg.channel,
                                                                    "{} voted to Skip! **{}/{} want to Skip**".format(
                                                                        msg.author.mention,
                                                                        len(self.skip_list),
                                                                        self._get_req_skips()
                                                                    )))
                else:
                    self.ddelete_message(
                        await super().send_message(msg.channel, "**{}/{} want to Skip!**".format(len(self.skip_list),
                                                                                                 self._get_req_skips()))
                                                                                                )
                if self._get_req_skips() <= len(self.skip_list):
                    setattr(self.stream_player, "after", None)
                    self.stream_player.stop()
                    if not self.queue.empty():
                        self.loop.create_task(self._play_song())
                    else:
                        self.is_playing = False
                        await self.change_presence(status=discord.Status.idle,
                                                   game=discord.Game(name="{}help".format(self.p)))
                    await self.ddelete_message(await
                                               super().send_message(msg.channel,
                                                                    "Enough users voted to skip!\n"
                                                                    "**Skipping NOW**"), delay=5)

            # Now Playing Command (Status)
            elif cmd == self.p + "np" or cmd == self.p + "status":
                await self.delete_message(msg)
                if self.stream_player.is_playing():
                    await self.ddelete_message(await super().send_message(msg.channel,
                                                                          "Now playing **{}** by _{}_! [{}-{}]"
                                                                          "\n{}".format(
                                                                              self.stream_player.title,
                                                                              self.stream_player.uploader,
                                                                              self._get_time(
                                                                                  utils.get_time_in_seconds() -
                                                                                  self.timer),
                                                                              self._get_time(
                                                                                  self.stream_player.duration),
                                                                              self.stream_player.url)))

        # ############## #
        # OnReady Method #
        # ############## #
    async def on_ready(self):
        self.log.print("[INFO] Bot started!")
        self.log.print("[INFO] Logged in as: {}".format(self.user))
        if len(self.servers) > 1:
            self.log.print("[WARNING] You're Bot is connected to more than 1 server! This could case some bugs")
        elif len(self.servers) == 1:
            self.log.print("[INFO] You're Bot is connected to 1 server! This is perfect!")
        else:
            self.log.print("[WARNING] You're Bot isn't connected to any server! Why?")
        await self._auto_join()
        self.role = self._get_admin_role()
        await self.change_presence(status=discord.Status.idle, game=discord.Game(name="{}help".format(self.p)))
        # ############# #
        # Advertisement #
        # ############# #

Main()
while Reconnect:
    try:
        print("Bot is starting!")
        Main()
    finally:
        print("Bot is offline!")
