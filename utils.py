import discord


# Get Channel by Name and Type
def get_channel_by_name(server, channel_name, stype=discord.ChannelType.text):
    for channel in server.channels:
        if channel.name == channel_name and channel.type == stype:
            return channel
    else:
        return False


# Get Channel by Name and Type
def get_server_by_name(client_instance, server_name):
    for server in client_instance.channels:
        if server.name == server_name:
            return server
    else:
        return False
