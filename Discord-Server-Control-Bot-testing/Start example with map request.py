@bot.command()
async def Start():

	if option.lower() not in gamelist.lower() #Do I need lower on both of these? is .upper() a thing?
		return Response('Not a valid game.'),
               reply=True, delete_after=10
	
	if any(role.name not in approved_roles for role in message.author.roles)
		return Response('You are not authorized to start any games.'),
                reply=True, delete_after=10

	if option.lower in ['ark']
		if "ark" not in [y.name.lower() for y in author.roles]:
			return Response('You are not authorized to start Ark.'),
					reply=True, delete_after=10
		elif "ark" in [y.name.lower() for y in author.roles]:
			def Arkgame(msg):
				return msg.content.startswith('$map')
			await client.send_message(message.channel, 'Enter Map Name: `$map map_name`. Available maps are {}.'.format(ark_map))
				message= await client.wait_for_message(author=message.author,check=map)
				map_name=message.content[len('$map'):].strip().lower()
				if map_name not in ark_map
					return Response('Invalid map name'),
						reply=True, delete_after=10
				elif 
					return Response('Starting Ark with {} map'.format(map_name)),
						reply=True, delete_after=10
					popen.howdoesthiswork ('start ShooterGameServer.exe {}?SessionName=potato?ServerPassword=potato?ServerAdminPassword=****?Port=?QueryPort=?listen?MaxPlayers=1 exit'.format(map_name)) #insert map name here when outputting with popen to track PID
