#DELETES POSTS FROM THE SPECIFIED CHANNEL IF THEY ARE MORE THAN A DAY OLD
import discord,asyncio
import datetime
client=discord.Client()

@client.event
async def on_ready():
	print('Logged in as: '+client.user.name)
	print('Bot ID: '+client.user.id)
	print('------')


async def channel_cleanup():
	await client.wait_until_ready()
	for server in client.servers:
		channel_list=dict( (channel.name,channel) for channel in server.channels)
	mlist=[]
	async for message in client.logs_from(channel_list['YOUR CHANNEL NAME HERE']):
		tdiff=(datetime.datetime.now()-message.timestamp).days
		if tdiff>=1: #Age, in days, that posts have to be to get deleted
			mlist.append(message)
	if len(mlist)>0:
		await client.delete_messages(mlist)
	await asyncio.sleep(60) #Time, in seconds, between checks for old posts

client.loop.create_task(channel_cleanup())
client.run('TOKEN')
