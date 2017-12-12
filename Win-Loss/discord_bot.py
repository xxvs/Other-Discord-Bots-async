#Simple bot to keep track of Wins and Losses for something
import discord,asyncio
import functions

client=discord.Client()

def save_stats():
	functions.edit_json('stats',stats)

stats=functions.read_json('stats')

if 'wins' not in stats.keys():
	stats['wins']=0
	save_stats()
if 'losses' not in stats.keys():
	stats['losses']=0
	save_stats()

@client.event
async def on_ready():
	print('Logged in as: '+client.user.name)
	print('Bot ID: '+client.user.id)
	await client.change_presence(game=discord.Game(name='!help - for commands'))
	print('------')

@client.event
async def on_message(message):

	if message.content.lower().startswith('!set_wins'):
		msg=message.content[len('!set_wins'):].strip()
		try:
			stats['wins']=int(msg)
			save_stats()
			await client.send_message(message.channel, '**Wins** has been set to {}'.format(msg))
		except ValueError:
			await client.send_message(message.channel, '{} is not a valid input'.format(msg))

	if message.content.lower().startswith('!set_losses'):
		msg=message.content[len('!set_losses'):].strip()
		try:
			stats['losses']=int(msg)
			save_stats()
			await client.send_message(message.channel, '**Losses** has been set to {}'.format(msg))
		except ValueError:
			await client.send_message(message.channel, '{} is not a valid input'.format(msg))

	if message.content.lower()=='!add_win':
		stats['wins']+=1
		save_stats()
		await client.send_message(message.channel,'Wins: {}'.format(stats['wins']))

	if message.content.lower()=='!add_loss':
		stats['losses']+=1
		save_stats()
		await client.send_message(message.channel,'Losses: {}'.format(stats['losses']))

	if message.content.lower()=='!stats':
		await client.send_message(message.channel, 'Wins: {}\nLosses: {}'.format(stats['wins'],stats['losses']))

	if message.content.lower().startswith('!help'):
		msg=functions.help()
		await client.send_message(message.channel, embed=msg)

client.run('token')
