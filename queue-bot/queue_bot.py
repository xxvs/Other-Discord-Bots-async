# queue bot
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

prefix = '!'
bot = commands.Bot(command_prefix=prefix)

# add roles that can use some commands
approved_roles = ['Admin', 'Bot', 'Mod']


def is_approved():
    def predicate(ctx):
        author = ctx.message.author
        if author is ctx.message.guild.owner:
            return True
        if any(role.name in approved_roles for role in author.roles):
            return True
    return commands.check(predicate)


@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    if isinstance(error, commands.NoPrivateMessage):
        return
    raise error


class QueueBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.qtoggle = False
        self.code = ''

    @commands.guild_only()
    @commands.command()
    async def room(self, ctx, arg):
        '''Set room code'''
        self.code = arg
        await self._queue(ctx)

    @commands.guild_only()
    @commands.command()
    async def add(self, ctx):
        ''': Add yourself to the queue!'''
        author = ctx.author
        message = ''
        if self.qtoggle:
            if author.id not in self.queue:
                self.queue.append(author.id)
                if len(self.queue) > 4:
                    message = await self.list_users(ctx, 'There are enough players for a game!\n', True)

                await ctx.send('You have been added to the queue.\n' + message)
            else:
                await ctx.send('You are already in the queue!')
        else:
            await ctx.send('The queue is closed.')

    @commands.guild_only()
    @commands.command()
    async def remove(self, ctx):
        ''': Remove yourself from the queue'''
        author = ctx.message.author
        if author.id in self.queue:
            self.queue.remove(author.id)
            await ctx.send('You have been removed from the queue.')
        else:
            await ctx.send('You were not in the queue.')

    async def list_users(self, ctx, text, mention=False):
        guild = ctx.message.guild
        message = ''
        for place, member_id in enumerate(self.queue):
            member = discord.utils.get(guild.members, id=member_id)
            message += f'**#{place+1}** : {member.mention}\n' if mention else f'**#{place+1}** : {str(member)}\n'
        if message != '':
            room_code = f'ROOM CODE: {self.code}\n' if self.code != '' else ''
            message = text + room_code + message
        return message

    @commands.guild_only()
    @commands.command(name='queue')
    async def _queue(self, ctx):
        ''': See users in queue'''
        message = await self.list_users(ctx, '')
        if message != '':
            await ctx.send(message)
        else:
            await ctx.send('The queue is empty.')

    @is_approved()
    @commands.guild_only()
    @commands.command()
    async def clear(self, ctx):
        ''': Clears the queue'''
        self.queue = []
        await ctx.send('The queue has been cleared.')

    @is_approved()
    @commands.guild_only()
    @commands.command()
    async def toggle(self, ctx):
        ''': Toggles the queue'''
        self.qtoggle = not self.qtoggle
        if self.qtoggle:
            state = 'OPEN'
        else:
            state = 'CLOSED'
        await ctx.send(f'The queue is now {state}')


bot.add_cog(QueueBot(bot))


bot.run('token')
