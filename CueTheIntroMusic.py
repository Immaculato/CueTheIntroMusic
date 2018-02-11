# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import opuslib
import glob

#224698254145617920

#global vars to hold various states of the bot
server = None
voice = None
file = None
botID = None
player = None
#holds the index in the file that the user entries start
indexListBegin = -1

#sometimes, you just want it to stfu
stfu = False

#list containing list of usernames, their configured mp3s, and their offset position in the file.
configuredUsers = list()
#list containing mp3's in the current directory
MP3s = None

#for voice transmission
print('opus library loaded:',discord.opus.is_loaded())

#load config/save info from file
file = None
try:
    file = open('config.txt', "r")
    botID = file.readline().rstrip()
    indexListBegin = len(botID)
    for line in file:
        parsedLine = line.rstrip().split(',')
        configuredUsers.append(parsedLine)
        print(parsedLine)
    file.close()
    MP3s = glob.glob("*.mp3")

except:
    print('config.txt not found')
    exit(-1)

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="CueTheIntroMusic bot by Immaculato#9416", command_prefix="-", pm_help = True)

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')
    print('Github Link: https://github.com/Immaculato/CueTheIntroMusic')
    print('--------')
    for clientServer in client.servers:
        if clientServer.name == 'cool kids only':
            global server
            server = clientServer

    return await client.change_presence(game=discord.Game(name='Some sick ass intro music'))

@client.event
async def on_voice_state_update(memberBefore, memberAfter):
    #if the bot is in a channel, and a user joined that channel,
    if (voice != None and voice.channel.name == memberAfter.voice.voice_channel.name):
        #look for the user in the configured list. if they exist, play their intro music!
        for i in range(len(configuredUsers)):
            if memberBefore.id == configuredUsers[i][0]:
                global player
                #if the player has been set by a joining user before, stop it and queue up the new song.
                if player != None:
                    player.stop()
                    player = None
                player = voice.create_ffmpeg_player(configuredUsers[i][1])
                #don't blow out everyone's eardrums
                player.volume = 0.25
                player.start()

#tricky way to get the user in a public message and spoof a command.
@client.event
async def on_message(message):
    parsedMessage = message.content.split(' ')
    #if we got the setmusic command, look for the user in the configured users list.
    if (len(parsedMessage) == 2 and parsedMessage[0] == '-set_music'):
        userFound = False
        #if the user's mp3 choice is valid
        if parsedMessage[1] in MP3s:
            #run through each configured user
            for i in range(len(configuredUsers)):
                #if the user exists in the list, change their mp3.
                if message.author.id == configuredUsers[i][0]:
                    configuredUsers[i][1] = parsedMessage[1]
                    userFound = True
            #if we couldn't find the user in the list, add a new entry for them.
            if not userFound:
                configuredUsers.append(list([message.author.id, parsedMessage[1]]))
            #rewrite the config file
            rewrite_file()
        else:
            await client.send_message(message.channel, 'That isn\'t a valid filename. Use -music_choices to get the options.')
                
    #yanked this line from the source @ https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/bot.py
    else:
        await client.process_commands(message)



@client.command(help = 'Usage -stfu: makes me stfu (leave a channel)')
async def stfu(*args):
    await voice.disconnect()
    await client.say(':zipper_mouth: FeelsBadMan')

@client.command(help = 'Usage: -cue_the_music [voice channel name]: This will summon me to a voice channel.')
async def cue_the_music(*args):
    if len(args) != 1:
        await client.say('Include a voice channel name pls')
        return

    for channel in server.channels: 
        if channel.type == channel.type.voice and channel.name == args[0]:
            global voice
            voice = await client.join_voice_channel(channel)
            await client.say('You have summoned me')
            return

    await client.say('Couldn\'t find that channel')
    return

#doesn't actually set the music, is a placeholder. The actual logic exists in on_message(message) above.
@client.command(help = 'Usage: -set_music [mp3 filename]: This will set the intro music for the user. User -music_choices to see possible mp3 filenames.')
async def set_music(*args):
    return

@client.command(help = 'Usage: -music_choices: This will print the mp3 options you can choose from.')
async def music_choices(*args):
    response = "Fresh memes (use the mp3 filename in -set_music [mp3]):"
    for i in range(len(MP3s)):
        response+=('\n '+str(i+1)+': '+MP3s[i])
    await client.say(response)

def rewrite_file():
    file = open('config.txt', "r+")
    file.seek(indexListBegin)
    file.truncate()
    for user in configuredUsers:
        file.write('\n'+user[0]+','+user[1])
    file.close()

# After you have modified the code, feel free to delete the line above so it does not keep popping up everytime you initiate the ping commmand.
    
client.run(botID)

# Basic Bot was created by Habchy#1665
# Please join this Discord server if you need help: https://discord.gg/FNNNgqb
# Please modify the parts of the code where it asks you to. Example: The Prefix or The Bot Token
# This is by no means a full bot, it's more of a starter to show you what the python language can do in Discord.
# Thank you for using this and don't forget to star my repo on GitHub! [Repo Link: https://github.com/Habchy/BasicBot]

# The help command is currently set to be not be Direct Messaged.
# If you would like to change that, change "pm_help = False" to "pm_help = True" on line 9.