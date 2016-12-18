import time
import discord


# Get Channel by Name and Type
def get_channel_by_name(server: discord.Server, channel_name: str, stype=discord.ChannelType.text):
    for channel in server.channels:
        if channel.name == channel_name and channel.type == stype:
            return channel
    else:
        return False


# Get Current time in Seconds
def get_time_in_seconds():
    return int(time.time())


# Get Channel by Name and Type
def get_server_by_name(client_instance: discord.client, server_name: str):
    for server in client_instance.channels:
        if server.name == server_name:
            return server
    else:
        return False


# Get Current Time as beauty Timestamp
def get_time():
    return "{:%d-%m-%y %S:%M:%H}".format(time.time())

