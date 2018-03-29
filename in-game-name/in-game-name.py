import discord
from discord.ext import commands
from json_functions import read_json,edit_json

bot=commands.Bot(command_prefix='!')

register_list=read_json('register_list')

@bot.event
async def on_ready():
	print(bot.user.name)
	print(bot.user.id)
	for server in bot.servers:
		print(server.name)

@bot.command(pass_context=True)
async def register(ctx,*,ig_name:str=None):
	'''Register your in-game name with the server'''
	author=ctx.message.author
	if ig_name is None:
		await bot.say('No name was input, please try again.')
		return
	if author.id not in register_list:
		register_list[author.id]=None
	register_list[author.id]=ig_name
	edit_json('register_list',register_list)
	await bot.say('Thank you {}, you have been registered successfully as **{}**!'.format(author.mention,ig_name))

@bot.command()
async def lookup(member:discord.Member):
	'''Lookup a members IGN'''
	if member.id not in register_list:
		await bot.say('{} has not registered an in-game-name'.format(member.mention))
		return
	ign=register_list[member.id]
	await bot.say("{}'s game name is **{}**".format(member.mention,ign))

bot.run('TOKEN')
