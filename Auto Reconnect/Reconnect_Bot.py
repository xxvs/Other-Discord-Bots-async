# A bot that will auto reconnect if connection is lost. It's not the cleanest, but it works.
import discord,asyncio

client = discord.Client()

@client.event
async def on_ready():
	global connect
	print('Logged in as: '+client.user.name)
	print('Bot ID: '+client.user.id)
	for server in client.servers:
		print ("Connected to server: {}".format(server))
	print('------')

async def connect():
	print('Logging in...')
	while not client.is_closed:
		try:
			await client.start('TOKEN')
		except:
			await asyncio.sleep(5)

client.loop.run_until_complete(connect())
