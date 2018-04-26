#DELETES POSTS FROM THE SPECIFIED CHANNELS IF THEY ARE MORE THAN A DAY OLD
import discord,asyncio
import datetime

bot=discord.Client()

channel_list=['ID# OF CHANNEL 1','ID# OF CHANNEL 2'] #list of channel ID#'s to remove messages from
message_age=1 #time, in days, messages need to be to be deleted
clean_time=3600 #time, in seconds, to check for old messages

@bot.event
async def on_ready():
	print('Logged in as: '+bot.user.name)
	print('Bot ID: '+bot.user.id)
	print('------')

async def channel_cleanup():
	await bot.wait_until_ready()
	while True:
		for server in bot.servers:
			for channel_id in channel_list:
				channel = discord.utils.get(server.channels,id=channel_id)
				if channel is not None:
					print('Checking channel: '+channel.name)
					mlist=[]
					async for message in bot.logs_from(channel):
						tdiff=(datetime.datetime.now()-message.timestamp).days
						if tdiff>=14:
							await bot.delete_message(message)
						elif tdiff>=message_age:
							mlist.append(message)
					if len(mlist)>0:
						await bot.delete_messages(mlist)
		await asyncio.sleep(clean_time)

bot.loop.create_task(channel_cleanup())
bot.run('TOKEN')
