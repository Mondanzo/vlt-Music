import discord
import yaml
import asyncio
import utils
import music

Reconnect = False
with open("config.yml", "r") as file:
    cfg = yaml.load(file)
    Reconnect = cfg['AutoReconnect']

# TODO: Add Warn Function, implement API, Now Playing Command, Skip Command, FIX THE F*CKING QUEUE


class Main(discord.Client):

    # Load Opus
    def _load_opus(self):
        discord.opus.load_opus(self.cfg['Opusfile'])
        if discord.opus.is_loaded():
            print("[INFO] Opus loaded successfully!")
        else:
            print("[ERROR] An error occured while loading opus! The bot won't be able to play music!\nShutting down!")
            exit(1)

    # Start the bot
    def __start_bot(self, *args):
        self.loop.run_until_complete(self.start(*args))

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
        print("ERROR Couldn't find a role! Using @everyone instead")
        return None

    async def _auto_join(self):
        await super().wait_until_ready()
        if self.cfg['Autojoin'] is True:
            print("[INFO] Autojoin is active!")
            auto_channel = self.get_channel(self.cfg['AutojoinChannel'])
            if auto_channel is not None:
                print("[INFO] Channel found! Connecting...")
                self.voiceClient = await super().join_voice_channel(auto_channel)
                if self.voiceClient is not None:
                    print("[INFO] Done!")
                else:
                    print("[ERROR] Error! Skipping Autojoin")
            else:
                print("[ERROR] Channel was not found! Skipping Autojoin")
        else:
            print("[INFO] Autojoin is deactivate! skip it")

    # Delete the message after a delay
    async def ddelete_message(self, message, delay=15):
        await asyncio.sleep(delay)
        await self.delete_message(message)

    # Play next Song
    async def _play_song(self):
        if self.stream_player is not None and not self.stream_player.is_done():
            print("Last Streamplayer wasn't done! Stopping him now!")
            self.stream_player.stop()
        next_song = await self.queue.get_next_song()
        self.stream_player = next_song[0]
        setattr(self.stream_player, "after", self._next_song)
        print("Start playing song...")
        self.is_playing = True
        self.stream_player.start()

    # Next Song
    def _next_song(self):
        if self.queue.get_queue_length() >= 1:
            print("Playing next song...")
            coro = self._play_song()
            fut = asyncio.run_coroutine_threadsafe(coro, self.loop)
            try:
                fut.result()
            except:
                # an error happened sending the message
                pass
        self.is_playing = False

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
        self.role = None
        self.conditions = asyncio.Condition()
        self.queue = music.Playlist()

        # Get the settings from the config.
        self.prefix = self.cfg['Prefix']
        self.allowedLinks = self._load_allowed_sites()
        self._load_opus()

        self.__start_bot(self.cfg['Token'])

    # On message event (Commands)
    # #MoreCommandsIncomming
    async def on_message(self, message: discord.Message):
        await super().wait_until_ready()
        if message.content == "":
            return
        if message.content.startswith(self.prefix):
            print("[LOG:{0}] ({1}) [{2}] <{3}> {4}".format(message.timestamp, message.server.name, message.channel.name,
                                                           message.author.display_name, message.content))
        args = message.content.split()
        cmd = args[0]
        del(args[0])

        # User commands without Voice Client
        if cmd == self.prefix + "help":
            await self.send_message(message.author,
"""--------------------------------- HELP ------------------------------------------
User Commands:
- {0}help - Shows this Help.
- {0}play <Song Url> - adds a Song to the playlist from a link.
~~- {0}skip - Vote to skip the current song. You can only skip one time per song.~~
- {0}queue - Shows the current queue.

Admin Commands:
- {0}shutdown{0} - Turns the bot off.
- {0}connect <Channel Name> - Connect the bot to the entered channel.
- {0}disconnect - Closes all connections and stop playing music.
                           """.format(self.prefix))
            await self.ddelete_message(await self.send_message(message.channel,
                                                   ":information_source: Check your private chat! :information_source:"))
        elif cmd == self.prefix + "version":
            await self.ddelete_message(await self.send_message(message.channel,
                                                               "Your using the vlt. Music Bot" +
                                                               " \nby Mondanzo\nVersion: {}".format(
                                                                   "2.0"
                                                               )))
        # Admin commands without Voice
        elif cmd == self.prefix + "shutdown" + self.prefix and self.role in message.author.roles:
            await self.send_message(message.channel, "Shutting down! Goodbye :hand_splayed:")
            await super().logout()
            exit(1)
        elif cmd == self.prefix + "connect" and self.role in message.author.roles:
            if self.is_voice_connected(message.server):
                await self.ddelete_message(self.send_message(message.channel, "[ERROR] I'm already connected to a channel!"))
            if len(args) >= 1:
                await self.delete_message(message)
                channel = utils.get_channel_by_name(message.server, ''.join(args), stype=discord.ChannelType.voice)
                if not channel:
                    await self.ddelete_message(await self.send_message(message.channel,
                                                                 "[ERROR] Channel was not found! " +
                                                                 ":negative_squared_cross_mark:"))
                    return
                self.voiceClient = await super().join_voice_channel(channel)
                if self.is_voice_connected(message.server):
                    await self.ddelete_message(
                        await self.send_message(message.channel, "[INFO] Connected successfully! :ok_hand:"))

        # User Commands WITH VoiceClient
        elif self.voiceClient is not None:
            # play Command (Adds Songs) TODO: Add Search Feature
            if cmd == self.prefix + "play":
                if len(args) >= 1:
                    if self.allowedLinks is not None:
                        if any(args[0].startswith(x) for x in self.allowedLinks):
                            if await self.queue.add_song(args[0], self.voiceClient, message.author):
                                if self.is_playing is False:
                                    self.loop.create_task(self._play_song())
                                await self.delete_message(message)
                                await self.ddelete_message(
                                    await super().send_message(message.channel,
                                                               "Added your Song successfully! " + message.author.mention))
                    elif await self.queue.add_song(args[0], self.voiceClient, message.author):
                        if self.is_playing is False:
                            self.loop.create_task(self._play_song())
                        await self.delete_message(message)
                        await self.ddelete_message(
                            await super().send_message(message.channel,
                                                       "Added your Song successfully! " + message.author.mention))
                else:
                    await self.delete_message(message)
                    await self.ddelete_message(await super().send_message(message.channel,
                                                                          "[ERROR] Wrong Command! Use: `{}play <Link>`!"
                                                                          .format(self.prefix)))

            elif cmd == self.prefix + "queue":
                if not self.queue.is_empty():
                    queue = ""
                    number = 1
                    for item in self.queue.get_queue():
                        queue += "\n{0}. **{1}** by *{2}*, submitted by {3}\n".format(number, item[1]['title'],
                                                                                      item[1]['uploader'],
                                                                                      item[1]['user'])
                        number += 1
                    await self.ddelete_message(
                        await super().send_message(message.channel, "__**[Queue]**__\n{}".format(queue)))

        # ############## #
        #                #
        # OnReady Method #
    async def on_ready(self):
        print("[INFO] Bot started!")
        print("[INFO] Logged in as: {}".format(self.user))
        if len(self.servers) > 1:
            print("[INFO] You're Bot is connected to more than 1 server! This could case some bugs")
        elif len(self.servers) == 1:
            print("[INFO] You're Bot is connected to 1 server! This is perfect!")
        else:
            print("[INFO] You're Bot isn't connected to any server! Why?")
        await self._auto_join()
        self.role = self._get_admin_role()

Main()
while Reconnect:
    try:
        Main()
    finally:
        print("Bot is offline!")
