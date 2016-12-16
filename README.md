# vlt-Music
A Music Bot for Discord

## Compossible
- [x] On Windows - No Bugs founded
- [ ] On Linux - Random Crash caused by async (I hate async -.-)
- [ ] On Mac - Not Tested

# Setup
A step-by-step tutorial to setup the bot.

1. Download this Repository
2. Install Python 3.5 (It's important that you use 3.5!)
3. Install the requirements (Run `pip install -r requirements.txt`)
4. Edit the `config.yml`.
5. Run Start.bat or Start.sh
6. Enjoy

# Configuration
Explanation of the whole `config.yml`

`Token: "..."`
Here you replace this crazy Stuff with your bot token that you've got from 
<url>https://discordapps.com/developers/applications</url>

`Opusfile: "libopus-0.dll"`
Here you replace the OpusFile.
on Windows, don't change it!
On Linux, change it to `libopus.so.0`, you also need to install FFMPEG if you haven't already.

`Prefix: "??"`
Replace this with your Prefix!
Example: `Prefix: "vlt."`
`vlt.help, vlt.play <Song>, vlt.np`

`AdminRole: "DJ"`
Replace this with the role name that should can use the Admin Commands. (See Commmands->Admin Commands)

`AllowedSites: ""`
Add there starts of Url's to add and split them with a `;`
WARNING: At the moment it's disable the search function!

`AutoReconnect: True`
Set this to `True` if you want that your bot restarts on a crash, otherwise set it to `False`.

`Volume: 1.0`
Change the Volume of the bot. (Normally it's 1.0)
Be careful! At the moment you can't change it while the bot is online!

`ReqSkips: 2`
Ignore this.

`Autojoin: False`
If you want that you're bot joins automatically a channel, set this on True.
This Feature is instable.

`AutojoinChannel: "000000000000000"`
Replace the Zero's with the Id of the Voice Channel.


# Commands
A list of all commands

### User Commands
- `help` - Show's the help
- `play <song>` - Add's a song to the playlist
- `queue` - Show's the current queue
- `np`/`status` - Show's the currently song (When a song is playing)
- `skip` - Doesn't work yet. Ignore this, okay?

### Admin Commands
- `connect <Channel Name>` - Connect the Music Bot to a voice channel.
- `shutdown` - Turns this damn awezome Music Bot off!
