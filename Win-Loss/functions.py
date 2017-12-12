import os,json
import discord

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

def help():
	list_of_commands={}
	list_of_commands['!set_wins']='```!set_wins {number}```'
	list_of_commands['!set_losses']='```!set_losses {number}```'
	list_of_commands['!add_win']='Adds a win'
	list_of_commands['!add_loss']='Adds a loss'
	list_of_commands['!stats']="Responds with *Wins and Losses*"
	output = discord.Embed(title='Discobot Commands', color=0x0000ff)
	for command,description in list_of_commands.items():
		output.add_field(name=command,value=description, inline=False)
	output.to_dict()


	return output
