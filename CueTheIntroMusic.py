# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import opuslib

global server
global voice
global file
global botID

#for voice transmission
print('opus library loaded:',discord.opus.is_loaded())

#load config/save info from file
file = None
try:
    file = open('config.txt', "r")
    botID = file.readline().rstrip()
except:
    print('config.txt not found')
    exit(-1)

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="CueTheIntroMusic bot by Tristan", command_prefix="-", pm_help = True)

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
	print('Support Discord Server: https://discord.gg/FNNNgqb')
	print('Github Link: https://github.com/Habchy/BasicBot')
	print('--------')
	print('You are running BasicBot v2.1') #Do not change this. This will really help us support you, if you need support.
	print('Created by Habchy#1665')
	for clientServer in client.servers:
		if clientServer.name == 'cool kids only':
			global server
			server = clientServer



#myServer = client.servers[0]
	return await client.change_presence(game=discord.Game(name='Some sick ass intro music')) #This is buggy, let us know if it doesn't work.

# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def ping(*args):

	await client.say(":ping_pong: Pong!")
	await asyncio.sleep(3)

@client.command()
async def get_args(*args):
	for a in args:
		await client.say(a)

@client.command()
async def cue_the_music(*args):
	if len(args) != 1:
		client.say('Include a voice channel name pls')
		return

	for channel in server.channels:	
		if channel.type == channel.type.voice and channel.name == args[0]:
			global voice
			voice = await client.join_voice_channel(channel)
			await client.say('You have summoned me')
			return

	client.say('Couldn\'t find that channel')
	return

@client.command()
async def andHisNameIs(*args):
	player = voice.create_ffmpeg_player('johncena.mp3')
	player.start()
# After you have modified the code, feel free to delete the line above so it does not keep popping up everytime you initiate the ping commmand.
	
client.run(botID)

# Basic Bot was created by Habchy#1665
# Please join this Discord server if you need help: https://discord.gg/FNNNgqb
# Please modify the parts of the code where it asks you to. Example: The Prefix or The Bot Token
# This is by no means a full bot, it's more of a starter to show you what the python language can do in Discord.
# Thank you for using this and don't forget to star my repo on GitHub! [Repo Link: https://github.com/Habchy/BasicBot]

# The help command is currently set to be not be Direct Messaged.
# If you would like to change that, change "pm_help = False" to "pm_help = True" on line 9.