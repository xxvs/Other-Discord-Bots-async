import discord,asyncio
import functions
client=discord.Client()

check_messages=functions.read_json('check_messages')
server_messages=[]

@client.event
async def on_ready():
	print('Logged in as: '+client.user.name)
	print('Bot ID: '+client.user.id)
	await client.change_presence(game=discord.Game(name='Checking Reactions'))
	for server in client.servers:
		for channel in server.channels:
			async for message in client.logs_from(channel,limit=5000):
				if message.id in check_messages.keys():
					client.messages.append(message)
	print('------')

@client.event
async def on_reaction_add(reaction,user):
	if reaction.message.id in check_messages.keys():
		if user.bot==True:
			return
		if user.id not in check_messages[reaction.message.id]['users']:
			await client.remove_reaction(reaction.message,reaction.emoji,user)
		if user.id in check_messages[reaction.message.id]['users']:
			check_messages[reaction.message.id]['users'].remove(user.id)
			if len(check_messages[reaction.message.id]['users'])==0:
				await client.send_message(reaction.message.author,'All users have reacted to message:\n```{}\n\nPosted: {}```'.format(reaction.message.clean_content,reaction.message.timestamp))
				del check_messages[reaction.message.id]
			functions.edit_json('check_messages',check_messages)

@client.event
async def on_message(message):

	if len(message.content)>50 and len(message.mentions)>1 and message.clean_content.startswith('@{}'.format(client.user.name)):
		check_messages[message.id]={'author':message.author.id,'users':[]}
		for mentioned in message.mentions:
			if mentioned.bot==False:
				check_messages[message.id]['users'].append(mentioned.id)
		if len(check_messages[message.id]['users'])>0:
			functions.edit_json('check_messages',check_messages)
			await client.add_reaction(message,'\U00002705')
		else:
			del check_messages[message.id]



client.run('TOKEN')
