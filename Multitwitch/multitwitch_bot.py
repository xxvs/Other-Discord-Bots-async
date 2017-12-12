# A bot that will generate a multitwitch link for members that are currently streaming in the server.
import discord,asyncio

client=discord.Client()

@client.event
async def on_ready():
	print('Logged in as: '+client.user.name)
	print('Bot ID: '+client.user.id)
	await client.change_presence(game=discord.Game(name='!mtwitch for multitwitch'))
	print('------')

@client.event
async def on_message(message):
	if message.content.lower()=='!mtwitch':
		twitch_list=list(member.game.url for member in message.server.members if member.game!=None and member.game.type==1)
		if len(twitch_list)>0:
			url='http://www.multitwitch.tv'
			for twitch_channel in twitch_list:
				c_name=twitch_channel[len('https://www.twitch.tv/'):]
				url=url+'/{}'.format(c_name)
			await client.send_message(message.channel,url)
		else:
			await client.send_message(message.channel,'Nobody is streaming now :cry:')

client.run('token')
