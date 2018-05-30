''' Assign a role to a member when they say a word and send a public message telling the server about it'''

import discord
from discord.ext import commands

# list of words to check for
trigger_words = ['list', 'of', 'Words']

# The ID# of the role to assign
assigned_role_id = 'YOUR ROLE ID#'

# bool, change if you want the filter to be case sensitive
case_sensitive = True

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)


async def alert(message, role):
    await bot.add_roles(message.author, role)
    await bot.send_message(message.channel, f'{message.server.default_role}, {message.author.mention} has been added to {role.mention}!!')


@bot.event
async def on_message(message):
    assigned_role = discord.utils.get(
        message.server.roles, id=assigned_role_id)
    if assigned_role not in message.author.roles:
        for word in trigger_words:
            if case_sensitive:
                if word in message.content:
                    await alert(message, assigned_role)
                    return
            else:
                if word.lower() in message.content.lower():
                    await alert(message, assigned_role)
                    return


bot.run('TOKEN')
