# A bot that will respond to certain words in messages sent

import discord,random
from discord.ext import commands

bot=commands.Bot(command_prefix='!')

trigger_words=['edit','this','list'] #add the trigger words to the list
responses=['Yum!','LIES!','more things!'] #add more responses for the bot

@bot.event
async def on_ready():
	print(bot.user.name)
	print(bot.user.id)

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if any(word.lower() in message.content.lower() for word in trigger_words):
		response=random.choice(responses)
		await bot.send_message(message.channel,response)

bot.run('TOKEN')
