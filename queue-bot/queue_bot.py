# queue bot

import discord
from discord.ext import commands

prefix = '!'  # change this to whatever prefix you'd like

bot = commands.Bot(command_prefix=prefix)

# add roles that can use some commands
approved_roles = ['Admin', 'Bot', 'Mod']


def is_approved():
    def predicate(ctx):
        author = ctx.message.author
        if author is ctx.message.server.owner:
            return True
        if any(role.name in approved_roles for role in author.roles):
            return True
    return commands.check(predicate)


@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)


class Queue:

    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.qtoggle = False

    @commands.command(pass_context=True)
    async def add(self, ctx):
        ''': Add yourself to the queue!'''
        author = ctx.message.author
        if self.qtoggle:
            if author.id not in self.queue:
                self.queue.append(author.id)
                await self.bot.reply('you have been added to the queue.')
            else:
                await self.bot.reply('you are already in the queue!')
        else:
            await self.bot.say('The queue is closed.')

    @commands.command(pass_context=True)
    async def remove(self, ctx):
        ''': Remove yourself from the queue'''
        author = ctx.message.author
        if author.id in self.queue:
            self.queue.remove(author.id)
            await self.bot.reply('you have been removed from the queue.')
        else:
            await bot.reply('you were not in the queue.')

    @commands.command(name='queue', pass_context=True)
    async def _queue(self, ctx):
        ''': See who's up next!'''
        server = ctx.message.server
        message = ''
        for place, member_id in enumerate(self.queue):
            member = discord.utils.get(server.members, id=member_id)
            message += f'**#{place+1}** : {member.mention}\n'
        if message != '':
            await self.bot.say(message)
        else:
            await self.bot.say('Queue is empty')

    @commands.command(pass_context=True)
    async def position(self, ctx):
        ''': Check your position in the queue'''
        author = ctx.message.author
        if author.id in self.queue:
            _position = self.queue.index(author.id)+1
            await self.bot.reply(f'you are **#{_position}** in the queue.')
        else:
            await self.bot.reply(f'you are not in the queue, please use {prefix}add to add yourself to the queue.')

    @is_approved()
    @commands.command(pass_context=True, name='next')
    async def _next(self, ctx):
        ''': Call the next member in the queue'''
        if len(self.queue) > 0:
            member = discord.utils.get(
                ctx.message.server.members, id=self.queue[0])
            await bot.say(f'You are up **{member.mention}**! Have fun!')
            self.queue.remove(self.queue[0])

    @is_approved()
    @commands.command()
    async def clear(self):
        ''': Clears the queue'''
        self.queue = []
        await self.bot.say('Queue has been cleared')

    @is_approved()
    @commands.command()
    async def toggle(self):
        ''': Toggles the queue'''
        self.qtoggle = not self.qtoggle
        if self.qtoggle:
            state = 'OPEN'
        else:
            state = 'CLOSED'
        await self.bot.say(f'Queue is now {state}')


bot.add_cog(Queue(bot))

bot.run('TOKEN')
