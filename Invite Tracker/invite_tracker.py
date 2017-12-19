import discord
client=discord.Client()

@client.event
async def on_ready():
	print('Logged in as: '+client.user.name)
	print('Bot ID: '+client.user.id)
	print('------')

@client.event
async def on_message(message):
	if message.content=='!invites':
		total_uses=0
		embed=discord.Embed(title='__Invites from {}__'.format(message.author.name))
		invites = await client.invites_from(message.server)
		for invite in invites:
			if invite.inviter == message.author and invite.max_age==0:
				total_uses += invite.uses
				embed.add_field(name='Invite',value=invite.id)
				embed.add_field(name='Uses',value=invite.uses)
				embed.add_field(name='Expires',value='Never')
		embed.add_field(name='__Total Uses__',value=total_uses)
		await client.send_message(message.channel,embed=embed)
		
client.run('TOKEN')
