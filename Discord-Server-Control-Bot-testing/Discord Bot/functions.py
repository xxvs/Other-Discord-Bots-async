import os,json,discord
import subprocess,time,signal

start_user=None
server_running=None
server_PID=None

def read_json(file_name):
	if file_name.endswith('.json')==False:
		file_name=file_name+'.json'
	if not os.path.isfile(file_name):
		list_name=open(file_name,"w+")
		list_name={}
	else:
		try:
			with open(file_name) as f:
				list_name = json.load(f)
		except ValueError:
			list_name={}
	return list_name

def edit_json(file_name,items):
	if file_name.endswith('.json')==False:
		file_name=file_name+'.json'
	with open(file_name,"w") as f:
		f.write(json.dumps(items))

def on_open():
	global data,game_list
	data=read_json('data')
	game_list=data['games']

def start(game,player,map=None):
	global server_running,start_user,server_PID
	if map!=None:
		if all(map_name.lower()!=map.lower() for map_name in game_list[game]['maps']):
			return '**{}** is not a valid map for **{}**'.format(map,game)
		for map_name in game_list[game]['maps']:
			if map_name.lower()==map.lower():
				map=map_name
		server_running='**{}** on **{}**'.format(game,map)
	else:
		server_running='**{}**'.format(game)
	start_user=player.mention
	script=eval(game_list[game]['script'])
	#proc = subprocess.Popen(script, shell=True, preexec_fn=os.setsid)
	#server_PID=proc.pid
	return 'Started: {}'.format(server_running)

def stop(player):
	global server_running,start_user
	msg='{} stopped - {}'.format(player.mention,server_running)
	#os.killpg(os.getpgid(server_PID),signal.SIGTERM)
	server_running=None
	start_user=None
	return msg

def status():
	return 'Running: {}\nStarted by: {}'.format(server_running,start_user)

def help():
	commands={}
	commands['!start']='Use one of the following:`{}`\nin the `$game` response.'.format(list(game_list.keys()))
	commands['!stop']='To stop current server. Only Mods or initiating user can stop the server.'
	commands['!status']='Will return current server state'
	embed=discord.Embed(title='Bot Commands',color=0x0000FF)
	for cmd,desc in commands.items():
		embed.add_field(name=cmd,value=desc,inline=False)
	return embed

on_open()
