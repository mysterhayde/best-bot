import	discord
import	requests
from 	discord.ext	import commands
from	init		import load_env

ft_uid = None
ft_secret = None
ft_token_access = None
ft_token_exp = 0

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Game('Work in progress'))

def get_access_token():
	global ft_token_exp, ft_token_access
	if (ft_token_access or ft_token_exp < 30):
		request = requests.post(
			"https://api.intra.42.fr/oauth/token",
			data={
				"grant_type": "client_credentials",
				"client_id": ft_uid,
				"client_secret": ft_secret
			},
			timeout=15
		)
		request.raise_for_status()
		ft_token_access = request.json()["access_token"]
		ft_token_exp = request.json()["expires_in"]



def main():
	global ft_uid, ft_secret

	discord_token, ft_uid, ft_secret = load_env()
	get_access_token()
	bot.run(discord_token)

if __name__ == "__main__":
	main()