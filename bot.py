"""
MIT License

Copyright (c) 2023 David Wolfe (Red-Thirten / Lilkingjr1)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import time
import psutil
import asyncio
import inflect

import discord
from discord.ext import tasks
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
VERSION = 1.0
TOKEN = str(os.getenv('DISCORD_TOKEN'))
TEXT_ID = int(os.getenv('DISCORD_TEXT_CHANNEL_ID'))
VCHAN_ID = int(os.getenv('DISCORD_VOICE_CHANNEL_ID'))
ADMIN_ID = int(os.getenv('DISCORD_ADMIN_ID'))
SAVES_DIR = str(os.getenv('SAVES_DIRECTORY'))
USER_SETTINGS = str(os.getenv('GAMEUSERSETTINGS_INI'))
FOREWARNING_TIME = int(os.getenv('FOREWARNING_TIME'))
BOOT_TIME = int(os.getenv('BOOT_TIME'))
AUTOSAVE_SETTING_NAME = "\"FG.AutosaveInterval\""
SAVE_CHECK_INTERVAL = 1 # seconds
SAVE_CHECK_MAX = 120 # seconds
PROC_CHECK_INTERVAL = 5 # seconds
PROC_CHECK_TIMEOUT = 5 # minutes
PROC_NAME = str(os.getenv('PROCESS_NAME'))

saveInterval = -1
latestFileTime = -1

p = inflect.engine()

def getLatestFileTime(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    if len(paths) > 0:
        return os.path.getmtime( max(paths, key=os.path.getmtime) )
    else:
        return -1

def getDateTimeStr():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
    

f = open(USER_SETTINGS, "r")
for x in f:
    if AUTOSAVE_SETTING_NAME in x:
        saveInterval = int(x[x.find(AUTOSAVE_SETTING_NAME) + len(AUTOSAVE_SETTING_NAME) + 2 : x.find(")", x.find(AUTOSAVE_SETTING_NAME))])
if saveInterval < 0:
    print(f"ERROR: Could not find valid autosave interval in {USER_SETTINGS}")
    quit()
saveWarningTime = saveInterval - FOREWARNING_TIME

latestFileTime = getLatestFileTime(SAVES_DIR)


########################################################
print(f"{getDateTimeStr()}: Bot attempting to login to Discord...")

# create intents before creating bot instance
intents = discord.Intents().default()
intents.members = True
# setup activity of bot
activity = discord.Activity(type=discord.ActivityType.watching, name="Satisfactory")
# create the bot
bot = discord.Bot(intents=intents, activity=activity)

@tasks.loop()
async def WarnMsg():
    global latestFileTime
    print(f"{getDateTimeStr()}: Waiting {p.no('minute', saveWarningTime/60)} before warning...")
    await asyncio.sleep(saveWarningTime)
    #await asyncio.sleep(1) # debugging
    latestFileTime = getLatestFileTime(SAVES_DIR) # get latest file time again in case a manual save was made
    
    _members = vchan.members
    if len(_members) > 0:
        _pings = ""
        for u in _members:
            _pings += f"<@{str(u.id)}>"
        _embed = discord.Embed(
            title=f"Save incoming in {p.no('minute', int(FOREWARNING_TIME/60))}!",
            description="Don't do anything silly while the server saves or it will crash!",
            color=discord.Colour.gold() # Pycord provides a class with default colors you can choose from
        )
        _embed.set_author(name="Save Warning System", icon_url="https://img2.storyblok.com/fit-in/0x200/filters:format(png)/f/110098/268x268/d1ebbafe03/logo.png")
        _embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/0/04/Save-icon-floppy-disk-transparent-with-circle.png")
        _embed.set_footer(text=f"It has been {p.no('minute', int(saveWarningTime/60))}, and the server is set to save every {p.no('minute', int(saveInterval/60))}.")
        _msg = await thread.send(_pings, embed=_embed)
        print(f"{getDateTimeStr()}: Sent warning message.")
    
    _timeWaited = 0
    while (latestFileTime >= getLatestFileTime(SAVES_DIR)):
        await asyncio.sleep(SAVE_CHECK_INTERVAL)
        _timeWaited += SAVE_CHECK_INTERVAL
        if _timeWaited > SAVE_CHECK_MAX: break
    print(f"{getDateTimeStr()}: Waited {p.no('second', _timeWaited)} for new save.")
    latestFileTime = getLatestFileTime(SAVES_DIR)
    if '_msg' in locals():
        if _timeWaited > SAVE_CHECK_MAX:
            _embed = discord.Embed(
                title="Save failed! 😢",
                description="Did the server crash?...",
                color=discord.Colour.red()
            )
            _embed.set_author(name="Save Warning System", icon_url="https://img2.storyblok.com/fit-in/0x200/filters:format(png)/f/110098/268x268/d1ebbafe03/logo.png")
            _embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Flat_cross_icon.svg/1200px-Flat_cross_icon.svg.png")
            _embed.set_footer(text=f"Save did not complete within {p.no('second', SAVE_CHECK_MAX)}.")
        else:
            _embed = discord.Embed(
                title="Save complete! 😄",
                description=f"Save completed: {datetime.fromtimestamp(time.time()).strftime('%I:%M %p')}",
                color=discord.Colour.green()
            )
            _embed.set_author(name="Save Warning System", icon_url="https://img2.storyblok.com/fit-in/0x200/filters:format(png)/f/110098/268x268/d1ebbafe03/logo.png")
            _embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/green/checkmark-xxl.png")
            _embed.set_footer(text=f"Save took {p.no('second', _timeWaited - FOREWARNING_TIME)} to complete.")

        await _msg.edit(embed=_embed)

@tasks.loop(seconds=PROC_CHECK_INTERVAL)
async def CrashCheck():
    if not checkIfProcessRunning(PROC_NAME):
        print(f"{getDateTimeStr()}: Satisfactory server crash detected!")
        _members = vchan.members
        _pings = ""
        for u in _members:
            _pings += f"<@{str(u.id)}>"
        _embed = discord.Embed(
            title="Crash detected!",
            description="The server process has stopped running.\nUse /saveinfo to see when the last successful save was made.",
            color=discord.Colour.red()
        )
        _embed.set_author(name="Crash Detection System", icon_url="https://img2.storyblok.com/fit-in/0x200/filters:format(png)/f/110098/268x268/d1ebbafe03/logo.png")
        _embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Computer_crash.svg/1200px-Computer_crash.svg.png")
        _embed.set_footer(text=f"Waiting {p.no('minute', PROC_CHECK_TIMEOUT)} before checking again.")

        await thread.send(_pings, embed=_embed)
        WarnMsg.restart()
        print(f"{getDateTimeStr()}: WarnMsg loop restarted.")
        await asyncio.sleep(PROC_CHECK_TIMEOUT * 60)

@bot.event
async def on_ready():
    print(f"{getDateTimeStr()}: {bot.user} is ready and online!")
    
    global thread
    thread = bot.get_channel(TEXT_ID)
    if thread == None:
        print(f"ERROR: Could not find valid thread with ID: {TEXT_ID}")
        await bot.close()

    global vchan
    vchan = bot.get_channel(VCHAN_ID)
    if vchan == None:
        print(f"ERROR: Could not find valid voice channel with ID: {VCHAN_ID}")
        await bot.close()
    
    await asyncio.sleep(BOOT_TIME)
    
    if not WarnMsg.is_running():
        WarnMsg.start()
        print(f"{getDateTimeStr()}: WarnMsg loop started.")
    
    if not CrashCheck.is_running():
        CrashCheck.start()
        print(f"{getDateTimeStr()}: CrashCheck loop started.")

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        if 'good bot' in message.content.lower():
            await message.channel.send("Aww shucks!", reference=message)
        else:
            await message.add_reaction('🤷‍♂️')

@bot.slash_command(name = "about", description="Displays information about the ADA bot.") # this decorator makes a slash command
async def about(ctx): # a slash command will be created with the name "about"
    _embed = discord.Embed(
        title="About:",
        description="Artificial Directory and Assistant (ADA) is a Discord bot, written in Python, that notifies of Satisfactory dedicated server saves and crashes.",
        color=discord.Colour.blue()
    )
    _embed.set_author(name="ADA", icon_url="https://img2.storyblok.com/fit-in/0x200/filters:format(png)/f/110098/268x268/d1ebbafe03/logo.png")
    _embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Information_icon.svg/1024px-Information_icon.svg.png")
    cmdText = "```"
    for command in bot.commands:
        cmdText += f"/{command}\n"
    cmdText += "```"
    _embed.add_field(name="Commands:", value=cmdText, inline=True)
    _embed.add_field(name="Author:", value="Red-Thirten\n(David Wolfe)", inline=True)
    _embed.add_field(name="Version:", value=VERSION, inline=True)
    _embed.set_footer(text=f"Bot latency is {bot.latency}")
    await ctx.respond(embed=_embed)

@bot.slash_command(name = "saveinfo", description="Gives time information about the previous and upcoming Satisfactory save.")
async def ping(ctx):
    _timeUntilNextSave = int((latestFileTime + saveInterval - time.time()) / 60)
    _embed = discord.Embed(
        color=discord.Colour.blurple()
    )
    _embed.set_author(name="Latest Save Info", icon_url="https://img2.storyblok.com/fit-in/0x200/filters:format(png)/f/110098/268x268/d1ebbafe03/logo.png")
    _embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/b/b2/Floppy-disk-icon-blue-transparent.png")
    _embed.add_field(name="Last Save:", value=datetime.fromtimestamp(latestFileTime).strftime('%I:%M %p'), inline=True)
    if _timeUntilNextSave >= 0:
        _embed.add_field(name="Next Save:", value=datetime.fromtimestamp(latestFileTime + saveInterval).strftime('%I:%M %p'), inline=True)
        _embed.add_field(name="Time Until Next Save:", value=f"Approx. {_timeUntilNextSave} min.", inline=True)
    else:
        _embed.add_field(name="Next Save:", value="*Unavailable*", inline=True)
        _embed.add_field(name="Time Until Next Save:", value="*Unavailable*", inline=True)
    await ctx.respond(embed=_embed)

@bot.slash_command(name = "shutdown", description="Cleanly shuts ADA off. Only bot admin can do this.")
async def shutdown(ctx):
    if ctx.author.id == ADMIN_ID:
        print(f"{getDateTimeStr()}: Shutdown command issued.")
        await ctx.respond("Goodbye.")
        await bot.close()
    else:
        await ctx.respond("You are not ADA's glorious master, so you cannot do this plebeian!")

bot.run(TOKEN)
