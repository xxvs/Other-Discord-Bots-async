# A bot that will notifiy the server when a member starts playing a game.
import discord,asyncio

client=discord.Client()

@client.event
async def on_ready():
	print('Logged in as: '+client.user.name)
	print('Bot ID: '+client.user.id)
	for server in client.servers:
		global server_channels
		server_channels=dict((channel.name,channel) for channel in server.channels)
	print('------')

@client.event
async def on_member_update(past,member):

	if member.game !=None:
		msg='{} has started playing {}'.format(member.mention,member.game)
		await client.send_message(server_channels['DISCORD CHANNEL NAME YOU WANT THE MESSAGE IN'],msg)

client.run('TOKEN')
