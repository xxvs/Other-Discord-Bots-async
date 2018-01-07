#OS is Debian, Jessie
#Python 3.5 or higher.

#Things we need variables / global variables for
gamelist=['ARK','7D2D','FOREST','RUST','L4D2'] #Names of games servers exist for. There are also matching roles in discord the same name as these.
#Map names for games that will support multiple?
ark_map=['TheIsland','TheCenter','Ragnarok','ScorchedEarth_P']
7D2D_map=['map1','map2'] #Insert game names here for check.
current_game
approved_roles=['ADMIN','MOD'] #add the name of the roles that can stop any server
start_user #To store user who initiated server
server_running=0
current_server='$game from gamelist'
server_PID

#Help command - Or this may just be a pinned message instead. Probably a pinned message since the channel will be kept clean.
#!help
#	!start - '!start game to start game. Use'{}'to start game.'.format(gamelist)
#	!stop - '!stop to stop current server. Only Mods or initiating user can stop the server.'
#	!status - '!status will return current server state'
#Delete any messages that are not !help/start/stop/status

#commands to start server from bot
#Ignore PMs
#Only monitor one channel E.G "SERVERS"
!start Rust
#starts Rust for example
#But bot checks user roles for a match
#Bot also checks if server_running=1, will not start a server if one is already active
if server_running=1
	message #- 'current_server' is currently running
	return
elif ('RUST' in message.author.roles) #Possibly a if statement reading in a message with the !start removed, rather than an if for every game
	#start rust using popen to capture PID to server_PID
	#save userid to start_user so only that user can stop server
	#changes server_running to 1
	#Deletes chats and outputs "Rust server is running"
else
	return

#if the game has multiple maps, send the request for map name after the !start command
if message(!start ARK)
	#Check if server_running=0
	if server_running=1
		message #- 'current_server' is currently running
		return
	elif
	#Check user roles for match again
	#Send new message asking for map with $map 'ark_map'
	#waits for message with map name
	#inserts value in place of ark_map (below) in start argument
	start ShooterGameServer.exe ark_map?SessionName=potato?ServerPassword=potato?ServerAdminPassword=****?Port=?QueryPort=?listen?MaxPlayers=1 exit
	#capture PID via popen and store as server_PID
	#set server_running to 1
	#Deletes chats and outputs "Ark server is running"

#Stop sequence
if message(!stop)
	#check if ADMIN or MOD is in message.author.roles
	killpid server_PID
	#else check if userid matches start_user
	killpid server_PID
	#killPID command sent with server_PID to shell
	#set server_running to 0
	#Deletes chat and outputs "No server is running"
else
	#Direct Message User 'you do not have authority to stop this server'



