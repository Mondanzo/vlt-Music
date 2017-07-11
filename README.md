# vlt-Music
A music bot for Discord.

## Compatibility
- [x] Windows - No Bugs found
- [x] Linux - Works fine
- [ ] Mac - Not Tested

# Setup
A step-by-step tutorial to setup the bot.

1. Download this Repository
2. Install Python 3.5 (it's important that you use 3.5!)
3. Install the requirements (Run `pip install -r requirements.txt`)
4. Edit `config.yml`.
5. Run Start.bat or Start.sh
6. Enjoy

# Configuration
Explanation of `config.yml`

`Token: "..."`
Insert the API token from [Discord](https://discordapp.com/developers/applications)

`Opusfile: "libopus-0.x86.dll" or libopus-0.x64.dll`
~~Opusfile, not required for Windows.~~ It is required.
You need to change `config.yml` to the correct version.
On Linux, change it to `libopus.so.0`, you also need to install FFMPEG if you haven't already.

`Prefix: "??"`
Replace this with your Prefix!
Example: `Prefix: "vlt."`
So the commands would be
`vlt.help, vlt.play <Song>, vlt.np`

`AdminRole: "DJ"`
Replace this with the role name that shall be able to use the Admin Commands. (See Commmands->Admin Commands)

`AllowedSites: ""`
Add there starts of Url's to add and split them with a `;`
CAUTION: At the moment search function is disabled!

`AutoReconnect: True`
Set this to `True` if you want your bot to restart on a crash.

`Volume: 1.0`
Change the Volume of the bot on a range from `0.0` to `1.0`.
You need to restart the bot to apply the changes!

`ReqSkips: 2`
You can ignore this for now.

`Autojoin: False`
If you want you're bot to join a channel automatically, set this to True.
This Feature is unstable.

`AutojoinChannel: "000000000000000"`
Replace the Zero's with the Id of the Voice Channel the bot should autojoin to.


# Commands
Documentation for availible commands.

### User Commands
- `help` - Show's the documentation
- `play <song>` - Add a song to the playlist
- `queue` - Show the current queue
- `np`/`status` - Show's the currently song (while a song is playing)
- `skip` - Vote to skip the current song

### Admin Commands
- `connect <Channel Name>` - Connect the Music Bot to a voice channel.
- `shutdown` - Shutdown the bot

