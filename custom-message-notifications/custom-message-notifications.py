# custom message notifications; keep track of when a specific member/role posts in a specified channel
import re
import os
import json
import discord
from discord.ext import commands
from datetime import datetime, date

prefix = '~'
bot = commands.Bot(command_prefix=prefix, pm_help=True)


def read_json(file_name):
    if not file_name.endswith('.json'):
        file_name = file_name + '.json'
    if not os.path.isfile(file_name):
        list_name = {}
    else:
        try:
            with open(file_name) as f:
                list_name = json.load(f)
        except ValueError:
            list_name = {}
    return list_name


not_settings = list(read_json('not_settings'))


def edit_json(file_name, items):
    if not file_name.endswith('.json'):
        file_name = file_name + '.json'
    with open(file_name, "w") as f:
        json.dump(items, f, indent=4, sort_keys=True)


def is_approved():
    def predicate(ctx):
        author = ctx.message.author
        if author is ctx.message.server.owner:
            return True
        if ('administrator', True) in author.server_permissions:
            return True
    return commands.check(predicate)


class Notifications:

    not_list = []

    def __init__(self, server, watch, watch_channel, message, not_channel):
        self.server = bot.get_server(str(server))
        self.watch = discord.utils.get(self.server.members, id=watch)
        if self.watch is None:
            self.watch = discord.utils.get(self.server.roles, id=watch)
        self.watch_channel = bot.get_channel(watch_channel)
        self.message = message
        self.not_channel = bot.get_channel(not_channel)
        Notifications.not_list.append(self)


def check_watch(mention):
    match = re.search(r'([0-9]+)', mention)
    return match.group()


def load_settings():
    for setting in not_settings:
        Notifications(setting['server'], setting['watch'],
                      setting['watch_channel'], setting['message'], setting['not_channel'])


def list_settings():
    types = ['Pos.', 'Trigger Member/Role',
             'Trigger Channel', 'Report Channel', 'Message']
    table_data = [types]
    for pos, setting in enumerate(Notifications.not_list):
        convert = [str(pos+1).strip(), setting.watch.name, setting.watch_channel.name,
                   setting.not_channel.name, str(setting.message)]
        table_data.append(convert)
    msg = ''
    for row in table_data:
        msg += ("{: <5} {: <20} {: <20} {: <20} {: <20}\n".format(*row))
    return msg


@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)
    load_settings()


@bot.event
async def on_message(message):
    for setting in Notifications.not_list:
        if message.channel == setting.watch_channel:
            if message.author == setting.watch:
                await message_formatter(message, setting)
            if setting.watch in message.author.roles:
                await message_formatter(message, setting)

    await bot.process_commands(message)


async def message_formatter(message, setting):
    if setting.message == 'None':
        embed = discord.Embed(title=message.author.name)
        embed.add_field(name='From Channel:', value=message.channel.mention)
        embed.add_field(name='Quote:', value=message.content, inline=False)
        embed.set_footer(text=message.timestamp.strftime('%Y-%m-%d %I:%M %p'))
        await bot.send_message(setting.not_channel, embed=embed)
    else:
        await bot.send_message(setting.not_channel, setting.message)


@is_approved()
@bot.command(pass_context=True)
async def notif(ctx, watch: str, watch_channel: discord.Channel, not_channel: discord.Channel, *, message: str='None'):
    ''': Add notification settings to the server'''
    server = ctx.message.server
    watch = check_watch(watch)
    new_notification = {
        'server': server.id,
        'watch': watch,
        'watch_channel': watch_channel.id,
        'not_channel': not_channel.id,
        'message': message
    }

    if new_notification not in not_settings:
        not_settings.append(new_notification)
        edit_json('not_settings', not_settings)
        Notifications(server.id, watch, watch_channel.id,
                      message, not_channel.id)
        msg = list_settings()
        await bot.whisper(f'Notification settings have been updated:```{msg}```')
    else:
        await bot.reply('that setting has already been saved!')


@is_approved()
@bot.command()
async def notlist():
    ''': List notification settings'''
    msg = list_settings()
    await bot.whisper(f'```Notification Settings:\n\n{msg}```')


@is_approved()
@bot.command(pass_context=True)
async def notremove(ctx):
    ''': Remove notifications'''
    author = ctx.message.author
    msg = list_settings()
    await bot.whisper(f'```Please select a position to be removed:\n\n{msg}```')
    info = None
    while info is None:
        try:
            info = await bot.wait_for_message(timeout=30, author=author)
            info = info.content
            if not int(info):
                await bot.whisper('You need to enter a valid option')
                info = None
            position = int(info)-1
            del Notifications.not_list[position]
            del not_settings[position]
            edit_json('not_settings', not_settings)
            msg = list_settings()
            await bot.whisper(f'Notification settings have been updated:```{msg}```')
        except:
            await bot.whisper('You need to enter a valid option')
            info = None

bot.run('TOKEN')
