import discord,asyncio
import json,datetime
import functions

approved_roles=['Admin','Moderator'] #add the name of the roles that can add keys and veiw player stats

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

	if message.content.lower().startswith('!purge'):
		async for msg in client.logs_from(message.channel,limit=1000):
			await client.delete_message(msg)
		print('purged!')

	if message.content.lower().startswith('!get_game'):
		game=message.content[len('!get_game'):].lower().strip()
		response=functions.get_game(game,message.author.mention)
		if game not in response:
			await client.send_message(message.channel,'{}, a key for **{}** has been sent to you.'.format(message.author.mention,game))
			await client.send_message(message.author,'Here is your key for **{}**: {}'.format(game,response))

		else:
			await client.send_message(message.channel, response)

	if message.content.lower().startswith('!list'):
		embed=functions.make_list()
		await client.send_message(message.channel,embed=embed)

	if any(role.name in approved_roles for role in message.author.roles) and message.content.lower()=='!stats':
		embed=functions.stats()
		await client.send_message(message.author,embed=embed)

	if message.content.lower().startswith('!help'):
		embed=functions.help()
		await client.send_message(message.channel,embed=embed)

	if any(role.name in approved_roles for role in message.author.roles) and message.content.lower()=='!add_key':
		def game(msg):
			return msg.content.startswith('$game')
		def key(msg):
			return msg.content.startswith('$key')
		await client.send_message(message.channel, 'Enter Game Name: `$game game_name` ')
		message= await client.wait_for_message(author=message.author,check=game)
		game_name=message.content[len('$game'):].strip()
		await client.send_message(message.channel, 'Enter Game Key: `$key game_key` ')
		message= await client.wait_for_message(author=message.author,check=key)
		game_key=message.content[len('$key'):].strip()
		await client.delete_message(message)
		functions.add_key(game_name.lower(),game_key)
		await client.send_message(message.channel,'Key for **{}** was added successfully.\nThank you {} for being awesome! :thumbsup:'.format(game_name,message.author.mention))


client.run('Discord API Key')
