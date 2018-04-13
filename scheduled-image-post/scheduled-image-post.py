import discord,os,random,asyncio
from datetime import datetime
from discord.ext import commands

bot=commands.Bot(command_prefix='!')

send_time='12:00' #time is in 24hr format
image_channel_id='429429283115630592' #channel ID to send images to
image_types=('.jpg','.png','.gif','.jpeg') #add image types if needed


folders={'Image Folder':'images','Sent Folder':'sent_images'}
for folder in folders.values():
	if not os.path.isdir(folder):
		os.mkdir(folder)

@bot.event
async def on_ready():
	print(bot.user.name)
	print(bot.user.id)

async def send_image():
	for item in os.walk('./{}'.format(folders['Image Folder'])):
		images=list(pic for pic in item[2] if pic.lower().endswith(image_types))
	if len(images) == 0:
		await bot.send_message(image_channel,"Oops! I'm all out of images to send. Notify my owner!")
	else:
		image= random.choice(images)
		await bot.send_file(image_channel,'./{}/{}'.format(folders['Image Folder'],image))
		os.rename('./{}/{}'.format(folders['Image Folder'],image), './{}/{}'.format(folders['Sent Folder'],image))

async def time_check():
	global image_channel
	await bot.wait_until_ready()
	image_channel=bot.get_channel(image_channel_id)
	while not bot.is_closed:
		now=datetime.strftime(datetime.now(),'%H:%M')
		if now == send_time:
			await send_image()
		await asyncio.sleep(60)

bot.loop.create_task(time_check())

bot.run('TOKEN')
