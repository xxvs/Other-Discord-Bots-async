import discord,asyncio
import functions

approved_roles=['Admin','Moderator']

client=discord.Client()


@client.event
async def on_ready():
	print('Logged in as: '+client.user.name)
	print('Bot ID: '+client.user.id)
	await client.change_presence(game=discord.Game(name='!help - for information'))
	for server in client.servers:
		print ("Connected to server: {}".format(server))
	print('------')

@client.event
async def on_message(message):
	if message.server==None:
		return

	if message.channel.name=='servers' and message.author!=client.user:

		if message.content.lower().startswith('!start'):
			if functions.server_running != None:
				msg=functions.status()
				await client.send_message(message.channel,msg)
				return
			def map(msg):
				return msg.content.startswith('$map')
			game_name=message.content[len('!start'):].upper().strip()
			if game_name not in functions.game_list.keys():
				await client.send_message(message.channel,'**{}** is not a valid game'.format(game_name))
				return
			if all(role.name!=game_name for role in message.author.roles):
				await client.send_message(message.channel, 'You need the **{0}** role to launch **{0}**'.format(game_name))
				return
			if 'maps' in list(functions.game_list[game_name].keys()):
				msg='Pick a map:\n\n`{}`\nEnter Map Name: `$map map_name`'.format(list(functions.game_list[game_name]['maps']))
				await client.send_message(message.channel, msg)
				message=await client.wait_for_message(author=message.author,check=map)
				map_name=message.content[len('$map'):].upper().strip()
				output=functions.start(game_name,message.author,map=map_name)
			else:
				output=functions.start(game_name,message.author)
			await client.send_message(message.channel,output)

		if message.content.lower().startswith('!status'):
			msg=functions.status()
			await client.send_message(message.channel,msg)

		if message.content.lower().startswith('!stop') and (any(role.name in approved_roles for role in message.author.roles) or message.author.mention==functions.start_user):
			if functions.server_running!=None:
				msg=functions.stop(message.author)
			else:
				msg='No servers currently running'
			await client.send_message(message.channel,msg)

		if message.content.lower().startswith('!help'):
			embed=functions.help()
			await client.send_message(message.channel,embed=embed)


async def clean_channel():
	global server_roles,server_channels
	await client.wait_until_ready()
	while not client.is_closed:
		for server in client.servers:
			server_channels=dict((channel.name,channel) for channel in server.channels)
			server_roles=dict((role.name,role) for role in server.roles)
		channel=server_channels['servers']
		async for message in client.logs_from(channel,limit=500):
			await client.delete_message(message)
		await asyncio.sleep(60)


client.loop.create_task(clean_channel())
client.run('API_Key')
