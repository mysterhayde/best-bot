import	discord
import	requests
import	asyncio
from 	discord.ext	import commands, tasks
from	init		import load_env, init_user_dict

ft_uid = None
ft_secret = None
ft_token_access = None
ft_token_exp = 0
ft_user_list = ["chpasqui", "emonacho", "emurillo", "hdougoud", "jrandet", "timmi"]
ft_user_location_dict = None

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Game('Work in progress'))
	get_users_state.start()

@tasks.loop(minutes=5)
async def get_users_state():
	global ft_user_location_dict
	channel_id = 1258451290619641909

	auth_info = {"Authorization": f"Bearer {ft_token_access}"}
	get_access_token()
	for login in ft_user_list:
		try:
			request = await asyncio.to_thread(
				requests.get, f"https://api.intra.42.fr/v2/users/{login}", headers=auth_info, timeout=15
			)
			request.raise_for_status()
			current_location = request.json().get("location")
			if (current_location != ft_user_location_dict.get(login)):
				channel = bot.get_channel(channel_id)
				if not channel:
					print("Error invalid channel")
				elif (current_location != None):
					await channel.send(f"{login} est arrivé/e à 42")
				else:
					await channel.send(f"{login} est parti de l'école")
				ft_user_location_dict[login] = current_location
		except Exception as error_id:
			print(f"Error {error_id} during verification of {login}")
		await asyncio.sleep(1)

def get_access_token():
	global ft_token_exp, ft_token_access

	if (ft_token_access == None or ft_token_exp < 30):
		request = requests.post(
			"https://api.intra.42.fr/oauth/token",
			data={"grant_type": "client_credentials", "client_id": ft_uid,"client_secret": ft_secret},
			timeout=15
		)
		request.raise_for_status()
		data = request.json()
		ft_token_access = data["access_token"]
		ft_token_exp = data["expires_in"]



def main():
	global ft_uid, ft_secret, ft_user_location_dict

	discord_token, ft_uid, ft_secret = load_env()
	get_access_token()
	ft_user_location_dict = init_user_dict(ft_user_list, ft_token_access)
	bot.run(discord_token)

if __name__ == "__main__":
	main()