
# ADA - Discord Bot for Satisfactory Dedicated Server

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/lilkingjr1/ADA-Discord-Bot?display_name=tag&logo=github)](https://github.com/lilkingjr1/ADA-Discord-Bot/releases/latest) [![Python version](https://img.shields.io/badge/python-3.x.x-brightgreen?logo=python)](https://www.python.org/downloads/) ![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux-lightgrey) ![Hosting](https://img.shields.io/badge/hosting-self--hosted-blue) ![Quality](https://img.shields.io/badge/quality-Literally%20my%20first%20Discord%20bot-yellow) ![Maitnence](https://img.shields.io/badge/maintained-When%20I%20have%20time%20%C2%AF%5C__(%E3%83%84)__%2F%C2%AF-yellowgreen) [![GitHub](https://img.shields.io/github/license/lilkingjr1/ADA-Discord-Bot)](https://choosealicense.com/licenses/mit/)

___

ADA (Artificial Directory and Assistant) is a simple Discord bot written in Python that notifies players of Satisfactory dedicated server saves and crashes.

###### Author

<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
    <tr>
        <td align="center">
            <a href="https://github.com/lilkingjr1">
                <img src="https://avatars.githubusercontent.com/u/4533989" width="50px;" alt=""/><br /><sub><b>Red-Thirten</b></sub>
            </a>
            <br />
            <a href="https://github.com/parkervcp/eggs/commits?author=lilkingjr1" title="Codes">💻</a>
            <a href="https://github.com/parkervcp/eggs/commits?author=lilkingjr1" title="Maintains">🔨</a>
        </td>
    </tr>
</table>
<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->

___
#### Why?
The dedicated server for Satisfactory currently (as of Update 7) does not notify players of upcomming world saves, and my friends and I found that coincidentally doing large operations during saves (like deleting or Blueprints) tends to crash the server. This bot aims to avoid this issue by giving players in a specific Discord voice channel a warning message just before the server saves. If the server still happens to crash for any reason, the bot will also notify of this.

[Satisfactory](https://www.satisfactorygame.com/) is otherwise a very fun game by Coffee Stain Studios, and is in no way associated with this bot.

___

## Prerequisites

- Fully installed Satisfactory dedicated server (via SteamCMD or otherwise) that has been booted at least once (to generate the GameUserSettings.ini file).
- Python 3
    - Bot was written in 3.11, but any 3.x version should work I think...
- PIP (should be included with Python)
- Discord account with verified email (to access developer portal)

## Installation

### Creating a Discord Application for the Bot

1. Go to Discord's [Developer Portal](http://discordapp.com/developers/applications) and log in.
2. Click "New Application"
3. Name it "ADA" or honestly whatever you'd like.
4. (Optional) Feel free to give it an App Icon and Description of whatever you'd like.
5. Click the "Bot" tab on the left and click "Add Bot". Then click "Yes, do it!".
6. Scroll down and turn on "SERVER MEMBERS INTENT".
7. Click the "OAuth2" tab on the left and click "URL Generator".
8. Check these Scopes:

![scopes](https://user-images.githubusercontent.com/4533989/215032768-fb2c4887-85cd-42fe-adaf-5927f17cb2a6.jpg)

9. Check these Bot Permissions:

![bot_permissions](https://user-images.githubusercontent.com/4533989/215032794-58778138-6889-4996-9965-4ecca7cf9ddb.jpg)

10. Copy the Generated URL, paste it into a new tab, and invite the bot to the Discord server of your choosing.

*(You will need a seperate bot instance / application **per** Satisfactory server, if you're wild like that...)*

### Installing the Bot

The bot ***must*** be installed on the same host as the Satisfactory dedicated server. Whether this is on bare metal, a VM, a VPS, or within a Docker container doesn't matter; the bot just needs to be able to see the Satisfactory server process and its save files.

1. [Download the latest release](https://github.com/lilkingjr1/ADA-Discord-Bot/releases/latest) and extract it (or `git clone` this repo), and place it wherever you'd like on the host.
2. Rename `.env-sample` to `.env`
3. Open command prompt or a terminal and navigate to the bot's folder:

```bash
cd /your/path/to/ADA-Discord-Bot
```

4. Verify you have the right version of Python installed:

```bash
python --version

OR (depending on what's in your path)

python3 --version
```

5. Install dependancies:

```bash
pip install -r requirements.txt
```

### Configure the Bot

The `.env` file can be used to configure the bot, or standard OS environment variables can be used (if so, reference the `.env` file for variable names).

1. Open `.env` with a text editor of your choice.
2. Set the Discord Token
    - Go to the Discord Developer Portal mentioned above
    - Go to the Bot tab
    - Click "Reset Token"
    - Copy the token
    - Replace `YOUR_DISCORD_TOKEN_HERE` with your token
3. Set the various Discord IDs
    - Open the Discord app
    - Click on the settings cog in the bottom left corner
    - Go to the Advanced tab and turn on "Developer Mode"
    - Right click the Channel/User you need the ID for, and click "Copy ID"
4. Set other settings according to their descriptions.
5. Save the file.

## Startup

Start the bot **before** starting the Satisfactory server.

Start with:

```bash
python bot.py

OR (depending on what's in your path)

python3 bot.py
```

The bot does not interact with the Satisfactory server and just uses "semi-dumb" timers to gauge when the next save will occur. Therefore, it is advised to start the bot *just* before starting your Satisfactory server.

For example, if you are running on Windows, you could add this towards the beginning of a Batch file that starts your Satisfactory server:

```batch
echo Starting ADA Discord Bot...
start python "C:\Servers\ADA Discord Bot\bot.py"
```

## Slash Commands

| Command | Description |
|---------|-------------|
| `/saveinfo` | Displays previous and expected future save times. |
| `/about` | Displays information about the bot. |
| `/shutdown` | Cleanly shuts down the bot (only the configured bot admin can do this). |

The bot also responds positively to "good bot" remarks 🙂

## Additional Notes

- If you get "Permission denied" errors, you may need to give appropriate permissions to the `bot.py` and `.env` files (ie. `sudo chmod 755 bot.py .env`).
- The `/saveinfo` command's "Next Save" and "Time Until Next Save" values are currently calculated relative to the last save's time. Therefore, until the server makes it's first save, these values may be incorrect or unavailable.
- The bot detects Satisfactory crashes but does not automatically reboot it. I figured most people already have their own solution for this and I didn't want to create a conflict. You can integrate the startup of this bot into the startup solution of you Satisfactory server if you would like to automate things, but this bot ideally *should not* be rebooted when the Satisfactory server is rebooted.

## Issues / Feedback

If you have have any issues running the bot, please feel free to open an Issue here on Github.

Regarding feedback, feel free to PR improvements if you'd like. However, I unfortunately cannot take feature requests at this time; fork the repo and play around with it if you'd like to add stuff.
