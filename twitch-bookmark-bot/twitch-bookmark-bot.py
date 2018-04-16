import discord,os,json
from discord.ext import commands

bot=commands.Bot(command_prefix='!')

clip_channel_id='435556105331015681' #channel ID for the twitch clips,replace with your own channel ID
key='https://clips.twitch.tv/'

def read_file(file_name):
	if not file_name.endswith('.txt'):
		file_name = file_name + '.txt'
	if not os.path.isfile(file_name):
		list_name = []
	else:
		try:
			with open(file_name) as f:
				list_name = json.load(f)
		except ValueError:
			list_name = []
	return list_name

def edit_file(file_name, items):
	if not file_name.endswith('.txt'):
		file_name = file_name + '.txt'
	with open(file_name, "w") as f:
		json.dump(items, f,indent=4,sort_keys=True)

twitch_clips=read_file('twitch_clips')

@bot.event
async def on_ready():
	global clip_channel
	print(bot.user.name)
	print(bot.user.id)
	await bot.wait_until_ready()
	clip_channel=bot.get_channel(clip_channel_id)

@bot.event
async def on_message(message):
	if key in message.content and message.channel.id != clip_channel_id:
		await bot.delete_message(message)
		await bot.send_message(message.channel, '{}, your message has been deleted.\nPlease use the {} channel to post twitch clips.'.format(message.author.mention,clip_channel.mention))

	if key in message.content and message.channel.id == clip_channel_id:
		for item in message.content.split():
			if item.startswith(key) and item not in twitch_clips:
				twitch_clips.append(item)
				edit_file('twitch_clips',twitch_clips)

bot.run('TOKEN')
